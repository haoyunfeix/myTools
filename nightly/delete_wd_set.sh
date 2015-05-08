#########create stub_xml webdriver_xml stub_merge_xml
cp orig_xml/stub_xml/*.xml stub_xml/
cp rerun_xml/stub_xml/*.xml stub_xml/
#grep 'type="ref"' -rn orig_xml/*>1.tmp
grep -E 'ui-auto="wd"|ui-auto="bdd"' -rn orig_xml/stub_xml/*>1.tmp
while read i ;do
    file=`echo $i|awk -F : '{print $1}'`
    filename=`basename $file`
    echo $i
    setname=`echo $i|awk -F '"' '{print $2}'`
    ./stats.py -f stub_xml/$filename -d --set $setname
done < 1.tmp
mkdir -p webdriver_xml
rm webdriver_xml/*.xml
cp orig_xml/webdriver_xml/*.xml webdriver_xml/
cp orig_xml/webdriver_all_xml/*.xml webdriver_xml/
cd webdriver_xml
rename 's//wd_/' *.xml
cd -
cp rerun_xml/webdriver_xml/*.xml webdriver_xml/
#./stats.py -f merge_xml/result_tct-extra-html5-tests.xml --id interfaces -c PASS
#./stats.py -f merge_xml/result_tct-canvas-html5-tests.xml --id canvasgradient_addColorStop_INDEX_SIZE_ERR -c PASS
#./stats.py -f merge_xml/result_tct-webstorage-w3c-tests.xml --id event_constructor -c PASS

mkdir -p stub_merge_xml
cp -a stub_xml/*.xml stub_merge_xml
cp -a webdriver_xml/*.xml stub_merge_xml/
#list="result_tct-3dtransforms-css3-tests.xml
#result_tct-audio-html5-tests.xml
#result_tct-backgrounds-css3-tests.xml
#result_tct-canvas-html5-tests.xml
#result_tct-colors-css3-tests.xml
#result_tct-csp-w3c-tests.xml
#result_tct-extra-html5-tests.xml
#result_tct-flexiblebox-css3-tests.xml
#result_tct-fonts-css3-tests.xml
#result_tct-multicolumn-css3-tests.xml
#result_tct-sandbox-html5-tests.xml
#result_tct-svg-html5-tests.xml
#result_tct-text-css3-tests.xml
#result_tct-ui-css3-tests.xml
#result_tct-webstorage-w3c-tests.xml"
list=`grep -E 'ui-auto="wd"|ui-auto="bdd"' -rl orig_xml/stub_xml/*`
for i in $list;do
    i=`basename $i`
    if test -f stub_merge_xml/wd_$i;then
        ./merge.py --f1 stub_merge_xml/$i --f2 stub_merge_xml/wd_$i --f3 stub_merge_xml/$i
    fi
done
rm stub_merge_xml/wd_*

############# create webdriver_all_xml
mkdir -p webdriver_all_xml
cp orig_xml/webdriver_all_xml/*.xml webdriver_all_xml
cp rerun_xml/webdriver_all_xml/*.xml webdriver_all_xml
#./stats.py -f wd_merge_xml/result_tct-extra-html5-tests.xml --id interfaces -c PASS
#./stats.py -f wd_merge_xml/result_tct-canvas-html5-tests.xml --id canvasgradient_addColorStop_INDEX_SIZE_ERR -c PASS
#./stats.py -f wd_merge_xml/result_tct-webstorage-w3c-tests.xml --id event_constructor -c PASS
mkdir -p other_xml
cp orig_xml/other_xml/*.xml other_xml
cp rerun_xml/other_xml/*.xml other_xml
