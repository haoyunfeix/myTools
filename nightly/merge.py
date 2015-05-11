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

def merge_xml(ep2=None, suiteparent=None):
    for suite in ep2.getiterator('suite'):
        suite.tail = "\n"
        suiteparent.append(suite)
    
    with open(PARAMETERS.xml3, 'w') as output:
        tree = ET.ElementTree(element=suiteparent)
        tree.write(output)

def update_xml(xml, update_id, id_result):
    cmd = "python stats.py -f %s --id %s -c %s" % \
        (xml, update_id, id_result)
    status, info = commands.getstatusoutput(cmd)
    if status == 0:
        pass
    else:
        print "Change Fail"
        print info

usage = "help"
opts_parser = OptionParser(usage=usage)
opts_parser.add_option(
    "--f1",
    dest="xml1",
    help="specify the xml 1, parent(old) xml.")
opts_parser.add_option(
    "--f2",
    dest="xml2",
    help="specify the xml 2, child(new) xml.")
opts_parser.add_option(
    "--f3",
    dest="xml3",
    help="specify the xml 3, output xml.")
(PARAMETERS, args) = opts_parser.parse_args()

parent_id_list = []
ep = ET.parse(PARAMETERS.xml1)
suiteparent = ep.getroot()
tcs_of_parent = ep.getiterator('testcase')
for tc_p in tcs_of_parent:
    parent_id_list.append(tc_p.get('id'))
ep2 = ET.parse(PARAMETERS.xml2)
tcs_of_child = ep2.getiterator('testcase')
if len(tcs_of_child) == 1 and \
    tcs_of_child[0].get('id') in parent_id_list:
    update_id = tcs_of_child[0].get('id')
    id_result = tcs_of_child[0].get('result')
    update_xml(PARAMETERS.xml1, update_id, id_result)
else:
    merge_xml(ep2, suiteparent)
    
