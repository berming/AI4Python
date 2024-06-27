import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

# 存储每部电影的链接
movie_links = []

# 遍历所有电影，收集链接
for movie in movies:
    title_element = movie.find('h5', class_='card-title text-primary')
    link_element = title_element.find('a')
    movie_link = link_element['href'] if link_element and 'href' in link_element.attrs else '链接不可用'
    movie_links.append("https://ciliku.net" + movie_link)  # 补全链接

# 创建一个空的 DataFrame 来存储数据
columns = ['标题', '文件数量', '文件大小', '链接', '磁力链接']
df = pd.DataFrame(columns=columns)

# 定义函数用于处理单个电影页面的信息提取
def process_movie(movie_link):
    driver.get(movie_link)
    time.sleep(3)  # 等待页面加载完成

    movie_html = driver.page_source
    movie_soup = BeautifulSoup(movie_html, 'html.parser')

    title_element = movie_soup.find('h1', class_='card-title')
    title = title_element.get_text(strip=True)

    subtitle_element = movie_soup.find('div', class_='card-subtitle text-muted mb-3')
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

    # 查找资源下载按钮，提取磁力链接
    download_btn = movie_soup.find('a', string='资源下载')
    magnet_link = ''
    if download_btn:
        download_link = download_btn['href']
        # 这里可以进一步访问下载链接页面来提取磁力链接，根据实际情况调整
        # 简化处理，直接将资源下载链接作为磁力链接（实际情况可能不同）
        magnet_link = download_link

    movie_info = {
        '标题': title,
        '文件数量': file_count,
        '文件大小': file_size,
        '链接': movie_link,
        '磁力链接': magnet_link
    }

    return movie_info

# 使用并行处理提取每部电影的信息
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # 提交任务并获取结果
    futures = [executor.submit(process_movie, movie_link) for movie_link in movie_links]
    for future in concurrent.futures.as_completed(futures):
        movie_info = future.result()
        # 将数据添加到 DataFrame
        df = pd.concat([df, pd.DataFrame([movie_info])], ignore_index=True)
        # 打印每部电影的信息
        print(movie_info)
        print('-' * 20)

print("数据提取完成")

# 将数据写入Excel文件
excel_file = 'ciliku_movies.xlsx'
df.to_excel(excel_file, index=False)
print(f"数据已保存到 {excel_file}")

# 关闭浏览器
driver.quit()
