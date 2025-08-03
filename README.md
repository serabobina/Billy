<p align="center">
  <img width="798" height="504" alt="Billy" src="https://github.com/serabobina/Billy/blob/main/data/logo.png"/>
</p>

# Billy
**Billy** — Remote Access Trojan (RAT) management tool with Telegram bot integration. Supports Linux and Windows.

> ⚠️ **Legal Disclaimer**
> This project is intended **only for authorized penetration testing and educational purposes**. Unauthorized use is illegal. The author is not responsible for misuse.

---

## 📌 Features
- **Cross-platform**: Control victims on Linux and Windows.
- **Telegram Bot**: Manage access remotely via Telegram.
- **Multiple Vectors**: Deploy via Rubber Ducky (Bad USB) or Installer.
- **Modules**:
  - 📸 Camera/Screen Capture
  - 🎤 Microphone Recording
  - 📁 File System Access
  - 🌐 Network/WiFi Data Extraction
  - ⚡ Admin Command Execution

[▶️ Full Capabilities Table](#supported-functions)

---

## 🛠️ Installation
### Linux
```bash
sudo apt install portaudio19-dev python3-tk python3-dev
pip install -r requirements-linux.txt
```

### Windows
```bash
pip install -r requirements-windows.txt
```

---

## 🚀 Quick Start
1. Run the tool:
   ```bash
   python Billy.py
   ```
2. **Add a Branch**: Select `Add branch` to generate:
   - 🦆 Rubber Ducky payload script
   - 📥 Installer download link
3. Deploy the payload to the target device.

---

## 📋 Menu Modes
| Mode                        | Description                                 |
|-----------------------------|---------------------------------------------|
| **Get branches**            | List all Yandex Drive branches.             |
| **Add branch**              | Create a new branch (victim session).       |
| **Delete branch**           | Remove a branch.                            |
| **Edit OAuth-token**        | Update Yandex Drive API token.              |
| **Manage branch**           | Edit bot token for the branch, add comment. |
| **Change compile commands** | Customize build commands for payloads.      |
| **About**                   | Get author and version.                     |

---

## 📸 Screenshots
| **Main Menu** | **Branch Management** |
|--------------|----------------------|
| <img width="481" height="356" alt="Menu" src="https://github.com/serabobina/Billy/blob/main/data/screenshot1.png"/> | <img width="481" height="356" alt="Branches" src="https://github.com/serabobina/Billy/blob/main/data/screenshot3.png"/> |

---

## 🔧 Technical Details
### Supported Functions
| Module | Linux  | Windows |
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

### Antivirus
This program may be detected by antiviruses as malware.
**Use at your own risk!**

- The program does not have a digital signature.
- Antiviruses (for example, Windows Defender, Avast, Kaspersky) may block it.
- To work, you may need to add to exceptions or disable the antivirus.

### Branches Policy  
- **One device = One branch**  
- Each branch contains a **unique RAT build** with device-specific configurations.  
- Do **not** mix targets in a single branch.  

### Common Errors
| Error                          | Solution                                  |
|--------------------------------|------------------------------------------|
| `PyInstaller not found`        | Change compile commands to `python -m PyInstaller ...` or install PyInstaller globally. |

---

## 📜 To-Do
- [ ] Add CLI argument support
- [ ] Expand Linux keylogging

---

## 📜 License
Educational use only. No warranties provided.

---

## ☕ Support  
Like this project? Buy me a *digital coffee* via Bitcoin or USDT: 
- BTC: 1AM59VRvaoz429UQqVe6TWrDgbTguGuPSL
- USDT: TCUZPyod5WB2pvQu5b1Zxd5uVc4473J8qH

---

## 🙏 Credits
- **Author**: [serabobina](https://github.com/serabobina)
- **Dependencies**: [Yandex Drive API](https://disk.yandex.ru/), [Colorama](https://pypi.org/project/colorama/), [PyInstaller](https://www.pyinstaller.org/)