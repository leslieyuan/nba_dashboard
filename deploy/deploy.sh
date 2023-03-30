#!/bin/bash

curdir=$(cd `dirname $0`; pwd)
echo "current work directory is ${curdir}"

# 1
cd ${curdir}
pip3 install -r requirements.txt
if [ $? -ne 0 ];then
    echo "install python libs error"
    exit -1
fi
echo "install python libs ok!"

# 2
cd ${curdir}
sh db_init.sh
if [ $? -ne 0 ];then
    echo "init db error"
    exit -1
fi
echo "init db ok!"

# 3
echo "start rank updater service..."
cd "${curdir}/../service"
nohup python3 rank_updater.py > ./rank_updater.log 2>&1 &
sleep 10

# 4
echo "start app..."
cd "${curdir}/.."
if [ "$1" == "debug" ] ;then
    python3 app.py
else
    nohup python3 app.py > ./web_app.log 2>&1 &
fi

echo "deploy success!"

