import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest


content= requests.get("https://pll.harvard.edu/catalog")
print (content)
