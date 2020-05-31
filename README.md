# AirticketMaster
Scraper for air tickets

# Get Started
### Install Scrapy
1. `pip install Scrapy`
2. Check [Scrapy installing guide ](https://docs.scrapy.org/en/latest/intro/install.html) if you are facing any problem.

### Install Selenium
- `pip install selenium`
- Download [Chrome web driver](https://chromedriver.chromium.org/downloads) or [FireFox web driver](https://github.com/mozilla/geckodriver/releases)
  * You need to find out your chrome version first:
    * Go to `chrome://settings/help` and find the version.
  * Find out which version of webdriver needs to be used.
- Put the downloaded webdriver into folder 
  * For mac: `/usr/local/bin/`
  * For windows: `C:\Windows`

# How to Run?
-> scrapy crawl [spider name]
e.g. scrapy crawl gospider
