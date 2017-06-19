# code: utf-8

import json
import socket
import urllib2

from . import proxy


def get_servername(url):
    server = url
    server = server[server.find('://')+3:]
    if '/' in server:
        server = server[:server.find('/')]
    return server


def try_request(url, timeout=30, debug=False, force_error=False):
    response = None
    socket.setdefaulttimeout(timeout)
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    req = urllib2.Request(url)
    http_error_proxy_auth = None
    error_message = ''
    try:
        response = urllib2.urlopen(req, timeout=timeout).read()
    except urllib2.HTTPError as e:
        if e.code == 407:
            http_error_proxy_auth = e.code
        error_message = e.read()
    except urllib2.URLError as e:
        if '10061' in str(e.reason):
            http_error_proxy_auth = e.reason
        error_message = 'URLError'
    except urllib2.socket.timeout:
        error_message = 'Time out!'
    except Exception as e:
        error_message = 'Unknown!'
        #raise
    if force_error is True:
        response = None
        http_error_proxy_auth = True
    if error_message != '':
        print((url, error_message, response, http_error_proxy_auth))
    return (response, http_error_proxy_auth, error_message)


class WebServicesRequester(object):

    def __init__(self, is_enabled=True, proxy_info=None):
        self.requests = {}
        self.skip = []
        self.proxy_info = proxy_info
        self.is_enabled = is_enabled

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(WebServicesRequester, self).__new__(self)
        return self.instance

    def update_proxy_info(self):
        if self.proxy_info is not None:
            proxy_checker = proxy.ProxyChecker(self.proxy_info)
            proxy_checker.update()
            self.proxy_info = proxy_checker.proxy_info
            self.registry_proxy_opener()
            proxy_handler = urllib2.ProxyHandler(self.proxy_info.handler_data)
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)

    def request(self, url, timeout=30, debug=False, force_error=False):
        #print(url)
        if self.is_enabled is False:
            return None

        response = self.requests.get(url)
        if response is None and url not in self.requests.keys():
            server = get_servername(url)
            if server not in self.skip:
                #print(' ==> request')
                response, http_error_proxy_auth, error_message = try_request(url, timeout, debug, force_error)
                if http_error_proxy_auth is True:
                    self.update_proxy_info()
                    response, http_error_proxy_auth, error_message = try_request(url, timeout, debug, force_error)

                if response is None and error_message != '':
                    self.skip.append(server)
                self.requests[url] = response
        return response

    def json_result_request(self, url, timeout=30, debug=False):
        if self.is_enabled is False:
            return None
        result = None
        if url is not None:
            r = self.request(url, timeout, debug)
            if r is not None:
                result = json.loads(r)
        return result

    def is_valid_url(self, url, timeout=30):
        if self.is_enabled is False:
            return None
        _result = self.request(url, timeout)
        return _result is not None
