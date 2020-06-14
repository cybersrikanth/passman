# passman
Password Manager and Generator

~~~
Latest version is available in branch v2.0, Please switch branch to v2.0
~~~

### Created for Linux... If you are using windows, you may have to modify source code as this program based on FSH standards of Linux

This is a simple password genrator and manager built with python.
It handles multiple users and saves all credentials with name of the user in hidden folder.

Every data in file is encrypted with user's password(AES algorithm).
The password is salted with username and hashed using SHA256 algorithm.
The password is generated in complete random way (every password more than 4 char will have **"caps, small, numbers and special char"** in it)
It is offline, but you can simply copy your password file (**"/home/user/.passman/your_file"**) and transfer it to any computer and access with the **passman** program.

#### If you want to access this file just by entering command in terminal, Follow this steps.

- Install python 3.7 or later
- paste the **passman.py** file in your home directory
- open **.bashrc** file in your home folder with any text editor (nano, vim).
- append the following line in **.bashrc**
```python
alias passman='python ~/passman.py'
```
- Save the file and exit the terminal.
- Now you can just type **passman** in your terminal from any location to open the pasword manger.

### ThankYou.......
