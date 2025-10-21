from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

MAX_ELEMENT_WAIT_TIME_IN_SEC = 60

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
        elem_go_btn = self.m_driver.find_element(By.CLASS_NAME, "start-text")
        elem_go_btn.click()

        # TODO start here -- this part does not work right now...
        WebDriverWait(self.m_driver, MAX_ELEMENT_WAIT_TIME_IN_SEC).until(EC.presence_of_element_located((By.CSS_SELECTOR, "result-container-data")))
        elem_label_download = WebDriverWait(self.m_driver, MAX_ELEMENT_WAIT_TIME_IN_SEC).until(EC.presence_of_element_located((By.CSS_SELECTOR, "data-upload-status-value")))
        elem_label_upload = WebDriverWait(self.m_driver, MAX_ELEMENT_WAIT_TIME_IN_SEC).until(EC.presence_of_element_located((By.CSS_SELECTOR, "data-download-status-value")))
        print(f"results: download={elem_label_download.text} Mbps, upload={elem_label_upload.text} Mbps")
        # attribute data-upload-status-value="0.51"
        # attribute data-download-status-value="0.35"
        pass

    def store_results_into_sheet(self):
        '''Stores the results of a speed test in a google sheet'''
        pass

    def shutdown(self):
        # close the browser when we're done using it
        # driver.close() # closes the active tab
        self.m_driver.quit() # closes the entire browser
