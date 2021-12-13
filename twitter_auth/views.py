import tweepy #API for twitter
from django.http import *
# from django.shortcuts import render_to_response
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render
from twitter_auth.forms import PostTweet #import form
from twitter_auth.utils import *
from profanityfilter import ProfanityFilter #it's a library for detecting proform word in any given list

from . import retrieve_tweet
from . import predict
from . models import Model
pf = ProfanityFilter()

def main(request):
	"""
	main view of app, either login page or info page
	"""
	# if we haven't authorised yet, direct to login page
	if check_key(request):
		return HttpResponseRedirect(reverse('info')) #goto info
	else:
		return render(request, 'twitter_auth/login.html') #goto login

def unauth(request):
	"""
	logout and remove all session data
	"""
	if check_key(request):
		api = get_api(request)
		request.session.clear()
		logout(request)
	return HttpResponseRedirect(reverse('main')) #goto main()

def info(request):
	"""
	display some user info to show we have authenticated successfully
	"""
	print(check_key)
	if check_key(request):
		api = get_api(request)
		user = api.me()
		tweets = retrieve_tweet.get_user_tweet(user.screen_name)
		#filename ='twitter_auth/users/'+ user.screen_name + '_tweets.csv'
		tweet = predict.prepare_tweet(tweets)
		tweet_data = predict.retrieve_data(tweets)
		reg , cat = predict.get_result(tweet)
		#traits = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
		#s_OPN,c_OPN = predict.perdict_OPN(tweet)
		sOPN = reg[0]
		cOPN = cat[0]
		sCON = reg[1]
		cCON = cat[1]
		sEXT = reg[2]
		cEXT = cat[2]
		sAGR = reg[3]
		cAGR = cat[3]
		sNEU = reg[4]
		cNEU = cat[4]

		return render(request, 'twitter_auth/info.html', {'user':user , 'sOPN':sOPN ,'cOPN':cOPN ,'sCON':sCON,'cCON':cCON,
		'sEXT':sEXT,'cEXT':cEXT,'sAGR':sAGR ,'cAGR':cAGR ,'sNEU':sNEU,'cNEU':cNEU, 'tweet_data':tweet_data , 'tweets':tweets,
		'number': range(10) })
	else:
		return HttpResponseRedirect(reverse('main'))

def auth(request):
	# start the OAuth process, set up a handler with our details
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	# direct the user to the authentication url
	# if user is logged-in and authorized then transparently goto the callback URL
	auth_url = oauth.get_authorization_url(True)
	response = HttpResponseRedirect(auth_url)
	# store the request token
	request.session['request_token'] = oauth.request_token
	return response

def callback(request):
	verifier = request.GET.get('oauth_verifier')
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	token = request.session.get('request_token')
	# remove the request token now we don't need it
	request.session.delete('request_token')
	oauth.request_token = token
	# get the access token and store
	try:
		oauth.get_access_token(verifier)
	except tweepy.TweepError:
		print('Error, failed to get access token')

	request.session['access_key_tw'] = oauth.access_token
	request.session['access_secret_tw'] = oauth.access_token_secret
	print(request.session['access_key_tw'])
	print(request.session['access_secret_tw'])
	response = HttpResponseRedirect(reverse('info'))
	return response

def check_key(request):
	"""
	Check to see if we already have an access_key stored, if we do then we have already gone through
	OAuth. If not then we haven't and we probably need to.
	"""
	try:
		access_key = request.session.get('access_key_tw', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True


#read tweet from home_timeline
def home_timeline(request):
    if check_key(request):
    	api = get_api(request) #Oauth user
    	public_tweets = api.home_timeline() #get homepage tweets

    	return render(request, 'twitter_auth/public_tweets.html', {'public_tweets': public_tweets})
    else:
        return render(request, 'twitter_auth/login.html') #goto login

#post tweet
def post_tweet(request):
   tweet = "not logged in"
   if check_key(request):
       	if request.method == "POST":
              #Get the posted form
              MyPostTweet = PostTweet(request.POST)
              if MyPostTweet.is_valid():
                #get user input
                tweet = request.POST.get("input_tweet", "")
                Approval=pf.is_profane(tweet)
                 #applying profanity for explicit content detection
                 #it won't allow post any explicit tweets
                if Approval == True:
                  messages.success(request, "Explicit Contect detected !")
                  messages.success(request, "Please try again.")
                else :
                  messages.success(request, "Neat and clean !")
                  messages.success(request, "Status Updating...")
                  api = get_api(request)
                  #update status
                  api.update_status(tweet)
       	else:
          		MyPostTweet = PostTweet()

        return render(request, 'twitter_auth/post_tweet.html', {"tweet" : tweet})

   else:
        return render(request, 'twitter_auth/login.html') #goto login
