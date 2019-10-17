#!/bin/python3

from august.api import Api 
from august.authenticator import Authenticator, AuthenticationState

api = Api(timeout=20)
authenticator = Authenticator(api, "phone", "+15555555555", "PASSWORD",
                                      access_token_cache_file="token.dat")

authentication = authenticator.authenticate()

# State can be either REQUIRES_VALIDATION, BAD_PASSWORD or AUTHENTICATED
# You'll need to call different methods to finish authentication process, see below
state = authentication.state

#print( state ) 

# If AuthenticationState is BAD_PASSWORD, that means your login_method, username and password do not match

# If AuthenticationState is AUTHENTICATED, that means you're authenticated already. If you specify "access_token_cache_file", the authentication is cached in a file. Everytime you try to authenticate again, it'll read from that file and if you're authenticated already, Authenticator won't call August again as you have a valid access_token

if state == AuthenticationState.REQUIRES_VALIDATION:
    # If AuthenticationState is REQUIRES_VALIDATION, then you'll need to go through verification process
    # send_verification_code() will send a code to either your phone or email depending on login_method
    authenticator.send_verification_code()
    # Wait for your code and pass it in to validate_verification_code()
    validation_result = authenticator.validate_verification_code(input())
    # If ValidationResult is INVALID_VERIFICATION_CODE, then you'll need to either enter correct one or resend by calling send_verification_code() again
    # If ValidationResult is VALIDATED, then you'll need to call authenticate() again to finish authentication process
    authentication = authenticator.authenticate()

# Once you have authenticated and validated you can use the access token to make API calls
locks = api.get_locks(authentication.access_token)

#print (locks[0].device_id)

#api.unlock(authentication.access_token, locks[0].device_id)

api.get_lock_detail(authentication.access_token, locks[0].device_id)
