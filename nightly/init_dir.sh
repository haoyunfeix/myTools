if [[ $# -ne 1 ]];then
    echo "The argument is not equal to 1, Please check..."
    exit 1
fi
DIRNAME=$1
mkdir -p $1/{cordova/{code,merge_xml,orig_xml/webdriver_xml,rerun_xml/webdriver_xml},wrt/{code,merge_xml,orig_xml/webdriver_xml,rerun_xml/webdriver_xml},webapi/{code,merge_xml,orig_xml/webdriver_xml,rerun_xml/webdriver_xml}}
