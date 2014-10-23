"""
A simple implementation of the selenium library (https://pypi.python.org/pypi/selenium).
The site being scraped (myanimelist.net) uses a platform called Incapsula which prevents
regular http requests.

The get around this, a firefox browser is opened and passed the url of the page to be scraped.
At this point, Incapsula does not see 'python' but rather 'firefox' and the required element is extracted
by xpath.
"""

from selenium import webdriver

browser = webdriver.Firefox()
for i in range(1,10):
    browser.get('http://myanimelist.net/people/'+str(i))
    x= browser.find_element_by_xpath('//*[@id="contentWrapper"]/h1')
    print x.text
browser.quit
browser.close
