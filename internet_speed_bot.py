from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time

class InternetSpeedBot:
    def __init__(self):
        # configure chrome to stay open
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # create a webdriver
        self.m_driver = webdriver.Chrome(options=chrome_options)

    def start(self):
        self.m_driver.get("https://www.speedtest.net")

    def get_internet_speed(self):
        '''Executes an internet speed test to track download and upload performance'''
        time.sleep(2)

        elem_go_btn = self.m_driver.find_element(By.CLASS_NAME, "start-text")
        elem_go_btn.click()

        time.sleep(60)

        elem_label_download = self.m_driver.find_element(By.CLASS_NAME, "download-speed")
        elem_label_upload = self.m_driver.find_element(By.CLASS_NAME, "upload-speed")
        elem_label_ping_in_ms = self.m_driver.find_element(By.CLASS_NAME, "ping-speed")
        elem_label_latency_up = self.m_driver.find_element(By.CSS_SELECTOR, '[data-latencyup-status-value]')
        elem_label_latency_down = self.m_driver.find_element(By.CSS_SELECTOR, '[data-latencydown-status-value]')
        #data-latency-up-status-value
        print(f"results: download={elem_label_download.text} Mbps, upload={elem_label_upload.text} Mbps, ping={elem_label_ping_in_ms.text}, down={elem_label_latency_down.text}, up={elem_label_latency_up.text}")

    def store_results_into_sheet(self):
        '''Stores the results of a speed test in a google sheet'''
        pass

    def shutdown(self):
        # close the browser when we're done using it
        # driver.close() # closes the active tab
        self.m_driver.quit() # closes the entire browser
