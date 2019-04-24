# -*- coding: utf-8 -*-
# UPDATE. 6.2.2019
# Python3 compatible
import mechanize
import user_agent
import time
import sys

if sys.version_info[0] >= 3:
    import http.cookiejar as cookielib
else:
    import cookielib


class DowloaderMechanize():

    # proxy format: IP:PORT
    def __init__(self, proxy=None):

        br = mechanize.Browser()

        # Cookie Jar
        self.cj = cookielib.LWPCookieJar()
        br.set_cookiejar(self.cj)

        # Browser options
        br.set_handle_equiv(False)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        # br.set_debug_http(True)
        # br.set_debug_redirects(True)
        # br.set_debug_responses(True)

        br.addheaders = [('User-Agent', user_agent.generate_user_agent()),
                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Language', 'en-gb,en;q=0.5'),
                         ('Accept-Encoding', 'gzip,deflate'),
                         ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
                         ('Keep-Alive', '115'),
                         ('Connection', 'keep-alive'),
                         ('Cache-Control', 'max-age=0')]

        if proxy:
            br.set_proxies({"https": proxy, "http": proxy})

        self.br = br

    # url and referrer must be passed as str if either if they contain non-ascii chars
    def getPage(self, url, retry=2, referer=None):

        if referer:
            self.br.set_header('Referer', referer)

        for i in range(retry):

            try:
                self.br.open(url)
                data = self.br.response().read()
                return data.decode('utf-8')
            except (mechanize.HTTPError,mechanize.URLError) as e:
                if isinstance(e,mechanize.HTTPError):
                    print (e.code)
                else:
                    print (e.reason.args)
            except Exception as e:
                print ('Mechanize general exception')
                print (e)

        return u''

import unittest
import lxml.html
import io
class Test_Mechanize(unittest.TestCase):

    def test_getpage(self):
        url="https://www.crunchbase.com/organization/stripe"
        browser = DowloaderMechanize(None)
        data = browser.getPage(url)
        assert len(data)
        with io.open(r'tmp\mechanize_test1.html', mode='w', encoding='utf=8') as f:
            f.write(data)




