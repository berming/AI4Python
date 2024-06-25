from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

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

# 遍历每部电影并提取信息
for movie in movies:
    title_element = movie.find('h5', class_='card-title text-primary')
    title = title_element.get_text(strip=True)

    link_element = title_element.find('a')
    link = link_element['href'] if link_element and 'href' in link_element.attrs else '链接不可用'
    link = "https://ciliku.net" + link  # 补全链接

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

    movie_info = {
        '标题': title,
        '文件数量': file_count,
        '文件大小': file_size,
        '链接': link
    }

    print(movie_info)

    movies_data.append({
        '标题': title,
        '文件数量': file_count,
        '文件大小': file_size,
        '链接': link
    })

print("数据提取完成")

# 将数据保存到Excel文件中
df = pd.DataFrame(movies_data)
df.to_excel('movies_info.xlsx', index=False)

print("数据已保存到movies_info.xlsx文件中")


# 关闭浏览器
driver.quit()
