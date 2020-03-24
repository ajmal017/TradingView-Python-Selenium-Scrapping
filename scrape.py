"""
Import necessary packages
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import csv
import os
from datetime import datetime

csv_header = [['DATE', 'TIME', 'PRIMARY_TICKER', 'CALCULATE_TICKER']]


def wait_until_load(driver, by, value):
    """
    Wait until any elements will be loaded
    :param driver: Chrome driver
    :param by: class, css selector, xpath etc for finding out elements.
    :param value: the real value of class, css selector, xpath etc.
    :return: Boolean Data
    """
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
        print('page loaded')
        return True
    except TimeoutException:
        print("Loading took too much time!")
        return False


def write_direct_csv(lines, filename):
    with open('output/%s' % filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)
    csv_file.close()


def write_csv(lines, filename):
    """
    Write results to csv file
    :param lines: 2D array for writing
    :param filename: filename for saving
    :return: Nothing
    """
    if not os.path.isdir('output'):
        os.mkdir('output')
    if not os.path.isfile('output/%s' % filename):
        write_direct_csv(lines=csv_header, filename=filename)
    write_direct_csv(lines=lines, filename=filename)


def extension():
    """
        Start chrome extension
        """
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.get("https://www.tradingview.com/chart/PiPMAZfh/")

    # Wait until sign button is loaded
    wait_until_load(driver, By.CLASS_NAME, 'tv-header__device-signin')
    # Click sign link
    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/a').click()

    # Wait until username input box of login page is loaded
    wait_until_load(driver, By.CSS_SELECTOR, 'input[name="username"]')
    # Input username to username input box.
    username = driver.find_element_by_tag_name("input[name='username']")
    username.clear()
    username.send_keys("sanforce")

    # Wait until password input box of login page is loaded
    wait_until_load(driver, By.CSS_SELECTOR, 'input[name="password"]')
    # Input password to password input box
    password = driver.find_element_by_tag_name("input[name='password']")
    password.clear()
    password.send_keys("PythonProject1")

    # Click submit button of login form
    submit = driver.find_element_by_tag_name('button[type="submit"]')
    submit.click()

    driver.maximize_window()
    wait = wait_until_load(driver, By.XPATH,
                           '/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div/div[2]/div/div[5]/div[2]')
    if not wait:
        driver.close()
    """
        Loop the process for reading and writing to csv file every 10 seconds
        """
    while True:
        # Wait for 6 seconds
        time.sleep(10)
        # Find ticker elements using xpath
        primary_ticker = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div/div[2]/div/div[5]/div[2]').text
        calculate_ticker = driver.find_element_by_xpath(
            '/html/body/div[2]/div[1]/div[3]/div[1]/div/table/tr[3]/td[2]/div/div[2]/div/div[2]/div[2]/div[3]/div/div/div').text

        if not primary_ticker:
            print('Not calculated primary ticker')
        if not calculate_ticker:
            print('Not calculated calculated ticker')

        # Get current date and time
        date = datetime.today().strftime('%Y-%m-%d')
        current_time = datetime.now().time().strftime('%H:%M:%S')
        # Make list for writing using result
        line = [date, current_time, primary_ticker, calculate_ticker]
        if '' not in line:
            print(line)
            # Write list to csv file with TradingView.csv name, here path will be 'output/TradingView.csv'
            write_csv(lines=[line], filename='TradingView.csv')

    # Close chrome browser
    driver.close()


if __name__ == "__main__":
    print('==================== START ===================')
    extension()
