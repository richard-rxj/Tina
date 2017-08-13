#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import time

#Twitter API credentials, removed due to privacy concerns, needs to be replaced when use. Note these keys can be applied via any twitter account
consumer_key = "4TROq0lwXWB5T7EWT5jVAf7Ii"
consumer_secret = "1Qdvmoq4KiD51jlF0Gdg8NbpaqKj6GWxlu4FCCHwQd2kZaoNsd"
access_key = "786201772096303108-pftfiLTyZ4vEs1QjrdGXKYHTtZzbEy2"
access_secret = "67Lg1gvsxet7YOLmS96DqpRYLGYoXX3WbiYXUDWwBTvFF"

keywords_list = ["acquisition", "articles", "asset sale", "auditor", "award", "blackout", "board", "certification", "conference call", "conferences", "credit agreement", "debt agreement", "debt restructure", "director interests", "dividends", "DRIPs", "drug trial", "earnings", "financial", "listing", "litigation", "merger", "management changes", "mineral updates", "option exercise", "own capital", "presentations", "private placements", "public offering", "ratings", "reorganization", "rights offering", "shareholder meeting", "shareholder resolution", "shareholder rights", "speech", "spin-off", "stock splits", "strategic alliance", "strike", "subsidiary dissolution", "sustainability", "tech report", "tender offer"]

sleep_time = 200
def get_alltweets_by_user(api, screen_name):
def get_tweets_info(input_file_name, output_file_name):
#Twitter only allows access to all users in 'input_file_name' most recent tweets with this method
# input_file_name: consists all informationa of users
# output_file_name: output information to the given file name

#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	with open(input_file_name, 'r') as inputFile :
		reader = csv.reader(inputFile)
		for row in reader:
			user_id = row[0]

			twitter_account = row[4]
			account_type = row[3]
			exec_id=row[0]
# get all tweets for the user with 'twitter_account'
# check whether the user has a twitter account if not skip this row

			if (twitter_account == "N/A") or (twitter_account==""):
				continue

			screen_name = twitter_account[1:]

			try:
				user_screen_name = api.get_user(screen_name)
				if user_screen_name.protected == True:
					print("%s do not authorize to access his/her account" % screen_name)
					continue
			except tweepy.error.TweepError as e:
					loop_flag = True
					while loop_flag:
						print ("Rate limit reached. Sleeping")
						time.sleep(sleep_time)
						try:
							user_screen_name = api.get_user(screen_name)
						except tweepy.TweepError as e2:
							if e.api_code == 88: continue
						loop_flag = False
				elif e.api_code == 34:
					print ("%s does not exist in twitter" % screen_name)
					continue
				elif e.api_code == 63:
					print ("%s 's user account is suspended" % screen_name)
					continue
				else:
					print (e)
					print ("%s" % screen_name)
			if user_screen_name is None: continue

	with open(output_file_name, 'w', newline='') as outputFile:
		writer = csv.writer(outputFile)
		write_row_string = ["execid", "EXEC_FULL_NAME", "Compared_Chen2016", "TYPE", "TWITTER ACCOUNT", "First_join", "First_tweet", "Comments",  "Number_follower", "Number_following", "Tweet_time", "Tweet_text"]
		print(write_row_string)
		writer.writerow(write_row_string)
		writer.writerows(all_tweets)


if __name__ == '__main__':
	output_file_name = "all_tweets_output.csv"
	user_info_file_name = "all_tweets_input.csv"
	get_tweets_info(user_info_file_name, output_file_name)

