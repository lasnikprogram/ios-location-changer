from tkinter import Tk, Canvas
import subprocess
from PIL import ImageTk, Image
import geotiler
from cache import Cache
from geotiler.cache import caching_downloader
from geotiler.tile.io import fetch_tiles
from functools import partial
from multiprocessing.pool import ThreadPool
import sys

window = Tk()
lat = 35.6769047216897
lon = 139.76209723465706

cache = Cache('cache.db')

downloader = partial(caching_downloader, cache.get, cache.set, fetch_tiles)

lat_center = lat
lon_center = lon

width, height, zoom = 512, 512, 15

canvas = Canvas(window, width=width, height=height)
canvas.pack(expand=True)

boundaries = []

marker = ImageTk.PhotoImage(file='assets/marker.png')
marker_id = None

pool = ThreadPool(processes=1)

def move_marker(n_x, n_y):
    x, y, *_ = canvas.bbox(marker_id)
    canvas.move(marker_id, n_x - x - marker.width() / 2, \
                n_y - y - marker.height())

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

    move_marker(width * (lon - boundaries[0]) / lon_diff,
             height * (lat - boundaries[3]) / lat_diff)

def update_map():
    global boundaries, marker_id

    map = geotiler.Map(center=(lon_center, lat_center), zoom=zoom, \
                       size=(width, height), provider='osm')
    image = geotiler.render_map(map, downloader=downloader)
    img = ImageTk.PhotoImage(image)
    canvas.image = img
    canvas.create_image(0, 0, image=canvas.image, anchor='nw')

    marker_id = canvas.create_image(0, 0, image=marker)

    boundaries = map.extent

def zoom_by(amount):
    global zoom
    if zoom + amount < 19 and zoom + amount > 3:
        zoom += amount
    update()

def update():
    update_map()
    draw_location()

def run_command():
    response = subprocess.run(['idevicesetlocation', str(lat), str(lon)],
                              capture_output=True, text=True)

    if 'Make sure a developer disk image is mounted!' in response.stdout:
        #TODO: automatically mount image
        pass
    elif 'No device found!' in response.stdout:
        print('Please attach a device via USB cable')
        window.quit()

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

    async_result = pool.apply_async(run_command)

    draw_location()

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

    update()

    async_result = pool.apply_async(run_command)

    window.title('ios-location-changer')
    window.mainloop()

if __name__ == '__main__':
    init_window()
