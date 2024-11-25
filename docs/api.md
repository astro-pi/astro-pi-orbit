# API

## How to read API docs
API docs or "Application Programming Interface Documentation" is a fancy name for a list of all the things a piece of software can do, and how to use them.

The docs list all of the **methods** and **attributes** available in `astro_pi_orbit`.

You will see a block of code like this:

```python
coordinates() -> str
```

This tells you:

 - there is a function called `coordinates`
 - the function has no arguments (blank parentheses)
 - the type the function returns (`-> str`)

You may also see a block of code like this:
```python
de421: skyfield.jpllib.SpiceKernel
```

This tells you:
 - there is an attribute called `de421` that is of type `skyfield.pkllib.SpiceKernel`.


## API docs

The `astro_pi_orbit` library exports four names: `ISS`, `de421`, `de440s`, and `ephemeries`.

### ISS

A function that returns a `Skyfield` `EarthSatellite` object with an additional `coordinates` method, produced by reading the latest [two-line element set](https://en.wikipedia.org/wiki/Two-line_element_set) file available on the operating system.

More information on the `Skyfield` objects returned and used can be found [here](https://rhodesmill.org/skyfield/earth-satellites.html) and [here](https://rhodesmill.org/skyfield/api-satellites.html).


```python
ISS() -> skyfield.sgp4lib.EarthSatellite
```

##### Example

The code below reads the latest TLE data into the `iss` variable, and prints the `iss` variable to the console:
```python
from astro_pi_orbit import ISS
iss = ISS()
print(iss)
```

When executed, this code outputs the following:
```txt
<EarthSatellite ISS (ZARYA) catalog #25544 epoch 2024-03-12 05:03:40 UTC>
```

#### coordinates

- Gets the current coordinates of the ISS.
- **Returns** a `skyfield.toposlib.GeographicPosition`.
```python
coordinates() -> <class 'skyfield.toposlib.GeographicPosition'>
```

##### Example

This function can be used to geotag photos using `picamzero`.

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

This will take a photo called `tagged-img.jpg`, and embed the ISS
coordinates into the image metadata.

---

### de421

- Access the standard `de421.bsp` ephemeris file data via the `skyfield.jpllib.SpiceKernel` interface. For more information on how this is used, see [here](https://rhodesmill.org/skyfield/planets.html)

```python
de421: skyfield.jpllib.SpiceKernel
```

##### Example

This code gets the current position of Mars and prints it to the console:
```python
from astro_pi_orbit import de421
from skyfield.api import load

ts = load.timescale()
print(de421['Mars Barycenter'].at(ts.now()))
```

---

### de440s
- Access the standard `de440s.bsp` ephemeris file data via the `skyfield.jpllib.SpiceKernel` interface. For more information on how this is used, see [here](https://rhodesmill.org/skyfield/planets.html)

##### Example

This code gets the current position of Earth and prints it to the console:

```python
from astro_pi_orbit import de440s
from skyfield.api import load

ts = load.timescale()
print(de421['earth'].at(ts.now()))
```

---

### ephemeris

A synonym for the `de421` attribute described above.
