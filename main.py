# -*- coding: utf-8 -*-

# Notes:
#  I. don't use capital letters in company name
#  II. Whitespaces in company name are substituted by '-' char

import io
import os
import string
import random
import xlsxwriter
from parser1 import Parser
from commandline_small import ParamsHelper
from downloader_mechanize import DowloaderMechanize

class Main():

    def __init__(self):
        self.parser = Parser()
        self.handleParams()
        self.current_row = 0

    def handleParams(self):
        ph = ParamsHelper()
        params = ph.getParams()

        self.options = {
            'company': params['company'][0],
            'outputfile': params['outfile'][0],
        }

        print ("company={} outputfile={}".format(self.options['company'], self.options['outputfile']))

    def DownloadSite(self, company_name):

        url = 'https://www.crunchbase.com/organization/{}'.format(company_name.lower().replace(' ', '-'))
        print ('Downloading url={}'.format(url))
        dm = DowloaderMechanize()
        return dm.getPage(url, 2, None)

    # return True/False
    def DownloadSiteToTempFile(self, company_name):
        self.tempfilename = 'tmp\\' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7)) + '.html'
        site_data = self.DownloadSite(company_name)
        if len(site_data):
            with io.open(self.tempfilename, 'w', encoding='utf-8') as f:
                f.write(site_data)
                return True

        return False

    def WriteDataToXlsx(self, data, worksheet):

        worksheet.write(self.current_row, 0, data['header'])
        self.current_row += 1
        for r, row in enumerate(data['lst']):
            for i in range(len(row)):
                worksheet.write(self.current_row, i, row[i])
            self.current_row += 1

        self.current_row += 1

    # return True/False
    def ExportData(self, data):

        workbook = xlsxwriter.Workbook(self.options['outputfile'], {'constant_memory': True})
        worksheet = workbook.add_worksheet()

        for d in data:
            self.WriteDataToXlsx(d, worksheet)

        workbook.close()
        return True

    def Process(self):
        r = self.DownloadSiteToTempFile(self.options['company'])
        if not r:
            print ("[-] Failed to download site data. Exiting")
            exit(1)

        print ("[+] Site data downloaded...\n\tfile={}".format(self.tempfilename))
        res = self.parser.parseFile(self.tempfilename)
        if len(res) == 0:
            print ('[-] Failed to scrape company data. Exiting')
            exit(1)

        print ('[+] Scraped company data.')
        self.ExportData(res)
        print ('[+] Data exported to file={}'.format(self.options['outputfile']))
        os.unlink(self.tempfilename)

def main():
    m = Main()
    m.Process()

main()









