#from scraper.scraper import get_data_from_url
from scraper.cleaner import cleaner
from datetime import datetime
import pandas as pd
import os

def save_ad_to_csv(path: str, data: pd.DataFrame):
    
    path = f"./data/{datetime.strftime(datetime.today(), '%d-%m-%Y')}/{path}-{datetime.strftime(datetime.today(), '%d-%m-%Y')}.csv"
    data.to_csv(path)

def create_folder():
    if not os.path.exists(f"./data/{datetime.strftime(datetime.today(), '%d-%m-%Y')}"):
       os.makedirs(f"./data/{datetime.strftime(datetime.today(), '%d-%m-%Y')}")


def get_clean_data(stranica):
    content = get_data_from_url(stranica)
    clean_data = cleaner(content)
    return clean_data



def main():
    stranica = "https://www.njuskalo.hr/iphone-14?condition%5Bused%5D=1&condition%5Bdefective%5D=1&page=3"


    content_scraped = get_data_from_url(stranica)
    


if __name__ == "__main__":
    main()



