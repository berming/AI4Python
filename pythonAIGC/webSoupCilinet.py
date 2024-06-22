from selenium import webdriver
from bs4 import BeautifulSoup

def fetch_movie_search_results_dynamic(url):
    """
    Fetch the search results from the given URL using Selenium.

    Parameters:
    - url (str): The URL of the search page.

    Returns:
    - dict: A dictionary with the status and content (title and paragraphs).
    """
    # 使用Selenium WebDriver
    driver = webdriver.Chrome()  # 需要安装ChromeDriver
    driver.get(url)

    # 等待页面加载完成
    driver.implicitly_wait(10)

    # 获取页面内容
    page_content = driver.page_source
    driver.quit()

    # 解析HTML内容
    soup = BeautifulSoup(page_content, 'html.parser')

    # 抓取网页标题
    title = soup.title.string if soup.title else 'No title found'

    # 抓取所有包含电影信息的段落
    # 假设电影信息在某个特定的标签中，比如 <div class="movie-item"> (需要根据实际网页结构调整)
    movies = []
    for div in soup.find_all('div', class_='movie-item'):
        movie_title = div.find('h3').text if div.find('h3') else 'No title'
        movie_info = div.find('p').text if div.find('p') else 'No information'
        movies.append({'title': movie_title, 'info': movie_info})

    return {
        'title': title,
        'movies': movies
    }

# 测试爬虫功能
url = 'https://ciliku.net/search/热门电影'
content = fetch_movie_search_results_dynamic(url)

if 'error' in content:
    print(content['error'])
else:
    print("Title:", content['title'])
    for movie in content['movies']:
        print(f"Movie Title: {movie['title']}")
        print(f"Movie Info: {movie['info']}")
        print("-" * 40)
