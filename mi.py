import os
import json
import argparse
from pymediainfo import MediaInfo # https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html
from colorama import Fore,Back,Style

def load_files(my_dir):
    ext = ('.mkv','.mp4')
    all_files = []
    for curr_file in os.listdir(my_dir):
        if curr_file.endswith(ext):
            all_files.append(curr_file)
        else:
            continue
    return all_files

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

def get_data(media_info):
    parsed_file = {
        "Path" : "?",
        "File" : "?",
        "Size" : 0,
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
            parsed_file["Size"] = curr_track["FileSize_String"].replace("GiB","Gb").replace("MiB","Mb").replace("KiB","Kb").replace(" ","")
            parsed_file["Path"] = curr_track["FolderName"]
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
                    if "rc=" in field: v_encode_method=field.split("rc=")[1].strip()
                    if "crf=" in field: v_encode_param=field.split("crf=")[1].strip().replace("000","")
                    if "bitrate=" in field: v_encode_param=field.split("bitrate=")[1].strip().replace("000","")
            if("InternetMediaType" in curr_track): v_codec = curr_track["InternetMediaType"].replace("video/","")
            if("StreamSize_String3" in curr_track): v_size = curr_track["StreamSize_String3"].replace("GiB","Gb").replace("MiB","Mb").replace("KiB","Kb").replace(" ","")

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
            if("StreamSize_String3" in curr_track): a_size = curr_track["StreamSize_String3"].replace("GiB","Gb").replace("MiB","Mb").replace("KiB","Kb").replace(" ","")

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

def print_mediainfo_dict(file_dict):
    output_f = output_v = output_s = ""
    output_a = {}
    # file name
    output_f = Fore.GREEN + "-> "+ file_dict["File"] + " ["+ file_dict["Size"] + "Gb]"+ Fore.RESET

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
        if curr_sub["Forced"]==True: 
            if output_s=="": output_s += Style.BRIGHT+"[F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL
            else: output_s += Style.BRIGHT+", [F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL
        else:
            if output_s=="": output_s += curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"
            else: output_s += ", "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"
    
    # print all
    print("") #formatting line
    print(output_f)
    print(Fore.CYAN+"Video: "+Fore.RESET + output_v)
    for key_lang in output_a:
        print(Fore.CYAN+"Audio " + key_lang + ": "+Fore.RESET + output_a[key_lang])
    print(Fore.CYAN+"Subs: "+Fore.RESET + output_s)

def main():
    # Commandline input
    parser = argparse.ArgumentParser(description='Print mediainfo output in a compact way')
    parser.add_argument('path', type=str, nargs=1, help='The folder or file path')

    args = parser.parse_args()

    # Variable migration
    path = args.path[0]

    # Load file/s & print info
    if os.path.isdir(path):     # -------- DIRECTORY --------
        if path[-1] != "/": path = path + "/" #fix path
        files = sorted(load_files(path), key=str.lower) #load file list

        for curr_file in files:
            # Parse info
            media_info_output = json.loads(MediaInfo.parse(path+curr_file,output="JSON"))
            file_dict = get_data(media_info_output)
            print_mediainfo_dict(file_dict)
            
    else:                       # -------- SINGLE FILE --------
            # Parse info
            media_info_output = json.loads(MediaInfo.parse(path,output="JSON"))
            file_dict = get_data(media_info_output)
            print_mediainfo_dict(file_dict)


if __name__ == "__main__":
    main()