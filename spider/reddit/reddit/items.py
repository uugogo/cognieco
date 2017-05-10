# -*- coding: utf-8 -*-

from scrapy import Item, Field


class RedditItem(Item):
	subreddit = Field()
	link = Field()
	title = Field()
	date = Field()
	vote = Field()
	top_comment = Field()