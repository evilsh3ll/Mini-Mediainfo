# Mini Mediainfo (mi)

A basic mediainfo wrapper with minimalistic output. A simple tool for DataHoarders, Muxers and Encoders, based on [pymediainfo](https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html) wrapper.

## Usage

```
usage: mi.py [-h] [-r] [-ef] [-af {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}] [-sf {vob,srt,sup,ass,vtt}] [-cf] [-cnf] [-pn] [-v] path

Print mediainfo output in a compact way

positional arguments:
  path                  The folder or file path

options:
  -h, --help            show this help message and exit
  -r, --recursive       Parse all foders recursively without depth limit
  -ef, --errors_filter  Show only files with errors in tags
  -af {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}, --audio_filter {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}
                        Show only files with specific audio
  -sf {vob,srt,sup,ass,vtt}, --subs_filter {vob,srt,sup,ass,vtt}
                        Show only files with specific subs
  -cf, --chapters_filter
                        Show only files with chapters
  -cnf, --not_chapters_filter
                        Show only files without chapters
  -pn, --printnames     Print only filenames
  -v, --verbose         Fallback to vanilla mediainfo output
```

## Screenshot

![screen](https://i.imgur.com/QdusOJ5.png)

## Installation

Copy `mi.py` inside `~/.local/bin` and you will be able to run it on any terminal by: `mi.py [parameters]`

**dependences**:

- mediainfo >= 22.0
- pymediainfo >= 5.1.0
- colorama >= 0.4.4

## Todo

- [x] Add a function to show only files with errors
- [x] Add a function to filter files for codec
- [ ] Add a function to filter files for specific problems
- [ ] Add a function to filter input file names
- [ ] Add a function to show track names in output
- [ ] Add a function to save output in a textfile (json/text)
- [x] Add a function to print the full mediainfo output (fallback)
- [ ] Fix output error when opening files (audio) not matching the video mediainfo output
- [x] Implement encoding info
- [ ] Make it multiplatform
