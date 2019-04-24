# -*- coding: utf-8 -*-

import io
from parser1 import Parser

import unittest

files = [
    'tmp\\test_paypal.html',
    'tmp\\test_stripe.html',
    'tmp\\test_yahoo.html',
    'tmp\\test_taco-bell.html',
    'tmp\\test_the-muse.html'
]

class Test_Parser(unittest.TestCase):

    def test_ParseFunding(self):

        for path in files:
            print ('Parsing={}'.format(path))

            with io.open(path, 'r', encoding='utf-8') as f:
                data = f.read()

            p = Parser()
            r = p.parseFunding(data)
            assert len(r)
            print (r)

    def test_Investors(self):

        for path in files:
            print ('Parsing={}'.format(path))

            with io.open(path, 'r', encoding='utf-8') as f:
                data = f.read()

            p = Parser()
            r = p.parseInvestors(data)
            assert len(r)
            print (r)

    def test_Acquisitions(self):
        for path in files:
            print ('Parsing={}'.format(path))

            with io.open(path, 'r', encoding='utf-8') as f:
                data = f.read()

            p = Parser()
            r = p.parseAcquisitons(data)
            assert len(r)
            print (r)


    def test_Description(self):
        for path in files:
            print ('Parsing={}'.format(path))

            with io.open(path, 'r', encoding='utf-8') as f:
                data = f.read()

            p = Parser()
            r = p.parseDescription(data)
            assert len(r)
            print (r)

    def test_Investments(self):
        for path in files:
            print ('Parsing={}'.format(path))

            with io.open(path, 'r', encoding='utf-8') as f:
                data = f.read()

            p = Parser()
            r = p.parseInvestments(data)
            #assert len(r)
            print (r)

    def test_BoardMembers(self):
        for path in files:
            print ('Parsing={}'.format(path))

            with io.open(path, 'r', encoding='utf-8') as f:
                data = f.read()

            p = Parser()
            r = p.parseBoardMembers(data)
            #assert len(r)
            print (r)

    def test_ParseFile(self):
        for path in files:
            p = Parser()
            p.parseFile(path)
            break


