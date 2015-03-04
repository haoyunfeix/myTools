#list=`grep 'type="ref"' -rn orig_xml/stub/*`
cp orig_xml/*.xml merge_xml/
cp rerun_xml/*.xml merge_xml/
#grep 'type="ref"' -rn orig_xml/*>1.tmp
grep -E 'type="ref"|type="script"|ui-auto="bdd"' -rn orig_xml/*>1.tmp
while read i ;do
    file=`echo $i|awk -F : '{print $1}'`
    filename=`basename $file`
    echo $i
    setname=`echo $i|awk -F '"' '{print $2}'`
    ./stats.py -f merge_xml/$filename -d --set $setname
done < 1.tmp
cp rerun_xml/webdriver_xml/*.xml merge_xml/
./stats.py -f merge_xml/result_tct-extra-html5-tests.xml --id interfaces -c PASS
./stats.py -f merge_xml/result_tct-canvas-html5-tests.xml --id canvasgradient_addColorStop_INDEX_SIZE_ERR -c PASS
./stats.py -f merge_xml/result_tct-webstorage-w3c-tests.xml --id event_constructor -c PASS

mkdir -p wd_merge_xml
cp -a merge_xml/* wd_merge_xml
cp -a rerun_xml/webdriver_xml/*.xml wd_merge_xml/
list="result_tct-3dtransforms-css3-tests.xml
result_tct-audio-html5-tests.xml
result_tct-backgrounds-css3-tests.xml
result_tct-canvas-html5-tests.xml
result_tct-colors-css3-tests.xml
result_tct-csp-w3c-tests.xml
result_tct-extra-html5-tests.xml
result_tct-flexiblebox-css3-tests.xml
result_tct-fonts-css3-tests.xml
result_tct-multicolumn-css3-tests.xml
result_tct-svg-html5-tests.xml
result_tct-text-css3-tests.xml
result_tct-webstorage-w3c-tests.xml"
for i in $list;do
    ./merge.py --f1 wd_merge_xml/$i --f2 wd_merge_xml/wd_$i --f3 wd_merge_xml/$i
done
rm merge_xml/wd_*
rm wd_merge_xml/wd_*
