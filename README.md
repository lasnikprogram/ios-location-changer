# ios-location-changer
## compatibility
This program is only tested on Debain using IOS 15. But it should also work on other Linux distributions and IOS versions.  
Windows will be supported soon, get the libimobiledevice binaries from [here](https://github.com/libimobiledevice-win32/imobiledevice-net/releases/tag/v1.3.17)  
*Note for IOS 16: The program requires the activation of [IOS Developer Mode](https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device).*

## installation
Install `python3`, `git`, `python3-pip` and `python3-tk` with your favourite package manager (here: names for `apt`)  
Install missing python modules:
```bash
pip install Pillow geotiler
```
Download and run the program:  
With `git`:
```bash
git clone https://github.com/lasnikprogram/ios-location-changer && cd ios-location-changer
python3 main.py
```

Without `git`:
```bash
wget https://github.com/lasnikprogram/ios-location-changer/archive/main.tar.gz
tar xf main.tar.gz
rm main.tar.gz
mv ios-location-changer-main ios-location-changer
cd ios-location-changer
python3 main.py
```

## usage
Connect your IOS device, the program will automatically try to install and mount a developer disk image to change the location of the device to the marker present on the map.
- Move with `WASD`, `HJKL` or arrow keys
- Contol zoom with `+` and `-`
- resetting location (will change soon): run `idevicesetlocation reset`
- more controls coming soon, suggest them in [Issues](https://github.com/lasnikprogram/ios-location-changer/issues)

 ## map data
 Currently provided by https://www.openstreetmap.org
