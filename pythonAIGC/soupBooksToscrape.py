import requests
from bs4 import BeautifulSoup

# 基础URL
base_url = "http://books.toscrape.com/catalogue/page-{}.html"
book_base_url = "http://books.toscrape.com/catalogue/{}"

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

    # 遍历每本书并提取详细信息
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()

        # 获取书籍详情页面的URL
        book_url = book_base_url.format(book.h3.a['href'])

        # 请求书籍详情页面
        book_response = requests.get(book_url)
        book_soup = BeautifulSoup(book_response.text, 'html.parser')

        # 提取详细信息
        description = book_soup.find('meta', {'name': 'description'})['content'].strip()
        upc = book_soup.find('th', text='UPC').find_next_sibling('td').text
        product_type = book_soup.find('th', text='Product Type').find_next_sibling('td').text
        price_excl_tax = book_soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text
        price_incl_tax = book_soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text
        tax = book_soup.find('th', text='Tax').find_next_sibling('td').text
        availability = book_soup.find('th', text='Availability').find_next_sibling('td').text
        number_of_reviews = book_soup.find('th', text='Number of reviews').find_next_sibling('td').text

        print(f"书名: {title}")
        print(f"价格: {price}")
        print(f"库存情况: {availability}")
        print(f"UPC: {upc}")
        print(f"产品类型: {product_type}")
        print(f"税前价格: {price_excl_tax}")
        print(f"含税价格: {price_incl_tax}")
        print(f"税: {tax}")
        print(f"描述: {description}")
        print(f"评论数: {number_of_reviews}")
        print('-' * 20)

    page += 1
