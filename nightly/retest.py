#!/usr/bin/python
#!encoding:utf-8

import os
import re
import sys
import commands

from xml.etree import ElementTree as ET

def listFiles(dirPath):
    fileList = [];
    for root, dirs, files in os.walk(dirPath):
        for fileObj in files:
            if fileObj.endswith("tests.xml"):
                fileList.append(os.path.join(root, fileObj))
    return fileList

def findString(filePath, regex):
    flag = False
    fileObj = open(filePath, 'r')
    for line in fileObj:
        if re.search(regex, line):
            print "find %s at %s" % (regex, filePath)
            flag = True
            break
    fileObj.close()
    return flag

def main():
    orig_dir = os.getcwd()
    launcher = "XWalkLauncher"
    if os.path.basename(os.getcwd()) == "cordova":
        launcher = "CordovaLauncher"
    fileDir = "code/opt/webapi-noneservice-tests/"
    targetFile = ""
    resultXml = ""
    if not sys.argv[1].endswith("-tests"):
        regex = "id=\"%s\"" % sys.argv[1]
        fileList = listFiles(fileDir)
        for fileObj in fileList:
            if findString(fileObj, regex):
                targetFile = os.path.basename(fileObj)
        if targetFile is "":
            print "Error: Not found ID: %s !" % sys.argv[1]
            sys.exit(1)
        print targetFile
        resultXml = "result_%s_%s.xml" % (targetFile[0:-10], sys.argv[1])
        print resultXml
        webdriver_flag = False
        ep = ET.parse("code/opt/webapi-noneservice-tests/%s" % targetFile)
        tc_sets = ep.getiterator('set')
        for tc_set in tc_sets:
            if tc_set.get('ui-auto') == "wd" or \
                tc_set.get('ui-auto') == "bdd":
                tcs = tc_set.getiterator('testcase')
                for tc in tcs:
                    if tc.get('id') == sys.argv[1]:
                        webdriver_flag = True
        if webdriver_flag:
            launcher += " -k webdriver"
            resultXml = "result_%s_%s_webdriver_single.xml" % (targetFile[0:-10], sys.argv[1])
        cmd = "if test -f ../../../rerun_xml/single_xml/%s ;then rm ../../../rerun_xml/single_xml/%s ;fi;" % (resultXml, resultXml)
        cmd += "testkit-lite -e %s --comm androidmobile -f $PWD/%s --id %s -o ../../../rerun_xml/single_xml/%s" % (launcher, targetFile, sys.argv[1], resultXml)
    else:
        targetFile = "%s.tests.xml" % sys.argv[1]
        resultXml = "result_%s.xml" % sys.argv[1]
        cmd = "if test -f ../../../rerun_xml/stub_xml/%s ;then rm ../../../rerun_xml/stub_xml/%s ;fi;" % (resultXml, resultXml)
        cmd += "testkit-lite -e %s -A --comm androidmobile -f $PWD/%s -o ../../../rerun_xml/stub_xml/%s" % (launcher, targetFile, resultXml)
    print cmd
    os.chdir("%s/%s" % (orig_dir, fileDir))
    status, info = commands.getstatusoutput(cmd)
    if status == 0:
        print "OK"        
        print info 
    else:
        print info 
    os.chdir(orig_dir)

if __name__ == '__main__':
    main()
