#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import time

#Twitter API credentials, removed due to privacy concerns, needs to be replaced when use. Note these keys can be applied via any twitter account
consumer_key = "xxx"
consumer_secret = "yyy"
access_key = "zzz"
access_secret = "mm"

keywords_list = ["acquisition", "articles", "asset sale", "auditor", "award", "blackout", "board", "certification", "conference call", "conferences", "credit agreement", "debt agreement", "debt restructure", "director interests", "dividends", "DRIPs", "drug trial", "earnings", "financial", "listing", "litigation", "merger", "management changes", "mineral updates", "option exercise", "own capital", "presentations", "private placements", "public offering", "ratings", "reorganization", "rights offering", "shareholder meeting", "shareholder resolution", "shareholder rights", "speech", "spin-off", "stock splits", "strategic alliance", "strike", "subsidiary dissolution", "sustainability", "tech report", "tender offer"]

sleep_time = 60

def check_friendships(input_file_name, output_file_name):
	#Twitter only allows access to all users in 'input_file_name' most recent tweets with this method
        # input_file_name: consists all informationa of users
        # output_file_name: output information to the given file name

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	#api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	api = tweepy.API(auth)
	
        # read file 'input_file_name' to obtain information about the user, such as fullname, twitter account, etc
        all_users_screen_names = []
        with open(input_file_name, 'rb') as inputFile:
                reader = csv.reader(inputFile)
                for row in reader:
                        twitter_account = row[3]
                        if twitter_account == "N/A":
                                continue
                        
                        screen_name = twitter_account[1:]
                        if screen_name == '' : continue
                        all_users_screen_names.append(screen_name)

        all_users_screen_names = all_users_screen_names[1:]
        #print all_users_screen_names
        follower_info_all_users = []
        with open(input_file_name, 'rb') as inputFile :
                reader = csv.reader(inputFile)
                for row in reader:
                        co_per_rol = row[0]
                        exec_full_name = row[1]
                        co_name = row[2]
                        twitter_account = row[3]
                        account_type = row[4]
                        exec_id = row[5]
                        gvkey = row[6]

                        if twitter_account == "N/A":
                                continue
                        
                        screen_name = twitter_account[1:]
                        user_screen_name = None
                        try:
                                user_screen_name = api.get_user(screen_name)
				if user_screen_name.protected == True:
					print "%s do not authorize to access his/her account" % screen_name
					continue
                        except tweepy.error.TweepError as e:
				if e[0][0]['code'] == 88:
					loop_flag = True
					while loop_flag:
						print "Rate limit reached. Sleeping"
						time.sleep(sleep_time)
						try:
							user_screen_name = api.get_user(screen_name)
						except tweepy.TweepError as e2:
							if e[0][0]['code'] == 88: continue
						loop_flag = False
				elif e[0][0]['code'] == 34:
					print "%s does not exist in twitter" % screen_name
					continue
				elif e[0][0]['code'] == 63:
					print "%s 's user account is suspended" % screen_name
					continue
				else:
					print e
			
			if user_screen_name is None: continue

                        print "%s" % screen_name
			
                        num_followers = user_screen_name.followers_count
                        num_following = user_screen_name.friends_count
                        ceo_followers = []

                        for follower in all_users_screen_names:
                                if follower == screen_name : continue
                                print follower
				try:
					if api.show_friendship(source_screen_name=follower, target_screen_name=screen_name)[0].followed_by :
						print "friend!!"
						ceo_followers.append(follower)
				except tweepy.error.TweepError as e:
					if e[0][0]['code'] == 88:
						loop_flag = True
						while loop_flag:
							print "Rate limit reached. Sleeping"
							time.sleep(sleep_time)
							try:
								if api.show_friendship(source_screen_name=follower, target_screen_name=screen_name)[0].followed_by:
									print "friend!!"
									ceo_followers.append(follower)
							except tweepy.TweepError as e2:
								if e[0][0]['code'] == 88: continue
							loop_flag = False
					elif e[0][0]['code'] == 34:
						print "%s does not exist in twitter" % screen_name
						continue
					elif e[0][0]['code'] == 63:
						print "%s 's user account is suspended" % screen_name
						continue
					else:
						print e

                        temp_list = [co_per_rol, exec_full_name, co_name, twitter_account, account_type, exec_id, gvkey, num_followers, num_following]
                        temp_list.extend(ceo_followers)
                        follower_info_all_users.extend([temp_list])
                pass
        pass
        with open(output_file_name, 'wb') as outputFile:
                writer = csv.writer(outputFile)
                write_row_string = ["CO_PER_ROL", "EXEC_FULL_NAME", "CO_NAME", "TWITTER ACCOUNT", "TYPE", "EXEC_ID", "GV_KEY", "# OF FOLLOWERS", "# OF FOLLOWING"]

                print write_row_string
	        writer.writerow(write_row_string)
                writer.writerows(follower_info_all_users)
        pass


def get_all_tweets(input_file_name, output_file_name):
	#Twitter only allows access to all users in 'input_file_name' most recent tweets with this method
        # input_file_name: consists all informationa of users
        # output_file_name: output information to the given file name

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

        # read file 'input_file_name' to obtain information about the user, such as fullname, twitter account, etc.

        all_users_tweets = []
                                               
        with open(input_file_name, 'rb') as inputFile :
                reader = csv.reader(inputFile)
                for row in reader:
                        #user_id = row[0]
                        co_per_rol = row[0]
                        exec_full_name = row[1]
                        co_name = row[2]
                        twitter_account = row[3]
                        account_type = row[4]
                        exec_id = row[5]
                        gvkey = row[6]
                        
                        # get all tweets for the user with 'twitter_account'
                        # check whether the user has a twitter account if not skip this row
                        if (twitter_account == "N/A") or (twitter_account==""):
                                continue
                        
                        screen_name = twitter_account[1:]
                        
                        try:
                                user_screen_name = api.get_user(screen_name)
				if user_screen_name.protected == True:
					print "%s do not authorize to access his/her account" % screen_name
					continue
                        except tweepy.error.TweepError as e:
				if e[0][0]['code'] == 88:
					loop_flag = True
					while loop_flag:
						print "Rate limit reached. Sleeping"
						time.sleep(sleep_time)
						try:
							api.get_user(screen_name)
						except tweepy.TweepError as e2:
							if e[0][0]['code'] == 88: continue
						loop_flag = False
				elif e[0][0]['code'] == 34:
					print "%s does not exist in twitter" % screen_name
					continue
				elif e[0][0]['code'] == 63:
					print "%s 's user account is suspended" % screen_name
					continue
				else:
				        print e

                        print "%s" % screen_name
                        #initialize a list to hold all the tweepy Tweets
	                alltweets = []	
	
	                #make initial request for most recent tweets (200 is the maximum allowed count)
	                new_tweets = []

                        try:
                                new_tweets.extend(api.user_timeline(screen_name = screen_name, count=200))
                        except tweepy.error.TweepError as e:
				if e[0][0]['code'] == 88:
					loop_flag = True
					while loop_flag:
						print "Rate limit reached. Sleeping"
						time.sleep(sleep_time)
						try:
							new_tweets.extend(api.user_timeline(screen_name = screen_name, count=200))
						except tweepy.TweepError as e2:
							if e[0][0]['code'] == 88: continue
						loop_flag = False
				elif e[0][0]['code'] == 34:
					print "%s does not exist in twitter" % screen_name
					continue
				elif e[0][0]['code'] == 63:
					print "%s 's user account is suspended" % screen_name
					continue
				else:
				        print e
	                if len(new_tweets) == 0:
                                print "%s has no new tweets" % exec_full_name
                                continue
                
                        #save most recent tweets
                        #alltweets.extend(new_tweets)
                        for tweet in new_tweets:
                                if tweet not in alltweets:
                                        alltweets.extend([tweet])
	
	                #save the id of the oldest tweet less one
	                oldest = alltweets[-1].id - 1
	
	                #keep grabbing tweets until there are no tweets left to grab
	                while len(new_tweets) > 0:
		                print "getting tweets before %s" % (oldest)
		                
		                #all subsiquent requests use the max_id param to prevent duplicates
				try:
					new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest)
				except  tweepy.error.TweepError as e:
					if e[0][0]['code'] == 88:
						loop_flag = True
						while loop_flag:
							print "Rate limit reached. Sleeping"
							time.sleep(sleep_time)
							try:
								new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
							except tweepy.TweepError as e2:
								if e[0][0]['code'] == 88: continue
							loop_flag = False
					elif e[0][0]['code'] == 34:
						print "%s does not exist in twitter" % screen_name
						continue
					elif e[0][0]['code'] == 63:
						print "%s 's user account is suspended" % screen_name
						continue
					else:
						print e
			
		                #save most recent tweets
		                #alltweets.extend(new_tweets)
                                for tweet in new_tweets:
                                        if tweet not in alltweets:
                                                alltweets.extend([tweet])
		                
		                #update the id of the oldest tweet less one
		                oldest = alltweets[-1].id - 1
		                
		                print "...%s tweets downloaded so far" % (len(alltweets))
	                        
	                #transform the tweepy tweets into a 2D array that will populate the csv
                        outtweets = []
                        for tweet in alltweets:
                                contains_keyword = 0
                                for key_w in keywords_list:
                                        if tweet.text.encode("utf-8").find(key_w) != -1:
                                                contains_keyword = 1
                                                break
                        
                                temp_list = [co_per_rol, exec_full_name, co_name, twitter_account, account_type, exec_id, gvkey, tweet.created_at, tweet.text.encode("utf-8"), contains_keyword]
                                at_users = [word for word in tweet.text.encode("utf-8").split() if word.startswith('@')]
                                #print at_users
                                temp_list.extend(at_users)
                                #print temp_list
                                outtweets.extend([temp_list])
	                all_users_tweets.extend(outtweets)   
                pass
        pass
        with open(output_file_name, 'wb') as outputFile:
                writer = csv.writer(outputFile)
                write_row_string = ["CO_PER_ROL", "EXEC_FULL_NAME", "CO_NAME", "TWITTER ACCOUNT", "TYPE", "EXEC_ID", "GV_KEY", "CREATED_AT", "TEXT", "CONTAINS_KEYWORDS"]

                print write_row_string
	        writer.writerow(write_row_string)
                writer.writerows(all_users_tweets)
        pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
        output_file_name = "tweets_all_uesrs.csv"
        output_file_name2 = "user_account_info_all_users.csv"
        user_info_file_name = "./input.csv/input1.csv"
	print "get all tweets of all users"
        get_all_tweets(user_info_file_name, output_file_name)
	#print "check friendships of all users"
	#check_friendships(user_info_file_name, output_file_name2)
	
