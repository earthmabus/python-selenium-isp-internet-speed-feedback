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
                'ipAddress' : results['ip_addr'],
                'mode' : results['mode'],
                'download (mbps)' : results['download'],
                'upload (mbps)' : results['upload'],
                'ping (ms)' : results['ping'],
                'latencyUp (ms)' : results['latency_up'],
                'latencyDown (ms)' : results['latency_down']
            }
        }

        sheety_response = requests.post(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/internetSpeedTracking/results", json=sheety_body, headers=sheety_header)
        sheety_response.raise_for_status()

    def get_all_results(self):
        sheety_header = {"Authorization": f"Bearer {GOOGLE_SHEET_INTERNET_SPEED_TRACKING_TOKEN}"}
        response = requests.get(url="https://api.sheety.co/3a66a46ee7c6d694f1a39c8a7971826a/internetSpeedTracking/results", headers=sheety_header)
        print(response.text)
        return response.text
