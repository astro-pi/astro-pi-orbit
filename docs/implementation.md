# Implementation

## ISS Coordinates

Behind the scenes, `astro_pi_orbit` downloads the necessary [Two-Line-Element](https://en.wikipedia.org/wiki/Two-line_element_set) files tracking the International Space Station from [https://celestrak.org/](https://celestrak.org/).

These are stored (cached) in a local directory for 3 days, after which an attempt is made to download a fresh file if the user is online.

The file storage location depends on the operating system: on Windows it is stored in `%LOCALAPPDATA%\astro_pi_orbit`, whereas on Unix operating systems such as macOS and Linux it is stored in `$XDG_STATE_HOME`, falling back to `~/.local/state/astro_pi_orbit`.
