#!/usr/bin/env python

# encoding: utf-8

import nltk
from textblob import TextBlob


class ToneAnalyseHelper:

    @classmethod
    def tone_analyze(cls, tweet_record):
        if tweet_record.tweet_text is not None:
            blob=TextBlob(tweet_record.tweet_text)
            tweet_record.polarity_score=blob.sentiment[0]
            tweet_record.subjectivity_score=blob.sentiment[1]

if __name__ == '__main__':
    pass
