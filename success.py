### 한국장학재단 크롤링 final code (IE)

import selenium
from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager

options = webdriver.IeOptions()

options.add_argument('--start-fullscreen')  # full screen

driver = webdriver.Ie('./IEDriverServer',options=options)
driver.maximize_window();

@contextmanager
def wait_for_new_window(driver, timeout=30):
    handles_before = driver.window_handles
    yield
    WebDriverWait(driver, timeout).until(
        lambda driver: len(handles_before) != len(driver.window_handles))

def check_exists_by_css_selector(css_selector):
    try:
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException :
        print("TimeOutException")

#button 누를 때 ajax
def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 30)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        print("AJAXException")

#curs = conn.cursor()
def LoanCrawling(url) :
    driver.get(url) #get 사용해서 text 불러옴

    id_send = "document.getElementById('userId').value = 'ivory93';"
    driver.execute_script(id_send)

    pw_send = "document.getElementById('passwd').value = 'mylord6899';"
    driver.execute_script(pw_send)

    start_login = driver.find_element_by_id('startIdLogin')
    start_login.click()

    # 로그인 후 페이지 로딩 기다림
    check_exists_by_css_selector('div.InnerWrap > ul > li ')

    # banner 때문에 오류 -> url로 이동
    driver.get('http://www.kosaf.go.kr/ko/mypage.do')

    check_exists_by_css_selector('#container > div > div > div.mem_con')

    loan_info = driver.find_elements_by_css_selector('#container > div > div > div.mem_con > div:nth-child(3) > div > dl:nth-child(1) > dd')

    loan = loan_info[0].text
    repayment =loan_info[1].text
    loan_balance = loan_info[2].text
    print(loan)
    print(repayment)
    print(loan_balance)
    print(" ")

    check_exists_by_css_selector("a[title='학자금대출 내역 더보기']")
    more = driver.find_element_by_css_selector("a[title='학자금대출 내역 더보기']")  #title 이 학자금 대출 내역 더보기인 a tag 선택
    more.click()

    check_exists_by_css_selector('#kosafLoan > tbody')
    Loantrs = driver.find_elements_by_css_selector('#kosafLoan > tbody > tr')      #tr의 list

    for rows in range(0, len(Loantrs)):
        window_before = driver.window_handles[0]
        detail_btn = Loantrs[rows].find_element_by_css_selector('td')

        loan_classify = Loantrs[rows].find_element_by_css_selector('td:nth-child(2)').text

        # 취업후상환학자금 or 일반상환학자금
        loan_classify.split('_')[0]
        print(loan_classify.split('_')[0] )

        # 생활비 or 등록금
        loan_classify.split('_')[1]
        print(loan_classify.split('_')[1] )


        detail_btn.click()

        wait_for_new_window(driver)
        # 새로운 window 화면 list index out of range error
        window_after = driver.window_handles[1]
        # 눌러서 detail 확인
        loanDetail(window_before,window_after)

def loanDetail(window_before,window_after) :

    # 기다려야 새로운 창 반영가능
    # driver가 바뀌어서 강제로 20초 설정
    driver.implicitly_wait(20)

    driver.switch_to.window(window_after)

    # 로딩이 완료되기를 기다림
    check_exists_by_css_selector('#popup_wrap > div.tableBox03.ml20.mr20.mb15 > table')

    detail_tr = driver.find_elements_by_css_selector('#popup_wrap > div.tableBox03.ml20.mr20.mb15 > table > tbody > tr')

    detail_td = detail_tr[0].find_elements_by_css_selector('td')  #td array
    #대출 상품
    loan_product = detail_td[1].text
    #세분류
    loan_detail = detail_td[3].text
    #대출계좌
    loan_account = detail_td[5].text

    detail_td = detail_tr[1].find_elements_by_css_selector('td')  #td array

    #대출 학기
    loan_semester = detail_td[1].text
    #대출 일자
    loan_date = detail_td[3].text
    #거치 기한
    loan_deadline = detail_td[5].text

    detail_td = detail_tr[2].find_elements_by_css_selector('td')  #td array

    #대출 금액
    loan_total = detail_td[1].text
    #상환 방법
    repayment_method = detail_td[3].text
    #대출 기한
    loan_period = detail_td[5].text

    detail_td = detail_tr[3].find_elements_by_css_selector('td')  #td array

    #대출 잔액
    loan_remain = detail_td[1].text
    #든든상환기간구분
    repayment_classification = detail_td[3].text
    #금리
    rate = detail_td[5].text

    detail_td = detail_tr[4].find_elements_by_css_selector('td')  #td array

    #자동이체납입일
    repayment_auto_day = detail_td[1].text
    #대출 상태
    loan_status = detail_td[3].text
    #정부 보전 금리
    gov_rate =detail_td[5].text

    detail_td = detail_tr[5].find_elements_by_css_selector('td')  #td array

    #이자 납입 자동이체 계좌
    interest_auto_account =detail_td[1].text

    print("대출상품: %s 세분류: %s 대출계좌: %s 대출학기: %s 대출일자: %s 거치기한: %s 대출 금액: %s 상환 방법: %s 대출기한: %s 대출 잔액: %s 든든상환기간구분: %s 금리: %s 자동이체납입일: %s 대출상태: %s 정부보전금리 :%s 이자 납입 자동 이체 계좌: %s " %(loan_product,loan_detail, loan_account, loan_semester, loan_date, loan_deadline, loan_total, repayment_method, loan_period, loan_remain, repayment_classification,rate, repayment_auto_day,loan_status, gov_rate, interest_auto_account))

    #거래 내역
    deal = driver.find_elements_by_css_selector('#popup_wrap > div:nth-child(5) > div.tableBox.mb20.clear > table > tbody')
    for td in deal :
        print(td.text)

    overdue = driver.find_element_by_css_selector('#lnkOvdBkd')
    overdue.click()
    wait_for_ajax(driver)
    deal = driver.find_elements_by_css_selector('#popup_wrap > div:nth-child(4) > div.tableBox.mb20.clear > table > tbody')
    for td in deal :
        print(td.text)

    wait_for_ajax(driver)
    repay = driver.find_element_by_css_selector('#lnkRpmtScd')
    repay.click()
    wait_for_ajax(driver)
    deal = driver.find_elements_by_css_selector('#popup_wrap > div:nth-child(5) > div.tableBox.mb20.clear > table > tbody')
    for td in deal :
        print(td.text)

    print(" ")

    driver.close()

    driver.switch_to.window(window_before)

url = "http://www.kosaf.go.kr/ko/login_sc.do"

LoanCrawling(url)
