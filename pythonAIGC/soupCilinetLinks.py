# ChatGPT 生成的爬虫代码，经多次反复调试，输出正常

#{'标题': '2008欧美最热门电影预告.rmvb1', '文件数量': '7', '文件大小': '826.40KB', '链接': 'https://ciliku.net/magnet/45c9f6c02dd8bfa530d15a62a8c063a6b0d14bf8/1', '磁力链接': 'magnet:?xt=urn:btih:45c9f6c02dd8bfa530d15a62a8c063a6b0d14bf8'}
#{'标题': '辛普森一家 The Simpsons Movie (2007)/[辛普森一家].The.Simpsons.Movie.2007.阿森一族大电影 辛普森家庭电影版 辛普森一家大电影.mkv', '文件数量': '4', '文件大小': '3.20GB', '链接': 'https://ciliku.net/magnet/c549380fc91fabe0138591919fbb8d50bacbac69/0', '磁力链接': 'magnet:?xt=urn:btih:c549380fc91fabe0138591919fbb8d50bacbac69'}
#{'标题': '果冻传媒 GDCM-066 热门电影改编《周处操三害》言嘉佑 米欧 领衔主演 .mp41', '文件数量': '2', '文件大小': '1015.08MB', '链接': 'https://ciliku.net/magnet/672AD271A9639D1B382E1D8C134EBD357452F9EB/1', '磁力链接': 'magnet:?xt=urn:btih:672AD271A9639D1B382E1D8C134EBD357452F9EB'}


import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 设置Chrome选项
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')  # 禁用GPU加速
options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度

# 启动Chrome浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 打开目标网址
url = "https://ciliku.net/search/热门电影"
driver.get(url)

# 等待页面加载完成
time.sleep(5)  # 可以根据需要调整等待时间

# 获取渲染后的HTML
html = driver.page_source

# 解析HTML
soup = BeautifulSoup(html, 'html.parser')

# 存储电影信息的列表
movies_data = []

# 找到所有电影的容器
movies = soup.find_all('div', class_='card mb-4')

# 创建一个空的 DataFrame 来存储数据
columns = ['标题', '文件数量', '文件大小', '链接', '磁力链接']
df = pd.DataFrame(columns=columns)

# 遍历每部电影并提取信息
for movie in movies:
    title_element = movie.find('h5', class_='card-title text-primary')
    title = title_element.get_text(strip=True)

    link_element = title_element.find('a')
    movie_link = link_element['href'] if link_element and 'href' in link_element.attrs else '链接不可用'
    movie_link = "https://ciliku.net" + movie_link  # 补全链接

    subtitle_element = movie.find('div', class_='card-subtitle text-muted mb-3')
    if subtitle_element:
        subtitle_text = subtitle_element.get_text(strip=True)
        parts = subtitle_text.split('｜')
        if len(parts) == 2:
            file_count = parts[0].split('：')[1].strip()
            file_size = parts[1].split('：')[1].strip()
        else:
            file_count = '未知'
            file_size = '未知'
    else:
        file_count = '未知'
        file_size = '未知'

    # 访问电影详情页获取磁力链接
    driver.get(movie_link)
    time.sleep(3)  # 等待页面加载完成

    # 获取渲染后的HTML
    movie_html = driver.page_source
    movie_soup = BeautifulSoup(movie_html, 'html.parser')

    # 查找磁力链接
    magnet_link = ''
    magnet_element = movie_soup.find('a', href=lambda x: x and x.startswith('magnet:?xt='))
    if magnet_element:
        magnet_link = magnet_element['href']

    movie_info = {
        '标题': title,
        '文件数量': file_count,
        '文件大小': file_size,
        '链接': movie_link,
        '磁力链接': magnet_link
    }

    # 打印每部电影的信息
    print(movie_info)

    # 将数据添加到 DataFrame
    df = pd.concat([df, pd.DataFrame([movie_info])], ignore_index=True)

print("数据提取完成")

# 将数据写入Excel文件
excel_file = 'ciliku_movies.xlsx'
df.to_excel(excel_file, index=False)
print(f"数据已保存到 {excel_file}")

# 关闭浏览器
driver.quit()
