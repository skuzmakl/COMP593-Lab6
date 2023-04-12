"""
=================================================

 _____ ________  _________   _____  _____  _____ 
/  __ \  _  |  \/  || ___ \ |  ___||  _  ||____ |
| /  \/ | | | .  . || |_/ / |___ \ | |_| |    / /
| |   | | | | |\/| ||  __/      \ \\____ |    \ \
| \__/\ \_/ / |  | || |     /\__/ /.___/ /.___/ /
 \____/\___/\_|  |_/\_|     \____/ \____/ \____/ 
                                                 
=================================================

Assignment 6 - Exercise 1

Description:
 Gets and compares the SHA-256 hash value of VLC Player, and if safe downloads,
 silently installs and deletes the installer

Usage:
 python COMP593_A6E1.py
"""

import requests
import os

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256'
    resp_msg = requests.get(file_url)

    # Check whether the download was successful
    if resp_msg.ok:
        # Extract and split text file content from response message body
        expected_hash = resp_msg.text.split()[0]

    return expected_hash

def download_installer():
    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe'
    resp_msg = requests.get(file_url)

    # Check whether the download was successful
    if resp_msg.ok:
        # Extract binary file content from response message
        installer_data = resp_msg.content

    return installer_data

def installer_ok(installer_data, expected_sha256):
    import hashlib

    # Calculate and compare SHA-256 hash value
    download_hash = hashlib.sha256(installer_data).hexdigest()
    if download_hash == expected_sha256:
        return True
    
    return False

def save_installer(installer_data):
    installer_path = os.path.join(os.getenv('TEMP'), 'vlc-3.0.18-win64.exe')
    # Save the binary file to disk
    with open(installer_path, 'wb') as file:
        file.write(installer_data)

    return installer_path

def run_installer(installer_path):
    import subprocess

    # Silently runs the installer
    subprocess.run([installer_path, '/L=1033', '/S'])
    
def delete_installer(installer_path):
    # Deletes the installer
    os.remove(installer_path)

if __name__ == '__main__':
    main()