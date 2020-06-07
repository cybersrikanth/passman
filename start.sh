if [ $1 = "push" ];
then
~/.passman-v2/env/bin/python backup_man.py push
elif [ $1 = "pull" ];
then
~/.passman-v2/env/bin/python backup_man.py pull
elif [ $1 = "signout" ];
then
rm token.pickle
else
~/.passman-v2/env/bin/python init.py
fi