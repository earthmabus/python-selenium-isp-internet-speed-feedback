import os
from internet_speed_bot import InternetSpeedBot

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = "/home/michael/PycharmProjects/chromedriver"
TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")

speedbot = InternetSpeedBot()
speedbot.start()
speedbot.get_internet_speed()