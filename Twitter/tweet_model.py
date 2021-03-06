#!/usr/bin/env python

# encoding: utf-8

from dateutil.parser import parse
import pandas as pd


class CompanyRecord:
    def __init__(self):
        self.hand_id = None
        self.coname = None
        self.gv_key = None
        self.company_screen_name = None
        self.company_tweet_accound_id = None
        self.company_type = None
        self.company_twitter_date = None
        self.total_tweet = None
        self.total_follower = None
        self.total_following = None
        self.first_tweet_date = None
        self.company_twitter_date_actual = None
        self.last_tweet_date = None
        self.other_comment = None
        self.total_tweet_actual = None

    def to_dict(self):
        result_dict = {}
        result_dict["handID"] = self.hand_id
        result_dict["CONAME"] = self.coname
        result_dict["gvkey"] = self.gv_key
        result_dict["Company_twitter"] = self.company_screen_name
        result_dict["Company_type"] = self.company_type
        result_dict["Company_twitter_date"] = self.company_twitter_date
        result_dict["TWITTER_ACCOUNT_ID"] = self.company_tweet_accound_id
        result_dict["Number_following"] = self.total_following
        result_dict["Number_follower"] = self.total_follower
        result_dict["total_tweet"] = self.total_tweet
        result_dict["first_tweet_date"] = self.first_tweet_date
        result_dict["Company_twitter_date_actual"] = self.company_twitter_date_actual
        result_dict["last_tweet_date"] = self.last_tweet_date
        result_dict["total_tweet_actual"] = self.total_tweet_actual
        result_dict["other_comment"] = self.other_comment
        return result_dict

    @classmethod
    def parse_dict(cls, dict_data):
        company_record = CompanyRecord()
        try:
            company_record.hand_id = dict_data["handID"]
            company_record.coname = dict_data["CONAME"]
            company_record.gv_key = dict_data["gvkey"]
            company_record.company_screen_name = dict_data["Company_twitter"]
            if company_record.company_screen_name is not None:
                company_record.company_type = dict_data["Company_type"]
                if "Company_twitter_date" in dict_data and dict_data["Company_twitter_date"] is not None:
                    company_record.company_twitter_date = parse(dict_data["Company_twitter_date"])
                if "Company_twitter_date_actual" in dict_data and dict_data["Company_twitter_date_actual"] is not None:
                    company_record.company_twitter_date_actual = parse(dict_data["Company_twitter_date_actual"])
                if "TWITTER_ACCOUNT_ID" in dict_data:
                    company_record.company_tweet_accound_id = dict_data["TWITTER_ACCOUNT_ID"]
                if "Number_following" in dict_data:
                    company_record.total_following = dict_data["Number_following"]
                if "Number_follower" in dict_data:
                    company_record.total_follower = dict_data["Number_follower"]
                if "total_tweet" in dict_data:
                    company_record.total_tweet = dict_data["total_tweet"]
                else:
                    company_record.total_tweet = 0
                if "first_tweet_date" in dict_data:
                    company_record.first_tweet_date = dict_data["first_tweet_date"]
                else:
                    company_record.first_tweet_date = None
                if "last_tweet_date" in dict_data:
                    company_record.last_tweet_date = dict_data["last_tweet_date"]
                else:
                    company_record.last_tweet_date = None
                if "total_tweet_actual" in dict_data:
                    company_record.total_tweet_actual = dict_data["total_tweet_actual"]
                else:
                    company_record.total_tweet_actual = None
                if "other_comment" in dict_data:
                    company_record.other_comment = dict_data["other_comment"]
                else:
                    company_record.other_comment = None
        except ValueError:
            print(dict_data)
        return company_record

    def update_by_tweet_record(self, tweet_record):
        self.total_tweet = self.total_tweet + 1
        if self.first_tweet_date is None:
            self.first_tweet_date = tweet_record.tweet_time
        elif self.first_tweet_date > tweet_record.tweet_time:
            self.first_tweet_date = tweet_record.tweet_time
        if self.last_tweet_date is None:
            self.last_tweet_date = tweet_record.tweet_time
        elif self.last_tweet_date < tweet_record.tweet_time:
            self.last_tweet_date = tweet_record.tweet_time


class TweetRecord:
    EARNINGS_KEYWORDS = set(["earnings", "eps", "profit", "income", "revenue", "sales", "results", "quarter"])
    INVESTOR_KEYWORDS = set(
        ["ceo", "executive", "dividend", "board", "new products", "launch", "acquisition", "merger", "repurchase",
         "investment", "customer"])

    def __init__(self):
        self.company_record = CompanyRecord()
        self.tweet_id = None
        self.tweet_time = None
        self.tweet_text = None
        self.total_likes = None
        self.total_retweets = None
        self.is_a_reply = None
        self.reply_tweet_id = None
        self.reply_tweet_text = None
        self.is_a_retweet = None
        self.retweet_id = None
        self.is_a_quote = None
        self.quote_tweet_id = None
        self.total_word = None
        self.is_earnings_related = None
        self.is_investor_related = None
        self.polarity_score = None
        self.subjectivity_score = None

    @classmethod
    def parse_dict(cls, dict_data):
        tweet_record = TweetRecord()
        tweet_record.company_record = CompanyRecord.parse_dict(dict_data)
        tweet_record.tweet_id = dict_data["Tweet_id_str"]
        if "Tweet_time" in dict_data and dict_data["Tweet_time"] is not None:
            tweet_record.tweet_time = parse(dict_data["Tweet_time"])
        tweet_record.tweet_text = dict_data["Tweet_text"]
        tweet_record.total_likes = dict_data["likes"]
        tweet_record.total_retweets = dict_data["retweets"]
        tweet_record.is_a_reply = dict_data["Is a reply"]
        tweet_record.reply_tweet_id = dict_data["reply_tweet_id"]
        tweet_record.reply_tweet_text = dict_data["reply_tweet_text"]
        tweet_record.is_a_retweet = dict_data["Is a retweet"]
        tweet_record.retweet_id = dict_data["retweet_tweet_id"]
        tweet_record.is_a_quote = dict_data["Is a quote"]
        tweet_record.quote_tweet_id = dict_data["quote_tweet_id"]
        if "total_word" in dict_data:
            tweet_record.total_word = dict_data["total_word"]
        if "is_earnings_related" in dict_data:
            tweet_record.is_earnings_related = dict_data["is_earnings_related"]
        if "is_investor_related" in dict_data:
            tweet_record.is_investor_related = dict_data["is_investor_related"]
        if "polarity_score" in dict_data:
            tweet_record.polarity_score = dict_data["polarity_score"]
        if "subjectivity_score" in dict_data:
            tweet_record.subjectivity_score = dict_data["subjectivity_score"]
        if tweet_record.tweet_text is not None:
            tweet_words = tweet_record.tweet_text.split()
            if tweet_record.total_word is None:
                tweet_record.total_word = len(tweet_words)
            if tweet_record.is_earnings_related is None:
                for single_word in tweet_words:
                    if single_word.lower() in cls.EARNINGS_KEYWORDS:
                        tweet_record.is_earnings_related = True
                        break
            if tweet_record.is_investor_related is None:
                for single_word in tweet_words:
                    if single_word.lower() in cls.INVESTOR_KEYWORDS:
                        tweet_record.is_investor_related = True
                        break
        return tweet_record

    def to_dict(self):
        dict_data = {}
        dict_data["handID"] = self.company_record.hand_id
        dict_data["CONAME"] = self.company_record.coname
        dict_data["gvkey"] = self.company_record.gv_key
        dict_data["Company_twitter"] = self.company_record.company_screen_name
        dict_data["Company_type"] = self.company_record.company_type
        dict_data["Company_twitter_date"] = self.company_record.company_twitter_date
        dict_data["TWITTER_ACCOUNT_ID"] = self.company_record.company_tweet_accound_id
        dict_data["Number_following"] = self.company_record.total_following
        dict_data["Number_follower"] = self.company_record.total_follower
        dict_data["Tweet_id_str"] = self.tweet_id
        dict_data["Tweet_time"] = self.tweet_time
        dict_data["Tweet_text"] = self.tweet_text
        dict_data["likes"] = self.total_likes
        dict_data["retweets"] = self.total_retweets
        dict_data["Is a reply"] = self.is_a_reply
        dict_data["reply_tweet_id"] = self.reply_tweet_id
        dict_data["reply_tweet_text"] = self.reply_tweet_text
        dict_data["Is a retweet"] = self.is_a_retweet
        dict_data["retweet_tweet_id"] = self.retweet_id
        dict_data["Is a quote"] = self.is_a_quote
        dict_data["total_word"] = self.total_word
        dict_data["is_investor_related"] = self.is_investor_related
        dict_data["is_earnings_related"] = self.is_earnings_related
        dict_data["polarity_score"] = self.polarity_score
        dict_data["subjectivity_score"] = self.subjectivity_score
        return dict_data


if __name__ == '__main__':
    pass
