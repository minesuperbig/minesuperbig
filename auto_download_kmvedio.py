#! /usr/bin/python3
import async_main
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

# 1.自动打开浏览器，进入快猫，自动登录。

while True:

    get_url = input("快猫视频网址：")

    if get_url:

        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--mute-audio")
        driver = webdriver.Chrome(options=opt)
        print('正在获取下载地址')
        driver.get(f'{get_url}')
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/div/div[1]/div/div/a').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[4]/div/div[2]/div[1]/input').send_keys(
            '18173708068')
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[4]/div/div[2]/div[2]/input').send_keys('123456')
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[4]/div/div[2]/button').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[7]/div/div[1]/button').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div/a[2]').click()
        time.sleep(1)
        act = ActionChains(driver)

        act.context_click(
            driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/div/div[2]/div/div')).perform()
        time.sleep(1)
        driver.find_element(By.XPATH,
                            '/html/body/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[6]/div[2]').click()
        time.sleep(3)
        k = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div[5]/div['
                                          '5]/span[2]').text
        print(f'成功获取下载地址{k}，正在下载！')
        async_main.main(k)

    else:
        break

