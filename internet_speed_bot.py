from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime as dt
import re

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

        start_time = dt.datetime.now()

        # start the speed test
        elem_go_btn = self.m_driver.find_element(By.CLASS_NAME, "start-text")
        elem_go_btn.click()

        # wait for it to complete
        time.sleep(60)

        # if the close "Try Speedtest for Desktop" dialog box is present, close it out
        try:
            print("checking if dialog box is present")
            elem_dialog_close_btn = self.m_driver.find_element(By.ID, "close-btn")
            if elem_dialog_close_btn.is_displayed():
                print("dialog box is present, closing")
                elem_dialog_close_btn.click()
        except NoSuchElementException:
            print("dialog box not detected")

        # acquire the results of the speed test
        elem_label_download = self.m_driver.find_element(By.CLASS_NAME, "download-speed")
        elem_label_upload = self.m_driver.find_element(By.CLASS_NAME, "upload-speed")
        elem_label_ping_in_ms = self.m_driver.find_element(By.CLASS_NAME, "ping-speed")
        elem_label_latency_up = self.m_driver.find_element(By.CSS_SELECTOR, '[data-latencyup-status-value]')
        elem_label_latency_down = self.m_driver.find_element(By.CSS_SELECTOR, '[data-latencydown-status-value]')
        elem_connection_mode = self.m_driver.find_element(By.CLASS_NAME, 'result-item-connection-mode')
        elem_ip_addr = self.m_driver.find_element(By.CLASS_NAME, 'js-data-ip')
        elem_result_id = self.m_driver.find_element(By.CSS_SELECTOR, '[data-result-id]')

        mode = re.search(r'Connections\s+(\S+)', elem_connection_mode.text)
        if not mode:
            mode = "Unknown"

        return {
            'date' : start_time.strftime("%m/%d/%Y"),
            'time' : start_time.strftime("%H:%M:%S"),
            'result_id' : elem_result_id.text,
            'ip_addr' : elem_ip_addr.text,
            'mode' : mode.group(0),
            'download' : elem_label_download.text,
            'upload' : elem_label_upload.text,
            'ping' : elem_label_ping_in_ms.text,
            'latency_up' : elem_label_latency_up.text,
            'latency_down' : elem_label_latency_down.text
        }

    def shutdown(self):
        # close the browser when we're done using it
        # driver.close() # closes the active tab
        self.m_driver.quit() # closes the entire browser
