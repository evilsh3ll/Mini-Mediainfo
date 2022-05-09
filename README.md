# Mini Mediainfo (mi)

A basic mediainfo wrapper with minimalistic output. A simple tool for muxers and encoders, based on [pymediainfo](https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html) wrapper.

## Usage

`mi.py --help` show help message

`mi.py -e <file/folder>` show only files with errors in tags

`mi.py -e -pn <file/folder>` show only the name of files with errors in tags

`mi.py <file/folder>` print output for a single file or all files in the folder

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
