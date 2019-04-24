# -*- coding: utf-8 -*-
import sys
import argparse

class StoreInDict(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        d = getattr(namespace, self.dest)
        for opt in values:
            k,v = opt.split(u"=", 1)
            k = k.lstrip(u"-")
            if k in d:
                d[k].append(v)
            else:
                d[k] = [v]
        setattr(namespace, self.dest, d)

class ParamsHelper():

    def getParams(self):
        s = sys.argv
        p = argparse.ArgumentParser(prefix_chars=u' ')
        p.add_argument("options", nargs=u"*", action=StoreInDict, default=dict())
        return p.parse_args(s[1:]).options



