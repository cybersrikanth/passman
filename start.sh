#!/bin/bash
function mv_cred(){
    echo "checking"
    if [ -f "./credentials.json" ];
    then
        return 0
    elif [ -f "$HOME/Downloads/credentials.json" ];
    then
        mv ~/Downloads/credentials.json .
        return 0
    else
        echo "missing credentials.json file"
        return 1
    fi
}
cd ~/.passman-v2
if [ "$1" = "push" ];
then
    if mv_cred;
    then
        ./env/bin/python backup_man.py push
    fi
elif [ "$1" = "pull" ];
then
    if mv_cred;
    then
        ./env/bin/python backup_man.py pull
    fi
elif [ "$1" = "signout" ];
then
    rm token.pickle
else
    ./env/bin/python init.py
fi