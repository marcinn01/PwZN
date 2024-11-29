import requests
from bs4 import BeautifulSoup
import json
import argparse
import rich

rich.get_console().clear()

parser = argparse.ArgumentParser(description="Loading data from a webpage and saving it into JSON file.")
parser.add_argument('output_file', help="Give name of JSON file for saving data")
args = parser.parse_args()

res = requests.get("https://www.fizyka.pw.edu.pl/")

if res.status_code == 200:
    soup = BeautifulSoup(res.content, 'html.parser')

    data = {}
    data['title'] = soup.title.text.strip()

    links = soup.find_all('a')
    data['links'] = [link.get('href') for link in links]

    with open(args.output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)
else:
    print(f"Failed to load webpage.")
