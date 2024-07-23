# 2024-07-16 ChatGPT 生成的爬虫代码，经多次反复调试，输出正常
# 2024-07-23 ChatGPT 添加分页按钮，有出错提示：“正在处理第 1 页 没有找到下一页按钮: Message: ”
# 2024-07-24 手工修正错误，时而正确，时而抛异常


#{'标题': '2008欧美最热门电影预告.rmvb1', '文件数量': '7', '文件大小': '826.40KB', '链接': 'https://ciliku.net/magnet/45c9f6c02dd8bfa530d15a62a8c063a6b0d14bf8/1', '磁力链接': 'magnet:?xt=urn:btih:45c9f6c02dd8bfa530d15a62a8c063a6b0d14bf8'}
#{'标题': '辛普森一家 The Simpsons Movie (2007)/[辛普森一家].The.Simpsons.Movie.2007.阿森一族大电影 辛普森家庭电影版 辛普森一家大电影.mkv', '文件数量': '4', '文件大小': '3.20GB', '链接': 'https://ciliku.net/magnet/c549380fc91fabe0138591919fbb8d50bacbac69/0', '磁力链接': 'magnet:?xt=urn:btih:c549380fc91fabe0138591919fbb8d50bacbac69'}
#{'标题': '果冻传媒 GDCM-066 热门电影改编《周处操三害》言嘉佑 米欧 领衔主演 .mp41', '文件数量': '2', '文件大小': '1015.08MB', '链接': 'https://ciliku.net/magnet/672AD271A9639D1B382E1D8C134EBD357452F9EB/1', '磁力链接': 'magnet:?xt=urn:btih:672AD271A9639D1B382E1D8C134EBD357452F9EB'}


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

def convert_file_size(file_size_str):
    """Convert file size to GB."""
    size, unit = float(file_size_str[:-2].replace(',', '').strip()), file_size_str[-2:].upper()
    if unit == 'GB':
        return size  # Already in GB
    elif unit == 'MB':
        return size / 1024  # MB to GB
    elif unit == 'KB':
        return size / (1024 * 1024)  # KB to GB
    else:
        return 0

def get_movie_info(url, page_number):
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
            title = title_element.get_text(strip=True) if title_element else '未知'

            link_element = title_element.find('a') if title_element else None
            movie_link = link_element['href'] if link_element and 'href' in link_element.attrs else '链接不可用'
            movie_link = "https://ciliku.net" + movie_link  # 补全链接

            file_count, file_size = get_file_size(movie)

            record_time, seed_hash = get_record_time(movie)

            magnet_link = get_magnet_link(movie_link)

            movie_info = {
                '标题': title,
                '文件数量': file_count,
                '文件大小 (GB)': file_size,
                '链接': movie_link,
                '磁力链接': magnet_link,
                '收录时间': record_time,
                '种子哈希': seed_hash
            }

            movies_data.append(movie_info)

        # 恢复打开目标网址
        driver.get(url)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card.mb-4')))

        return movies_data
    except Exception as e:
        print(f"处理电影信息时出现错误: {e}")
        return []


def get_record_time(movie):
    # 获取收录时间和种子哈希
    record_time_element = movie.find('p', class_='card-text')
    if record_time_element:
        record_time_text = record_time_element.get_text(strip=True)
        record_time = record_time_text.split('：')[1].strip().split(' | ')[0]
        seed_hash = record_time_text.split('：')[2].strip().split(' | ')[0]
    else:
        record_time = '未知'
        seed_hash = '未知'
    return record_time, seed_hash


def get_file_size(movie):
    subtitle_element = movie.find('div', class_='card-subtitle text-muted mb-3')
    if subtitle_element:
        subtitle_text = subtitle_element.get_text(strip=True)
        parts = subtitle_text.split('｜')
        if len(parts) == 2:
            file_count = int(parts[0].split('：')[1].strip())
            file_size = convert_file_size(parts[1].split('：')[1].strip())
        else:
            file_count = '未知'
            file_size = '未知'
    else:
        file_count = '未知'
        file_size = '未知'
    return file_count, file_size


def get_magnet_link(movie_link):
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
    return magnet_link


def get_all_pages(url, max_pages=10):
    all_movie_info = []
    page_number = 1

    while page_number <= max_pages:
        print(f"正在处理第 {page_number} 页")
        page_url = f"{url}?page={page_number}"
        movie_info = get_movie_info(url, page_number)

        if not movie_info:
            break

        all_movie_info.extend(movie_info)
        page_number += 1

        # 检查是否有下一页
        try:
            # 查找并点击“下一页”按钮
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.btn-next')))
            next_button = driver.find_element(By.CSS_SELECTOR, 'button.btn-next')

            # 确保按钮在视口内
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(2)  # 等待滚动完成

            # 使用JavaScript直接点击按钮，绕过元素遮挡的问题
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(2)  # 等待页面加载
        except Exception as e:
            print(f"没有找到下一页按钮: {e}")
            # 记录当前页面HTML以便调试
            with open(f"page_{page_number}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            break

    return all_movie_info

if __name__ == "__main__":
    url = 'https://ciliku.net/search/高分电影'
    max_pages = 8  # 设置最大分页数
    all_movie_info = get_all_pages(url, max_pages)

    if all_movie_info:
        # 将数据转换为 DataFrame
        df = pd.DataFrame(all_movie_info)

        # 将数据写入Excel文件
        excel_file = 'ciliku_movies.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"数据已保存到 {excel_file}")
    else:
        print("未能获取电影信息。请检查网络连接或网页结构是否发生变化。")

    # 关闭浏览器
    driver.quit()
