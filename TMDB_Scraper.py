# File for all valid movie ids with titles
# http://files.tmdb.org/p/exports/movie_ids_MM_DD_YYYY.json.gz

from tqdm import tqdm
import numpy as np
import pandas as pd
import requests
import time

movie_titles = ['Avatar', 'Avengers: Endgame', 'Pulp Fiction', 'Superbad', 'Avengers: Age of Ultron', 'The Avengers', 'Joker', 'The Dark Knight', 'Scarface', 'The Dark Knight Rises', 'Iron Man', 'Iron Man 2', 'Thor', 'Get Out', 'It', 'Spider-Man Homecoming', 'Cars', 'Toy Story']

api_key = '04cf8c70677690f36ab3e4b1b0464548'

# def get_movie(title):
#     resp = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&language=en-US&query=' + title + '&page=1&include_adult=false&region=US') #get movies by title from search
#     result = resp.json()['results'][0]
    
#     movie = {
#         'title': result['title'],
#         'tmdb_id': result['id']
#     }
#     return movie

movies = []
# for title in tqdm(movie_titles):
#     movies.append(get_movie(title))

def get_movie_info(name):
	resp = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&language=en-US&query=' + name + '&page=1&include_adult=false&region=US') #get movies by title from search
	search = resp.json()['results'][0]
	id = search['id']
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=' + api_key + '&language=en-US') #get movie by id
	result = resp.json()
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/credits?api_key=' + api_key + '&language=en-US')
	credits = resp.json()
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/keywords?api_key=' + api_key)
	keywords = resp.json()
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/release_dates?api_key=' + api_key)
	release_dates = resp.json()
	rating = next(certification for certification in release_dates['results'] if certification['iso_3166_1'] == 'US')
	release = next(certification for certification in rating['release_dates'] if certification['certification'] != '')
	movie = {
		'title': search['title'],
		'id': id,
		'budget': result['budget'],
		'in_collection': 1 if result['belongs_to_collection'] else 0,
		'genres': [genre['name'] for genre in result['genres']],
		'imdb_id': result['imdb_id'],
		'overview': result['overview'],
		'production_companies': [producer['name'] for producer in result['production_companies']],
		'release_date': result['release_date'],
		'total_revenue': result['revenue'],
		'runtime': result['runtime'],
		'cast': [credit['name'] for credit in credits['cast']],
		'crew': [{credit['job']: credit['name']} for credit in credits['crew']],
		'keywords': [word['name'] for word in keywords['keywords']],
		'rating': release['certification']
	}
	time.sleep(0.1)
	return movie

for movie in tqdm(movie_titles):
    movies.append(get_movie_info(movie))

df = pd.DataFrame(movies)

df.to_csv('test.csv')

