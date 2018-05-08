#!/usr/bin/env python# encoding: utf-8import tweepy #https://github.com/tweepy/tweepyimport csvimport timefrom _datetime import datetime#Twitter API credentials, removed due to privacy concerns, needs to be replaced when use. Note these keys can be applied via any twitter accountconsumer_key = "4TROq0lwXWB5T7EWT5jVAf7Ii"consumer_secret = "1Qdvmoq4KiD51jlF0Gdg8NbpaqKj6GWxlu4FCCHwQd2kZaoNsd"access_key = "786201772096303108-pftfiLTyZ4vEs1QjrdGXKYHTtZzbEy2"access_secret = "67Lg1gvsxet7YOLmS96DqpRYLGYoXX3WbiYXUDWwBTvFF"sleep_time = 200def get_alltweets_by_user(api, screen_name):    all_tweets=[]    temp_tweets=[]    try:        temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200))    except tweepy.error.TweepError as e:        if e.api_code == 88:            loop_flag = True            while loop_flag:                print("Rate limit reached. Sleeping")                time.sleep(sleep_time)                try:                    temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200))                except tweepy.TweepError as e2:                    if e.api_code == 88: continue                    else:	print(e)                loop_flag=False    while len(temp_tweets)>0:        oldest_id=temp_tweets[-1].id-1        all_tweets.extend(temp_tweets)        temp_tweets=[]        try:            #time.sleep(sleep_time)            temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200, max_id=oldest_id))        except tweepy.error.TweepError as e:            if e.api_code == 88:                loop_flag = True                while loop_flag:                    print("Rate limit reached. Sleeping")                    time.sleep(sleep_time)                    try:                        temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200, max_id=oldest_id))                    except tweepy.TweepError as e2:                        if e.api_code == 88: continue                        else: print(e)                    loop_flag=False    return all_tweetsdef get_tweets_info(input_file_name, output_file_name):#Twitter only allows access to all users in 'input_file_name' most recent tweets with this method# input_file_name: consists all informationa of users# output_file_name: output information to the given file name#authorize twitter, initialize tweepy    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)    auth.set_access_token(access_key, access_secret)    api = tweepy.API(auth)    all_tweets=[]    with open(input_file_name, 'r') as inputFile :        reader = csv.reader(inputFile)        #next(reader)        for row in reader:            exec_id = ""#row[0]            #if exec_id=="784": break            twitter_account = row[0]            account_type = ""#row[4]            gvkey=""#row[2]            exec_full_name=""#row[1]            #exec_compared=row[2]            #first_join=row[5]            #first_join=datetime.strptime(str(row[5]), "%d/%m/%y")            #first_tweet=row[6]            #first_tweet=datetime.strptime(row[6], "%d/%m/%y")            #comments=row[7]# get all tweets for the user with 'twitter_account'# check whether the user has a twitter account if not skip this row            if (twitter_account == "N/A") or (twitter_account==""):                continue            screen_name = get_screen_name(twitter_account)            try:                user_screen_name = api.get_user(screen_name)                if user_screen_name.protected == True:                    print("%s do not authorize to access his/her account" % screen_name)                    row.append("do not authorize to access his/her account")                    all_tweets.extend([row])                    continue            except tweepy.error.TweepError as e:                if e.api_code == 88:                    loop_flag = True                    while loop_flag:                        print ("Rate limit reached. Sleeping")                        time.sleep(sleep_time)                        try:                            user_screen_name = api.get_user(screen_name)                        except tweepy.TweepError as e2:                            if e.api_code == 88: continue                        loop_flag = False                elif e.api_code == 34:                    print ("%s does not exist in twitter" % screen_name)                    row.append("does not exist in twitter")                    all_tweets.extend([row])                    continue                elif e.api_code == 63:                    print ("%s 's user account is suspended" % screen_name)                    row.append("user account is suspended")                    all_tweets.extend([row])                    continue                else:                    print (e)                    row.append(str(e))                    all_tweets.extend([row])                    print ("%s" % screen_name)                    continue            if user_screen_name is None: continue            num_followers = user_screen_name.followers_count            user_id=user_screen_name.id_str            num_following = user_screen_name.friends_count                        row.append(str(num_followers))                        row.append(str(num_following))            temp_tweets=get_alltweets_by_user(api, screen_name)            print("_"+screen_name)            for single_tweet in temp_tweets:                is_retweet=False                original_retweet_id = ""                if hasattr(single_tweet, "retweeted_status"):                    is_retweet=True                    original_retweet_id=single_tweet.retweeted_status.id_str                is_quote=False                original_quote_id=""                if hasattr(single_tweet, "quoted_status"):                    is_quote=True                    original_quote_id=single_tweet.quoted_status['id_str']                single_output=[exec_id, exec_full_name, gvkey, account_type, twitter_account,user_id, num_followers, num_following, single_tweet.id_str, single_tweet.created_at, single_tweet.text.encode("utf-8"), single_tweet.favorite_count, single_tweet.retweet_count, single_tweet.in_reply_to_screen_name, single_tweet.in_reply_to_status_id_str, is_retweet, original_retweet_id, is_quote, original_quote_id];                all_tweets.extend([single_output])    with open(output_file_name, 'w', newline='') as outputFile:        writer = csv.writer(outputFile)        write_row_string = ["Id", "ConName", "Gvkey", "Account", "TWITTER ACCOUNT", "TWITTER_ACCOUNT_ID",  "Number_follower", "Number_following", "Tweet_id_str", "Tweet_time", "Tweet_text", "likes", "retweets", "Is a reply","reply_tweet_id", "Is a retweet", "retweet_tweet_id","Is a quote","quote_tweet_id"]        print(write_row_string)        writer.writerow(write_row_string)        writer.writerows(all_tweets)def get_screen_name(inputString):    return inputString[0:]if __name__ == '__main__':    output_file_name = "20180422_reply_account_result.csv"    user_info_file_name = "20180422_reply_account.csv"    get_tweets_info(user_info_file_name, output_file_name)