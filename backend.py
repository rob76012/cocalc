"""
Workspace Server Backend

"""

# todo -- implement proper logging
LOG = False
if LOG:
    if not os.path.exists('logs'):
        os.makedirs('logs')

import cgi, json, sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from session import SimpleStreamingSession

from misc import get, post
    
##############################
# compute session object
##############################

class ComputeSession(object):
    def __init__(self, url, frontend_url, output_url, execpath):
        
        class Handler(BaseHTTPRequestHandler):
            session = self
            def do_GET(self):
                if self.path == '/execpath':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(Handler.session._session._execpath)
                else:
                    self.send_error(404,'File Not Found: %s' % self.path)
                    
            def do_POST(self):
                try:
                    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                    if ctype == 'application/x-www-form-urlencoded':
                        length = int(self.headers.getheader('content-length'))
                        postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
                    else:
                        postvars = {}
                    Handler.session._postvars = postvars
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write('ok')
                except IOError, msg:
                    self.log('error in do_POST', msg)
                    self.send_error(404,'File Not Found: %s' % self.path)
                    
        self._url = url
        self._frontend_url = frontend_url
        self._output_url = output_url
        self._port = int(url.split(':')[-1])
        # TODO: the '' in the next line is probably wrong
        self._server  = HTTPServer(('', self._port), Handler)
        self._session = SimpleStreamingSession(
                          0, lambda msg: self.output(msg), execpath=execpath)

    def log(self, *msg):
        if LOG:
            open('logs/%s'%self._port,'a').write(''.join([str(x) for x in msg]) + '\n')

    def run(self):
        while True:
            self._postvars = {}
            self.log('handle_request')
            self._server.handle_request()
            self.log(self._postvars)
            if self._postvars.has_key('cells'):
                # the request resulted in a POST request with code to execute
                cells = json.loads(self._postvars['cells'][0])
                self.log("cells = ", cells)
                for cell in cells:
                    # TODO: we are temporarily ignoring the double check of cell['exec_id']. Use it!
                    self._session.execute(str(cell['code']))

                # Next, get more cells to evaluate, if there are some:
                while True:
                    msg = json.loads(get(self._frontend_url))
                    if msg['status'] == 'done':
                        break
                    for cell in msg['cells']:
                        # TODO: we are ignoring the double check of cell['exec_id']. Use it somehow?
                        self._session.execute(str(cell['code']))

                # no more tasks: we go back to top of while loop and
                # which means switching back into webserver state
                
                # TODO: above code is way too redundant.  Needs clever refactoring!

    def output(self, msg):
        post(self._output_url, msg, timeout=60)
            

        


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: %s URL FRONTEND_URL OUTPUT_URL EXEC_PATH"%sys.argv[0]
        sys.exit(1)
    url          = sys.argv[1]
    frontend_url = sys.argv[2]
    output_url   = sys.argv[3]
    execpath     = sys.argv[4]
    S = ComputeSession(url, frontend_url, output_url, execpath)
    S.run()
    
