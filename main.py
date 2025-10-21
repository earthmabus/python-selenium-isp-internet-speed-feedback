import os
import time
from internet_speed_bot import InternetSpeedBot
from speed_test_results_storage import SpeedTestResultsStorage

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = "/home/michael/PycharmProjects/chromedriver"
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

speedbot = InternetSpeedBot()
speedbot.start()
results_storage = SpeedTestResultsStorage()

while True:
    # conduct a speed test
    result = speedbot.get_internet_speed()

    # print the results
    print(result)

    # store the results
    results_storage.store_results(result)

    time.sleep(180)