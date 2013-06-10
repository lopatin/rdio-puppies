#!/usr/bin/env python
import oauth2 as oauth
import urllib, cgi
import json

class RdioAPI(object):
    
    def __init__(self):
        self.consumer = self.create_consumer()
        self.client = self.create_client()
        self.request_token, self.parsed_content = self.get_request_token()
        self.authorization_url = self.create_authorization_url()
        print self.authorization_url
        # wait for user to give me pin to create access_token
        self.access_token = None

    def create_consumer(self):
        """ create the OAuth consumer credentials """ 
        CONSUMER_KEY, CONSUMER_SECRET = self.get_consumer_credentials()
        return oauth.Consumer(CONSUMER_KEY, CONSUMER_SECRET) 

    def get_consumer_credentials(self): 
        f = open('config', 'r') 
        CONSUMER_KEY = f.readline().strip()
        CONSUMER_SECRET = f.readline().strip()
        return CONSUMER_KEY, CONSUMER_SECRET
	
    def create_client(self):
        return oauth.Client(self.consumer)

    def get_request_token(self):
        response, content = self.client.request('http://api.rdio.com/oauth/request_token', 'POST', urllib.urlencode({'oauth_callback':'oob'}))
        parsed_content = dict(cgi.parse_qsl(content))
        request_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])
        return request_token, parsed_content

    def create_authorization_url(self):
        return '%s?oauth_token=%s' % (self.parsed_content['login_url'], self.parsed_content['oauth_token'])
	
    def authorize_user(self, pin):
        self.authorize_user_with_pin(pin)
        self.exchange_request_token_for_access_token()
        self.create_client_token

    def authorize_user_with_pin(self, oauth_verifier): 
        self.request_token.set_verifier(oauth_verifier)

    def exchange_request_token_for_access_token(self):
        """ upgrade the request token to an access token """
        self.client = self.upgrade_client_to_use_request_token()
        response, content = self.client.request('http://api.rdio.com/oauth/access_token', 'POST')
        parsed_content = dict(cgi.parse_qsl(content))
        self.access_token = oauth.Token(parsed_content['oauth_token'], parsed_content['oauth_token_secret'])
        self.client = self.upgrade_client_to_use_access_token()

    def upgrade_client_to_use_request_token(self):
        return oauth.Client(self.consumer, self.request_token)

    def upgrade_client_to_use_access_token(self):
        return oauth.Client(self.consumer, self.access_token)
    
    def grouper(iterable, n, fill=None):
        args = [iter(iterable)]*n
        return izip_longest(*args, fillvalue=fillvalue)

    def add_to_collection(self, obj_list):
        keys = []
        tracks = []
        for obj in obj_list:
            response = self.client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'search', 'query': obj, 'types': 'Track', 'count': '1'}))

            r = json.loads(response[1])['result']['results'][0]
            keys.append(r['key'])
            tracks.append({"name": str(r["name"]).replace("'",""), "artist": str(r["artist"]).replace("'",""), "icon": str(r["icon"]).replace("'","")})

        keystr = ','.join(keys)
        response = self.client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'addToCollection', 'keys': keystr}))
        return tracks

		# example authorized request
		#response = client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'currentUser'}))
		#print response[1]

    def make_authenticated_call(self):
        response = self.client.request('http://api.rdio.com/1/', 'POST', urllib.urlencode({'method': 'currentUser'}))
        print response[1]

   

