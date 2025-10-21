from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

TWITTER_URL = "https://www.x.com/"
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

SELENIUM_USER_ACTION_SLEEP_IN_SEC = 6

class SocialMedia:
    def __init__(self):
        self.m_driver = None

    def login(self):
        # configure chrome to stay open
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # navigate to X's website
        self.m_driver = webdriver.Chrome(options=chrome_options)
        self.m_driver.get(TWITTER_URL)
        time.sleep(SELENIUM_USER_ACTION_SLEEP_IN_SEC)

        # login with phone and password
        elem_signin_btn = self.m_driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a/div/span/span")
        elem_signin_btn.click()
        time.sleep(SELENIUM_USER_ACTION_SLEEP_IN_SEC)

        elem_phone_txt = self.m_driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input")
        elem_phone_txt.send_keys(TWITTER_EMAIL)
        time.sleep(SELENIUM_USER_ACTION_SLEEP_IN_SEC)
        elem_next_btn = self.m_driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div/span/span")
        elem_next_btn.click()
        time.sleep(SELENIUM_USER_ACTION_SLEEP_IN_SEC)

        elem_password_txt = self.m_driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/label/div/div[2]/div[1]/input")
        elem_password_txt.send_keys(TWITTER_PASSWORD)
        time.sleep(SELENIUM_USER_ACTION_SLEEP_IN_SEC)
        elem_login_btn = self.m_driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div/span/span")
        elem_login_btn.click()
        time.sleep(SELENIUM_USER_ACTION_SLEEP_IN_SEC)

    def post_to_social_media(self, msg : str):
        # click on the "Home" button so we can make it to the main page where a post can be sent
        elem_home_btn = self.m_driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[1]/div")
        elem_home_btn.click()
        time.sleep(SELENIUM_USER_ACTION_SLEEP_IN_SEC)

        # post a message
        elem_post_txt = self.m_driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div")
        elem_post_txt.send_keys(msg)
        elem_post_btn = self.m_driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span")
        elem_post_btn.click()
