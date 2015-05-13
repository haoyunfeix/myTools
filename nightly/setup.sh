#!/bin/bash

function print_error(){
    echo $1
    exit 1
}
status=`adb devices|wc -l`
if [[ $status -ne 3 ]];then
    print_error "No device found or there is more than one device"
fi
list=`ls *.zip`
for i in $list;do
    unzip -u $i
done
#if test -d opt/webapi-service-tests;then
#    cd opt/webapi-service-tests
#    ./inst.py -u;./inst.py
#    cd -
#else
#    print_error "opt/webapi-service-tests is not exist"
#fi
#
#if test -d opt/webapi-noneservice-tests;then
#    cd opt/webapi-noneservice-tests
#    ./inst.py -u;./inst.py
#    cp ../webapi-service-tests/*.xml .
#    cd -
#else
#    print_error "opt/webapi-noneservice-tests is not exist"
#fi
#
#if test -d webapi-service-docroot-tests;then
#    cd webapi-service-docroot-tests
#    ./inst.py -u;./inst.py
#    cd -
#else
#    print_error "opt/webapi-service-docroot-tests is not exist"
#fi

list=`find . -name "inst.py"`
for i in $list;do
    dir=`dirname $i`
    cd $dir
    ./inst.py -u
    ./inst.py
    cd -
done
cp opt/webapi-service-tests/*.xml opt/webapi-noneservice-tests

if test -f /opt/data.conf;then
    cp /opt/data.conf opt/webapi-noneservice-tests/ -a
fi
mkdir -p opt/webapi-noneservice-tests/data
dirList=`sudo find /opt/ -maxdepth 3 -name "data"`
for dir in $dirList;do
    cp -a $dir/* opt/webapi-noneservice-tests/data
done
echo "-------------------"
echo "setup successfully!"

