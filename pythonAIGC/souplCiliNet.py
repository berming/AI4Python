import requests
from bs4 import BeautifulSoup

def fetch_hot_movies_magnet(url):
    """
    Fetch magnet search results for hot movies from given URL.

    Parameters:
    - url (str): The URL of the search results page.

    Returns:
    - list: A list of dictionaries containing movie details.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # 发送HTTP GET请求
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找电影卡片
    movie_cards = soup.find_all('div', class_='card')

    movies = []
    for card in movie_cards:
        title_elem = card.find('h5', class_='card-title')
        if title_elem:
            title = title_elem.text.strip()
            link = title_elem.find('a')['href']
            details_elem = card.find_all('p', class_='card-text')
            files = details_elem[0].text.strip().split('：')[1].strip()
            size = details_elem[1].text.strip().split('：')[1].strip()
            timestamp = details_elem[2].text.strip().split('：')[1].strip()
            btih = details_elem[2].find_next_sibling('p').text.strip().split('：')[1].strip()

            movie_info = {
                'title': title,
                'link': link,
                'files': files,
                'size': size,
                'timestamp': timestamp,
                'btih': btih
            }
            movies.append(movie_info)

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
