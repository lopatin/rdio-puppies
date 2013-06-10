import rdio
import LastfmQuery
import cPickle as pickle
import sys

def get_url():
	rdio_api = rdio.RdioAPI()
	# use this url for rdio button
	authorization_url = rdio_api.authorization_url  
	save_api(rdio_api)

def verify_pin():
	rdio_api = load_api()
	
	# at this point, user will click rdio button, get pin from rdio, and give us pin
	rdio_api.authorize_user_with_pin(pin)
	rdio_api.exchange_request_token_for_access_token()
	# ready to make authrorized calls, example call:
	rdio_api.make_authenticated_call()
	# rdio_api.add_to_collection(list_of_artists, type="Album")

	save_api(rdio_api)
	
def import_lastfm(username):
	rdio_api = load_api()
	lastfm = LastfmQuery.LastfmQuery()
	lastfm_list_of_tracks = lastfm.getTracks(username)
	tracks = rdio_api.add_to_collection(lastfm_list_of_tracks)
	print str(tracks).replace("'", '"')

def load_api():
	return pickle.load( open( "pickles/api_"+client_id+".p", "rb" ))

def save_api(rdio_api):
	pickle.dump(rdio_api, open( "pickles/api_"+client_id+".p", "wb" ))

if __name__ == "__main__":
	args = sys.argv
	method, client_id = args[1], args[2]

	if method == 'url':
		get_url()
	elif method == 'pin':
		pin = args[3] 
		verify_pin()
	elif method == 'lastfm':
		import_lastfm(args[3])
