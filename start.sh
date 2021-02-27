#! /bin/bash
kill $(pgrep "" -a | grep "main.py" | awk '{print $1}') ;
dir=/your/path/wx_notify
cd $dir && python3 main.py 22778

supervisorctl reload
