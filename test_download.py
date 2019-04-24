# -*- coding: utf-8 -*-

from downloader_mechanize import DowloaderMechanize
import unittest
import time
import io

class Test_Download(unittest.TestCase):

    def test_Download(self):

        mechanize = DowloaderMechanize()

        lst = [
            'https://www.crunchbase.com/organization/paypal',
            'https://www.crunchbase.com/organization/stripe',
            'https://www.crunchbase.com/organization/yahoo',
            'https://www.crunchbase.com/organization/taco-bell',
            'https://www.crunchbase.com/organization/the-muse'
        ]

        for l in lst:
            file = 'tmp\\test_{}.html'.format(l.rsplit('/', 1)[1])
            data = mechanize.getPage(l, 2)
            assert len(data)
            with io.open(file, 'w', encoding='utf-8') as f:
                f.write(data)

            time.sleep(5)








