import json, time
from authy.api import AuthyApiClient

class Dispatcher():
    """ Busy boy. Push authorizing all the things """

    def __init__(self):
        """ Establish street cred """

	## Get API Key from local json
	self.config = json.load(open('config.json'))
	self.authy_api = AuthyApiClient(self.config["api_key"])

    def oneTouch_Auth(self, auth_id, user_id, message, seconds_to_expire, details):
        """ Send push authorization based on data inside mod_msg dict """

	#Place backend data inside hidden_details dict
	hidden_details={}
	hidden_details["auth_id"]=auth_id

	#Package all the mod_msg info into a response and send it on its way
	response = self.authy_api.one_touch.send_request(user_id,
	                                        message,
	                                        seconds_to_expire=seconds_to_expire,
	                                        details=details,
	                                        hidden_details=hidden_details)

	return response, seconds_to_expire, auth_id

    def getResponseStatus(self, response, seconds_to_expire, auth_id):
        """ Very valid response and use response uuid to find and return the push authorization result """

	##Verify valid response
	if response.ok():
    		uuid = response.get_uuid()
    		start = time.time()
    		end = time.time()
    		#Loop until request has been approved/denied or expired
    		while(start-end < seconds_to_expire):
			status_response = self.authy_api.one_touch.get_approval_status(uuid)
    			if status_response.ok():
        			# one of 'pending', 'approved', 'denied', or 'expired'
        			approval_status = status_response.content['approval_request']['status']
        			if((approval_status=="approved") | (approval_status=="denied")):
					break
			else:
				approval_status = "Error"
        			print resp.errors()
	else:
		approval_status = "Error"
		print response.errors()

	return approval_status, auth_id


if __name__ == '__main__':
    import argparse
    mod_msg=json.load(open("mod_msg.json"))

    parser = argparse.ArgumentParser()
    parser.add_argument('--uid', '-u', help="The user id", default=mod_msg["user_id"], type=int)
    parser.add_argument('--aid', '-a', help="The authorization id", default=mod_msg["auth_id"])
    parser.add_argument('--message', '-m', help="The message", default=mod_msg["message"])
    parser.add_argument('--expiration', '-e', help="The expiration time (seconds)", default=mod_msg["expiration_time"], type=int)
    parser.add_argument('--details', '-d', help="The authorization details", default=mod_msg["details"])
    args = parser.parse_args()

    #Basic use demo
    pushBoy = Dispatcher()
    resp, exp, a_id = pushBoy.oneTouch_Auth(args.aid, args.uid, args.message, args.expiration, args.details)
    tuple=pushBoy.getResponseStatus(resp,exp,a_id)
    print("Status: " + str(tuple[0]) + "\nAuthorization ID: " + str(tuple[1]))

