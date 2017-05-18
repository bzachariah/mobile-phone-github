#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "mobilePhoneAction":
        return {}

    result = req.get("result")
    parameters = result.get("parameters")
    os = parameters.get("os")
    if os is None:
        return {}
    display = parameters.get("display")
  

    res = makeWebhookResult(os, display)
    return res


    
    


def makeWebhookResult(os, display):

    with open("tyy-4io.csv", "r") as ins:
        for line in ins:
            if os in line:
                speech = line
                break
                
    
    
            
    #speech = os + " " + display
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        # "source": "apiai-weather-webhook-sample"
        "source": "bzachariah/mobile-phone-github"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
