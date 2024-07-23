#2024-07-16 单页显示正确


import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 设置Chrome选项
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')  # 禁用GPU加速
options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度

# 启动Chrome浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_movie_info(url):
    try:
        # 打开目标网址
        driver.get(url)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card.mb-4')))

        # 获取渲染后的HTML
        html = driver.page_source

        # 解析HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 存储电影信息的列表
        movies_data = []

        # 找到所有电影的容器
        movies = soup.find_all('div', class_='card mb-4')

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

            # 获取收录时间和种子哈希
            record_time_element = movie.find('p', class_='card-text')
            if record_time_element:
                record_time_text = record_time_element.get_text(strip=True)
                record_time = record_time_text.split('：')[1].strip().split(' | ')[0]
                seed_hash = record_time_text.split('：')[2].strip().split(' | ')[0]
            else:
                record_time = '未知'
                seed_hash = '未知'

            # 访问电影详情页获取磁力链接
            driver.get(movie_link)

            # 等待页面加载完成
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

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
                '磁力链接': magnet_link,
                '收录时间': record_time,
                '种子哈希': seed_hash
            }

            movies_data.append(movie_info)

        return movies_data
    except Exception as e:
        print(f"处理电影信息时出现错误: {e}")
        return []

if __name__ == "__main__":
    url = 'https://ciliku.net/search/热门电影'
    movie_info = get_movie_info(url)

    if movie_info:
        # 将数据转换为 DataFrame
        df = pd.DataFrame(movie_info)

        # 将数据写入Excel文件
        excel_file = 'ciliku_movies.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"数据已保存到 {excel_file}")
    else:
        print("未能获取电影信息。请检查网络连接或网页结构是否发生变化。")

    # 关闭浏览器
    driver.quit()
