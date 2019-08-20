import tweepy
import json

twitter_file = open("/home/hedmund/Shoes_Data/lost_data/LD/lost_data2.json", "a+", encoding="utf8")
auth = tweepy.OAuthHandler("eG6y9nmTYFwuZyrOj8dKyRKVj", "K5uwMwxeH6rh2ChOc4Fiuz3ecB31dIBULTJE5WhtC3snuk7Aji")
auth.set_access_token("189632432-go5JBsupvHc8TbbBm8vqwxoJJehFXBjEZrZO4GnP", "ceGLw7rM2oGzRvCxctOWb78WGF8ocIMtuTn9WJZNyu1CS")

api = tweepy.API(auth, wait_on_rate_limit=True)

for tweet in tweepy.Cursor(api.search,
                           q="nike OR adidas OR reebok",
                           since="2018-06-25",
                           include_rts=True,
                           count = "1000000",
                           until="2018-06-27",
                           lang="en").items():
    print(tweet.created_at, tweet.text)
    json.dump(tweet._json, twitter_file)
    twitter_file.write("\n")

twitter_file.close()