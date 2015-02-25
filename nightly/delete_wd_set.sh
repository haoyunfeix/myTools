#list=`grep 'type="ref"' -rn orig_xml/stub/*`
cp orig_xml/*.xml merge_xml/
cp rerun_xml/*.xml merge_xml/
#grep 'type="ref"' -rn orig_xml/*>1.tmp
grep -E 'type="ref"|type="script"' -rn orig_xml/*>1.tmp
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

