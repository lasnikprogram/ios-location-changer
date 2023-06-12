from tkinter import Tk, Text, Canvas
import subprocess
from PIL import ImageTk, Image
import geotiler

window = Tk()
lon = 139.76209723465706
lat = 35.6769047216897

width, height = 512, 512

panel = Canvas(window, width=width, height=height)
panel.pack(expand=True)

def update_map():
    map = geotiler.Map(center=(lon, lat), zoom=19, size=(512, 512))
    image = geotiler.render_map(map)
    img = ImageTk.PhotoImage(image)
    panel.create_image(0, 0, image=img, anchor='nw')
    panel.image = img
    panel.create_oval(width / 2, height / 2, width / 2, height / 2, width=5)


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

    update_map()

    subprocess.run(['idevicesetlocation', str(lat), str(lon)])


def bind_keys(keys, direction):
    for key in keys:
        window.bind(key, lambda x: move(direction))


def init_window():
    bind_keys(['<Left>', 'a', 'h'], 'left')
    bind_keys(['<Right>', 'd', 'l'], 'right')
    bind_keys(['<Up>', 'w', 'k'], 'up')
    bind_keys(['<Down>', 's', 'j'], 'down')

    update_map()

    window.title('ios-location-changer')
    window.mainloop()


if __name__ == '__main__':
    init_window()
