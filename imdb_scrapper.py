# IMDB scrap using BeautifulSoup and requests. Then realize some analysis of the data with pandas, and then to csv.
# If we avoid hammering the server with lots of requests p/ second, then we are much less likely to get our IP banned.
# We could use from time import sleep to control the velocity of the scrapping.

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)


def parse_and_extract_imdb(start_year='2021', pages=6):
    # Lists to store the scraped data
    names = []
    years = []
    imdb_ratings = []
    metascores = []
    votes = []
    genres = []
    durations = []
    # For every page in the interval
    for i in range(0, pages + 1):
        response = get('https://www.imdb.com/search/title?release_date=' + str(start_year) +
                       '&sort=num_votes,desc&page=' + str(i), headers={"Accept-Language": "en-US, en;q=0.5"}
                       )
        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_='ratings-metascore') is not None:
                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape genre
                genre = container.p.find('span', class_="genre").text
                genres.append(genre)

                # Scrape duration ---> It is not an int yet
                duration = container.p.find('span', class_='runtime').text
                durations.append(duration)

                # Scrape the year ---> It is not an int yet.
                year = container.h3.find('span', class_='lister-item-year').text
                years.append(year)

                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = container.find('span', class_='metascore').text
                metascores.append(int(m_score))

                # Scrape the number of votes
                vote = container.find('span', attrs={'name': 'nv'})['data-value']
                votes.append(int(vote))

    # Pandas Dataframe to store all the information
    df = pd.DataFrame({'Movie': names,
                       'Genre': genres,
                       'Duration': durations,
                       'Year': years,
                       'Imdb_rating': imdb_ratings,
                       'Metascore_rating': metascores,
                       'Votes': votes
                       })

    # Convert all the values in the year column to integers.
    df.loc[:, 'Year'] = df['Year'].str[-5:-1].astype(int)
    # Refactor genre
    df.loc[:, 'Genre'] = df['Genre'].str[1:-10].replace('"', '')
    # Convert all the values in the duration column to integers.
    df.loc[:, 'Duration'] = df['Duration'].str[0:3].astype(int)
    # Convert all the values in the IMDB ratings to 0/100 values.
    df.loc[:, 'Imdb_rating'] = (df['Imdb_rating'] * 10).astype(int)

    path = os.path.join(BASE_DIR, 'data_imdb')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join('data_imdb', f'{start_year}.csv')
    df.to_csv(filepath, index=False)


def run_imdb(start_year=2021, page_number=6, years_ago=2):
    assert isinstance(start_year, int)
    assert isinstance(page_number, int)
    assert isinstance(years_ago, int)
    assert len(f"{start_year}") == 4
    for i in range(0, years_ago + 1):
        parse_and_extract_imdb(start_year=start_year, pages=page_number)
        print(f"Finished {start_year}")
        start_year -= 1


if __name__ == "__main__":
    run_imdb()
