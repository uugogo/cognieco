# -*- coding: utf-8 -*-

import re

import BeautifulSoup

from scrapy import Spider, Request
from reddit.items import RedditItem



class RedditSpider(Spider):
	name = 'reddit'
	allowed_domains = ['reddit.com']
	start_urls = ['https://www.reddit.com/r/bigdata/',
				  'https://www.reddit.com/r/datascience/',
				  'https://www.reddit.com/r/bigdatajobs/',
				  'https://www.reddit.com/r/datagangsta/',
				  'https://www.reddit.com/r/machinelearning/',
				  'https://www.reddit.com/r/datacleaning/',
				  'https://www.reddit.com/r/scientificresearch/',
				  'https://www.reddit.com/r/artificial/',
				  'https://www.reddit.com/r/robotics/',
				  'https://www.reddit.com/r/statistics/',
				  'https://www.reddit.com/r/automate/',
				# 'https://www.reddit.com/r/gaming/',
				# 'https://www.reddit.com/r/bigdata/',
				# 'https://www.reddit.com/r/movies/',
				# 'https://www.reddit.com/r/science/',
				# 'https://www.reddit.com/r/totallynotrobots/',
				# 'https://www.reddit.com/r/uwotm8/',
				# 'https://www.reddit.com/r/videos/',
				'https://www.reddit.com/r/worldnews/']


	def parse(self, response):

		i = 0
		links = response.xpath('//p[@class="title"]/a[@class="title may-blank outbound"]/@href').extract()
		titles = response.xpath('//p[@class="title"]/a[@class="title may-blank outbound"]/text()').extract()
		dates = response.xpath('//p[@class="tagline"]/time[@class="live-timestamp"]/@title').extract()
		votes = response.xpath('//div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract()
		comments = response.xpath('//div[@id="siteTable"]//a[@class="comments may-blank"]/@href').extract()
		#comments = response.xpath('//div[@id="siteTable"]//li[@class="first"]/a/text()').extract()
		for l in links:
			i=i+1
		if i == 0:
			links = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/@href').extract()
			titles = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/text()').extract()


		# for link in links:
		# 	print "links:	",link
		# for link in titles:
		# 	print "titles:	",link
		# for link in dates:
		# 	print "dates:	",link
		# for link in votes:
		# 	print "votes:	",link
		# for link in comments:
		# 	print "comments:	",link

		for i, link in enumerate(links):
			item = RedditItem()
			item['subreddit'] = ""#str(re.findall('/r/[A-Za-z]*8?', link))[3:len(str(re.findall('/r/[A-Za-z]*8?', link))) - 2]
			item['link'] = links[i]
			item['title'] = titles[i]
			item['date'] = dates[i]
			if votes[i] == u'\u2022':
				item['vote'] = 'hidden'
			else:
				item['vote'] = votes[i]
			item['top_comment']=""

			yield item

			# request = Request(link, callback=self.parse_comment_page)
			# request.meta['item'] = item
            #
			# yield request


	def parse_comment_page(self, response):

		item = response.meta['item']
		print "parse fuck comment",item

		top = response.xpath('//div[@class="commentarea"]//div[@class="md"]').extract()[0]
		top_soup = BeautifulSoup(top, 'html.parser')
		item['top_comment'] = top_soup.get_text().replace('\n', ' ')

		yield item

		