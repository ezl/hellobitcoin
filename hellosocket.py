import websocket
import cjson
from hello import HelloBitcoin

server = "hellobitcoin.com"

class WebSocketListener(websocket.WebSocketApp):
    def on_message(self, ws, message):
        print message
        print "# " * 20
        print

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        print "### closed ###"

    def on_open(self, ws):
        print 'onopen'
        if self.auth_token is not None:
            print 'sending'
            self.send(cjson.encode({'msg_type':'authentication', 'auth_token':self.auth_token}))
    
    def __init__(self, url='wss://%s:9000/websocket' % server, auth_token=None):
        self.auth_token = auth_token
        super(WebSocketListener, self).__init__(url,
                                                  on_message = self.on_message,
                                                  on_error = self.on_error,
                                                  on_open = self.on_open,
                                                  on_close = self.on_close)



class HelloBitcoinListener(HelloBitcoin):
    @property
    def BASE_URL(self):
        return  "https://%s:9000/" % server
    
    @property
    def WSS_URL(self):
        return  "wss://%s:9000/websocket" % server
    
    def connect_websocket(self):
        self.listener = WebSocketListener(url=self.WSS_URL, auth_token=self.auth_token)

if __name__ == "__main__":
    username = "foo"
    passwd = "bar"

    subscriber = HelloBitcoinListener(username, passwd)
    subscriber.authenticate()
    subscriber.connect_websocket()
    subscriber.listener.run_forever()
