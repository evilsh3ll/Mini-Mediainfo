# Mini Mediainfo (mi)

A basic mediainfo wrapper with minimalistic output. A simple tool for muxers and encoders, based on [pymediainfo](https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html) wrapper.

## Usage

```
usage: mi.py [-h] [-r] [-e] [-pn] path

Print mediainfo output in a compact way

positional arguments:
path The folder or file path

options:
-h, --help show this help message and exit
-r, --recursive Parse all foders recursively without depth limit
-e, --errors Show only files with errors in tags
-pn, --printnames Print only filenames
```

## Screenshot

![screen](https://i.postimg.cc/0QbgKHSn/image.png)

## Installation

Copy `mi.py` inside `~/.local/bin` and you will be able to run it on any terminal by: `mi.py [parameters]`

**dependences**:

- mediainfo >= 22.0
- pymediainfo >= 5.1.0
- colorama >= 0.4.4

## Todo

- [x] Add a function to show only files with errors
- [ ] Add a function to filter files with specific problems
- [ ] Add a function to save output in a textfile (json/text)
- [ ] Add a function to print the full mediainfo output (fallback)
- [ ] Add a debug mode
- [ ] Make it multiplatform

## Status

Beta

## License

GNU GPLv3

```

```
