# Mini Mediainfo (mi)

A basic mediainfo wrapper with minimalistic output. A simple tool for DataHoarders, Muxers and Encoders, based on [pymediainfo](https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html) wrapper.

## Usage

```
usage: mi.py [-h] [-r] [-fn FILTER_NAME] [-fr {SD,HD,FHD,UHD}] [-fe] [-fm]
             [-fa {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}]
             [-fs {vob,srt,sup,ass,vtt}] [-fc] [-fnc] [-nc] [-pfn] [-pn] [-v]
             path

print mediainfo output in a compact way

positional arguments:
  path                  the folder or file path

options:
  -h, --help            show this help message and exit
  -r, --recursive       parse all foders recursively without depth limit
  -fn FILTER_NAME, --filter_name FILTER_NAME
                        show only files with specific name
  -fr {SD,HD,FHD,UHD}, --filter_resolution {SD,HD,FHD,UHD}
                        show only files with specific resolution
  -fe, --filter_errors  show only files with errors in tags
  -fm, --filter_missing_info
                        show only files with missing tags "?" or "-empty-"
  -fa {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}, --filter_audio {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}
                        show only files with specific audio
  -fs {vob,srt,sup,ass,vtt}, --filter_subs {vob,srt,sup,ass,vtt}
                        show only files with specific subs
  -fc, --filter_chapters
                        show only files with chapters
  -fnc, --filter_not_chapters
                        show only files without chapters
  -nc, --no_colors      show output without colors
  -pfn, --printfullnames
                        print only full filenames
  -pn, --printnames     print only filenames
  -v, --verbose         fallback to vanilla mediainfo output

```

## Screenshot

![screen](https://i.imgur.com/XAejBtu.png)

## Installation

Copy `mi.py` inside `~/.local/bin` and you will be able to run it on any terminal by: `mi.py [parameters]`

**dependences**:

- mediainfo >= 23.04
- pymediainfo >= 6.0.1
- colorama >= 0.4.6

## How to save output

`mi . --nc >> output.txt`
