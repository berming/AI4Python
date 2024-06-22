import requests
from bs4 import BeautifulSoup

def fetch_webpage_content(url):
    """
    Fetch the title and paragraphs from a given webpage.

    Parameters:
    - url (str): The URL of the webpage to fetch.

    Returns:
    - dict: A dictionary with the title and list of paragraphs.
    """
    # 发送HTTP请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code != 200:
        return {'error': 'Failed to retrieve the webpage.'}

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 抓取网页标题
    title = soup.title.string if soup.title else 'No title found'

    # 抓取所有段落内容
    paragraphs = [p.text for p in soup.find_all('p')]

    return {
        'title': title,
        'paragraphs': paragraphs
    }

# 测试爬虫功能
url = 'https://example.com'
content = fetch_webpage_content(url)
print("Title:", content['title'])
print("Paragraphs:", content['paragraphs'])
