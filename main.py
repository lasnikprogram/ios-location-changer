from tkinter import Tk, Text, Canvas
import subprocess
from PIL import ImageTk, Image
import geotiler
import redis
import functools
from geotiler.cache import redis_downloader

window = Tk()
lat = 35.6769047216897
lon = 139.76209723465706

client = redis.Redis('localhost')
downloader = redis_downloader(client)

lat_center = lat
lon_center = lon

width, height, zoom = 512, 512, 17

panel = Canvas(window, width=width, height=height)
panel.pack(expand=True)

boundaries = []

def draw_dot(x, y):
    panel.create_oval(x, y, x, y, width=5, outline='red')

def draw_location():
    global lon_center, lat_center
    lon_diff = boundaries[2] - boundaries[0]
    lat_diff = boundaries[1] - boundaries[3]
    if lon < boundaries[0]:
        lon_center = boundaries[0] - lon_diff / 2
        update()
    if lon > boundaries[2]:
        lon_center = boundaries[2] + lon_diff / 2
        update()
    if lat < boundaries[1]:
        lat_center = boundaries[1] + lat_diff / 2
        update()
    if lat > boundaries[3]:
        lat_center = boundaries[3] - lat_diff / 2
        update()

    panel.create_image(0, 0, image=panel.image, anchor='nw')
    draw_dot(width * (lon - boundaries[0]) / lon_diff,
             height * (lat - boundaries[3]) / lat_diff)

def update_map():
    global boundaries
    render_map = functools.partial(geotiler.render_map, downloader=downloader)

    map = geotiler.Map(center=(lon_center, lat_center), zoom=zoom, \
                       size=(width, height), provider='stamen-toner')
    image = render_map(map)
    img = ImageTk.PhotoImage(image)
    panel.image = img
    boundaries = map.extent

def zoom_by(amount):
    global zoom
    if zoom + amount < 19 and zoom + amount > 6:
        zoom += amount 
    update_map()
    draw_location()

def update():
    update_map()
    draw_location()


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

    draw_location()

    subprocess.run(['idevicesetlocation', str(lat), str(lon)])


def bind_keys(keys, direction):
    for key in keys:
        window.bind(key, lambda x: move(direction))


def init_window():
    bind_keys(['<Left>', 'a', 'h'], 'left')
    bind_keys(['<Right>', 'd', 'l'], 'right')
    bind_keys(['<Up>', 'w', 'k'], 'up')
    bind_keys(['<Down>', 's', 'j'], 'down')

    window.bind('+', lambda x: zoom_by(+1))
    window.bind('-', lambda x: zoom_by(-1))

    update_map()
    draw_location()

    window.title('ios-location-changer')
    window.mainloop()


if __name__ == '__main__':
    init_window()
