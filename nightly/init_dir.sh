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
    ln -s ../../move.sh move.sh
    ln -s ../../diff.py diff.py
    ln -s ../../retest.py retest.py
    ln -s ../../../setup.sh code/setup.sh
    cd ..
}
mkdir -p $1/{cordova/{code,merge_xml,orig_xml/{stub_xml,webdriver_xml,webdriver_all_xml,other_xml},rerun_xml/{stub_xml,webdriver_xml,webdriver_all_xml,other_xml},stub_xml},wrt/{code,merge_xml,orig_xml/webdriver_xml,rerun_xml/{webdriver_xml,webdriver_all_xml}},webapi/{code,merge_xml,orig_xml/{stub_xml,webdriver_xml,webdriver_all_xml,other_xml},rerun_xml/{stub_xml,webdriver_xml,webdriver_all_xml,other_xml},stub_xml}}
cd $1
init_sub_folder cordova
init_sub_folder wrt
init_sub_folder webapi
