

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def fetch_nvda_info(url):
    """
    Fetch information between "简介" and "公司访谈" from the given URL using Selenium and BeautifulSoup.

    Parameters:
    - url (str): The URL of the page to scrape.

    Returns:
    - str: The extracted information as a string.
    """
    options = Options()
    options.headless = True  # 在后台运行Chrome
    service = Service('/path/to/chromedriver')  # 修改为你的Chrome驱动路径
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    try:
        # 等待简介部分加载完成
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'stock-info'))
        )

        # 获取完整的HTML页面内容
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 找到简介部分和公司访谈部分
        intro_section = soup.find('div', class_='stock-info')
        company_interviews = soup.find('div', class_='company-visit')

        if not intro_section or not company_interviews:
            return "无法找到目标内容。"

        # 提取简介和公司访谈之间的内容
        content = []
        for elem in intro_section.find_next_siblings():
            if elem == company_interviews:
                break
            content.append(elem.text.strip())

        return "\n".join(content)

    finally:
        driver.quit()

# 测试爬虫功能
url = 'https://xueqiu.com/S/NVDA'
info = fetch_nvda_info(url)

# 打印结果
print("Extracted Information:")
print(info)
