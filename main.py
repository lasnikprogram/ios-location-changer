from tkinter import Tk, Text
import subprocess

window = Tk()
lat = 35.6769047216897
lon = 139.76209723465706


def move(direction):
    global lat, lon
    step_size = 0.0001

    if direction == 'left':
        lon -= step_size
    elif direction == 'right':
        lon += step_size
    elif direction == 'up':
        lat += step_size
    elif direction == 'down':
        lat -= step_size

    subprocess.run(['idevicesetlocation', str(lat), str(lon)])


def bind_keys(keys, direction):
    for key in keys:
        window.bind(key, lambda x: move(direction))


def init_window():
    bind_keys(['<Left>', 'a', 'h'], 'left')
    bind_keys(['<Right>', 'd', 'l'], 'right')
    bind_keys(['<Up>', 'w', 'k'], 'up')
    bind_keys(['<Down>', 's', 'j'], 'down')

    window.title('ios-location-changer')
    window.configure(bg='#856ff8')
    window.mainloop()


if __name__ == '__main__':
    init_window()
