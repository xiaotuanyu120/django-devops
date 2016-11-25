#!/bin/bash

function stop(){
    pid=`ps aux|grep uwsgi|grep -v grep|awk '{print $2}'`
    kill -9 $pid;
}

function start(){
    cd /data/classmate;
    uwsgi uwsgi.ini
}

case $1 in
    stop)
        stop;
    ;;
    start)
        start;
    ;;
    restart)
        stop;
        start;
    ;;
esac
