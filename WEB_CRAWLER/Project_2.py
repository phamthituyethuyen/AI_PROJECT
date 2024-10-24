import asyncio 
import aiohttp
import pandas as pd
import html
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests_cache

requests_cache.install_cache('tiki_cache', expire_after=3600)  # Bộ nhớ đệm trong 1 giờ


def connect_to_mongo():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        client.admin.command('ping')
        print("Good connect!")
        return client['tikiProduct']['Product']
    except Exception as error:
        print(f"Error: {error}")
        return None

async def getProduct(productID, urlApiTiki, semaphore, session):
    urlDetail = f"{urlApiTiki}{productID}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        async with semaphore:
            async with session.get(urlDetail, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"ERROR: {response.status} với sản phẩm có id {productID}. URL: {urlDetail}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None


def getFromFile(fileName):
    try:
        dataID = pd.read_csv(f'{fileName}.csv')
        return dataID['id']
    except FileNotFoundError:
        print("File không tồn tại")
        return None

def productDetail(product_detail):
    if product_detail:
        description = product_detail.get('description', '').replace('\n', ' ')
        description_decoded = html.unescape(description)
        soup = BeautifulSoup(description_decoded, 'html.parser')
        cleaned_description = soup.get_text(separator=' ', strip=True)

        product_data = {
            'id': product_detail.get('id'),
            'name': product_detail.get('name'),
            'url_key': product_detail.get('url_key'),
            'price': product_detail.get('price'),
            'description': cleaned_description,
            'images': product_detail.get('images', [])
        }
        return product_data
    return None

def insertProduct(collection, productInsert):
    if productInsert:
        try:
            collection.insert_many(productInsert)
            print(f"{len(productInsert)} sản phẩm đã được lưu!")
        except Exception as error:
            print(f"Fail to insert: {error}")

async def main():
    # Connect to MongoDB and get collection from Tiki product db
    collection = connect_to_mongo()

    # Input URL API Tiki product và file lưu ID product
    urlApiTiki = input("Nhập URL API Tiki:\n")
    fileName = input("Nhập tên file chứa product IDs:\n")

    # Trích xuất cột ID trong file CSV
    idFromFile = getFromFile(fileName)
    if idFromFile is None:
        return

    # Giới hạn số lượng kết nối đồng thời
    semaphore = asyncio.Semaphore(100)  # Giới hạn tối đa 100 kết nối cùng lúc
    tasks = []
    
    print('\n--------------DOING------------------')
    async with aiohttp.ClientSession() as session:
        for i, product_id in enumerate(idFromFile):
            if i > 2176:  
                tasks.append(getProduct(product_id, urlApiTiki, semaphore, session))
                await asyncio.sleep(0.05)  

        
        results = await asyncio.gather(*tasks)

    # Get data và đưa vào MongoDB nếu lấy đủ 100 sản phẩm
    product_insert = []
    for product_detail in results:
        if product_detail:
            product_insert.append(productDetail(product_detail))
        if len(product_insert) == 100:
            insertProduct(collection, product_insert)
            product_insert = []

    # Insert các sản phẩm còn lại
    insertProduct(collection, product_insert)

if __name__ == "__main__":
    asyncio.run(main())
