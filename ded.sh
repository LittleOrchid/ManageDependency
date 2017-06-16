#!/bin/bash

PROGDIR=`dirname $0`
PROGDIR=`cd $PROGDIR && pwd -P`

HOME_DIR=`cd ~ && pwd -P`
REMOTE_REPO="jcenter"
#0:No handle; 
#1: list all versions of the jar in local repository; 
#2: list all versoions of the jar in remote repository;
#3: download the specific jar from the remote reposity;
CONTROL_TYPE=0 
while getopts "hlrd" arg #选项后面的冒号表示该选项需要参数
do
        case "$arg" in
            h)
                echo "Usage: ded [-h] [-l] [-r] [-d] jar"
                echo "       -l : list all jars in local repositoy" 
                echo "       -r : list all jars in remote repository"
                echo "       -d : download jar from remote, and format likes group:artfact:version:classifer:extension into maven's local repository"
                echo "       -h : manpage"
                echo "       jar format is group:artifact:version[:classifer:extension]"
                exit 0
                ;;
            l)
                CONTROL_TYPE=1
                ;;
            r)
                CONTROL_TYPE=2
                ;;
            d) 
                CONTROL_TYPE=3
                ;;
            ?)  #当有不认识的选项的时候arg为?
                echo "Invalid arguments"
                exit 1
                ;;
        esac
done

#循环获取最后一个参数作为jar包的名称
while [[ $# > 0 ]]
do
    DOWNLOAD_JAR=$1
    shift
done
#正则判断最后一个参数是否符合jar包的格式
echo "$DOWNLOAD_JAR" | grep '^\([a-zA-Z0-9_\.\-]*:\)\{1,4\}[a-zA-Z0-9][a-zA-Z0-9_\.\-]*$' > /dev/null
if [[  $? != 0 ]] ; then
    echo "$DOWNLOAD_JAR is not a valid jar"
    exit 1
fi

list_local() #列举本地所有的jar包
{
    python $PROGDIR/py/route.py $PROGDIR local $DOWNLOAD_JAR
}

list_remote() #列举远程所有的jar包
{
    python $PROGDIR/py/remote_dependency.py $REMOTE_REPO $DOWNLOAD_JAR
}

download_remote() #下载需要的jar包到本地maven库
{
    python $PROGDIR/py/download_dependency.py $REMOTE_REPO $DOWNLOAD_JAR
}

case "$CONTROL_TYPE" in
    0)
        echo "Hei, no commond set. Now exit!"
        exit 1
        ;;
    1)
        list_local
        ;;
    2)
        list_remote
        ;;
    3) 
        download_remote 
        ;;
esac


