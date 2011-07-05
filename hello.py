import urllib, urllib2
import json

class HelloBitcoin(object):
    def __init__(self, username=None, passwd=None, auth_token=None):
        self.username = username
        self.passwd = passwd
        self.auth_token = auth_token

# Public methods
    def historical(self, contract_id="BTC_USD"):
        """Get recent trades.

           Note: Only this native API call returns CSV"""

        api = "api/data/historical?contract_id=%s" % contract_id
        return self._curl(api=api, responseformat="csv")

    def orderbook(self, contract_id="BTC_USD"):
        """Get orderbook"""

        api = "api/data/orderbook?contract_id=%s" % contract_id
        return self._curl(api=api)

    def snapshot(self, contract_id="BTC_USD"):
        """Get current bid, offer, last px, timestamp"""

        api = "api/data/snapshot?contract_id=%s" % contract_id
        return self._curl(api=api)

# Authentication required methods
    def set_credentials(self, username, passwd):
        """Set authentication information"""
        self.username = username
        self.password = password

    def authenticate(self, username=None, passwd=None):
        """Authenticate with HelloBitcoin.

           Login function will set the authentication token for the object
           instance and return the token."""

        api = "api/authenticate"
        username = username or self.username
        passwd = passwd or self.passwd
        postdict = dict(username=username, passwd=passwd)
        response = self._curl(api=api, postdict=postdict)
        if "success" in response.keys():
            self.auth_token = response.get("auth_token")
            return self.auth_token
        else:
            return None

    def authentication_required(function):
        def wrapped(self, *args, **kwargs):
            if not self.auth_token:
                msg = "You must be authenticated to use this method"
                raise Exception, msg
            else:
                return function(self, *args, **kwargs)
        return wrapped

    @authentication_required
    def new(self, quantity, price, side, contract_id="BTC_USD"):
        """Place a new order.

           On success:
               Returns order ID
            On error:
                Returns error message

        """

        api = "api/order/new"
        assert side in ('bid', 'ask'), "Argument 'side' must be either 'bid' or 'ask'"
        postdict = {
            'quantity'          : quantity,
            'price'             : price,
            'side'              : side,
            'contract_id'       : contract_id,
            'auth_token'        : self.auth_token,
            }
        response = self._curl(api=api, postdict=postdict)
        if "success" in response.keys():
            return response.get("order_id")
        else:
            return False

    @authentication_required
    def cancel(self, order_id, contract_id="BTC_USD"):
        """Cancel an existing order.

           Returns True for successful cancel else False
        """

        api = "api/order/cancel"
        postdict = {
            'order_id'          : order_id,
            'contract_id'       : contract_id,
            'auth_token'        : self.auth_token,
            }
        response = self._curl(api=api, postdict=postdict)
        if "success" in response.keys():
            return True
        else:
            return False

    @authentication_required
    def cancel_all(self):
        """Cancel all live orders

           Returns True for success else False
        """

        api = "api/order/cancelall"
        postdict = { 'auth_token': self.auth_token }
        response = self._curl(api=api, postdict=postdict)
        if "success" in response.keys():
            return True
        else:
            return False

    @authentication_required
    def get_open_orders(self):
        """Get open orders.
        """

        api = "api/order/open"
        postdict = dict(auth_token=self.auth_token)
        return self._curl(api=api, postdict=postdict)


    BASE_URL = "https://hellobitcoin.com/"
    def _curl(self, api, postdict=dict(), timeout=8, responseformat="json"):
        url = self.BASE_URL + api
        if postdict:
            postdata = urllib.urlencode(postdict)
            request = urllib2.Request(url, postdata)
        else:
            request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=timeout)
        body = response.read()
        if responseformat == "json":
            return json.loads(body)
        elif responseformat == "csv":
            return body
        else:
            return None

if __name__ == "__main__":
    username = "foo"
    passwd = "bar"

    hello = HelloBitcoin(username, passwd)

    # Usage example
    import time

    # Authenticate
    auth_token = hello.authenticate()
    print "Auth token: %s " % auth_token
    print "We won't ever need this though because the object holds it"
    print
    time.sleep(3)

    # Create an order
    print "Lets create an order"
    my_order_id = hello.new(quantity=11, price=12.65, side="bid", contract_id="BTC_USD")
    print "Newly created order has ID: %s" % my_order_id
    print
    time.sleep(3)

    print "Now cancel it"
    cancel_success = hello.cancel(order_id=my_order_id, contract_id="BTC_USD")
    print "Cancellation attempts return True on success and False on failure"
    print "Successfully cancelled order '%s'? %s" % (my_order_id, cancel_success)
    print

    time.sleep(3)
    print "We can also request public data"
    print
    time.sleep(5)

    # Unauthenticated examples
    print hello.historical()
    print "Above is a recent trades list as csv"
    print
    time.sleep(5)
    print hello.orderbook()
    print "The full orderbook for a given contract_id"
    print
    time.sleep(5)
    print hello.snapshot()
    print "a top of book snapshot"
    print
