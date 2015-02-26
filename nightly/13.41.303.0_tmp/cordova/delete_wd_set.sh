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
