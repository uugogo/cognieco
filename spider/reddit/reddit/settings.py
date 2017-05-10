# -*- coding: utf-8 -*-

BOT_NAME = 'reddit'

SPIDER_MODULES = ['reddit.spiders']
NEWSPIDER_MODULE = 'reddit.spiders'

DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {'reddit.pipelines.DuplicatesPipeline':300,
'reddit.pipelines.MongoDBPipeline':800, }

MONGODB_SERVER = "10.154.156.125"
MONGODB_PORT = 27017
MONGODB_DB = "reddit"
MONGODB_COLLECTION = "post"