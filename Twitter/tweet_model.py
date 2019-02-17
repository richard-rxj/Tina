#!/usr/bin/env python

# encoding: utf-8

from dateutil.parser import parse


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

    @classmethod
    def parse_dict(cls, dict_data):
        company_record = CompanyRecord()
        company_record.hand_id = dict_data["handID"]
        company_record.coname = dict_data["CONAME"]
        company_record.gv_key = dict_data["gvkey"]
        company_record.company_screen_name = dict_data["Company_twitter"]
        company_record.company_type = dict_data["Company_type"]
        company_record.company_twitter_date = parse(dict_data["Company_twitter_date"])
        company_record.company_tweet_accound_id = dict_data["TWITTER_ACCOUNT_ID"]
        company_record.total_following = dict_data["Number_following"]
        company_record.total_follower = dict_data["Number_follower"]
        company_record.total_tweet = 0
        company_record.first_tweet_date = None
        return company_record

    def update_by_tweet_record(self, tweet_record):
        self.total_tweet = self.total_tweet + 1
        if self.first_tweet_date is None:
            self.first_tweet_date = tweet_record.tweet_time
        elif self.first_tweet_date > tweet_record.tweet_time:
            self.first_tweet_date = tweet_record.tweet_time


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
        self.tone_analysis = None

    @classmethod
    def parse_dict(cls, dict_data):
        tweet_record = TweetRecord()
        tweet_record.company_record = None
        tweet_record.tweet_id = dict_data["Tweet_id_str"]
        tweet_record.tweet_time = parse(dict_data["Tweet_time"])
        tweet_record.tweet_text = dict_data["Tweet_text"]
        tweet_record.total_likes = dict_data[""]
        tweet_record.total_retweets = dict_data[""]
        tweet_record.is_a_reply = dict_data[""]
        tweet_record.reply_tweet_id = dict_data[""]
        tweet_record.reply_tweet_text = dict_data[""]
        tweet_record.is_a_retweet = dict_data[""]
        tweet_record.retweet_id = dict_data[""]
        tweet_record.is_a_quote = dict_data[""]
        tweet_record.quote_tweet_id = dict_data[""]
        if tweet_record.tweet_text is not None:
            tweet_words = tweet_record.tweet_text.split()
            tweet_record.total_word = len(tweet_words)
            for single_word in tweet_words:
                if single_word.lower() in cls.EARNINGS_KEYWORDS:
                    tweet_record.is_earnings_related = True
                    break
            for single_word in tweet_words:
                if single_word.lower() in cls.INVESTOR_KEYWORDS:
                    tweet_record.is_investor_related = True
                    break
        return tweet_record


if __name__ == '__main__':
    pass
