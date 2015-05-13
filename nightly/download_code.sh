#!/bin/sh

#/mnt/sync.sh
code_dir=/mnt/jiaxxx/master
orig_dir=$PWD
type=`basename $(dirname $orig_dir)`
version=`basename $(dirname $(dirname $orig_dir))`
echo $orig_dir
echo $type
echo $version

dl_common(){
local list="
embedding-api-android-tests
sampleapp-android-tests
tct
usecase-webapi-xwalk-tests
usecase-wrt-auto-tests
webapi-noneservice-tests
webapi-service
webapi-webspeech-w3c-tests
"
for i in $list;do
    cp -au $code_dir/$version/$1/$i*.zip .
done
}

if test ${version##*.} -ne 0;then
    code_dir=/mnt/jiaxxx/beta
fi
case "$type" in
    "webapi-sharemode" ) dl_common "testsuites-shared/x86" ;; 
    "webapi-x86" ) dl_common "testsuites-embedded/x86" ;; 
    "webapi-arm" ) dl_common "testsuites-embedded/arm" ;; 
    "cordova" ) dl_common "cordova4.0-embedded/arm" ;; 

esac

