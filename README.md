# passman
Password Manager and Generator [v-2.0]

# Installation

Note: If you installed older version of passman please remove them. This version of passman will work perfectly in any gnome based terminal.

### Requirements
* Python3.7
* Python3 pip
* virtual environment [virtualenv] (recomended but not necessary)
* Google drive ( you can ignore this if you dont want cloud backup)
* git (sudo apt install git)
* wget (sudo apt install wget)

### Setup Google drive for backup
* [click here](https://developers.google.com/drive/api/v3/quickstart/python) and enable google drive api by clicking `Enable the drive api` button.
* Signin with the google account where you want to store the backup.
* Choose `desktop app` as your OAuth client and click create button.
* Download the client configuration. (make sure the name of the file is `credentials.json` inside Downloads folder).

### automatic installation

[![Passman V-2.0](https://raw.githubusercontent.com/cybersrikanth/passman/v2.0/Screenshot%20from%202020-06-28%2014-18-28.png)](https://www.youtube.com/watch?v=RqumJNVxE2Q "Passman V-2.0")

~~~~ 
wget -O - https://raw.githubusercontent.com/cybersrikanth/passman/v2.0/one_line_install.sh | bash
~~~~
* copy and paste the above line in your terminal. (enter password if prompted)
* After installation completed type `passman` in your terminal and start using it.
* To activate gdrive backup type `passman push`. For the first time it will ask permission via browser. Allow it to save backup.

### Backup & Restore
* use `passman push` to backup localcopy to cloud.
* use `passman pull` to restore backup.

Note: 
if you use password for backup, You will need to provide them while restoring it. If you entered wrong password wile restoring, it willnot warn you, It will simply creash your database. Please be careful.
Use `passman push` after everytime when you update credentials. and `passman pull` before you login each time, to keep your password uptodate and prevent dataloss.

### manual installation
* If you are facing any trouble with automaitc installation, you can try manual installation.
* Make sure Requirements are satisfied.
* open terminal and type the following commands
~~~~
git clone --single-branch --branch v2.0 https://github.com/cybersrikanth/passman.git
mv passman ~/.passman-v2
cd ~/.passman-v2
bash install.sh
~~~~
