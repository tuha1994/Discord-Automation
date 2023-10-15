#discord

import time
import requests
import openpyxl
import asyncio
import random
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from channel import CHANNEL_DISCORD ,CHANNEL_CHAT
from token_discord import TOKEN_DISCORD
from timer import time_start,time_stop
import datetime


url = CHANNEL_DISCORD
url1 = CHANNEL_CHAT
headers = {
    "Authorization": TOKEN_DISCORD
}
plt.rcParams['font.family'] = 'Arial'
chromium_binary_path = 'C:\\Program Files\\Chromium\\Application\\chrome.exe'
chromium_driver_path = './chromedriver/chromedriver.exe'
service = Service(executable_path=chromium_driver_path)
options = webdriver.ChromeOptions()
options.binary_location = chromium_binary_path
options.add_argument('--headless')
options.add_argument('--disable-features=AutoUpdate')
options.add_argument('--no-sandbox')

user_data_dir = 'C:\\Users\\tuha\\AppData\\Local\\Chromium\\User Data\\'
options.add_argument(f'--user-data-dir={user_data_dir}')
driver = webdriver.Chrome(service=service, options=options)
driver.get(url1)
#time.sleep(5)
async def random_delay():
    delay_time = random.uniform(time_start, time_stop)
    await asyncio.sleep(delay_time)

# Hàm gửi tin nhắn
async def send_message(content):
    await random_delay()

    # Lấy thời gian hiện tại và định dạng nó thành chuỗi
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content_with_time = f"{current_time}: {content}"

    payload = {
        "content": content
    }
    res = requests.post(url, json=payload, headers=headers)
    with open('log.txt', 'a',encoding='utf-8') as file:
        file.write(f'Tin nhắn đã gửi lúc {current_time},nội dung là :{content}\n')
    
    # Thêm đoạn mã dưới đây để xóa tin nhắn sau khi gửi
    if res.status_code == 200:
        message_id = res.json().get('id')
        if message_id:
            delete_url = f"{url}/{message_id}"
            delete_response = requests.delete(delete_url, headers=headers)
            if delete_response.status_code == 204:
                print(f'Tin nhắn đã được xóa: {current_time},nội dung là :{content}')
            else:
                print(f'Không thể xóa tin nhắn: {current_time},nội dung là :{content}')

async def main():
    wb = openpyxl.load_workbook('./Chat Discord.xlsx')
    sheet = wb.active
    for row in sheet.iter_rows(values_only=True):
        content = row[0]
        await send_message(content)
    wb.close()

if __name__ == "__main__":
    asyncio.run(main())
