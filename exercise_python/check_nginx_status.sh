#! /bin/bash

Res1=$(systemctl status nginx | grep running | wc -l)

if [ $Res1 -eq 0 ];then
  systemctl restart nginx
  sleep 1
  Res2=$(systemctl status nginx | grep running | wc -l)
  if [ $Res2 -eq 0 ];then
    killall keepalived
    /home/user/dacent/stopall.sh
  fi
fi