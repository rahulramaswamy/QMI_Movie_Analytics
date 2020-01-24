import scrapy
import pandas as pd
import json
import re
import time

class ReviewSpider(scrapy.Spider):
	name = "reviews"
	df = pd.read_csv('titles.csv')

	start_urls = []
	for title in df['title']:
		title = title.replace(' ', '%20').lower()
		start_urls.append(f'https://www.metacritic.com/search/movie/{title}/results')
	def parse(self, response):
		data = {
			'url': response.xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a/@href').extract_first(),
		}
		df = pd.DataFrame([data])
		with open('metacritic_urls.csv', 'a') as fd:
		   	df.to_csv(fd, mode = 'a', header=False)
		yield data