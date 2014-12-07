# -*- coding: utf-8 -*-
#__author__ = 'kxekxe'

import facebook
import os
import sys
from dateutil.parser import parse

LAST_UPD = 'last_update'
#getting new token from https://developers.facebook.com/tools/explorer/
TOKEN = 'CAACEdEose0cBAMv7SDmHAKQBzafh3nQk2bTRDa204iMv5kUN04t75L7WSUJKuo8DO9UmZAELxEhZCZAhoSpflibZCU3C8lS89xrB3cEY36Tv0VYI7Og99oHMnWaA7U8SilVi0ctxlZALy9Nzll6D5IneYCvDvZB7sSL2clLNDuETZBLtZCejFfIpCVlw1cEN7mpZBgZAXp6IXLZCJH4zks3ja5ZB'

def main():
	page = sys.argv[1]
	last_time = ''
	file_text = ''
	#load last update
	if os.path.exists(LAST_UPD):
		with open('last_update', 'r') as infile:
			file_text = infile.readlines()
			for line in file_text:
				if line.split(' ')[0] == page:
					last_time = line.split(' ')[1]
		infile.close()
	try:
		print 'getting posts from %s...' % page
		graph = facebook.GraphAPI(TOKEN)
		profile = graph.get_object(page)
		posts = graph.get_connections(profile['id'], 'posts')
	except facebook.GraphAPIError, e:
		print 'error: GraphAPIError: %s ' % (e.result)
		raise
	updated = []
	if last_time == posts['data'][0]['updated_time']:
		print 'there are no new posts'
	#if it first start
	if not last_time:
		last_time = posts['data'][0]['updated_time']
		print 'last post from %s\n%s ' % (posts['data'][0]['updated_time'], posts['data'][0]['message'].encode(sys.stdout.encoding, errors='replace'))
	else:
		for post in posts['data']:
			if parse(post['updated_time']) > parse(last_time):
				updated.append(post)
			else:
				break
	if updated:
		for post in updated:
			print '%s\n%s\n\n' % (parse(post['updated_time']).strftime('%Y.%m.%d %H:%M:%S'), post['message'].encode(sys.stdout.encoding, errors='replace'))
	#save last update
	with open('last_update', 'w') as outfile:
		outfile.write('%s %s'%(page, posts['data'][0]['updated_time']))
		for line in file_text:
			if line.split(' ')[0] != page:
				outfile.write(line)
	outfile.close()


if __name__ == '__main__':
	main()
