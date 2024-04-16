import tornado.ioloop
import tornado.web
import tornado.websocket
import time

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("open success")
        # timer that sends data to the front end once per second
        self.timer = tornado.ioloop.PeriodicCallback(self.send_data, 1000)
        self.timer.start()

    def on_close(self):
        self.timer.stop()

    def send_data(self):
        # send the current time to the front end
        self.write_message('Now is' + str(time.time()))

application = tornado.web.Application([
    (r'/', WebSocketHandler),
])

if __name__ == '__main__':
    port = 3001
    print(f"Starting WebSocket server on port {port}")
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

