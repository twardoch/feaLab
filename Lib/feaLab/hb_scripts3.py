#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mini-module to convert between Unicode and OpenType
script tags.

Uses the 'harfpy' ctypes-based Python 3 bindings for HarfBuzz
https://github.com/ldo/harfpy

1. Until https://github.com/ldo/harfpy/pull/12 is merged, use:
https://github.com/twardoch/harfpy

2. On macOS, works with HarfBuzz installed via
brew install harfbuzz

3. On Windows, should work with the prebuilt binaries from
https://www.freedesktop.org/software/harfbuzz/release/

4. The actual conversion functions are implemented in:
https://github.com/harfbuzz/harfbuzz/blob/master/src/hb-ot-tag.cc
"""

from __future__ import unicode_literals, print_function

__version__ = '0.0.1'

import re

import fontTools.ttLib
import fontTools.unicodedata as ud
from fontTools.misc.py23 import *

import harfbuzz as hb
hbu = hb.UnicodeFuncs.get_default()

def _getTag(s):
    s = s.ljust(4)[:4].encode()
    return hb.HB.TAG(s)

def isoScript(s):
    tag = _getTag(s)
    rtag = hb.script_to_iso15924_tag(hb.hb.hb_ot_tag_to_script(tag))
    if rtag == 0:
        return 'Zyyy'
    else:
        return hb.tag_to_string(rtag)

def otScripts(s):
    s = isoScript(s)
    if s[:1] == 'Z':
        return ['DFLT']
    else:
        tag = _getTag(s)
        scripts = [hb.tag_to_string(tag) for tag in hb.ot_tags_from_script(tag)]
        if scripts[1] == 'DFLT':
            return scripts[:1]
        else:
            return scripts

def otScript(s):
    return otScripts(s)[0]

def charScript(char):
    code = byteord(char)
    return hb.tag_to_string(hbu.script(code))

def getIsoToOtScriptMap():
    OTSCRIPTS = {isoScript: otScripts(isoScript) for isoScript in ud.Scripts.NAMES.keys()}
    return OTSCRIPTS

def updateLanguageSystemsInFea(feaText='', ftFont=None, unicodes=[]):
    if ftFont:
        unicodes = []
        tCmap = ftFont['cmap']
        cmap = tCmap.getcmap(3, 10)
        if not cmap:
            cmap = tCmap.getcmap(3, 1)
        if not cmap:
            cmap = tCmap.getcmap(0, 3)
        if not cmap:
            cmap = tCmap.getcmap(3, 0)
        if cmap:
            unicodes = cmap.cmap.keys()

    feaLines = []
    langsyses = []
    for line in feaText.splitlines():
        langsys = None
        for script, lang in re.findall(
                r'^.*?languagesystem\s+([A-Za-z]{4})\s+([A-Z]+|dflt)\s*;',
                line):
            langsys = (script, lang)
        if langsys:
            langsyses.append(langsys)
        else:
            feaLines.append(line)
    for u in unicodes:
        langsys = (otScript(charScript(u)), 'dflt')
        langsyses.append(langsys)
    langsysesFirst = [('DFLT', 'dflt'), ('latn', 'dflt')]
    langsyses = set(langsyses) - set(langsysesFirst)
    langsyses = langsysesFirst + sorted(list(langsyses))
    langsysLines = ['languagesystem {} {};'.format(l[0], l[1]) for l in langsyses]
    feaText= '\n'.join(langsysLines + feaLines)
    return feaText

if __name__ == '__main__':
    #print(isoScript('dev2'))
    #print(otScript('DFLT'))
    #print(otScript('Zzzz'))
    #print(otScript('Zyyy'))
    #print(otScript('Zinh'))
    #print(otScript('Latn'))
    #print(otScript('dev2'))
    #print(otScript('Grek'))
    #print(otScript('deva'))
    #print(charScript('আ'))
    #print(ud.script('আ'))
    #print(getIsoToOtScriptMap())

    fea = """
languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem latn PLK;
languagesystem cyrl dflt;
languagesystem cyrl SRB;
# Comment
feature smcp { 
  sub a by a.sc;
} smcp;
"""
    print(updateLanguageSystemsInFea(feaText=fea, unicodes=[0x010A, 0x20AC, 0x063C]))
