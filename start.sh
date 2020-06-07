#!/bin/bash
cd ~/.passman-v2
if [ "$1" = "push" ];
then
./env/bin/python backup_man.py push
elif [ "$1" = "pull" ];
then
./env/bin/python backup_man.py pull
elif [ "$1" = "signout" ];
then
rm token.pickle
else
./env/bin/python init.py
fi