import scrapy
import pandas as pd
import json

class TitleSpider(scrapy.Spider):
	name = "titles"

	url = "https://www.boxofficemojo.com/yearly/chart/?yr="

	temp1 = []

	for x in range(2008,2020):
		temp = url+str(x)
		temp1.append(temp)

	start_urls=temp1


	def parse(self, response):
		data = {
			'year': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/h1/text()').extract_first()[:4],
			'title': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/table/tr[2]/td/table/tr[@bgcolor="#ffffff" or @bgcolor="#f4f4ff"]//td[2]//text()').getall()[:-2],
			'studio': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/table/tr[2]/td/table/tr[@bgcolor="#ffffff" or @bgcolor="#f4f4ff"]//td[3]//text()').getall()[:-2],
			'total_gross': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/table/tr[2]/td/table/tr[@bgcolor="#ffffff" or @bgcolor="#f4f4ff"]//td[4]//text()').getall()[:-2],
			'total_theaters': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/table/tr[2]/td/table/tr[@bgcolor="#ffffff" or @bgcolor="#f4f4ff"]//td[5]//text()').getall()[:-2],
			'openining_gross': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/table/tr[2]/td/table/tr[@bgcolor="#ffffff" or @bgcolor="#f4f4ff"]//td[6]//text()').getall()[:-2],
			'opening_gross': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/table/tr[2]/td/table/tr[@bgcolor="#ffffff" or @bgcolor="#f4f4ff"]//td[7]//text()').getall()[:-2],
			'opening_date': response.xpath('//*[@id="body"]/table[3]/tr/td[1]/table/tr[2]/td/table/tr[@bgcolor="#ffffff" or @bgcolor="#f4f4ff"]//td[8]//text()').getall()
		}
		import json
		with open('result.json', 'a') as fp:
		    json.dump(data, fp)

		yield data