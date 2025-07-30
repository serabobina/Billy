<p align="center">
  <img width="798" height="504" alt="Billy" src="https://github.com/serabobina/Billy/main/data/logo.png"/>
</p>

# Billy
**Billy** - Software for using the remote access trojan Billy. Billy supports Linux and Windows OS. You can control Billy with Telegram bot!


> ⚠️ **Attention!**  
> The project is developed only for legal pentesting and the author is not responsible for illegal use.


## Content
- [Installation](#installation)
- [Usage](#usage)
- [Getting started](#getting-started)
- [Modes](#modes)
- [Structure](#structure)
- [Screenshots](#screenshots)
- [To do](#to-do)
- [Thanks](#thanks)
- [Sources](#sources)


## Installation
### Linux
```
sudo apt install portaudio19-dev python3-tk python3-dev
pip install -r requirements-linux.txt
```
### Windows
```
pip install -r requirements-windows.txt
```


## Usage
Run Billy.py with python:
```
python Billy.py
```


## Getting started
When you run Billy.py, a menu with commands will open.
1) Get branches
2) Add branch
3) Delete branch
4) Edit OAuth-token
5) Manage branch
6) Change compile commands
7) Exit

For the first action, you need to add the first branch. Select the second mode.
After creating the first branch, you will get the Rubber Ducky script and the URL for the Installer file.
Now you can install the Billy remote access trojan to the victim's computer using Bad USB (Rubber Ducky script) or the Installer.


## Modes
### Get branches
 - This mode allows you to get a list of the branches on your Yandex drive.
### Add branch
 - This mode allows you to add new branch.
### Delete branch
 - This mode allows you to delete branch.
### Edit OAuth-token
 - This mode allows you to edit Yandex OAuth token in session.
### Change compile commands
 - This mode allows you to replace compile commands. The commands should compile the Installer and Billy into the dist/ directory in the project root. Linux: dist/Billy and dist/Installer, Windows: dist/Billy.exe and dist/Installer.exe.


## Structure
The project consists of tool for managing the branch system and the remote access trojan "Billy".


## Screenshots
### Menu
<img width="481" height="356" alt="Billy2" src="https://github.com/serabobina/Billy/main/data/screenshot1.png" />

### Admin
<img width="364" height="195" alt="Billy3" src="https://github.com/serabobina/Billy/main/data/screenshot2.png" />


## Functions of the remote access trojan Billy
|  | Linux  | Windows |
| ------------- | ------------- | ------------- |
| Admin | ✅ | ✅ |
| Camera | ✅ | ✅ |
| Network | ✅ | ✅ |
| Keyboard | ❌ | ✅ |
| WIFI | ⚠️ | ✅ |
| Mouse | ❌ | ✅ |
| Microphone | ✅ | ✅ |
| Screen | ✅ | ✅ |
| Browser | ✅ | ✅ |
| File | ✅ | ✅ |
| Photo | ✅ | ✅ |
| Command | ✅ | ✅ |
| About | ✅ | ✅ |


## Compiling errors
| Error | Cause | Solution |
|----------------------|----------------------------------|-----------------------------|
| Command not found: "PyInstaller" | PyInstaller is not installed globally | Install PyInstaller globaly or edit compile command with absolute path to PyInstaller(python -m PyInstaller ) |


## To do
- [x] Add a README
- [ ] Add support for command line arguments


## Thanks
- serabobina — author


## Sources
- [Yandex drive](https://disk.yandex.ru/)
- [Colorama](https://super-devops.readthedocs.io/en/latest/misc.html)
- [Art](https://pypi.org/project/art/)
- [Readme sample](https://gist.github.com/bzvyagintsev/0c4adf4403d4261808d75f9576c814c2)