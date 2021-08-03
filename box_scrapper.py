# Scrap www.boxofficemojo.com to take ratings of the best movies by year using requests. 
import os
import requests
from requests_html import HTML
import datetime
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(__file__)

# This function allow you to import the html from the url and save it locally in case you want to parse later.
def url_to_txt(url, filename="world.html", save=False):
    r = requests.get(url)
    if r.status_code == 200: # 200 in HTML means that the program found the page that we want to scrap.
        html_text = r.text
        if save:
            with open(filename, 'w') as f:
                f.write(html_text)
        return html_text
    return None


# This function allow you to search into the html and find the data that we want.
def parse_and_extract(url, year='2021'):
    
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
    r_html = HTML(html=html_text)
    table_class = ".imdb-scroll-table"
    r_table = r_html.find(table_class)

    table_data = []

    if len(r_table) == 1:
        parsed_table = r_table[0]
        rows = parsed_table.find("tr")
        header_row = rows[0]
        header_cols = header_row.find("th")
        header_names = [x.text for x in header_cols]

        for row in rows[1:]:
            cols = row.find("td")
            row_data = []
            for i, col in enumerate(cols):
                row_data.append(col.text)
            table_data.append(row_data)


    df = pd.DataFrame(table_data, columns=header_names)
    df = df.drop(columns='Rank')
    df['Year'] = np.full(len(table_data), year)
    path = os.path.join(BASE_DIR, 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join('data', f'{year}.csv')
    df.to_csv(filepath, index=False)


def run(start_year=2021, years_ago=25):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year
    assert isinstance(start_year, int)
    assert isinstance(years_ago, int)
    assert len(f"{start_year}") == 4
    for i in range(0, years_ago+1):
        url = f'https://www.boxofficemojo.com/year/world/{start_year}'
        parse_and_extract(url, year=start_year)
        print(f"Finished {start_year}")
        start_year -= 1


if __name__ == "__main__":
    run()