import os
import time
from internet_speed_bot import InternetSpeedBot
from speed_test_results_storage import SpeedTestResultsStorage
from social_media import SocialMedia

PROMISED_DOWN = 150
PROMISED_UP = 10
CHROME_DRIVER_PATH = "/home/michael/PycharmProjects/chromedriver"

# create a bot that can run speed tests
speedbot = InternetSpeedBot()
speedbot.start()

# create a class to store results
results_storage = SpeedTestResultsStorage()
#results_storage.get_all_results()

# instantiate social media
# commenting out social media since X seems to have a detector where it doesn't allow logins from selenium
#socialmedia = SocialMedia()
#socialmedia.login()
socialmedia = None

while True:
    # conduct a speed test
    result = speedbot.get_internet_speed()

    # print the results
    print(result)

    # store the results
    results_storage.store_results(result)

    if socialmedia is not None and result['download'] > PROMISED_DOWN and result['upload'] > PROMISED_UP:
        # post that we're having a great internet experience
        message = "I'm having excellent results with my internet connection right now.\n"
        message += f"I'm getting downloads of {result['download']} Mbps and uploads of {result['upload']} Mbps.\n"
        message += "Thank you for being a great internet provider!"
        socialmedia.post_to_social_media(message)
    else:
        # let's stick to positive reinforcement when it comes to social media
        print("connection sucks right now, so i'm not posting anything")

    time.sleep(600)