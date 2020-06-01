if command -v python3 >/dev/null 2>&1
then 
echo "python3 installed"
else
sudo apt install python3 -y
fi

if command -v pip3 >/dev/null 2>&1
then
echo "pip installed"
else
sudo apt install python3-pip
fi

if command -v virtualenv >/dev/null 2>&1
then
echo "virtualenv installed"
else
python3 -m pip install virtualenv
fi

virtualenv env

./env/bin/python -m pip install -r requirments.txt