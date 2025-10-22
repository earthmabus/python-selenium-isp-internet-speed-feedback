import os
from internet_speed_bot import InternetSpeedBot
from speed_test_results_storage import SpeedTestResultsStorage
from social_media import SocialMedia
import time
import webbrowser
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

PROMISED_DOWN = float(150)
PROMISED_UP = float(10)
CHROME_DRIVER_PATH = "/home/michael/PycharmProjects/chromedriver"
TIME_BETWEEN_SPEED_TESTS_IN_SEC = 600

X_CLIENT_ID = os.environ.get("TWITTER_CLIENT_ID")
X_CLIENT_SECRET = os.environ.get("TWITTER_CLIENT_SECRET")
X_CALLBACK_REDIRECT_PORT = 5000
X_CALLBACK_IP = "127.0.0.1"
X_CALLBACK_REDIRECT_URI = f"http://{X_CALLBACK_IP}:{X_CALLBACK_REDIRECT_PORT}/callback"

# instantiate and log into X so that this application can post results to social media.
# a browser window to X.com will be launched and you will need to login using the account associated with the
# X_CLIENT_ID and X_CLIENT_SECRET.
#
# Successfully, logging into X.com will result in the browser issuing a callback to X_CALLBACK_REDIRECT_URI -- at this
# location will be a temporary webserver designed to handle a single request, running on this machine, in this
# application that is incarnated by the Handler class.  The Handler will handle an authentication handshake an ensure
# that the base user page can be loaded from X.com.
sm = SocialMedia(
    client_id=X_CLIENT_ID,
    client_secret=X_CLIENT_SECRET,     # keep secret safe; for public apps you can omit
    redirect_uri=X_CALLBACK_REDIRECT_URI,
    scopes="tweet.read tweet.write users.read offline.access",
    token_store_path="tokens.json")

class X_Callback_Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/callback"):
            qs = parse_qs(urlparse(self.path).query)
            code = qs.get("code", [None])[0]
            state = qs.get("state", [None])[0]
            ok = sm.exchange_code_for_token(code, state)
            if ok and sm.login():
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Authorized and posted.  You can close this tab.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Authorization failed.  Check terminal logs.")
        else:
            self.send_response(404)
            self.end_headers()

# start local server
httpd = HTTPServer((X_CALLBACK_IP, X_CALLBACK_REDIRECT_PORT), X_Callback_Handler)

# present the user a browser page to the authorization URL
auth_url = sm.new_auth_flow()
print("Visit and authorize:", auth_url)
webbrowser.open(auth_url)

# wait for the callback to occur after the user logs into X.com
print(f"Listening on {X_CALLBACK_REDIRECT_URI} ...")
httpd.handle_request()  # handle exactly one callback request and exit
print("Successfully authenticated with Social Media")

# create a bot that can run speed tests
speedbot = InternetSpeedBot()
speedbot.start()

# create a class to store results
results_storage = SpeedTestResultsStorage()
#results_storage.get_all_results()

print("Starting speed test bot...")
while True:
    # conduct a speed test
    result = speedbot.get_internet_speed()

    # print the results
    print(result)

    # store the results
    results_storage.store_results(result)

    if sm is not None and result['download'] > PROMISED_DOWN and result['upload'] > PROMISED_UP:
        # post that we're having a great internet experience
        message = "I'm having excellent results with my internet connection right now.\n"
        message += f"I'm getting downloads of {result['download']} Mbps and uploads of {result['upload']} Mbps.\n"
        message += "Thank you for being a great internet provider!"
        sm.create_post(message)
    else:
        # let's stick to positive reinforcement when it comes to social media
        print("Your internet connection sucks right now, so I'm not posting anything")

    time.sleep(TIME_BETWEEN_SPEED_TESTS_IN_SEC)