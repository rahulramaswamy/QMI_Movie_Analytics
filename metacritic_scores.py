import scrapy
import pandas as pd
import json
import re
import time

class ReviewSpider(scrapy.Spider):
	name = "reviews"
	df = pd.read_csv('test_5.csv')
	start_urls = []
	for title in df['url']:
		start_urls.append(f'https://www.metacritic.com{title}')
	def parse(self, response):
		data = {
			'title': response.xpath('//*[@id="main_content"]/div/div[1]/div/table/tr/td[2]/div/table/tr/td[1]/div/div/div[1]/div/h1/text()').extract_first().strip(),
			'score': response.xpath('//*[@id="main_content"]/div/div[1]/div/table/tr/td[2]/div/table/tr/td[1]/div/div/div[2]/table/tr/td[2]/a/span/text()').extract_first()
		}
		df = pd.DataFrame([data])
		with open('metacritic_scores.csv', 'a') as fd:
		   	df.to_csv(fd, mode = 'a', header=False)
		yield data