"""Module simulating Letterboxd API using LetterboxdUser class."""

from typing import List, Dict
import requests
from bs4 import BeautifulSoup


class LetterboxdUser():
    """Letterboxed user class
    """

    def __init__(self, letterboxd_username: str, letterboxd_base_url: str):

        self.username = letterboxd_username
        self.base_url = letterboxd_base_url

    def get_list(self, list_type: str) -> List[str]:
        """Gets followers and following lists

        Args:
            type (str): chooses between followers and following 

        Returns:
            list (str): string list containing usernames
        """

        url = f'{self.base_url}/{list_type}'
        soup = BeautifulSoup(requests.get(url, timeout=200).text, 'html.parser')
        username_list = []
        base_url_list = []
        username_base_url_list = []

        for soup_text in soup.find_all("a", {"class": "name"}):
            username_list += [soup_text.text.strip()]

        for soup_text in soup.find_all("a", {"class" : "avatar -a40"}):
            base_url_list += [f"https://letterboxd.com{soup_text.attrs['href']}"]

        for i, username in enumerate(username_list):
            username_base_url_list += [(username, base_url_list[i])]

        return username_base_url_list

    def get_film_dict(self) -> Dict:
        """gets dictionary containing film information

        Returns:
            dict: film dictionary
        """
        
        print(f'Getting film rating dictionary for {self.username}')
        url = f'{self.base_url}/films'
        soup = BeautifulSoup(requests.get(url, timeout=200).text, 'html.parser')

        try:
            page_count = int(soup.find_all("li", {"class": "paginate-page"})[-1].text.strip())
        except IndexError:
            page_count = 1

        film_rating_dict = {}

        for page_number in range(1, page_count + 1):

            url = f'{self.base_url}/films/page/{page_number}'
            soup = BeautifulSoup(requests.get(url, timeout=200).text, 'html.parser')
            film_poster_rating_list = [(div_soup.find("div"), div_soup.find("p")) for div_soup in soup.find_all("li", {"class": "poster-container"})]
            for film_poster_rating in film_poster_rating_list:
                film_relative_link = film_poster_rating[0].attrs['data-target-link']
                film_url = f'https://letterboxd.com{film_relative_link}'
                try:
                    film_rating_text = film_poster_rating[1].find('span').text.strip()
                    film_rating = film_rating_text.count('★') + (0.5 * film_rating_text.count('½'))
                except AttributeError:
                    continue
                film_rating_dict[film_url] = film_rating

        return film_rating_dict
