source move.list
mkdir -p final_xml
cp stub_merge_xml/*.xml final_xml
for i in $list;do
    i=tct-$i
    i=`echo $i|sed 's/tct-webapi/webapi/g'`
    cp webdriver_all_xml/result_$i.xml final_xml
done
