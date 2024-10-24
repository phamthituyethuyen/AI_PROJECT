import requests
import pandas as pd 

file_url = input("Hãy nhập URL:")
file_path = 'product_ids.csv'

getContent = requests.get(file_url)
if getContent.status_code ==200 :
    with open(file_path, 'wb') as file:
        file.write(getContent.content)
    print("Susessful!")

else:
    print(f"Error :{getContent.status_code} : Can't download file!")
          