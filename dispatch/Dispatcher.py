import json
from authy.api import AuthyApiClient

class Dispatcher():
    """ Busy boy. Push authorizing all the things """

    def __init__(self):
        """ Establish street cred """

        ## Get API Key from local json
        self.config = json.load(open('config.json'))
        self.authy_api = AuthyApiClient(self.config["api_key"])

    def oneTouchAuth(self, auth_id, user_id, message, seconds_to_expire, details):
        """ Send a push authorization """

        #Place backend data inside hidden_details dict
        hidden_details={}
        hidden_details["auth_id"] = auth_id

        #Package all the mod_msg info into a response and send it on its way
        response = self.authy_api.one_touch.send_request(user_id,
                        message,
                        seconds_to_expire=seconds_to_expire,
                        details=details,
                        hidden_details=hidden_details)
        #Verify valid response
        if response.ok():
                        uuid = response.get_uuid()
        else:
                        uuid = -1
                        print(response.errors())

        return uuid, auth_id

    def getResponseStatus(self, uuid, auth_id):
        """ Use response uuid to find and return the push authorization result """

        status_response = self.authy_api.one_touch.get_approval_status(uuid)
        if status_response.ok():
                    # one of 'pending', 'approved', 'denied', or 'expired'
            approval_status = status_response.content['approval_request']['status']
        else:
            approval_status = "Response status fizzled..."
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
    uuid, a_id = pushBoy.oneTouchAuth(args.aid, args.uid, args.message, args.expiration, args.details)
