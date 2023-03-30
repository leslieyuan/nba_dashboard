#!/bin/bash

db_path=$(cd `dirname $0`; pwd)

cd "${db_path}/../service"
sqlite3 ./rank.db "drop table if exists t_nba_rank;"
sqlite3 ./rank.db "create table if not exists t_nba_rank(rank integer, team varchar(50) primary key, win integer, loss integer, east_west integer);"
if [ $? -ne 0 ]; then
    echo "create table failed"
    exit -1
fi
exit 0
