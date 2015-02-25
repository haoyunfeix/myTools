#!/usr/bin/python
#!encoding:utf-8

#yunfeix.hao@intel.com

import os
import sys
import re
import commands
import glob
import fnmatch
import sqlite3
from datetime import datetime
from xml.etree import ElementTree as ET
from optparse import OptionParser, make_option

usage = "help"
opts_parser = OptionParser(usage=usage)
opts_parser.add_option(
    "--f1",
    dest="xml1",
    help="specify the xml 1.")
opts_parser.add_option(
    "--f2",
    dest="xml2",
    help="specify the xml 2.")
opts_parser.add_option(
    "--f3",
    dest="xml3",
    help="specify the xml 3.")
(PARAMETERS, args) = opts_parser.parse_args()

ep = ET.parse(PARAMETERS.xml1)
suiteparent = ep.getroot()
ep2 = ET.parse(PARAMETERS.xml2)
for suite in ep2.getiterator('suite'):
    suite.tail = "\n"
    suiteparent.append(suite)

with open(PARAMETERS.xml3, 'w') as output:
    tree = ET.ElementTree(element=suiteparent)
    tree.write(output)
