# Mini Mediainfo (mi)

A basic mediainfo wrapper with minimalistic output. A simple tool for DataHoarders, Muxers and Encoders, based on [pymediainfo](https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html) wrapper.

## Usage

```
usage: mi.py [-h] [-r] [-fn FILTER_NAME] [-fr {SD,HD,FHD,UHD}] [-fe]
             [-fa {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}]
             [-fs {vob,srt,sup,ass,vtt}] [-fc] [-fnc] [-pfn] [-pn] [-v]
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
  -fa {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}, --filter_audio {TrueHD,TrueHD-Atmos,DD,DDP,DDP-Atmos,DD-Atmos,DTS,DTS-ES,DTS-HD,DTS-MA,AAC}
                        show only files with specific audio
  -fs {vob,srt,sup,ass,vtt}, --filter_subs {vob,srt,sup,ass,vtt}
                        show only files with specific subs
  -fc, --filter_chapters
                        show only files with chapters
  -fnc, --filter_not_chapters
                        show only files without chapters
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

- mediainfo >= 22.0
- pymediainfo >= 5.1.0
- colorama >= 0.4.4

## Todo

- [x] Add a function to show only files with errors
- [x] Add a function to filter files for codec
- [ ] Add a function to filter files for specific problems
- [x] Add a function to filter input file names
- [x] Add a function to show only names in output
- [ ] Add a function to save output in a textfile (json/text)
- [x] Add a function to print the full mediainfo output (fallback)
- [x] Add mediainfo tracks numbers
- [ ] Fix output error when opening files (audio) not matching the video mediainfo output
- [ ] Fix audio missing when opening files (avi)
- [x] Implement encoding info
- [ ] Make it multiplatform
