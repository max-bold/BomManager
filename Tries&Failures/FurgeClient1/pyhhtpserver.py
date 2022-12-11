from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import webbrowser
from urllib.parse import urlparse, parse_qs
from threading import Thread

class rhandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server) -> None:
        self.req = request
        super().__init__(request, client_address, server)
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b'DONE')
        print(parse_qs(self.requestline))
        # print(self.req)


# server  = HTTPServer(('',8000), rhandler)
# server.serve_forever()

class ServerThread(Thread):
    def __init__(self, address:str,port:int) -> None:
        super().__init__()
        self.server = server  = HTTPServer((address,port), rhandler)

    def run(self) -> None:
        self.server.serve_forever()
        return super().run()



# webbrowser.open('https://docs.python.org/3/library/webbrowser.html')

if __name__ == '__main__':
    server = ServerThread('localhost',8000)
    server.start()