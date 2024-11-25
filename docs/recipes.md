# Recipes

This page contains a few common recipes using the functions provided by `astro_pi_oribit`.

## Get the current coordinates of the ISS

```python
from astro_pi_orbit import ISS

iss = ISS()
print(ISS.coordinates())
```
## Take a photo and embed it with the current ISS coordinates

```python
from picamzero import Camera
from astro_pi_orbit import ISS

iss = ISS()
camera = Camera()

def take_photo(image_name):
    """
    Takes a photo and embeds the current coordinates of the ISS
    into the metadata.
    """
    point = iss.coordinates()
    coordinates = (point.latitude.signed_dms(), point.longitude.signed_dms())
    cam.take_photo(image_name, gps_coordinates=get_gps_coordinates(iss))

take_photo("tagged-img.jpg")
```

## Read the ISS trajectory from the latest two-line-element file

```python
from astro_pi_orbit import ISS
iss = ISS()
```

## Get the coordinate of the ISS at a specific time

```python
from astro_pi_orbit import ISS
from skyfield.api import load
iss = ISS()
ts = load.timescale()
coordinates = iss.at(ts.utc(2021, 12, 2, 14, 7))
print(coordinates)
```

## Get the position of a planet or the Earth

```python
from astro_pi_orbit import de421
earth = de421['earth']
mars = de421['Mars Barycenter']
print(earth, mars)
```
