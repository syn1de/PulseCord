﻿﻿﻿<div align="center">
    

[![forthebadge](https://forthebadge.com/images/badges/fuck-it-ship-it.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

# 🚀 PulseCord: Uniting Communities with Vibrant Connections

PulseCord provides a suite of tools for managing media content on Discord channels, fostering vibrant connections and communities. It enables you to collect links from Discord channels, download media from these links, and upload media to Discord channels.

![PulseCord Preview](https://i.imgur.com/FCSp3Ip.png)

## 🛠️ Features

- **Collect Links from Discord Channel**: Gather links to media files (images, videos, etc.) from specified Discord channels and store them in text files.
- **Download Media from Links File**: Download media files from the links saved in text files.
- **Upload Media to Discord Channel**: Share media files from local directories to Discord channels.
- **Interactive Interface**: Enjoy an intuitive command-line interface for seamless execution of tasks.

## ⚙️ Prerequisites

- Python 3.x installed.
- Required Python libraries (`requests`, `tqdm`, `discord`).

## 📝 Installation

1. Clone or download the PulseCord repository.
2. Install the required Python libraries by running:
    ```bash
    pip install requests tqdm discord
    ```

## 🚦 Usage

1. **Collect Links from Discord Channel**:
    - Run the PulseCord script and choose option 1 from the menu.
    - Enter your Discord token and the channel ID to collect links.
    - Links will be saved to text files (`<channel_id>_links.txt`).

2. **Download Media from Links File**:
    - Prepare a text file containing links to media files.
    - Run PulseCord and choose option 2 from the menu.
    - Enter the path to the text file and the output folder for downloaded media.
    - Specify the maximum file size to download (in MB).
    - Media files will be downloaded to the specified folder.

3. **Upload Media to Discord Channel**:
    - Run PulseCord and choose option 3 from the menu.
    - Enter your Discord token.
    - Follow the on-screen instructions to select the channel and directory containing media files.
    - Media files will be uploaded to the chosen Discord channel.

4. **Exit**:
    - To exit PulseCord, choose option 4 from the menu.

## 📝 Author

PulseCord was crafted with ❤️‍ by Cyanide.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
