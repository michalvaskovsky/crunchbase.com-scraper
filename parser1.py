# -*- coding: utf-8 -*-
#import
import lxml.html
from lxml.etree import tostringlist, tostring
import io


# id="section-funding-rounds"

class Parser():

    #
    #   Board members and advisors
    def parseBoardMembers(self, data):

        x = [
            '//*[@id="section-board-members-and-advisors"]/mat-card/div[2]/big-values-card/div/div/mat-card/span[2]/field-formatter/a',
            '//*[@id="section-board-members-and-advisors"]/mat-card/div[2]/image-list-card/div[1]/div/div/a'
        ]

        html = lxml.html.fromstring(data)
        elems = html.xpath(x[0])
        if len(elems) == 0:
            return {}

        res = [['Members and advisors', elems[0].text]]
        elems = html.xpath(x[1])
        [res.append([e.text]) for e in elems]

        return {
            'header': 'Board members and advisors',
            'lst': res
        }

    #
    #   Investments section
    #    if section is missing, return empty dict
    def parseInvestments(self, data):
        x = [
            '//*[@id="section-investments"]/mat-card/div[2]/big-values-card/div/div[1]/mat-card/span[2]/field-formatter/a',
            '//*[@id="section-investments"]//tr',
            './/td'
        ]

        html = lxml.html.fromstring(data)
        elems = html.xpath(x[0])
        if len(elems) == 0:
            return {}

        res = [['Number of investments', elems[0].text]]
        elems = html.xpath(x[1])
        for elem in elems:
            tds = elem.xpath(x[2])
            if len(tds) >= 5:
                res.append([
                    tds[0].text_content(),
                    tds[1].text_content(),
                    tds[4].text_content()
                ])

        return {
            'header': 'Investments',
            'lst': res
        }

    #
    #   Main company description
    #       return list of pairs [ itemtype, data ]
    def parseDescription(self, data):
        x = [
            '//*[@id="section-overview"]/mat-card/div[2]/fields-card[{}]/div/span'
        ]

        html = lxml.html.fromstring(data)

        res = []
        for i in range(1, 5):
            elems = html.xpath(x[0].format(i))
            if len(elems):
                itr = iter(elems)
                while True:
                    try:
                        res.append([
                            next(itr).text_content().replace(u'\xa0', u''),
                            next(itr).text_content().replace(u'\xa0', u'')
                        ])
                    except StopIteration:
                        break


        return {
            'header': 'Description',
            'lst': res
        }

    #
    #   Acquisitions
    def parseAcquisitons(self, data):
        ack = dict(header='Acquisitions')

        x = [
            '//*[@id="section-acquisitions"]/mat-card/div[2]/big-values-card/div/div/mat-card/span[2]/field-formatter/a',
            '//*[@id="section-acquisitions"]/mat-card//td/field-formatter/span',
            '//*[@id="section-acquisitions"]/mat-card//td/field-formatter/identifier-formatter/a/div/div[2]'
        ]

        html = lxml.html.fromstring(data)
        elems = html.xpath(x[0])
        if len(elems) == 0:
            return {}

        lst =[['Number of acquisitions', elems[0].text]]
        elems = iter(html.xpath(x[1])) # pairs: date, price
        elems1 = iter(html.xpath(x[2])) # pairs: organization name, transaction name
        switch = False
        d = list()
        for e1, e2 in zip(elems, elems1):
            if switch:
                d.extend([e1.text, e2.text])
                lst.append(d)
                d = list()
                switch = False
            else:
                d.extend([e1.text, e2.text])
                switch = True

        ack['lst'] = lst
        return ack

    #
    #   Investors
    def parseInvestors(self, data):
        investors = dict(header='Investors')
        x = [
            '//*[@id="section-investors"]//field-formatter/a',  # investors
            '//*[@id="section-investors"]//a/div/div[2]'
        ]

        html = lxml.html.fromstring(data)

        # Funding rounds
        # number of funding rounds and total investment
        # first from the list are ours
        elems = html.xpath(x[0])
        if len(elems) == 0:
            return {}

        lst = [
            ['Number of lead investors', elems[0].text],
            ['Investors total', elems[1].text]
        ]

        lines = iter(html.xpath(x[1]))
        for line in lines:
            lst.append([line.text, next(lines).text])

        investors['lst'] = lst
        return investors


    #
    #   Funding
    def parseFunding(self, data):
        funding = dict(header='Funding')
        x = [
            '//*[@id="section-funding-rounds"]//field-formatter/a', # funding rounds top
            '//*[@id="section-funding-rounds"]//tr', # lines in the funding table
            './/span',      # relative to table tr
            './/a/div/div', # relative to table tr
            './/a'          # relative to tr
        ]

        html = lxml.html.fromstring(data)

        # Funding rounds
        # number of funding rounds and total investment
        # first from the list are ours
        elems = html.xpath(x[0])
        if len(elems) == 0:
            return {}

        lst = [
            ['Funding rounds', elems[0].text],
            ['Amount total', elems[1].text],
            ['Date', 'Amount', 'Trans name', 'Num investors', 'Lead investor'],

        ]

        lines = iter(html.xpath(x[1]))
        next(lines) # skip the table header
        for line in lines:
            elems = line.xpath(x[2])
            if len(elems) < 3:
                raise Exception("xpath={}".format(x[2]))

            d = [elems[0].text, elems[1].text,'','','']

            # Transaction name
            elem = line.xpath(x[3])
            if len(elem) < 2:
                raise Exception("xpath={}".format(x[3]))
            d[2] = elem[1].text

            # Number of investors, lean investor
            elems = line.xpath(x[4])
            if len(elems) < 2:
                raise Exception("xpath={}".format(x[4]))
            d[3] = elems[1].text
            if len(elems) >= 3:
                d[4] = elems[2].text if len(elems[2].text) > 1 else ''

            lst.append(d)

        funding['lst'] = lst
        return funding


    def parseFile(self, path):
        with io.open(path, 'r', encoding='utf-8') as f:
            data = f.read()


        final = []
        functions = [
            self.parseDescription,
            self.parseBoardMembers,
            self.parseInvestments,
            self.parseAcquisitons,
            self.parseInvestors,
            self.parseFunding
        ]

        for f in functions:
            #print ('f={}'.format(f))
            try:
                res = f(data)
                if len(res):
                    final.append(res)
            except Exception as e:
                print ('Parser.parseFile().Exception.\n\tfunction={}\n\tmessage={}'.format(f, e))

        return final




