import requests
from bs4 import BeautifulSoup

# 基础URL
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# 迭代所有页面
page = 1
while True:
    # 构建当前页面的URL
    url = base_url.format(page)
    response = requests.get(url)

    # 检查页面是否存在
    if response.status_code != 200:
        break

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    # 如果当前页面没有书籍，则退出循环
    if not books:
        break

    # 遍历每本书并提取信息
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()

        print(f"书名: {title}")
        print(f"价格: {price}")
        print(f"库存情况: {availability}")
        print('-' * 20)

    page += 1
