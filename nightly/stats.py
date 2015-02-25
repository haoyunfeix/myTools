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


def iterfindfiles (path, fnexp):
    for root, dirs, files in os.walk(path):
	    for filename in fnmatch.filter(files, fnexp):
		    yield os.path.join(root, filename)

def gogogo(xml=None, key=None):
    tree = ET.parse(xml)
    root = tree.getroot()
    for testcase_node in root.findall('suite/set/testcase'):
        if testcase_node.get('id') == key:
            entry_node = testcase_node.findall('description/test_script_entry')
            entry_node_ref = testcase_node.findall('description/refer_test_script_entry')
            if entry_node and entry_node_ref:
                print "%s: %s %s" % (key, entry_node[0].text, entry_node_ref[0].text)
                return 0
            elif entry_node:
                print "%s: %s" % (key, entry_node[0].text)
                return 0
            else:
                print " %s Not find entry" % key
                return 1

def read_xml(file_path = None):
    tree = ET.parse(file_path) 
    return tree
def write_xml(tree, outfile):
    tree.write(outfile, encoding="UTF-8", xml_declaration=True)
def update_xml(outfile):
    fp = file(outfile)
    s = fp.read()
    fp.close()
    a = s.split('\n')
    a.insert(1, '<?xml-stylesheet type="text/xsl" href="testresult.xsl"?>')
    s = '\n'.join(a)
    fp = file(outfile,'w')
    fp.write(s)
    fp.close()

def delete_node_by_set_name(nodelist=None, setname=None):
    for testset_parent_node in nodelist.findall('suite'):
        print testset_parent_node.get('name')
        children = testset_parent_node.getchildren()
        for child in children:
            print child.get('name')
            if setname is not None:
                if child.get('name') == setname:
                    testset_parent_node.remove(child)
            else:
                if child.get('name').find('ref') != -1:
                    testset_parent_node.remove(child)


def delete_node_by_case_id(nodelist=None, caseid=None):
    for testset_parent_node in nodelist.findall('suite/set'):
        print testset_parent_node.get('name')
        children = testset_parent_node.getchildren()
        for child in children:
            print child.get('id')
            if child.get('id') == caseid:
                testset_parent_node.remove(child)
        
        
def change_result_by_set_name(nodelist=None, setname=None, value=None, parent=None, chd=None):
    for testset_parent_node in nodelist.findall('suite'):
        print testset_parent_node.get('name')
        children = testset_parent_node.getchildren()
        for child in children:
            print child.get('name')
            if child.get('name') == setname:
                testcase_nodes = child.findall('testcase')
                for testcase_node in testcase_nodes:
                    testcase_node.set("result", value)
                    print testcase_node.get("result")

def change_result_by_case_id(nodelist=None, caseid=None, value=None, parent=None, chd=None):
    for testset_parent_node in nodelist.findall('suite/set'):
        print testset_parent_node.get('name')
        children = testset_parent_node.getchildren()
        for child in children:
            print child.get('id')
            if child.get('id') == caseid:
                    child.set("result", value)

def get_info(nodelist=None): 
    rlt_dict = {"pass":0 , "fail":0, "block":0, "not_run": 0, "sum": 0, "pass_rate": 0}
    for result_testcase in nodelist.getiterator("testcase"):
        if result_testcase.get("result") == "PASS":
            rlt_dict["pass"] += 1
            rlt_dict["sum"] += 1
        elif result_testcase.get("result") == "FAIL":
            rlt_dict["fail"] += 1
            rlt_dict["sum"] += 1
        elif result_testcase.get("result") == "BLOCK":
            rlt_dict["block"] += 1
            rlt_dict["sum"] += 1
        else:
            #rlt_dict["not_run"] += 1
            rlt_dict["block"] += 1
            rlt_dict["sum"] += 1
    if not rlt_dict["sum"] == 0:
        rlt_dict["pass_rate"] = float(rlt_dict["pass"]) * 100 / int(rlt_dict["sum"])
    return rlt_dict

def get_conn(path):
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        print ('on disk:[{}]'.format(path) )
        return conn
    else:
        print "%s not found" % path
        sys.exit(1)

def get_cursor(conn):
    if conn is not None:
        return conn.cursor()
    else:
        print "conn is none"
        sys.exit(1)

def close_all(conn,cu):
    try:
        if cu is not None:
            cu.close()
    finally:
        if conn is not None:
            conn.close()

def insert(conn, sql, data):
    if sql is not None and sql != '':
        if data is not None:
            cu = get_cursor(conn)
            for d in data:
                print('sql:[{}],opts:[{}]'.format(sql,d))
                cu.execute(sql, d)
                conn.commit()
            close_all(conn, cu)
    else:
        print ('the [{}] is empty or None!'.format(sql))

def create(conn, sql):
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        print('sql:[{}]'.format(sql))
        cu.execute(sql)
        conn.commit()
        close_all(conn, cu)
    else:
        print ('the [{}] is empty or None!'.format(sql))

def show(conn,sql):
    if sql is not None and sql != '':
        cu = get_cursor(conn)
        print('sql:[{}]'.format(sql))
        cu.execute(sql)
        r = cu.fetchall()
        if len(r) >0:
            for e in range(len(r)):
                for i in range(len(r[e])):
                    print "%s" % r[e][i],
                print ""
        conn.commit()
        close_all(conn, cu)
    else:
        print ('the [{}] is empty or None!'.format(sql))

def insert_database_from_xml(folder_path):
    if folder_path is not None and folder_path != '':
        table_name = "t_%s" % os.path.basename(folder_path).replace(".", "_")
        create_sql = "create table %s (path, name, pass, fail, block, notrun, passrate)" % table_name
        conn = get_conn(DATA_BASE_PATH)
        create(conn, create_sql)
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".xml"):
                continue
            file_real_path = os.path.join(root, filename)
            tree1 = read_xml(file_real_path)
            nodelist1 = tree1.getroot()
            rlt1 = get_info(nodelist1)
            path = os.path.dirname(file_real_path.replace(folder_path, ""))
            name = filename.replace(".xml", "").replace("result_","")
            data = [(path, name, rlt1["pass"], rlt1["fail"], rlt1["block"], rlt1["not_run"], rlt1["pass_rate"])]
            insert_sql = "insert into %s values (?, ?, ?, ?, ?, ?, ?)" % table_name
            conn = get_conn(DATA_BASE_PATH)
            insert(conn, insert_sql, data)

def show_table_data(sql):
    conn = get_conn(DATA_BASE_PATH)
    show(conn, sql)

def count_cases(xml):
    name = os.path.basename(xml).replace(".xml", "").replace("result_","").replace("tct-","")
    if os.path.isfile(xml):
        tree1 = read_xml(xml)
        nodelist1 = tree1.getroot()
        rlt1 = get_info(nodelist1)
        print "%s %s %s %s %s %s%%" % (name,rlt1["sum"],rlt1["pass"],rlt1["fail"],rlt1["block"],int(round(rlt1["pass_rate"])))
    else:
        print 'wrong 1'

def main():
    global DATA_BASE_PATH 
    DATA_BASE_PATH = "/home/tizen/00_yunfei/temp/nightly.db"
    try:
        usage = "./stats.py -f ../../webapi/tct-2dtransforms-css3-tests/tests.full.xml"
        opts_parser = OptionParser(usage=usage)
        opts_parser.add_option(
            "--id",
            dest="caseid",
            help="specify the case id.")
        opts_parser.add_option(
            "--set",
            dest="caseset",
            help="specify the case set.")
        opts_parser.add_option(
            "-f",
            dest="xmlfile",
            help="specify the path of tests.full.xml file")
        opts_parser.add_option(
            "--f1",
            dest="xmlfile1",
            help="specify the path of tests.full.xml file1")
        opts_parser.add_option(
            "--f2",
            dest="xmlfile2",
            help="specify the path of tests.full.xml file2")
        opts_parser.add_option(
            "-o",
            dest="outfile",
            help="specify the path out file")
        opts_parser.add_option(
            "-c","--change",
            dest="changevalue",
            help="specify the value to change")
        opts_parser.add_option(
            "-d","--delete",
            dest="deletevalue",
            action="store_true",
            help="specify the node to delete")
        opts_parser.add_option(
            "--insert",
            dest="insert",
            action="store_true",
            help="specify the flag of insert table")
        opts_parser.add_option(
            "--show",
            dest="showsql",
            help="specify the flag of show table")
        opts_parser.add_option(
            "--count",
            dest="countxml",
            help="specify the flag of count case number")

        if len(sys.argv) == 1:
		    sys.argv.append("-h")
        (PARAMETERS, args) = opts_parser.parse_args()

        # count the result case number 
        if PARAMETERS.countxml:
            if os.path.isfile(PARAMETERS.countxml):
                count_cases(PARAMETERS.countxml)
            elif os.path.isdir(PARAMETERS.countxml):
                file_list = []
                for root, dirs, files in os.walk(PARAMETERS.countxml):
                    for filename in files:
                        if dirs == []:
                            file_list.append(os.path.join(root, filename))
                file_list.sort()
                for file_real_path in file_list:
                    count_cases(file_real_path)
            else:
                print "wront path for --count"
                sys.exit(1)
            sys.exit(1) 
        
        # insert into db
        if PARAMETERS.insert:
            insert_database_from_xml(PARAMETERS.xmlfile1)    
            insert_database_from_xml(PARAMETERS.xmlfile2)    
            sys.exit(1)
        if PARAMETERS.showsql is not None:
            show_table_data(PARAMETERS.showsql)
            sys.exit(1)
        if not PARAMETERS.xmlfile:
            print "xml file not defined, exit..."
            #sys.exit(1)

        tree = read_xml(PARAMETERS.xmlfile)
        nodelist = tree.getroot()
        #print PARAMETERS.xmlfile
        #print PARAMETERS.deletevalue
        #print PARAMETERS.caseset
        #print PARAMETERS.caseid
        #print PARAMETERS.changevalue
        #print PARAMETERS.xmlfile1
        #print PARAMETERS.xmlfile2
        print PARAMETERS.showsql
        #conn = get_conn(DATA_BASE_PATH)
        #cu = get_cursor(conn)
        if PARAMETERS.outfile:
            exe_time = datetime.today().strftime("%Y-%m-%d_%H_%M_%S")
            PARAMETERS.xmlfile = "/tmp/%s.%s.xml" % (PARAMETERS.outfile, exe_time)
        # delete by set name
        #if PARAMETERS.deletevalue and PARAMETERS.caseset:
        if PARAMETERS.deletevalue:
            delete_node_by_set_name(nodelist, PARAMETERS.caseset)
            write_xml(tree, PARAMETERS.xmlfile)
        # delete by case id
        if PARAMETERS.deletevalue and PARAMETERS.caseid:
            delete_node_by_case_id(nodelist, PARAMETERS.caseid)
            write_xml(tree, PARAMETERS.xmlfile)
        # change resule by set name
        if PARAMETERS.changevalue and PARAMETERS.caseset:
            change_result_by_set_name(nodelist, PARAMETERS.caseset, PARAMETERS.changevalue)
            write_xml(tree, PARAMETERS.xmlfile)
        # change resule by case id
        if PARAMETERS.changevalue and PARAMETERS.caseid:
            change_result_by_case_id(nodelist, PARAMETERS.caseid, PARAMETERS.changevalue)
            write_xml(tree, PARAMETERS.xmlfile)
       
        if not PARAMETERS.deletevalue and not PARAMETERS.changevalue \
            and PARAMETERS.xmlfile1 and PARAMETERS.xmlfile2:
            #print PARAMETERS.xmlfile1 
            #print PARAMETERS.xmlfile2 
            for file1 in glob.glob("%s/*.xml" % PARAMETERS.xmlfile1):
                filename1 = os.path.basename(file1)
                #print filename1
                for file2 in glob.glob("%s/%s" % (PARAMETERS.xmlfile2,filename1)):
                    tree1 = read_xml(file1)
                    nodelist1 = tree1.getroot()
                    rlt1 = get_info(nodelist1)
                    tree2 = read_xml(file2)
                    nodelist2 = tree2.getroot()
                    rlt2 = get_info(nodelist2)
                    if rlt1["pass_rate"] == rlt2["pass_rate"]:
                        pass
                        #print "the pass rate of %s is the same" % filename1
                    elif rlt1["pass_rate"] < rlt2["pass_rate"]:
                        print "\033[0;31m the pass rate of %s/\033[0;31;4;1m%s \033[0;31m down from %.f%% to %.f%%\033[0m" % (PARAMETERS.xmlfile1, filename1, rlt2["pass_rate"], rlt1["pass_rate"])
                    else:
                        print "\033[0;32m the pass rate of %s/\033[0;32;4;1m%s\033[0;32m up from %.f%% to %.f%%\033[0m" % (PARAMETERS.xmlfile1, filename1, rlt2["pass_rate"], rlt1["pass_rate"])
            sys.exit(1)
            for root, dirs, files in os.walk(PARAMETERS.xmlfile1):
                for filename in files:
                    if not filename.endswith(".xml"):
                        continue
                    #print os.path.join(root, filename)
                    for root2, dirs2, files2 in os.walk(PARAMETERS.xmlfile2):
                        for filename2 in files2:
                            #if os.path.join(root, filename).replace("11.40.276.0_201412310300","")== \
                            #    os.path.join(root2, filename2).replace("11.40.277.0_201501041331",""):
                            if os.path.join(root, filename).replace(os.path.basename(PARAMETERS.xmlfile1),"")== \
                                os.path.join(root2, filename2).replace(os.path.basename(PARAMETERS.xmlfile2),""):
                                print os.path.join(root2, filename2)
                                tree1 = read_xml(os.path.join(root, filename))
                                nodelist1 = tree1.getroot()
                                rlt1 = get_info(nodelist1)
                                tree2 = read_xml(os.path.join(root2, filename2))
                                nodelist2 = tree2.getroot()
                                rlt2 = get_info(nodelist2)
                                if rlt1["pass_rate"] == rlt2["pass_rate"]:
                                    print "the pass rate of %s is the same" % filename2
                                elif rlt1["pass_rate"] < rlt2["pass_rate"]:
                                    print "\033[0;32m the pass rate of %s/%s upper from %.f%% to %.f%%\033[0m" % (PARAMETERS.xmlfile2, filename2, rlt1["pass_rate"], rlt2["pass_rate"])
                                else:
                                    print "\033[0;31m the pass rate of %s/%s lower from %.f%% to %.f%%\033[0m" % (PARAMETERS.xmlfile2, filename2, rlt1["pass_rate"], rlt2["pass_rate"])
                    #for filename2 in iterfindfiles(PARAMETERS.xmlfile2, filename):
                    #    #filename2 = os.path.basename(filename2)
                    #    #print filename2
                    #    #print "%s/%s" % (PARAMETERS.xmlfile1, filename2)
                    #    #tree1 = read_xml("%s/%s" % (PARAMETERS.xmlfile1, filename2))
                    #    #nodelist1 = tree1.getroot()
                    #    #rlt1 = get_info(nodelist1)
                    #    #tree2 = read_xml("%s/%s" % (PARAMETERS.xmlfile2, filename2))
                    #    #nodelist2 = tree2.getroot()
                    #    #rlt2 = get_info(nodelist2)
                    #    print os.path.join(root, filename)
                    #    print filename2
                    #   # if rlt1["pass_rate"] == rlt2["pass_rate"]:
                    #   #     print "the pass rate of %s is the same" % filename2
                    #   # elif rlt1["pass_rate"] < rlt2["pass_rate"]:
                    #   #     print "\033[0;32m the pass rate of %s/%s upper from %.f%% to %.f%%\033[0m" % (PARAMETERS.xmlfile2, filename2, rlt1["pass_rate"], rlt2["pass_rate"])
                    #   # else:
                    #   #     print "\033[0;31m the pass rate of %s/%s lower from %.f%% to %.f%%\033[0m" % (PARAMETERS.xmlfile2, filename2, rlt1["pass_rate"], rlt2["pass_rate"])
                            
            #rlt = get_info(nodelist)
            #print "%.f%%" % rlt["pass_rate"]
            sys.exit(1)

        update_xml(PARAMETERS.xmlfile)
        print "---------------------"
        print "New xml file is %s"  % PARAMETERS.xmlfile

    except Exception as e:
        print "Got error: %s, exit" % e
        sys.exit(1)

if __name__ == '__main__':
	main()

