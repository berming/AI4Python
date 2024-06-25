from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def fetch_hot_movies_magnet(url):
    """
    Fetch magnet search results for hot movies from given URL using Selenium and BeautifulSoup.

    Parameters:
    - url (str): The URL of the search results page.

    Returns:
    - list: A list of dictionaries containing movie details.
    """
    options = Options()
    options.headless = True  # 在后台运行Chrome
    service = Service('/path/to/chromedriver')  # 修改为你的Chrome驱动路径
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    try:
        # 等待搜索结果加载完成（等待30秒）
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'card'))
        )

        # 获取完整的HTML页面内容
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 解析电影信息
        movie_cards = soup.find_all('div', class_='card')

        movies = []
        for card in movie_cards:
            title_elem = card.find('h5', class_='card-title')
            if title_elem:
                title = title_elem.text.strip()
                link_elem = title_elem.find('a')
                if link_elem:
                    link = link_elem.get('href')
                else:
                    link = ''

                details_elem = card.find_all('p', class_='card-text')

                files = ''
                size = ''
                timestamp = ''
                btih = ''

                if len(details_elem) > 0:
                    files_text = details_elem[0].text.strip()
                    if '文件数量' in files_text:
                        files = files_text.split('：')[1].strip()

                if len(details_elem) > 1:
                    size_text = details_elem[1].text.strip()
                    if '文件大小' in size_text:
                        size = size_text.split('：')[1].strip()

                if len(details_elem) > 2:
                    timestamp_text = details_elem[2].text.strip()
                    if '收录时间' in timestamp_text:
                        timestamp = timestamp_text.split('：')[1].strip()

                if len(details_elem) > 3:
                    btih_text = details_elem[3].text.strip()
                    if '种子哈希' in btih_text:
                        btih = btih_text.split('：')[1].strip()

                movie_info = {
                    'title': title,
                    'link': link,
                    'files': files,
                    'size': size,
                    'timestamp': timestamp,
                    'btih': btih
                }
                movies.append(movie_info)

    finally:
        driver.quit()

    return movies

# 测试爬虫功能
url = 'https://ciliku.net/search/热门电影'
movies = fetch_hot_movies_magnet(url)

# 打印结果
for movie in movies:
    print("Title:", movie['title'])
    print("Link:", movie['link'])
    print("Files:", movie['files'])
    print("Size:", movie['size'])
    print("Timestamp:", movie['timestamp'])
    print("BTIH:", movie['btih'])
    print("=" * 50)
