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

import retest

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
opts_parser.add_option(
    "--rerun",
    dest="rerun",
    help="flag of rerun")
opts_parser.add_option(
    "--show",
    dest="show",
    action="store_true",
    help="flag of show number")
(PARAMETERS, args) = opts_parser.parse_args()

def rtn (x):
    if x == "FAIL":
        return "\33[0;31m" + x + "\033[0m"
    elif x == "PASS":
        return "\33[0;32m" + x + "\033[0m"
    else:
        return x

def diff_xml(xml1, xml2):
    rList = []
    ep = ET.parse(xml1)
    ep2 = ET.parse(xml2)
    list1 = []
    dict1 = {}
    list2 = []
    dict2 = {}
    for testcase in ep.getiterator('testcase'):
        t1_id = testcase.get('id')
        t1_rlt = testcase.get('result')
        list1.append((t1_id, t1_rlt))
    dict1 = dict(list1) 
    for testcase in ep2.getiterator('testcase'):
        t2_id = testcase.get('id')
        t2_rlt = testcase.get('result')
        list2.append((t2_id, t2_rlt))
    dict2 = dict(list2) 
    rlt = []
    for key in dict1:
        if dict1.get(key) ==dict2.get(key):
            pass
        else:
            rlt.append(key)
    if rlt != []:
        print "----- %s -----" % xml1
        for i in rlt:
            print "Case ID is: %s" % i
            print "%s -> %s" % (rtn(dict2.get(i)), rtn(dict1.get(i)))
            if dict2.get(i) == "PASS":
                rList.append(i)
        print "---------------------------------"
        print  
    return rList

retestList = []
retestSuiteList = []
if os.path.isfile(PARAMETERS.xml1) and os.path.isfile(PARAMETERS.xml2):
    retestList = diff_xml(PARAMETERS.xml1, PARAMETERS.xml2)
elif os.path.isdir(PARAMETERS.xml1):
    file_list = [] 
    for root, dirs, files in os.walk(PARAMETERS.xml1): 
        for filename in files: 
            if root == PARAMETERS.xml1: 
                if filename.endswith('.xml'): 
                    file_list.append(os.path.join(root, filename))
    file_list.sort()
    for file_real_path in file_list:
        if os.path.isfile(file_real_path) and os.path.isfile(file_real_path.replace(PARAMETERS.xml1, PARAMETERS.xml2)):
            subList = diff_xml(file_real_path, file_real_path.replace(PARAMETERS.xml1, PARAMETERS.xml2))
            if subList != []:
                retestSuiteList.append(file_real_path)
                for i in subList:
                    retestList.append(i)
if PARAMETERS.rerun == "id":
    if len(retestList) <= 20:
        for cid in retestList:
            print cid
            os.system("python ./retest.py %s" % cid)
    else:
        print "Warning: reRun cases number is \"%s\" more than 30, stop!!!" % len(retestList)
        sys.exit(1)
elif PARAMETERS.rerun == "set":
    for sid in retestSuiteList:
        sid = os.path.basename(sid).replace("result_","").replace(".xml","")
        print sid
        os.system("python ./retest.py %s" % sid)
else:
    print "rerun: %s" % PARAMETERS.rerun
    print "Invalid value of \"rerun \", use --rerun id or --rerun set"
if PARAMETERS.show is True:
    print len(retestList)
