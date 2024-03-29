#!/usr/bin/python
import os
import json
import argparse
import re
from pymediainfo import MediaInfo # https://pymediainfo.readthedocs.io/en/stable/pymediainfo.html
from colorama import Fore,Back,Style

def clear_colors(my_string):
    return re.sub(r'\033\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]?', '', my_string)

def get_files(path):
    all_files = []
    all_folders = []
    for curr_file in os.listdir(path):
        if os.path.isfile(path+curr_file): 
            all_files.append(curr_file)
        if os.path.isdir(path+curr_file):
            all_folders.append(curr_file)
    return all_files,all_folders

def convert_b2_to_b10(size_b2):
    if("Byte0" in size_b2): return "0B"
    if("Bytes" in size_b2): return str(size_b2.replace("Bytes","")) + "B"
    if("KiB" in size_b2): return str(round(float(size_b2.replace("KiB",""))*(1.024),1)) + "kB"
    if("MiB" in size_b2): return str(round(float(size_b2.replace("MiB",""))*(1.048576),1)) + "MB"
    if("GiB" in size_b2): return str(round(float(size_b2.replace("GiB",""))*(1.073741824),1)) + "GB"
    return size_b2

def minimize_channels(channels):
    lfe = int("LFE" in channels)
    ch_value = str(len(channels.split(" ")) - lfe)+"."+str(lfe)
    return ch_value

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
    if codec == "mp4s-E0":          return "vob"
    if codec == "S_TEXT/UTF8":      return "srt"
    if codec == "S_HDMV/PGS":       return "sup"
    if codec == "S_TEXT/ASS":       return "ass"
    if codec == "S_TEXT/WEBVTT":    return "vtt"
    return codec

def get_resolution(h):
    if(int(h)>=0 and int(h)<=576):         return "SD"
    elif(int(h)>576 and int(h)<=720):      return "HD"
    elif(int(h)>720 and int(h)<=1080):     return "FHD"
    elif(int(h)>1080 and int(h)<=2160):    return "UHD"
    else:                                  return ">UHD"

def get_data(path,media_info):
    parsed_file = {
        "FullPath" : "?",
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
            parsed_file["FullPath"] = path
            parsed_file["File"] = curr_track["FileNameExtension"]
            continue
            
        # Video parsing
        if curr_track["@type"] == "Video":
            v_id = v_resolution = v_aspectratio = v_duration = v_fps = v_originalfps = v_profile = v_bitrate = v_encode_lib = v_codec = v_size = "?"    # general video
            v_rc_type = v_rc_value = v_ref = v_subme = v_me = v_merange = v_trellis = v_deblock = v_bframes = v_zones = "?"       # encoding params

            if("ID" in curr_track): v_id = curr_track["ID"]
            if("Width" in curr_track and "Height" in curr_track): v_resolution = curr_track["Width"]+"x"+curr_track["Height"]
            if("DisplayAspectRatio_String" in curr_track): v_aspectratio = curr_track["DisplayAspectRatio_String"]
            if("Duration_String" in curr_track): v_duration = curr_track["Duration_String"].replace("min","m").replace(" ","")
            if("FrameRate" in curr_track): v_fps = curr_track["FrameRate"].replace(".000","")
            if("FrameRate_Original" in curr_track): v_originalfps = curr_track["FrameRate_Original"].replace(".000","")
            if("Format_Profile" in curr_track and "Format_Level" in curr_track): 
                if(curr_track["Format_Level"]=="Main" or curr_track["Format_Level"]=="High"): v_profile = curr_track["Format_Profile"]
                else: v_profile = curr_track["Format_Profile"] + "@L" + curr_track["Format_Level"]
            if("BitRate_String" in curr_track): v_bitrate = curr_track["BitRate_String"].replace(" ","")
            if("Encoded_Library_Version"in curr_track): v_encode_lib = curr_track["Encoded_Library_Version"]
            if("Encoded_Library_Settings" in curr_track):
                for field in curr_track["Encoded_Library_Settings"].split(" / "):
                    if("ref=" in field          and v_ref=="?"):            v_ref = field.split("ref=")[1].strip()
                    if("subme=" in field        and v_subme=="?"):          v_subme = field.split("subme=")[1].strip()
                    if("me=" in field           and v_me=="?"):             v_me = field.split("me=")[1].strip()
                    if("me_range=" in field     and v_merange=="?"):        v_merange = field.split("me_range=")[1].strip()
                    if("trellis=" in field      and v_trellis=="?"):        v_trellis = field.split("trellis=")[1].strip()
                    if("deblock=" in field      and v_deblock=="?"):
                        if(len(field.split("deblock=")[1].split(":"))>2):   v_deblock = field.replace("deblock=0:","").replace("deblock=1:","").strip()
                        else:                                               v_deblock = field.split("deblock=")[1].strip()
                    if("bframes=" in field      and v_bframes=="?"):        v_bframes = field.split("bframes=")[1].strip()
                    if("bitrate=" in field      and v_rc_value=="?"):       v_rc_value=field.split("bitrate=")[1].strip()
                    if("zones=" in field        and v_zones=="?"):          v_zones="zoned"
                    if("rc=" in field           and v_rc_type=="?"): 
                        if "." or "," in field.split("rc=")[1].strip():
                            v_rc_type=field.split("rc=")[1].strip().strip("0").strip(".").strip(",")
                        else: 
                            v_rc_type=field.split("rc=")[1].strip()
                    if("crf=" in field and v_rc_value=="?"): 
                        if "." or "," in field.split("crf=")[1].strip():
                            v_rc_value=field.split("crf=")[1].strip().strip("0").strip(".").strip(",")
                        else:
                            v_rc_type=field.split("rc=")[1].strip()
            if("/" in v_rc_value): v_rc_value = v_rc_value.split("/")[0] # clean ZONED crf
            if("InternetMediaType" in curr_track): v_codec = curr_track["InternetMediaType"].replace("video/","").replace("MP4V-ES","XviD")
            if("StreamSize_String3" in curr_track): v_size = convert_b2_to_b10(curr_track["StreamSize_String3"].replace(" ",""))

            parsed_file["Video"] = {
                "ID": v_id,
                "Resolution" : v_resolution,
                "AspectRatio" : v_aspectratio,
                "Duration" : v_duration,
                "FPS" : v_fps,
                "OriginalFPS" : v_originalfps,
                "Profile" : v_profile,
                "Bitrate" : v_bitrate,
                "ENC_lib" : v_encode_lib,
                "ENC_rc_type" : v_rc_type,
                "ENC_rc_value" : v_rc_value,
                "ENC_ref" : v_ref,
                "ENC_subme" : v_subme,
                "ENC_me" : v_me,
                "ENC_merange" : v_merange,
                "ENC_trellis" : v_trellis,
                "ENC_deblock" : v_deblock,
                "ENC_bframes" : v_bframes,
                "ENC_zones": v_zones,
                "Codec" : v_codec,
                "Size" : v_size
            }
            continue

        # Audio parsing
        if curr_track["@type"] == "Audio":
            a_id = a_lang = a_codec = a_channels = a_bitrate = a_size = a_default = "?"

            if("ID" in curr_track): a_id = curr_track["ID"]
            if("Language_String3" in curr_track): a_lang = curr_track["Language_String3"].upper()
            if("Format_Commercial" in curr_track): a_codec = minimize_a_codec(curr_track["Format_Commercial"])
            if("ChannelLayout" in curr_track): a_channels = minimize_channels(curr_track["ChannelLayout"])
            if("ChannelLayout_Original" in curr_track): a_channels = minimize_channels(curr_track["ChannelLayout_Original"])
            if("BitRate_String" in curr_track): a_bitrate = curr_track["BitRate_String"].replace(" ","")
            if("Default" in curr_track):
                if curr_track["Default"] == "Yes" : a_default = True
                elif curr_track["Default"] == "No" : a_default = False
            if("StreamSize_String3" in curr_track): a_size = convert_b2_to_b10(curr_track["StreamSize_String3"].replace(" ",""))

            curr_audio_dict = {
                "ID": a_id,
                "Language" : a_lang,
                "Codec" : a_codec,
                "Channels" : a_channels,
                "Bitrate" : a_bitrate,
                "Default" : a_default,
                "Size" : a_size
            }
            
            audio_list.append(curr_audio_dict)
            continue
  
        # Subtitle parsing
        if curr_track["@type"] == "Text":
            s_id = s_lang = s_codec = s_forced = s_size = s_default = "?"

            if("ID" in curr_track): s_id = curr_track["ID"]
            if("Language_String3" in curr_track): s_lang = curr_track["Language_String3"].upper()
            if("CodecID" in curr_track): s_codec = minimize_s_codec(curr_track["CodecID"])
            if("Default" in curr_track):
                if curr_track["Default"] == "Yes" : s_default = True
                elif curr_track["Default"] == "No" : s_default = False
            if("Forced" in curr_track): 
                if curr_track["Forced"] == "Yes" : s_forced = True
                else: s_forced = False
            if("StreamSize_String1" in curr_track):
                s_size = convert_b2_to_b10(curr_track["StreamSize_String1"].replace(" ",""))

            curr_sub_dict = {
                "ID": s_id,
                "Language" : s_lang,
                "Codec" : s_codec,
                "Default" : s_default,
                "Forced" : s_forced,
                "Size" : s_size
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

def print_mediainfo_dict(media_info_output,file_dict,filter_errors,filter_name,filter_resolution,printfullnames_flag,printnames_flag,filter_audio,filter_subs,filter_chapters,filter_not_chapters,print_mediainfo_dict,no_colors_flag,filter_missing_info):
    output_f = output_e = output_v = output_s = ""
    output_a = {}

    
    # file name
    output_f = Fore.GREEN + "-> "+ file_dict["File"] + " ["+ file_dict["Size"] + "]"+ Fore.RESET

    # video info
    if(len(file_dict["Video"])!=0):
        output_v = Fore.YELLOW+ file_dict["Video"]["ID"] + Fore.RESET+" "+file_dict["Video"]["Resolution"]+" "+get_resolution(file_dict["Video"]["Resolution"].split("x")[1])+" "+file_dict["Video"]["Duration"]

        if file_dict["Video"]["OriginalFPS"]!="?": output_v += " "+file_dict["Video"]["OriginalFPS"]+"->"+file_dict["Video"]["FPS"]+"fps"
        else: output_v += " "+file_dict["Video"]["FPS"]+"fps"

        if file_dict["Video"]["Profile"]!="?": output_v += " "+file_dict["Video"]["Profile"]
        else: output_v += Fore.RED+" profile=?"+Fore.RESET

        if file_dict["Video"]["Bitrate"]!="?": output_v += " "+file_dict["Video"]["Bitrate"]
        else: output_v += Fore.RED+" bitrate=?"+Fore.RESET

        if file_dict["Chapters"]==True: output_v += " Chaps"

        output_v += " "+file_dict["Video"]["Codec"]+Style.DIM+" [" + file_dict["Video"]["Size"] +"]"+Style.RESET_ALL


        # encoding info
        #if file_dict["Video"]["ENC_lib"]!="?": output_e += Style.DIM + file_dict["Video"]["ENC_lib"] + Style.RESET_ALL
        #else: output_e += Fore.RED+" enc_library=?"+Fore.RESET

        if file_dict["Video"]["ENC_rc_type"]!="?": output_e += file_dict["Video"]["ENC_rc_type"]+"="+file_dict["Video"]["ENC_rc_value"]
        else: output_e += Fore.RED+"encode_method=?"+Fore.RESET

        if file_dict["Video"]["ENC_deblock"]!="?": output_e += " "+ "deblock="+file_dict["Video"]["ENC_deblock"]
        else: output_e += Fore.RED+" deblock=?"+Fore.RESET
        
        if file_dict["Video"]["ENC_ref"]!="?": output_e += " "+"ref="+file_dict["Video"]["ENC_ref"]
        else: output_e += Fore.RED+" ref=?"+Fore.RESET

        if file_dict["Video"]["ENC_me"]!="?": output_e += " "+ "me="+file_dict["Video"]["ENC_me"]
        else: output_e += Fore.RED+" me=?"+Fore.RESET

        if file_dict["Video"]["ENC_merange"]!="?": output_e += " "+"merange="+file_dict["Video"]["ENC_merange"]
        else: output_e += Fore.RED+" merange=?"+Fore.RESET

        if file_dict["Video"]["ENC_subme"]!="?": output_e += " "+ "subme="+file_dict["Video"]["ENC_subme"]
        else: output_e += Fore.RED+" subme=?"+Fore.RESET

        if file_dict["Video"]["ENC_trellis"]!="?": output_e += " "+"trellis="+file_dict["Video"]["ENC_trellis"]
        else: output_e += Fore.RED+" trellis=?"+Fore.RESET

        if file_dict["Video"]["ENC_bframes"]!="?": output_e += " "+"bframes="+file_dict["Video"]["ENC_bframes"]
        else: output_e += Fore.RED+" bframes=?"+Fore.RESET

        if file_dict["Video"]["ENC_zones"]!="?": output_e += " "+ "ZONED"


    # audio info
    for curr_audio in file_dict["Audio"]:
        if "?" in curr_audio["Language"]: # audio with errors
            if curr_audio["Language"] not in output_a:
                if curr_audio["Default"]==True:
                    output_a[curr_audio["Language"]] = Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ Style.BRIGHT + Fore.RED + curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+ curr_audio["Bitrate"]+ Style.RESET_ALL +Fore.RESET+Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
                else:
                    output_a[curr_audio["Language"]] = Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ Fore.RED + curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+ Fore.RESET +Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
            else:
                if curr_audio["Default"]==True:
                    output_a[curr_audio["Language"]] += ", " +Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ Style.BRIGHT + Fore.RED + curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+ Style.RESET_ALL+ Fore.RESET + Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
                else:
                    output_a[curr_audio["Language"]] += ", "+Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ Fore.RED + curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+  Fore.RESET + Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
        else:                           # audio without errors
            if curr_audio["Language"] not in output_a:
                if curr_audio["Default"]==True:
                    output_a[curr_audio["Language"]] = Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ Style.BRIGHT + curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+ curr_audio["Bitrate"]+ Style.RESET_ALL +Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
                else:
                    output_a[curr_audio["Language"]] = Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
            else:
                if curr_audio["Default"]==True:
                    output_a[curr_audio["Language"]] += ", " +Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ Style.BRIGHT + curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+ Style.RESET_ALL +Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL
                else:
                    output_a[curr_audio["Language"]] += ", "+Fore.YELLOW+ curr_audio["ID"] + Fore.RESET + " "+ curr_audio["Language"] + " " + curr_audio["Codec"]+" "+curr_audio["Channels"]+" "+curr_audio["Bitrate"]+Style.DIM+" ["+curr_audio["Size"]+"]"+Style.RESET_ALL


    # subs info
    for curr_sub in file_dict["Subs"]:
        if curr_sub["Language"]=="?": # sub with error in language
            if curr_sub["Forced"]==True:
                if curr_sub["Default"]==True: 
                    if output_s=="": output_s += Fore.YELLOW+ curr_sub["ID"] + Fore.RESET +Fore.RED +Style.BRIGHT+" [F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.DIM+Style.RESET_ALL+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                    else: output_s += Fore.RED +", "+ Fore.YELLOW+ curr_sub["ID"] + Fore.RESET +Style.BRIGHT +" [F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.DIM+Style.RESET_ALL+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                else:
                    if output_s=="": output_s += Fore.YELLOW+ curr_sub["ID"] + Fore.RESET +Fore.RED +" [F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                    else: output_s += Fore.RED +", "+Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " [F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
            else:
                if curr_sub["Default"]==True: 
                    if output_s=="": output_s +=  Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Style.BRIGHT +Fore.RED + curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.RESET_ALL+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                    else: output_s += ", " + Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Style.BRIGHT +Fore.RED + curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.RESET_ALL+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                else:
                    if output_s=="": output_s +=  Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Fore.RED + curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                    else: output_s += ", " + Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Fore.RED + curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+ Fore.RESET+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
            continue
            
        # subs without errors
        if curr_sub["Forced"]==True:
            if curr_sub["Default"]==True: 
                if output_s=="": output_s += Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Style.BRIGHT+"[F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                else: output_s += ", "+Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Style.BRIGHT+"[F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
            else:
                if output_s=="": output_s += Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+"[F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                else: output_s += ", "+Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+"[F] "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
        else:
            if curr_sub["Default"]==True:
                if output_s=="": output_s += Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Style.BRIGHT+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                else: output_s += ", "+Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+Style.BRIGHT+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.RESET_ALL+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
            else:
                if output_s=="": output_s += Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
                else: output_s += ", "+Fore.YELLOW+ curr_sub["ID"] + Fore.RESET + " "+curr_sub["Language"]+" {"+curr_sub["Codec"]+"}"+Style.DIM+" ["+curr_sub["Size"]+"]"+Style.RESET_ALL
    
    # FILTERS
    if( filter_missing_info==True and ("?" not in output_v) and all('?' not in value for value in output_a.values()) and ("?" not in output_s) and all('-empty-' not in value for value in output_a.values()) and ("-empty-" not in output_s) ): return # missinginfo mode: jump file if it has missing information
    if( filter_errors==True and all('0b/s' not in value for value in output_a.values()) and ("0b/s" not in output_s) ): return # error mode: jump file if it has errors
    if( filter_name!=None and ( filter_name not in file_dict["File"] ) ): return # error mode: jump file if it has errors
    if( filter_resolution!=None and filter_resolution!=get_resolution(file_dict["Video"]["Resolution"].split("x")[1]) ): return # resolution filter mode: jump file if it has the resolution string
    if( filter_audio!=None and (not any(curr_audio_dict["Codec"] == filter_audio for curr_audio_dict in file_dict["Audio"] )) ): return # audio filter mode: jump file if it has the audio string
    if( filter_subs!=None and (not any(curr_sub_dict["Codec"] == filter_subs for curr_sub_dict in file_dict["Subs"] )) ): return # subs filter mode: jump file if it has the sub string 
    if( filter_chapters==True and file_dict["Chapters"]==False): return # chaps mode: jump file if it has no chapters   
    if( filter_not_chapters==True and file_dict["Chapters"]==True): return # not chaps mode: jump file if it has no chapters   
    
    # check: print only names
    if (printfullnames_flag == True):
            print(file_dict["FullPath"])
            return

    # check: print only names
    if (printnames_flag == True):
            print(file_dict["File"])
            return
            
    if(print_mediainfo_dict==True):
        # ------ Verbose Print -----
        print(media_info_output)

    else:
        # ------ Minimal Print ------
        # FILE OUTPUT
        if(no_colors_flag==True): # no colors
            print(clear_colors(output_f)) 
        else: # colored
            print(output_f)
        
        # VIDEO OUTPUT        
        if(no_colors_flag==True): # no colors
            if(output_v==""): print("VID: " +"-empty-")
            else: print(clear_colors(output_v))
        else: # colored
            if(output_v==""): print(Fore.CYAN+"VID: "+Fore.RESET+Style.DIM+"-empty-"+Style.RESET_ALL)
            else: print(Fore.CYAN+"VID: "+Fore.RESET + output_v)

        # ENCODING OUTPUT
        if(no_colors_flag==True): # no colors
            if(output_e=="" or clear_colors(output_e)=="encode_method=? deblock=? ref=? me=? merange=? subme=? trellis=? bframes=?"): print("ENC: " +"-empty-")
            else: print(clear_colors(output_e))
        else: # colored
            if(output_e=="" or clear_colors(output_e)=="encode_method=? deblock=? ref=? me=? merange=? subme=? trellis=? bframes=?"): print(Fore.CYAN+"ENC: "+Fore.RESET+Style.DIM+"-empty-"+Style.RESET_ALL)
            else: print(Fore.CYAN+"ENC: "+Fore.RESET + output_e)

        # AUDIO OUTPUT
        if(no_colors_flag==True): # no colors
            if output_a == {}:
                print("AUD: "+"-empty-")
            else:
                for key_lang in output_a:
                    print("AUD:"+" "+ clear_colors(output_a[key_lang]))
        else: # colored
            if output_a == {}:
                print(Fore.CYAN+"AUD: "+Fore.RESET+Style.DIM+"-empty-"+Style.RESET_ALL)
            else:
                for key_lang in output_a:
                    print(Fore.CYAN+"AUD:"+Fore.RESET +" "+ output_a[key_lang])
        
        # SUBS OUTPUT
        if(no_colors_flag==True): # no colors
            if output_s == "": print("SUB: "+"-empty-")
            else: print("SUB: "+ clear_colors(output_s))
        else: # colored
            if output_s == "": print(Fore.CYAN+"SUB: "+Fore.RESET +Style.DIM+"-empty-"+Style.RESET_ALL)
            else: print(Fore.CYAN+"SUB: "+Fore.RESET + output_s)
        print("")

def parse_all_files(path,filter_errors,filter_name,filter_resolution,printfullnames_flag,printnames_flag,recursive_flag,filter_audio,filter_subs,filter_chapters,filter_not_chapters,verbose_flag,no_colors_flag,filter_missing_info):
    if path[-1] != "/": path = path + "/" #fix path
    files,folders = get_files(path) #load files and folders
    files = sorted(files, key=str.lower) #sort files list
    folders = sorted(folders, key=str.lower) #sort folders list

    for curr_file in files:
        # -- Parse info --
        # unsupported mediainfo file
        if(MediaInfo.parse(path+curr_file,output="JSON")==""): continue
        # supported mediainfo file
        media_info_output = json.loads(MediaInfo.parse(path+curr_file,output="JSON"))
        file_dict = get_data(os.path.abspath(path+curr_file),media_info_output)
        print_mediainfo_dict(MediaInfo.parse(path+curr_file,output="",full=False),file_dict,filter_errors,filter_name,filter_resolution,printfullnames_flag,printnames_flag,filter_audio,filter_subs,filter_chapters,filter_not_chapters,verbose_flag,no_colors_flag,filter_missing_info)

    if(recursive_flag):
        for curr_folder in folders:
            if(not printnames_flag and not printfullnames_flag): 
                print("")
                if(no_colors_flag): print(path + curr_folder)
                else: print(Fore.MAGENTA + path + curr_folder +"/" + Fore.RESET)
            parse_all_files(path+curr_folder,filter_errors,filter_name,filter_resolution,printfullnames_flag,printnames_flag,recursive_flag,filter_audio,filter_subs,filter_chapters,filter_not_chapters,verbose_flag,no_colors_flag,filter_missing_info)

def main():
    # Commandline input
    parser = argparse.ArgumentParser(description='print mediainfo output in a compact way')
    parser.add_argument('path', type=str, nargs=1, help='the folder or file path')
    parser.add_argument('-r',  '--recursive', help='parse all foders recursively without depth limit', action='store_true')
    parser.add_argument('-fn', '--filter_name', type=str, help='show only files with specific name', action='store')
    parser.add_argument('-fr', '--filter_resolution', type=str, help='show only files with specific resolution', choices=['SD','HD','FHD','UHD'])
    parser.add_argument('-fe', '--filter_errors', help='show only files with errors in tags', action='store_true')
    parser.add_argument('-fm', '--filter_missing_info', help='show only files with missing tags "?" or "-empty-"', action='store_true')
    parser.add_argument('-fa', '--filter_audio', type=str, help='show only files with specific audio', choices=['TrueHD','TrueHD-Atmos','DD','DDP','DDP-Atmos','DD-Atmos','DTS','DTS-ES','DTS-HD','DTS-MA','AAC'])
    parser.add_argument('-fs', '--filter_subs', type=str, help='show only files with specific subs', choices=['vob','srt','sup','ass','vtt'])
    parser.add_argument('-fc', '--filter_chapters', help='show only files with chapters', action='store_true')
    parser.add_argument('-fnc','--filter_not_chapters', help='show only files without chapters', action='store_true')
    parser.add_argument('-nc', '--no_colors', help='show output without colors', action='store_true')
    parser.add_argument('-pfn','--printfullnames', help='print only full filenames', action='store_true')
    parser.add_argument('-pn', '--printnames', help='print only filenames', action='store_true')
    parser.add_argument('-v',  '--verbose', help='fallback to vanilla mediainfo output', action='store_true')
    args = parser.parse_args()

    # Variable migration
    path = os.path.abspath(args.path[0])
    filter_errors = args.filter_errors
    filter_missing_info = args.filter_missing_info
    filter_name = args.filter_name
    filter_resolution= args.filter_resolution
    recursive_flag = args.recursive
    filter_audio= args.filter_audio
    filter_subs= args.filter_subs
    filter_chapters= args.filter_chapters
    filter_not_chapters= args.filter_not_chapters
    no_colors_flag=args.no_colors
    printfullnames_flag = args.printfullnames
    printnames_flag = args.printnames
    verbose_flag = args.verbose
    
    # Load file/s & print info
    if os.path.isdir(path):     # -------- DIRECTORY --------
        parse_all_files(path,filter_errors,filter_name,filter_resolution,printfullnames_flag,printnames_flag,recursive_flag,filter_audio,filter_subs,filter_chapters,filter_not_chapters,verbose_flag,no_colors_flag,filter_missing_info)
            
    else:                       # -------- SINGLE FILE --------
        # check errors
        if(filter_errors or filter_audio):
            print("ERR: Can't filter a single file")
            return

        # -- Parse info --
        # unsupported or not valid file
        if(not os.path.isfile(path) or MediaInfo.parse(path,output="JSON")==""): 
            print("ERR: unsupported or not valid file")
            return
        # supported mediainfo file        
        media_info_output = json.loads(MediaInfo.parse(path,output="JSON"))
        file_dict = get_data(os.path.abspath(path),media_info_output)
        print_mediainfo_dict(MediaInfo.parse(path, output="", full=False),file_dict,False,filter_name,filter_resolution,printfullnames_flag,printnames_flag,None,None,None,None,verbose_flag,no_colors_flag,filter_missing_info)


if __name__ == "__main__":
    main()