# python-selenium-isp-internet-speed-feedback

This application is designed to monitor the upload and download speeds of the machine it runs on.  If the internet speeds are acceptable, the application will write a positive post onto it's social media account.

The application works by
* Communicating with X.com via its API (go to https://developer.x.com)
* Gathering network performance using https://www.speedtest.net via selenium automation
* Storing results into a google sheet

Upgrade Ideas
* Store results into a real data source that would allow for analytics
* Post graphs of network performance instead of just tweets of momentary results
* Run analytics
