import os
import time
from internet_speed_bot import InternetSpeedBot
from speed_test_results_storage import SpeedTestResultsStorage

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = "/home/michael/PycharmProjects/chromedriver"
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

# create a bot that can run speed tests
speedbot = InternetSpeedBot()
speedbot.start()

# create a class to store results
results_storage = SpeedTestResultsStorage()
#results_storage.get_all_results()

while True:
    # conduct a speed test
    result = speedbot.get_internet_speed()

    # print the results
    print(result)

    # store the results
    results_storage.store_results(result)

    time.sleep(180)