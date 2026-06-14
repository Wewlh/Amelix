# Amelix — Open-Source Personal System Assistant 🟢

Amelix is a lightweight, open-source personal system assistant built with Python. It allows you to monitor your computer's performance, capture screen media, and automate simple operating system tasks through a secure, private interface using discord.py.

This project is a developer portfolio demonstration showcasing asynchronous OS integration and automation.

---

## ⚠️ Disclaimer & Ethical Use Policy

**CRITICAL WARNING:** This software is designed strictly for remote administration and management of your own personal computer. You are strictly prohibited from installing or using this tool to monitor, spy on, or control anyone else's device without their explicit, legal consent. Unauthorized access or monitoring violates privacy laws and computing regulations. Use responsibly.

---

## ✨ Features

- 📊 System Statistics: Live reporting of CPU and RAM usage percentages.
- 🎮 Performance Check: Measure screen capture performance (FPS tracking).
- 🎥 Media Clipping: Record and compile short screen recordings into .mp4 video clips directly in your DMs.
- 🖼️ Wallpaper Management: Instantly update and customize your desktop background by attaching images.
- 📂 Process Overview: View active non-system user background applications.
- 🌐 Web Utility: Open specified URLs inside the default web browser.
- 💤 Power Management: Trigger native user-level power states (Sleep, Restart, Shutdown) without requiring Administrator privileges.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- A Discord Bot Token (with Message Content Intent enabled in the Discord Developer Portal)

### 1. Clone the Repository
  git clone [https://github.com/Wewlhh/Amelix.git](https://github.com/Wewlh/Amelix.git)
  cd Amelix

### 2. Install Dependencies
  pip install discord.py pyautogui psutil numpy pillow moviepy

### 3. Run the Assistant
  python amelix.py

*On the very first launch, the console will prompt you to enter your Bot Token and Owner Discord User ID. This configuration will be securely stored locally in a config.json file.*

---

## 🔒 Security Architecture

- Owner-Locked: The bot strictly ignores instructions from any user ID that does not match the configured Owner ID initialized during setup.
- DM Restricted: High-level OS control hooks are completely disabled in public servers and can only be executed within private Direct Messages (DMs).
- Non-Admin Safe: Designed to run entirely inside user-level scopes without needing "Run as Administrator" privileges.
