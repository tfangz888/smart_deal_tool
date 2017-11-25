#!/home/tops/bin/python -u
import sys
from log import getLogger
from collect import StockManager
from optparse import OptionParser
try:
    import gevent
except ImportError:
    print "error: httpd require gevent package."
    sys.exit(1)
from gevent import monkey
from gevent.pool import Pool
import gevent.wsgi
monkey.patch_all(subprocess=True)

parser = OptionParser(usage="./%prog [host][port]", version="%prog v0.1")
parser.add_option("-H", "--host", default="0.0.0.0", help="default: %default", metavar="HOST")
parser.add_option("-P", "--port", default=20041, type="int", help="default: %default", metavar="PORT")
(options, args) = parser.parse_args()

def init(sleep=0):
    #init data for trade
    s.init()

def get_stock_realtime_info(sleep=0):
    s.get_stock_realtime_info()

def get_index_realtime_info(sleep=0):
    s.get_index_realtime_info()

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    (_, _, path_info, _, _, _) = urlparse(environ["PATH_INFO"])
    start_response("200 OK", headers)
    return status_handler(environ, start_response)

def main():
    log = getLogger(__name__)
    gevent.spawn_later(5, init, 86400)
    #gevent.spawn_later(10, get_stock_realtime_info, 10)
    #gevent.spawn_later(10, get_index_realtime_info, 15)
    log.info("serving on port %s:%s." % (options.host, options.port))
    httpd = gevent.wsgi.WSGIServer((options.host, options.port), application)
    httpd.serve_forever()

s = StockManager()
if __name__ == "__main__":
    main()