# Import Library to Twitter API
import tweepy

# Change which user you want to bombard with replies (without @)
UserToTrack = "MeItzLarz"

# Twitter API Tokens
consumer_key = "CONSUMER_KEY"
consumer_secret = "CONSUMER_SECRET"
acces_key = "ACCES_KEY"
acces_secret = "ACCES_SECRET"

# Connecting to Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(acces_key, acces_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# Twitter Stream Class
class UserTracker(tweepy.StreamListener):
    # Initializing Class
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    # Tweet met the criteria
    def on_status(self, tweet):
        print("Tweet found")
        
        # Checking if Tweet is a reply
        if tweet.in_reply_to_status_id == None:
            tweet_handler(tweet)

        else:
            print("Tweet is a reply")
            print("\n")

    # Error Handling
    def on_error(self, status):
        print("Error detected: " + str(status))


# Function to reply to Original Tweet
def tweet_handler(tweet):
    # Instantiate Backwards Tweet and Original Tweet
    backwardsTweet = ""
    original = tweet.text

    # Replace characters that went wrong
    original = original.replace("&amp;", "&")
    original = original.replace("&gt;", ">")
    original = original.replace("&lt;", "<")

    # Split Tweet on newline
    tweetList = original.split("\n")

    # Split newlines on spaces
    for i in range(len(tweetList)):
        tweetList[i] = tweetList[i].split(" ")

    # Shuffle the letters and put back spaces and newlines
    for i in range(len(tweetList)):
        for j in range(len(tweetList[i])):
            for k in range(len(tweetList[i][j])):
                backwardsTweet += tweetList[i][j][-1 - k]
            backwardsTweet += " "
        backwardsTweet += "\n"

    # Reply with Backwards Tweet
    api.update_status(backwardsTweet, tweet.id)
    print("Reply Sent")
    print("\n")


# Instantiating Twitter Stream
twitterStream = tweepy.Stream(api.auth, UserTracker(api))

# Waiting for Tweet meeting the criteria
user = api.get_user(UserToTrack)
twitterStream.filter(follow=[str(user.id)])
