# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 18:31:22 2014

@author: Nikita
"""

from lxml import html
import requests

index_url = "http://investing.businessweek.com/research/common/symbollookup/symbollookup.asp?letterIn=A&firstrow=180"


page = requests.get(index_url)
tree = html.fromstring(page.text)

names = tree.xpath('//*[@id="columnLeft"]/table/tbody/tr[1]/td[1]/a')