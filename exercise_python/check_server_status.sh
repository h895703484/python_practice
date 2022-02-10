#!/usr/bin/env bash

VIP="192.168.12.158"
IPs=(server1 server2 server3)

function check_con() {
    local count=0
    for ip in ${IPs[*]}
    do
        ping $ip -c 1 -W 1
        if [ $? -eq 0 ];then
            let count++
        fi
    done
    echo "$count"
}

function check_master() {
    local is_master=$(ip add|grep -s $VIP|wc -l)
    local master=true
    if [ $is_master -eq 0 ];then
        master=false
    fi
    echo "$master"
}

master=$(check_master)
count=$(check_con)
if [ $count -ge 2 -a $master ];then
    /home/user/dacent/startall.sh
else
    /home/user/dacent/startall.sh slave
fi

while true
do
    master_change=$(check_master)
    count_change=$(check_con)
    if [ $master -ne $master_change ];then
        let master=$master_change
        if [ $master -a $count_change -ge 2 ];then
            /home/user/dacent/startall.sh other
        else
            /home/user/dacent/startall.sh stop other
        fi
    else
        if [ $count_change -lt 2 ];then
            pm2 kill
        fi
    fi
    sleep 1
done