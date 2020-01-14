import tweepy

#Application key
CONSUMER_KEY = 'uhzOXpxETxaIXRKFmG4J10ztP'
CONSUMER_SECRET = 'SZBltYRGECF2pJ6t4PMqtRYRGReEFHVam2jxZa97xkJnyiSCki'

def get_api(request):
	# set up and return a twitter api object
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	access_key = request.session['access_key_tw']
	access_secret = request.session['access_secret_tw']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api
