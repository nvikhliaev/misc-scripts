# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 17:00:21 2014

"""

from selenium import webdriver

browser = webdriver.Firefox()
for i in range(1,10):
    browser.get('http://myanimelist.net/people/'+str(i))
    x= browser.find_element_by_xpath('//*[@id="contentWrapper"]/h1')
    print x.text
browser.quit
browser.close