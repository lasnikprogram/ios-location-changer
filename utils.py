import subprocess
import requests
import zipfile
import io
import os.path

url = 'https://github.com/mspvirajpatel/Xcode_Developer_Disk_Images/releases/download/XXX/XXX.zip'


def download_as_folder(url, version):
    response = requests.get(url.replace('XXX', version))
    if response.ok:
        zip = zipfile.ZipFile(io.BytesIO(response.content))
        zip.extractall('assets/developer_images')
        return True
    else:
        return False

def mount_developer_image(window):
    information = subprocess.run(['ideviceinfo'],
                                 capture_output=True, text=True)
    if 'Could not connect to lockdownd: Invalid HostID' in information.stderr:
        print('Your computer has to be a trusted device for your mobile device')
        window.quit()

    lines = information.stdout.split('\n')
    for line in lines:
        if line.startswith('ProductVersion:'):
            version = line.split(':')[1].strip()
    if version:
        version_trunc = '.'.join(version.split('.')[:2])
        version_path = f'assets/developer_images/{version_trunc}'
        if os.path.exists(version_path):
            mount_state = subprocess.run(['ideviceimagemounter', 
                            f'{version_path}/DeveloperDiskImage.dmg'],
                            capture_output=True, text=True)
            if 'Device is locked, can\'t mount. Unlock device and try again.' \
                in mount_state.stdout:
                print('Your mobile device has to be unlocked')
                window.quit()
        success = download_as_folder(url, version_trunc)
        if not success:
            print('Couldn\'t find appropiate developer disk image')
            window.quit()
