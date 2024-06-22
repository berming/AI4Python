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
            link_elem = title_elem.find('a')
            if link_elem:
                link = link_elem.get('href')
            else:
                link = ''

            # 查找文件数量、文件大小、时间戳、BTIH
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
