'''
Author: Jane1729
Date: 05-07-2020
Description: Scanning function
'''

import ctypes
import requests
import sqlite3
import sys

api_key = 'PUT_YOUR_OWN_VIRUSTOTAL_API_HERE'
scan_url = 'https://www.virustotal.com/vtapi/v2/file/scan'                          # URL to scan the file
rep_url = 'https://www.virustotal.com/vtapi/v2/file/report'                         # URL to get the reports for the uploaded file

def scan_file(file_loc):
    
    ###### **** Asking for user consent to scan the newly downloaded file or not [code 6 = Yes & code 7 = None] **** ######

    msgbox = ctypes.windll.user32.MessageBoxW
    usr_respn = msgbox(None, "Do you want to scan the newly downloaded file ?", "Information", 0x40 | 0x4)
    if usr_respn == 7 :
        sys.exit()
    
    ###### ********** Uploading and scanning the downloaded file ********** ######
    file_to_scan  = file_loc

    ### Use this to upload a file to scan ###
    scan_params = {'apikey': api_key} 
    detect_flag = 0
    warn_list = []
    warn_cnt = 0
    detect_list = []               

    ### File to upload ###
    files = {'file': (file_to_scan, open(file_to_scan, 'rb'))}
    scan_response = requests.post(scan_url, files=files, params=scan_params)
    scan_reply = scan_response.json()

    ### To get all field names from the above reportzz ###
    '''
    for field1 in scan_reply:
        print("Field name: ",field1)
    '''

    scan_id = scan_reply["scan_id"]
    link = scan_reply["permalink"]
    message = scan_reply["verbose_msg"]

    #print (link)

    ### Use this to get the particular file scan report using SCAN-ID in resource ###
    rep_params = {'apikey': api_key ,'resource': scan_id}
    rep_response = requests.get(rep_url, params=rep_params)
    rep_reply = rep_response.json()                           ## Gives the full report scan from Virus Total

    #print (rep_reply)


    ### To get all field names in the above reportzz ###
    '''
    for field2 in rep_reply:
        print("Field name:",field2)
    '''

    #sha1 = rep_reply["sha1"]                               ## Gives the sha1 hash, print this value to get direct hash value 
    #sha256 = rep_reply["sha256"]                           ## Gives the sha256 hash, print this value to get direct hash value 
    #md5 = rep_reply["md5"]                                 ## Gives the md5 hash, print this value to get direct hash value 

    if 'scans' in rep_reply:
        scans = rep_reply["scans"]                             ## Gives the details of respective scan engine in dictionary format
        for scan_engine,attrbset in scans.items():
            #print (attrbset)
            if attrbset["detected"] == 'True':
                detect_flag = 1
                detect_list.append("Detected by engine:", scan_engine)
        
            ### Checking for warnings ###

            if attrbset["result"] != None:                  
                warn_cnt +=1
                warn_msg = "Problem detected: " + str(attrbset["result"]) + " by engine " + str(scan_engine)
                warn_list.append(warn_msg)

    ### Printing Warnings and Detections if any ###

    if detect_flag != 0:
        detect_content = "\n".join(detect_list) 
        ctypes.windll.user32.MessageBoxExW(None, detect_content,"Detected", 0)

    if warn_cnt >0:
        warn_content = "\n".join(warn_list) 
        ctypes.windll.user32.MessageBoxExW(None, warn_content,"Warning", 0)
    else:
        #print(detect_flag)
        #print (warn_cnt)
        print ("Nothing")