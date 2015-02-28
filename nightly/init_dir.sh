if [[ $# -ne 1 ]];then
    echo "The argument is not equal to 1, Please check..."
    exit 1
fi
DIRNAME=$1

function init_sub_folder()
{
    cd $1
    ln -s ../../delete_wd_set.sh delete_wd_set.sh
    ln -s ../../merge.py merge.py
    ln -s ../../stats.py stats.py
    cd ..
}
mkdir -p $1/{cordova/{code,merge_xml,orig_xml/webdriver_xml,rerun_xml/webdriver_xml},wrt/{code,merge_xml,orig_xml/webdriver_xml,rerun_xml/webdriver_xml},webapi/{code,merge_xml,orig_xml/webdriver_xml,rerun_xml/webdriver_xml}}
cd $1
init_sub_folder cordova
init_sub_folder wrt
init_sub_folder webapi
