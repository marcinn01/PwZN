from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
import json
import rich

rich.get_console().clear()

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="name of created json file")
args = parser.parse_args()

name = args.file_name + ".json"

options = Options()
options.add_argument('--disable-notifications')

driver = webdriver.Chrome(options=options)
driver.get('https://allegro.pl/')

page_html = driver.page_source

data = {
    "page_html": page_html
}

with open(name, 'w') as f:
    json.dump(data, f)