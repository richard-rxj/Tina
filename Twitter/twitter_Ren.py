#!/usr/bin/env python# encoding: utf-8import tweepy  # https://github.com/tweepy/tweepyimport csvfrom pathlib import Pathimport sysimport time# Twitter API credentials, removed due to privacy concerns, needs to be replaced when use. Note these keys can be applied via any twitter accountconsumer_key = "4TROq0lwXWB5T7EWT5jVAf7Ii"consumer_secret = "1Qdvmoq4KiD51jlF0Gdg8NbpaqKj6GWxlu4FCCHwQd2kZaoNsd"access_key = "786201772096303108-pftfiLTyZ4vEs1QjrdGXKYHTtZzbEy2"access_secret = "67Lg1gvsxet7YOLmS96DqpRYLGYoXX3WbiYXUDWwBTvFF"keywords_list = ["acquisition", "articles", "asset sale", "auditor", "award", "blackout", "board", "certification",                 "conference call", "conferences", "credit agreement", "debt agreement", "debt restructure",                 "director interests", "dividends", "DRIPs", "drug trial", "earnings", "financial", "listing",                 "litigation", "merger", "management changes", "mineral updates", "option exercise", "own capital",                 "presentations", "private placements", "public offering", "ratings", "reorganization",                 "rights offering", "shareholder meeting", "shareholder resolution", "shareholder rights", "speech",                 "spin-off", "stock splits", "strategic alliance", "strike", "subsidiary dissolution", "sustainability",                 "tech report", "tender offer"]sleep_time = 1000def get_tweetInfo_byId(twitter_id):    if (twitter_id is None or len(twitter_id) < 1):        return ""    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)    auth.set_access_token(access_key, access_secret)    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)    try:        twitter_info = api.get_status(twitter_id)        return twitter_info.text    except tweepy.error.TweepError as e:        return ""    except:        return ""def read_info_from_csv(file_name, key_index, nrows=None):    result = {}    file_check = Path(file_name)    if (not file_check.exists()):        return result    with open(file_name, 'r', encoding='utf-8', errors='ignore') as inputFile:        reader = csv.reader(inputFile)        next(reader)        cur_rows = 0        for row in reader:            screen_name=get_screen_name(row[key_index])            if(screen_name not in result):                result[screen_name]=row            cur_rows += 1            if nrows == cur_rows:                break    return resultdef to_csv(line, file_name, is_append):    mode = 'w'    if (is_append == True):        mode = 'a'    try:        with open(file_name, mode, encoding='utf-8', errors='ignore',newline='') as outputFile:            writer = csv.writer(outputFile)            writer.writerow(line)    except:        print("write failed-------"+line)def get_screen_name(inputString):    return inputString[1:]def trans_long_digit(input):    inputStr=str(input)    if(input is None or len(inputStr)<1):        return input    else:        return "'"+inputStrdef get_tweet_info(api, screen_name):    result=[]    try:        user_screen_name = api.get_user(screen_name)        if user_screen_name.protected == True:            print("%s do not authorize to access his/her account" % screen_name)            result.append("do not authorize to access his/her account")            return result    except tweepy.error.TweepError as e:        if e.api_code == 88:            loop_flag = True            while loop_flag:                print("Rate limit reached. Sleeping")                time.sleep(sleep_time)                try:                    user_screen_name = api.get_user(screen_name)                except tweepy.TweepError as e2:                    if e.api_code == 88: continue                loop_flag = False        else:            print(e)            result.append(str(e))            return result    if user_screen_name is None:        result.append("None screen name")    num_followers = user_screen_name.followers_count    user_id = user_screen_name.id_str    num_following = user_screen_name.friends_count    result.append(trans_long_digit(user_id))    result.append(str(num_followers))    result.append(str(num_following))    return resultdef get_alltweets_by_user(api, screen_name):    all_tweets=[]    temp_tweets=[]    try:        temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200))    except tweepy.error.TweepError as e:        if e.api_code == 88:            loop_flag = True            while loop_flag:                print("Rate limit reached. Sleeping")                time.sleep(sleep_time)                try:                    temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200))                except tweepy.TweepError as e2:                    if e.api_code == 88: continue                    else:	print(e)                loop_flag=False    while len(temp_tweets)>0:        oldest_id=temp_tweets[-1].id-1        all_tweets.extend(temp_tweets)        temp_tweets=[]        try:            #time.sleep(sleep_time)            temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200, max_id=oldest_id))        except tweepy.error.TweepError as e:            if e.api_code == 88:                loop_flag = True                while loop_flag:                    print("Rate limit reached. Sleeping")                    time.sleep(sleep_time)                    try:                        temp_tweets.extend(api.user_timeline(screen_name = screen_name, count=200, max_id=oldest_id))                    except tweepy.TweepError as e2:                        if e.api_code == 88: continue                        else: print(e)                    loop_flag=False    result=[]    for single_tweet in all_tweets:        is_retweet = False        reply_tweet_text=get_tweetInfo_byId(single_tweet.in_reply_to_status_id_str)        original_retweet_id = ""        if hasattr(single_tweet, "retweeted_status"):            is_retweet = True            original_retweet_id = single_tweet.retweeted_status.id_str        is_quote = False        original_quote_id = ""        if hasattr(single_tweet, "quoted_status"):            is_quote = True            original_quote_id = single_tweet.quoted_status['id_str']        single_output = [trans_long_digit(single_tweet.id_str), single_tweet.created_at, single_tweet.text.encode("utf-8"),                         single_tweet.favorite_count, single_tweet.retweet_count, single_tweet.in_reply_to_screen_name,                         trans_long_digit(single_tweet.in_reply_to_status_id_str), reply_tweet_text, is_retweet, trans_long_digit(original_retweet_id), is_quote,                         trans_long_digit(original_quote_id)];        result.append(single_output)    return resultif __name__ == '__main__':    output_file_name = "20180226_output_20180507.csv"    input_file_name = "20180226_input.csv"    tweet_column_index = 3    input_user_infos = read_info_from_csv(input_file_name, tweet_column_index)    existing_user_infos_in_output = read_info_from_csv(output_file_name, tweet_column_index)    print("-------")    if (len(existing_user_infos_in_output) <= 0):        title=["handID",	"CONAME",	"gvkey",	"Company_twitter",	"Company_type",	"Company_twitter_month",	"Company_twitter_day", 	"Company_twitter_year",	"Company_twitter_date",                            "TWITTER_ACCOUNT_ID",  "Number_follower", "Number_following",                            "Tweet_id_str", "Tweet_time", "Tweet_text", "likes", "retweets", "Is a reply","reply_tweet_id", "reply_tweet_text", "Is a retweet", "retweet_tweet_id","Is a quote","quote_tweet_id"]        to_csv(title, output_file_name, False)    total = len(input_user_infos)    index = len(existing_user_infos_in_output)    #initialize the tweet api    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)    auth.set_access_token(access_key, access_secret)    api = tweepy.API(auth)    for screen_name in input_user_infos.keys():        if screen_name in existing_user_infos_in_output:            continue        index = index + 1        print(str(total) + "-" + str(index) + "_" + screen_name)        origin_input_info=input_user_infos[screen_name]        tweet_account_info=get_tweet_info(api,screen_name)        if(len(tweet_account_info)>1):            all_tweets=get_alltweets_by_user(api,screen_name)            for single_tweet in all_tweets:                to_output=[]                to_output.extend(origin_input_info)                to_output.extend(tweet_account_info)                to_output.extend(single_tweet)                to_csv(to_output, output_file_name, True)        else:            to_output=[]            to_output.extend(origin_input_info)            to_output.extend(tweet_account_info)            to_csv(to_output, output_file_name, True)