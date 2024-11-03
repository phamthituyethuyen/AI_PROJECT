import requests
from bs4 import BeautifulSoup 
import os

import requests.compat # to maker a folder contain image

# ghi ds ra log
visited_url = set()

download_image =set()

# check các url đã lưu thành công
def load_download_image(logfile):
    if os.path.exists(logfile):
        with open(logfile,'r') as file:
            for line in file:
                download_image.add(line.strip())

#ghi url vào log
def log_image_url(img_url, log_file):
    with open(log_file,'a') as f: ### chế độ a là ghi text vào cuối file log
        f.write(f"{img_url}\n")

def crawl_image(url,base_domain,log_file):
    if url in visited_url:
        return
    visited_url.add(url)

    try:
        respone = requests.get(url)
        respone.raise_for_status()
        soup = BeautifulSoup(respone.text,"html.parser")

        os.makedirs('Glamira_image',exist_ok=True)

        image = soup.find_all('img')

        for img in image:
            img_url = img.get('src')
            if img_url:
                if not img_url.startswith('http'):
                    img_url = requests.compat.urljoin(url,img_url)
                img_name = os.path.join("Glamira_image",img_url.split("/")[-1]) ###tạo tên file ảnh


                if img_url in download_image:
                    print(f"Image :{img_url} đã được save!")
                    continue  # Nếu đã lưu rồi thì bỏ qua

                try:
                    img_data = requests.get(img_url).content
                    with open(img_name,'wb') as f:
                        f.write(img_data)
                    print(f"Đã save thành công ảnh {img_name}")

                    log_image_url(img_url,log_file)
                    download_image.add(img_url)
                except Exception as e:
                    print(f"Lỗi khi lưu ảnh {img_url}: {e}")

        links = soup.find_all('a',href=True)
        if not links:
            return 
        for link in links:
            next_url = link['href']
            if not next_url.startswith('http'):
                next_url = requests.compat.urljoin(url,next_url)
            if base_domain in next_url:
                crawl_image(next_url,url,log_file)
    except Exception as e:
        print(f"Lỗi khi crawl URL {url}: {e}")

if __name__ =="__main__":
    load_download_image("log_project_3.txt")
    start_url= 'https://www.glamira.com'
    base_domain = 'glamira.com'

    crawl_image(start_url,base_domain,"log_project_3.txt")