import requests
from bs4 import BeautifulSoup
import pandas as pd

# 基础URL
base_url = "http://books.toscrape.com/catalogue/page-{}.html"
book_base_url = "http://books.toscrape.com/catalogue/{}"

# 用于存储书籍信息的列表
books_data = []

# 迭代所有页面
page = 1
while page < 8:
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
        upc = book_soup.find('th', string='UPC').find_next_sibling('td').text
        product_type = book_soup.find('th', string='Product Type').find_next_sibling('td').text
        price_excl_tax = book_soup.find('th', string='Price (excl. tax)').find_next_sibling('td').text
        price_incl_tax = book_soup.find('th', string='Price (incl. tax)').find_next_sibling('td').text
        tax = book_soup.find('th', string='Tax').find_next_sibling('td').text
        availability = book_soup.find('th', string='Availability').find_next_sibling('td').text
        number_of_reviews = book_soup.find('th', string='Number of reviews').find_next_sibling('td').text

        # 将书籍信息添加到列表中
        books_data.append({
            '书名': title,
            '价格': price,
            '库存情况': availability,
            'UPC': upc,
            '产品类型': product_type,
            '税前价格': price_excl_tax,
            '含税价格': price_incl_tax,
            '税': tax,
            '描述': description,
            '评论数': number_of_reviews
        })

    page += 1

# 将数据保存到Excel文件中
df = pd.DataFrame(books_data)
df.to_excel('books_info.xlsx', index=False)

print("数据已保存到books_info.xlsx文件中")
