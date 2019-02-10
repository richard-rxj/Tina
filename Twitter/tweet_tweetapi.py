import json
import os
from searchtweets import ResultStream, gen_rule_payload, load_credentials

class TweetApiHelper:

    os.environ["SEARCHTWEETS_ACCOUNT_TYPE"] = "premium"
    os.environ["SEARCHTWEETS_ENDPOINT"] = "https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json"
    # os.environ["SEARCHTWEETS_ENDPOINT"] = "https://api.twitter.com/1.1/tweets/search/30day/dev.json"
    os.environ["SEARCHTWEETS_CONSUMER_KEY"] = "VuFoEiBj2fOkvz63GVuT8KWwt"
    os.environ["SEARCHTWEETS_CONSUMER_SECRET"] = "JK7i3oJ5ZkaJLq2OtKezK9DLsDSjvSio554tGwFh6fg1pci0Mu"

    search_args = load_credentials(filename="nothing_here.yaml", yaml_key="no_key_here")

    def get_tweets_tweetAPI(tweet_name):
        tweets=[]
        next_token=None
        while True:
            rule = gen_rule_payload("from:"+tweet_name
                                    ,from_date="2006-01-01" #UTC 2017-09-01 00:00
                                #,to_date="2017-10-30" #UTC 2017-10-30 00:00
                                # ,results_per_call=100
                                    ,next=next_token
                                    )
            rs = ResultStream(**TweetApiHelper.search_args, rule_payload=rule)
            tweets.append(list(rs.stream()))
            next_token = rs.next_token
            if next_token is None:
                break
        return tweets

    def generate_powertrack_rule(screen_name_list, outputname):
        rule_list=[]
        current_count=0;
        current_rule=[]
        for screen_name in screen_name_list:
            if screen_name.strip() =="":
                continue
            current_count = current_count + 1
            current_rule.append(screen_name)
            if(current_count==10):
                rule="from:"+" OR ".join(current_rule)
                rule_list.append({"value":rule})
                current_rule=[]
                current_count=0
        if current_count != 0:
            rule = "from:" + " OR ".join(current_rule)
            rule_list.append({"value":rule})
        data={"rules":rule_list}
        with open(outputname, "w") as write_file:
            json.dump(data, write_file)

if __name__ == '__main__':
    #tweets=TweetApiHelper.get_tweets_tweetAPI("Oracle")
    TweetApiHelper.generate_powertrack_rule(["test1", "test2", "test3"], "tmp_rule")