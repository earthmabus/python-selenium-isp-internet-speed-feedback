import os
import requests

GOOGLE_SHEET_INTERNET_SPEED_TRACKING_TOKEN = os.environ.get("SHEETYCO_BEARER_TOKEN_INTERNET_SPEED_TEST_RESULTS")

# this class internet speed test results into a google sheet
# the information on the sheet can be analyzed
class SpeedTestResultsStorage:
    def __init__(self):
        pass

    def store_results(self, results):
        sheety_header = {"Authorization": f"Bearer {GOOGLE_SHEET_INTERNET_SPEED_TRACKING_TOKEN}"}
        sheety_body = {
            "result" : {
                'date' : results['date'],
                'time' : results['time'],
                'resultId' : results['result_id'],
                'ipAddr' : results['ip_addr'],
                'mode' : results['mode'],
                'download' : results['download'],
                'upload' : results['upload'],
                'ping' : results['ping'],
                'latencyUp' : results['latency_up'],
                'latencyDown' : results['latency_down']
            }
        }

        sheety_response = requests.post(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/internetSpeedTracking/results", json=sheety_body, headers=sheety_header)
        sheety_response.raise_for_status()