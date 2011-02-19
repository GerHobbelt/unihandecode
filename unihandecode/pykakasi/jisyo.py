# -*- coding: utf-8 -*-
#  jisyo.py
#
# Copyright 2011 Hiroshi Miura <miurahr@linux.com>
import os
try: #python2
    from cPickle import load
except: #python3
    from pickle import load

class jisyo (object):
    _len = None
    _dict = None

    def __init__(self, pklname):
        dict_pkl = open(os.path.join('unihandecode','pykakasi',pklname), 'rb')
        (self._dict, self._len) = load(dict_pkl)

    def haskey(self, key):
        return key in self._dict

    def lookup(self,key):
        return self._dict[key]
        
    def maxkeylen(self):
        return self._len
