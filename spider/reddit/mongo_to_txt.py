# -*- coding: utf-8 -*-

import sys
import pymongo

reload(sys)
sys.setdefaultencoding('UTF8')

client = pymongo.MongoClient()
db = client.reddit

subreddits = ['/r/circlejerk', '/r/gaming', '/r/FloridaMan', '/r/movies',
					'/r/science', '/r/Seahawks', '/r/totallynotrobots', 
					'/r/uwotm8', '/r/videos', '/r/worldnews']

for sub in subreddits:
	cursor = db.post.find({"subreddit": sub})
	for doc in cursor:
		with open("text_files/%s.txt" % sub[3:], 'a') as f:
			f.write(doc['title'])
			f.write('\n\n')
			f.write(doc['top_comment'])
			f.write('\n\n')

client.close()