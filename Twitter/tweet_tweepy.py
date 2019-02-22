import tweepy
import time
from dateutil.parser import parse


class TweepyHelper:
    # Twitter API credentials, removed due to privacy concerns, needs to be replaced when use. Note these keys can be applied via any twitter account

    consumer_key = "4TROq0lwXWB5T7EWT5jVAf7Ii"

    consumer_secret = "1Qdvmoq4KiD51jlF0Gdg8NbpaqKj6GWxlu4FCCHwQd2kZaoNsd"

    access_key = "786201772096303108-pftfiLTyZ4vEs1QjrdGXKYHTtZzbEy2"

    access_secret = "67Lg1gvsxet7YOLmS96DqpRYLGYoXX3WbiYXUDWwBTvFF"

    keywords_list = ["acquisition", "articles", "asset sale", "auditor", "award", "blackout", "board", "certification",
                     "conference call", "conferences", "credit agreement", "debt agreement", "debt restructure",
                     "director interests", "dividends", "DRIPs", "drug trial", "earnings", "financial", "listing",
                     "litigation", "merger", "management changes", "mineral updates", "option exercise", "own capital",
                     "presentations", "private placements", "public offering", "ratings", "reorganization",
                     "rights offering", "shareholder meeting", "shareholder resolution", "shareholder rights", "speech",
                     "spin-off", "stock splits", "strategic alliance", "strike", "subsidiary dissolution",
                     "sustainability",
                     "tech report", "tender offer"]

    sleep_time = 60

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    def get_tweetInfo_byId(twitter_id):
        if (twitter_id is None or len(twitter_id) < 1):
            return ""
        auth = tweepy.OAuthHandler(TweepyHelper.consumer_key, TweepyHelper.consumer_secret)
        auth.set_access_token(TweepyHelper.access_key, TweepyHelper.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        try:
            twitter_info = api.get_status(twitter_id)
            return twitter_info.text
        except tweepy.error.TweepError as e:
            return ""
        except:
            return ""

    def get_tweet_info(screen_name, company_record=None):
        result = []
        try:
            user_screen_name = TweepyHelper.api.get_user(screen_name)

            if user_screen_name.protected == True:
                print("%s do not authorize to access his/her account" % screen_name)
                result.append("do not authorize to access his/her account")
                if company_record is not None:
                    company_record.other_comment = "do not authorize to access his/her account"
                return result
        except tweepy.error.TweepError as e:
            if "Rate limit" in e.reason:
                loop_flag = True
                while loop_flag:
                    print("Rate limit reached. Sleeping")
                    time.sleep(TweepyHelper.sleep_time)
                    try:
                        user_screen_name = TweepyHelper.api.get_user(screen_name)
                    except tweepy.error.TweepError as e2:
                        if "Rate limit" in e2.reason: continue
                    loop_flag = False
            else:
                print(e)
                result.append(str(e))
                if company_record is not None:
                    company_record.other_comment = str(e)
                return result

        if user_screen_name is None:
            result.append("None screen name")
        num_followers = user_screen_name.followers_count
        user_id = user_screen_name.id_str
        num_following = user_screen_name.friends_count
        result.append(TweepyHelper.trans_long_digit(user_id))
        result.append(str(num_followers))
        result.append(str(num_following))

        if company_record is not None:
            try:
                company_record.company_tweet_accound_id = TweepyHelper.trans_long_digit(user_id)
                company_record.total_following = num_following
                company_record.total_follower = num_followers
                company_record.company_twitter_date_actual=parse(str(user_screen_name.created_at))
                company_record.total_tweet_actual=user_screen_name.statuses_count
            except ValueError:
                print(company_record.company_screen_name)
        return result

    def get_alltweets_by_user(screen_name):
        all_tweets = []
        temp_tweets = []
        try:
            temp_tweets.extend(TweepyHelper.api.user_timeline(screen_name=screen_name, count=200))
        except tweepy.error.TweepError as e:
            if e.api_code == 88:
                loop_flag = True
                while loop_flag:
                    print("Rate limit reached. Sleeping")
                    time.sleep(TweepyHelper.sleep_time)
                    try:
                        temp_tweets.extend(TweepyHelper.api.user_timeline(screen_name=screen_name, count=200))
                    except tweepy.TweepError as e2:
                        if e.api_code == 88:
                            continue
                        else:
                            print(e)
                    loop_flag = False
        while len(temp_tweets) > 0:
            oldest_id = temp_tweets[-1].id - 1
            all_tweets.extend(temp_tweets)
            temp_tweets = []
            try:
                # time.sleep(sleep_time)
                temp_tweets.extend(TweepyHelper.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest_id))
            except tweepy.error.TweepError as e:
                if e.api_code == 88:
                    loop_flag = True
                    while loop_flag:
                        print("Rate limit reached. Sleeping")
                        time.sleep(TweepyHelper.sleep_time)
                        try:
                            temp_tweets.extend(
                                TweepyHelper.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest_id))
                        except tweepy.TweepError as e2:
                            if e.api_code == 88:
                                continue
                            else:
                                print(e)
                        loop_flag = False
        result = []
        for single_tweet in all_tweets:
            is_retweet = False
            reply_tweet_text = TweepyHelper.get_tweetInfo_byId(single_tweet.in_reply_to_status_id_str)
            original_retweet_id = ""
            if hasattr(single_tweet, "retweeted_status"):
                is_retweet = True
                original_retweet_id = single_tweet.retweeted_status.id_str
            is_quote = False
            original_quote_id = ""
            if hasattr(single_tweet, "quoted_status"):
                is_quote = True
                original_quote_id = single_tweet.quoted_status.id_str
            single_output = [TweepyHelper.trans_long_digit(single_tweet.id_str), single_tweet.created_at,
                             single_tweet.text.encode("utf-8"),
                             single_tweet.favorite_count, single_tweet.retweet_count,
                             single_tweet.in_reply_to_screen_name,
                             TweepyHelper.trans_long_digit(single_tweet.in_reply_to_status_id_str), reply_tweet_text,
                             is_retweet,
                             TweepyHelper.trans_long_digit(original_retweet_id), is_quote,
                             TweepyHelper.trans_long_digit(original_quote_id)];
            result.append(single_output)
        return result

    def trans_long_digit(input):
        inputStr = str(input)
        if (input is None or len(inputStr) < 1):
            return input
        else:
            return "'" + inputStr


if __name__ == '__main__':
    pass
