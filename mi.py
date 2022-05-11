#!/usr/bin/python
import os
import json
import argparse
from pymediainfo import MediaInfo # https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html
from colorama import Fore,Back,Style

def get_files(path):
    ext = ('.mkv','.mp4','.avi')
    all_files = []
    all_folders = []
    for curr_file in os.listdir(path):
        if curr_file.endswith(ext):
            all_files.append(curr_file)
        if os.path.isdir(path+curr_file):
            all_folders.append(curr_file)
    return all_files,all_folders

def convert_b2_to_b10(size_b2):
    if("KiB" in size_b2): return str(round(float(size_b2.replace("KiB",""))*(1.024),1)) + "KB"
    if("MiB" in size_b2): return str(round(float(size_b2.replace("MiB",""))*(1.048576),1)) + "MB"
    if("GiB" in size_b2): return str(round(float(size_b2.replace("GiB",""))*(1.073741824),1)) + "GB"

def minimize_channels(channels):
    if channels == "C":                         return "1.0"
    if channels == "Lt Rt":                     return "2.0"
    if channels == "L R":                       return "2.0"
    if channels == "L R LFE":                   return "2.1"
    if channels == "L R C":                     return "3.0"
    if channels == "C R L":                     return "3.0"
    if channels == "C L R":                     return "3.0"
    if channels == "L R Cb":                    return "3.0"
    if channels == "L R C LFE":                 return "3.1"
    if channels == "C L R LFE":                 return "3.1"
    if channels == "L R Lb Rb":                 return "4.0"
    if channels == "L R Ls Rs":                 return "4.0"
    if channels == "C L R Cb":                  return "4.0"
    if channels == "L R C Cb":                  return "4.0"
    if channels == "L R C LFE Cb":              return "4.1"
    if channels == "L R C Ls Rs":               return "5.0"
    if channels == "C L R Ls Rs":               return "5.0"
    if channels == "L R C LFE Lb Rb":           return "5.1"
    if channels == "L R C LFE Ls Rs":           return "5.1"
    if channels == "C L R Ls Rs LFE":           return "5.1"
    if channels == "C L R Ls Rs Cb":            return "6.0"
    if channels == "C L R Lb Rb Cb":            return "6.0"
    if channels == "L R C Ls Rs Cb":            return "6.0"
    if channels == "L R C Lb Rb Cb":            return "6.0"
    if channels == "C L R Ls Rs Cb LFE":        return "6.1"
    if channels == "C L R Lb Rb Cb LFE":        return "6.1"
    if channels == "L R C Ls Rs Cb LFE":        return "6.1"
    if channels == "L R C Lb Rb Cb LFE":        return "6.1"
    if channels == "L R C LFE Ls Rs Lb Rb":     return "7.1"
    if channels == "C L R LFE Lb Rb Lss Rss":   return "7.1"
    if channels == "C L R Ls Rs Lw Rw LFE":     return "7.1"
    if channels == "C L R LFE Ls Rs Lw Rw":     return "7.1"
    return channels

def minimize_a_codec(codec):
    if codec == "Dolby TrueHD":                         return "TrueHD"
    if codec == "Dolby TrueHD with Dolby Atmos":        return "TrueHD-Atmos"
    if codec == "Dolby Digital":                        return "DD"
    if codec == "Dolby Digital Plus":                   return "DDP"
    if codec == "Dolby Digital Plus with Dolby Atmos":  return "DDP-Atmos"
    if codec == "Dolby Digital with Dolby Atmos":       return "DD-Atmos"
    if codec == "DTS-ES Discrete":                      return "DTS-ES"
    if codec == "DTS-ES Matrix":                        return "DTS-ES"
    if codec == "DTS-HD High Resolution Audio":         return "DTS-HD"
    if codec == "DTS-HD Master Audio":                  return "DTS-MA"
    if codec == "HE-AAC":                               return "AAC"
    return codec

def minimize_s_codec(codec):
    if codec == "S_VOBSUB":         return "vob"
    if codec == "S_TEXT/UTF8":      return "srt"
    if codec == "S_HDMV/PGS":       return "sup"
    if codec == "S_TEXT/ASS":       return "ass"
    if codec == "S_TEXT/WEBVTT":    return "vtt"
    return codec

def get_data(path,media_info):
    parsed_file = {
        "Path" : "?",
        "File" : "?",
        "Size" : "?",
        "Video" : {},
        "Audio" : [],
        "Subs" : [],
        "Chapters" : False
    }
    audio_list = []
    subtitles_list = []
    for curr_track in media_info["media"]["track"]:

        # General Parsing
        if curr_track["@type"] == "General":
            parsed_file["Size"] = convert_b2_to_b10(curr_track["FileSize_String"].replace(" ",""))
            parsed_file["Path"] = path
            parsed_file["File"] = curr_track["FileNameExtension"]
            continue
            
        # Video parsing
        if curr_track["@type"] == "Video":
            v_resolution = v_aspectratio = v_duration = v_fps = v_originalfps = v_bitrate = v_encode_method = v_encode_param = v_codec = v_size = "?"
            
            if("Width" in curr_track and "Height" in curr_track): v_resolution = curr_track["Width"]+"x"+curr_track["Height"]
            if("DisplayAspectRatio_String" in curr_track): v_aspectratio = curr_track["DisplayAspectRatio_String"]
            if("Duration_String" in curr_track): v_duration = curr_track["Duration_String"].replace("min","m").replace(" ","")
            if("FrameRate" in curr_track): v_fps = curr_track["FrameRate"].replace(".000","")
            if("FrameRate_Original" in curr_track): v_originalfps = curr_track["FrameRate_Original"].replace(".000","")
            if("BitRate_String" in curr_track): v_bitrate = curr_track["BitRate_String"].replace(" ","")
            if("Encoded_Library_Settings" in curr_track):
                for field in curr_track["Encoded_Library_Settings"].split(" / "):
                    if(("rc=" in field) and (v_encode_method=="?")): v_encode_method=field.split("rc=")[1].strip()
                    if(("crf=" in field) and (v_encode_param=="?")): v_encode_param=field.split("crf=")[1].strip()
                    if(("bitrate=" in field) and (v_encode_param=="?")): v_encode_param=field.split("bitrate=")[1].strip()
            if("/" in v_encode_param): v_encode_param = v_encode_param.split("/")[0] # clean ZONED crf
            if("InternetMediaType" in curr_track): v_codec = curr_track["InternetMediaType"].replace("video/","")
            if("StreamSize_String3" in curr_track): v_size = convert_b2_to_b10(curr_track["StreamSize_String3"].replace(" ",""))

            parsed_file["Video"] = {
                "Resolution" : v_resolution,
                "AspectRatio" : v_aspectratio,
                "Duration" : v_duration,
                "FPS" : v_fps,
                "OriginalFPS" : v_originalfps,
                "Bitrate" : v_bitrate,
                "EncodeMethod" : v_encode_method,
                "EncodeParameter" : v_encode_param,
                "Codec" : v_codec,
                "Size" : v_size
            }
            continue

        # Audio parsing
        if curr_track["@type"] == "Audio":
            a_lang = a_codec = a_channels = a_bitrate = a_size = "?"

            if("Language_String3" in curr_track): a_lang = curr_track["Language_String3"].capitalize()
            if("Format_Commercial" in curr_track): a_codec = minimize_a_codec(curr_track["Format_Commercial"])
            if("ChannelLayout" in curr_track): a_channels = minimize_channels(curr_track["ChannelLayout"])
            if("BitRate_String" in curr_track): a_bitrate = curr_track["BitRate_String"].replace(" ","")
            if("StreamSize_String3" in curr_track): a_size = convert_b2_to_b10(curr_track["StreamSize_String3"].replace(" ",""))

            curr_audio_dict = {
                "Language" : a_lang,
                "Codec" : a_codec,
                "Channels" : a_channels,
                "Bitrate" : a_bitrate,
                "Size" : a_size
            }
            
            audio_list.append(curr_audio_dict)
            continue
  
        # Subtitle parsing
        if curr_track["@type"] == "Text":
            s_lang = s_codec = s_forced = "?"

            if("Language_String3" in curr_track): s_lang = curr_track["Language_String3"].capitalize()
            if("CodecID" in curr_track): s_codec = minimize_s_codec(curr_track["CodecID"])
            if("Forced" in curr_track): 
                if curr_track["Forced"] == "Yes" : s_forced = True
                else: s_forced = False
            
            curr_sub_dict = {
                "Language" : s_lang,
                "Codec" : s_codec,
                "Forced" : s_forced
            }

            subtitles_list.append(curr_sub_dict)
            continue

        # Chapters Parsing
        if curr_track["@type"] == "Menu":
            parsed_file["Chapters"] = True
            continue

    parsed_file["Audio"] = audio_list
    parsed_file["Subs"] = subtitles_list

    return parsed_file

def print_mediainfo_dict(file_dict,errors_filter,printnames_flag,audio_filter):
    output_f = output_v = output_s = ""
    output_a = {}
    # file name
    output_f = Fore.GREEN + "-> "+ file_dict["File"] + " ["+ file_dict["Size"] + "]"+ Fore.RESET

    # check: print only names
    if (printnames_flag == True): 
            print(output_f)
            return

    # video info
    output_v = file_dict["Video"]["Resolution"]+" "+file_dict["Video"]["Duration"]

    if file_dict["Video"]["OriginalFPS"]!="?": output_v += " "+file_dict["Video"]["OriginalFPS"]+"->"+file_dict["Video"]["FPS"]+"fps"
    else: output_v += " "+file_dict["Video"]["FPS"]+"fps"

    if file_dict["Video"]["Bitrate"]!="?": output_v += " "+file_dict["Video"]["Bitrate"]
    else: output_v += Fore.RED+" bitrate=?"+Fore.RESET

    if file_dict["Video"]["EncodeMethod"]!="?": output_v += " "+file_dict["Video"]["EncodeMethod"]+"="+file_dict["Video"]["EncodeParameter"]
    else: output_v += Fore.RED+" encode_method=?"+Fore.RESET

    if file_dict["Chapters"]==True: output_v += " Chapters"

    output_v += " "+file_dict["Video"]["Codec"]+Style.DIM+" [" + file_dict["Video"]["Size"] +"]"+Style.RESET_ALL

    # audio info
    for curr_audio in file_dict["Audio"]:
        if curr_audio["Language"] not in output_a:
            output_a[curr_audio["Language"]] = curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
        else:
            output_a[curr_audio["Language"]] += ", "+curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL

    # subs info
    for curr_sub in file_dict["Subs"]:
        if curr_sub["Language"]=="?": # sub with error in language
            if curr_sub["Forced"]==True: 
                if output_s=="": output_s += Style.BRIGHT + Fore.RED +"[F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET + Style.RESET_ALL
                else: output_s += Style.BRIGHT + Fore.RED +", [F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET + Style.RESET_ALL
            else:
                if output_s=="": output_s +=  Fore.RED + curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET
                else: output_s += ", " + Fore.RED + curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET
            continue
            
        # sub without errors
        if curr_sub["Forced"]==True: 
            if output_s=="": output_s += Style.BRIGHT+"[F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL
            else: output_s += Style.BRIGHT+", [F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL
        else:
            if output_s=="": output_s += curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"
            else: output_s += ", "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"
    

    # FILTERS
    if( errors_filter and ( ("?" not in output_v) and ("?" not in output_a.values()) and ("?" not in output_s) ) ): return # error mode: jump file if it has errors
    if( audio_filter!=None and (not any(curr_audio_dict["Codec"] == audio_filter for curr_audio_dict in file_dict["Audio"] )) ): return # audio filter mode: jump file if it has the audio string

    # PRINT
    # FILE OUTPUT
    print(output_f)
    # VIDEO OUTPUT
    print(Fore.CYAN+"Video: "+Fore.RESET + output_v)
    # AUDIO OUTPUT
    if output_a == {}:
        print(Fore.CYAN+"Audio: Empty"+Fore.RESET)
    else:
        for key_lang in output_a:
            if key_lang=="?": print(Fore.RED+"Audio " + key_lang + ": "+Fore.RESET + output_a[key_lang])
            else: print(Fore.CYAN+"Audio " + key_lang + ": "+Fore.RESET + output_a[key_lang])
    # SUBS OUTPUT
    if output_s == "": print(Fore.CYAN+"Subs: Empty"+Fore.RESET)
    else: print(Fore.CYAN+"Subs: "+Fore.RESET + output_s)
    print("")

def parse_all_files(path,errors_filter,printnames_flag,recursive_flag,audio_filter):
    if path[-1] != "/": path = path + "/" #fix path
    files,folders = get_files(path) #load files and folders
    files = sorted(files, key=str.lower) #sort files list
    folders = sorted(folders, key=str.lower) #sort folders list

    for curr_file in files:
        # Parse info
        media_info_output = json.loads(MediaInfo.parse(path+curr_file,output="JSON"))
        file_dict = get_data(os.path.abspath(path+curr_file),media_info_output)
        print_mediainfo_dict(file_dict,errors_filter,printnames_flag,audio_filter)

    if(recursive_flag):
        for curr_folder in folders:
            print("")
            print(Fore.MAGENTA + path + curr_folder +"/" + Fore.RESET)
            parse_all_files(path+curr_folder,errors_filter,printnames_flag,recursive_flag,audio_filter)

def main():
    # Commandline input
    parser = argparse.ArgumentParser(description='Print mediainfo output in a compact way')
    parser.add_argument('path', type=str, nargs=1, help='The folder or file path')
    parser.add_argument('-r', '--recursive', help='Parse all foders recursively without depth limit', action='store_true')
    parser.add_argument('-ef', '--errors_filter', help='Show only files with errors in tags', action='store_true')
    parser.add_argument('-af', '--audio_filter', type=str, help='Show only files with specific audio', choices=['TrueHD','TrueHD-Atmos','DD','DDP','DDP-Atmos','DD-Atmos','DTS','DTS-ES','DTS-HD','DTS-MA','AAC'])
    parser.add_argument('-pn', '--printnames', help='Print only filenames', action='store_true')
    args = parser.parse_args()

    # Variable migration
    path = os.path.abspath(args.path[0])
    errors_filter = args.errors_filter
    audio_filter= args.audio_filter
    printnames_flag = args.printnames
    recursive_flag = args.recursive
    
    # Load file/s & print info
    if os.path.isdir(path):     # -------- DIRECTORY --------
        parse_all_files(path,errors_filter,printnames_flag,recursive_flag,audio_filter)
            
    else:                       # -------- SINGLE FILE --------
        # check errors
        if(errors_filter or audio_filter):
            print("ERR: Can't filter a single file")
            return

        # Parse info
        media_info_output = json.loads(MediaInfo.parse(path,output="JSON"))
        file_dict = get_data(os.path.abspath(path),media_info_output)
        print_mediainfo_dict(file_dict,False,printnames_flag,None)


if __name__ == "__main__":
    main()