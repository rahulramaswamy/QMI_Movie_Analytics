# File for all valid movie ids with titles
# http://files.tmdb.org/p/exports/movie_ids_MM_DD_YYYY.json.gz

from tqdm import tqdm
import numpy as np
import pandas as pd
import requests
import time

#movie_titles = ['Avatar', 'Avengers: Endgame', 'Pulp Fiction', 'Superbad', 'Avengers: Age of Ultron', 'The Avengers', 'Joker', 'The Dark Knight', 'Scarface', 'The Dark Knight Rises', 'Iron Man', 'Iron Man 2', 'Thor', 'Get Out', 'It', 'Spider-Man Homecoming', 'Cars', 'Toy Story']

api_key = '04cf8c70677690f36ab3e4b1b0464548'

movies = []

movies_df = pd.read_csv('movies_initial.csv')
movies_df = movies_df.sort_values('year')

movie_titles = movies_df['title'].tolist()
def get_movie_info(name):
	resp = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&language=en-US&query=' + name + '&page=1&include_adult=false&region=US')
	search = resp.json()['results'][0]
	id = search['id']
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=' + api_key + '&language=en-US')
	result = resp.json()
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/credits?api_key=' + api_key + '&language=en-US')
	credits = resp.json()
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/keywords?api_key=' + api_key)
	keywords = resp.json()
	resp = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '/release_dates?api_key=' + api_key)
	release_dates = resp.json()
	rating = next(certification for certification in release_dates['results'] if certification['iso_3166_1'] == 'US')
	try: 
		release = next(certification for certification in rating['release_dates'] if certification['certification'] != '')
	except Exception as e: 
		release = {'certification': 'N/A'}
	row = movies_df.loc[movies_df['title'] == search['title']]
	print(row)
	print(search['title'])
	movie = {
		'title': search['title'],
		'year': row['year'].tolist()[0],
		'release_date': result['release_date'],
		'cast': [credit['name'] for credit in credits['cast']],
		'crew': [{credit['job']: credit['name']} for credit in credits['crew']],
		'rating': release['certification'],
		'genres': [genre['name'] for genre in result['genres']],
		'studio': row['studio'].tolist()[0],
		'production_companies': [producer['name'] for producer in result['production_companies']],
		'runtime': result['runtime'],
		'in_collection': 1 if result['belongs_to_collection'] else 0,
		'overview': result['overview'],
		'keywords': [word['name'] for word in keywords['keywords']],
		'total_theaters': row['total_theaters'].tolist()[0],
		'opening_theaters': row['opening_theaters'].tolist()[0],
		'budget': result['budget'],
		'total_revenue': result['revenue'],
		'total_gross': row['total_gross'].tolist()[0],
		'opening_gross': row['opening_gross'].tolist()[0],
		'tmdb_id': id,
		'imdb_id': result['imdb_id'],
	}
	df2 = pd.DataFrame([movie])
	with open('movie_data.csv','a') as fd:
		df2.to_csv(fd, mode = 'a', header=False)
	time.sleep(0.2)
	return movie

for movie in tqdm(movie_titles):
    movies.append(get_movie_info(movie))

# df = pd.DataFrame(movies)

# df.to_csv('test.csv')

