import webbrowser as wb
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs
import json
from pyhhtpserver import ServerThread


class rhandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'DONE')
        print(parse_qs(self.requestline))


if __name__ == '__main__':
    address = 'localhost'
    port = 8000
    server = ServerThread(address, port)
    server.start()
    # server.serve_forever()
    url = 'https://developer.api.autodesk.com/authentication/v2/authorize?'
    creds = open("Tries&Failures\FurgeClient1\creds.json", "r")
    params = {
        'response_type': 'code',
        'client_id': json.load(creds)['clientid'],
        'redirect_uri': f'http://{address}:{port}/oauth/callback?foo=bar',
        'scope': 'data:read'
    }
    rurl = url+urlencode(params)
    print(rurl)
    print(params['redirect_uri'])
    wb.open(rurl)
