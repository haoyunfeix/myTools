filelist=`find $PWD -type f -name "*.html"`
for file in $filelist;do
    echo $file
    cat $file | while read line
    do
        echo $line
    done
done
