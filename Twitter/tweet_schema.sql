create table company_record (
    hand_id      text,
    coname      text,
    gv_key   text,
    company_screen_name  text primary key,
    company_tweet_account_id text,
    company_type  text,
    company_twitter_date date,
    total_tweet integer,
    total_follower integer,
    total_following integer,
    first_tweet_date date,
    company_twitter_date_actual date
    last_tweet_date date,
    other_comment text
);

create table tweet_record (
    hand_id      text,
    coname      text,
    gv_key   text,
    company_screen_name  text,
    company_tweet_account_id text,
    company_type  text,
    company_twitter_date date,
    total_follower integer,
    total_following integer,
    tweet_id text primary key,
    tweet_time date,
    tweet_text text,
    total_likes integer,
    total_retweets integer,
    is_a_reply text,
    reply_tweet_id text,
    reply_tweet_text text,
    is_a_retweet text,
    retweet_id text,
    is_a_quote text,
    quote_tweet_id text,
    total_word integer,
    is_earnings_related text,
    is_investor_related text,
    tone_analysis text
);