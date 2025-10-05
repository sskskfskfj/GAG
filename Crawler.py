from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import pandas as pd


base = 'https://blog.naver.com/congguksu/'
paths = ['70104758212','70108578583','70188231557']

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 크롬 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def crawl_gag_page(path : str):
    # 페이지 열기
    driver.get(base + path)
    time.sleep(3)  # 페이지 로딩 대기 (필요시 조정)

    # 네이버 블로그는 iframe 안에 본문이 있음 → iframe 전환
    driver.switch_to.frame('mainFrame')

    spans = driver.find_elements(
        By.CSS_SELECTOR,
        'div.se-module.se-module-text span.se-fs-fs13.se-ff-'
    )

    df = pd.DataFrame(columns = ['question', 'answer'])
    temp_list = []
    pattern = re.compile(r'^(?:\d{1,3}\.\s*|[가-힣A-Za-z])')

    for span in spans:
        span_strip = span.text.strip()

        if(span_strip == '구분'): break
        if(pattern.match(span_strip)):
            temp_list.append(re.sub(r'^\d+\.\s*', '', span_strip))
    
    for i in range(0, len(temp_list), 2):
        df.loc[i] = [temp_list[i], temp_list[i+1]]
        
    return df

concat_df = []
c = 1
for path in paths:
    print(f'attempt {c}')
    df = crawl_gag_page(path).reset_index(drop = True)
    concat_df.append(df)
    c += 1

result = pd.concat(concat_df, axis = 0, ignore_index = True)[:993]
print(result)

result.to_csv("df.csv")

