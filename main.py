"""Module to provide film suggestions based on Letterboxd information."""

from typing import Dict
import pandas as pd
from letterboxd import LetterboxdUser


def analyze_film_dict(film_dict: Dict, list_type: str, output_file_name: str) -> None:
    """Exports metadata dataframe from film dictionary

    Args:
        film_dict (Dict): film dictionary where keys are users
        list_type (str): follower vs following
        output_file_name (str): name of output file
    """

    print(f'Analyzing film dictionary list for all {list_type}')
    film_url_collection = []
    film_export = {
        'FILM_URL' : [],
        'RATER_COUNT': [],
        'AVERAGE_SCORE': []
        }

    for film_username in film_dict:
        film_url_collection += list(film_dict[film_username].keys())

    film_url_collection = list(set(film_url_collection))

    for film_url in film_url_collection:

        rater_count = 0
        rating_sum = 0

        for film_username in film_dict:

            try:
                film_rating = film_dict[film_username][film_url]
                rater_count += 1
                rating_sum += film_rating
            except KeyError:
                continue

        film_export['FILM_URL'] += [film_url]
        film_export['RATER_COUNT'] += [rater_count]
        film_export['AVERAGE_SCORE'] += [round((rating_sum / rater_count ) * 2) / 2]

    pd.DataFrame.from_dict(film_export).to_csv(output_file_name, index=False)


if __name__ == "__main__":

    USERNAME = 'naveenthebatman'
    PROFILE_URL = 'https://letterboxd.com/naveenthebatman'
    LIST_TYPE = 'following'
    OUTPUT_FILE_NAME = 'summary.csv'

    master_film_dict = {}

    for username, base_url in LetterboxdUser(USERNAME, PROFILE_URL).get_list(list_type=LIST_TYPE):
        master_film_dict[username] = LetterboxdUser(username, base_url).get_film_dict()

    analyze_film_dict(master_film_dict, LIST_TYPE, OUTPUT_FILE_NAME)
