#!/usr/bin/env python

# encoding: utf-8

import os
import sqlite3
from .tweet_model import CompanyRecord
from .tweet_model import TweetRecord


class SqlLiteHelper:
    db_filename = 'twitter_tina.db'
    schema_filename = 'tweet_schema.sql'
    db_is_new = not os.path.exists(db_filename)

    @classmethod
    def create_schema(cls):
        with sqlite3.connect(cls.db_filename) as conn:
            print('Creating schema')
            with open(cls.schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
        cls.db_is_new = False

    @classmethod
    def save_company_record(cls, company_records):
        insert_sql = """ replace into company_record (
        company_screen_name, hand_id, coname, gv_key,
         company_tweet_account_id, company_type,
        company_twitter_date, total_tweet, total_follower,
        total_following, first_tweet_date, company_twitter_date_actual
        ) values (
        ?, ?, ?,
        ?,?,?,
        ?,?,?,
        ?,?,?
        )"""
        if (cls.db_is_new):
            cls.create_schema()
        with sqlite3.connect(cls.db_filename) as conn:
            cur = conn.cursor()
            cur.execute('begin transaction')
            for company_record in company_records:
                cur.execute(insert_sql, (company_record.company_screen_name,
                                         company_record.hand_id, company_record.coname, company_record.gv_key,
                                         company_record.company_tweet_accound_id, company_record.company_type,
                                         company_record.company_twitter_date,
                                         company_record.total_tweet, company_record.total_follower,
                                         company_record.total_following,
                                         company_record.first_tweet_date, company_record.company_twitter_date_actual))
            cur.execute('commit')

    @classmethod
    def save_tweet_record(cls, tweet_records):
        insert_sql = """ insert into tweet_record (
        hand_id, coname, gv_key,
        company_screen_name, company_tweet_account_id, company_type,
        company_twitter_date, total_follower, total_following,
        tweet_id, tweet_time, tweet_text,
        total_likes, total_retweets, 
        is_a_reply, reply_tweet_id, reply_tweet_text,
        is_a_retweet, retweet_id, is_a_quote, quote_tweet_id,
        total_word, is_earnings_related, is_investor_related, tone_analysis
        ) values (
        ?, ?, ?,
        ?,?,?,
        ?,?,?,
        ?,?,?,
        ?,?,
        ?,?,?,
        ?,?,?,?,
        ?,?,?,?
        )"""
        if (cls.db_is_new):
            cls.create_schema()
        with sqlite3.connect(cls.db_filename) as conn:
            cur = conn.cursor()
            cur.execute('begin transaction')
            for tweet_record in tweet_records:
                company_record = tweet_record.company_record
                cur.execute(insert_sql, (company_record.hand_id, company_record.coname, company_record.gv_key,
                                         company_record.company_screen_name,
                                         company_record.company_tweet_accound_id, company_record.company_type,
                                         company_record.company_twitter_date,
                                         company_record.total_follower,
                                         company_record.total_following,
                                         tweet_record.tweet_id, tweet_record.tweet_time, tweet_record.tweet_text,
                                         tweet_record.total_likes, tweet_record.total_retweets,
                                         tweet_record.is_a_reply, tweet_record.reply_tweet_id,
                                         tweet_record.reply_tweet_text,
                                         tweet_record.is_a_retweet, tweet_record.retweet_id,
                                         tweet_record.is_a_quote, tweet_record.quote_tweet_id,
                                         tweet_record.total_word, tweet_record.is_earnings_related,
                                         tweet_record.is_investor_related, tweet_record.tone_analysis))
            cur.execute('commit')

    @classmethod
    def get_all_company_records(cls):
        company_records = []
        sql_script = """
        select hand_id, coname, gv_key, 
        company_screen_name, company_tweet_account_id,
        company_type, company_twitter_date,
        total_tweet, total_follower, total_following,
        first_tweet_date, company_twitter_date_actual
        from company_record
        """
        with sqlite3.connect(cls.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_script)
            for row in cursor:
                hand_id, coname, gv_key, company_screen_name, company_tweet_account_id, company_type, company_twitter_date, total_tweet, total_follower, total_following, first_tweet_date, company_twitter_date_actual = row
                company_record = CompanyRecord()
                company_record.hand_id=hand_id
                company_record.coname=coname
                company_record.gv_key=gv_key
                company_record.company_screen_name=company_screen_name
                company_record.company_tweet_accound_id=company_tweet_account_id
                company_record.company_type=company_type
                company_record.company_twitter_date=company_twitter_date
                company_record.total_tweet=total_tweet
                company_record.total_follower=total_follower
                company_record.total_following=total_following
                company_record.first_tweet_date=first_tweet_date
                company_record.company_twitter_date_actual=company_twitter_date_actual
                company_records.append(company_record)
        return company_records


if __name__ == '__main__':
    SqlLiteHelper.create_schema();
