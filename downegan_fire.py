'''
Author: Jane1729
Date: 04-07-2020
Description: Watches firefox browser for downloads
'''

import sqlite3
import time
import sys
import requests
import ctypes
import filescan

db_loc = '''C:/Users/%username%/AppData/Roaming/Mozilla/Firefox/Profiles/%foldername%/places.sqlite'''

##### Function to scan the FireFox database for latest download ID and return the path where the downloaded file is present #####

def get_updt_id(firfox_down_id):
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    c.execute('select * from moz_annos;')
    c.execute("SELECT * FROM moz_annos ORDER BY id DESC LIMIT 1")
    result = c.fetchone()
    conn.commit()
    id_in_db = result[0]

    if firfox_down_id == 'init':
        return id_in_db

    if id_in_db == firfox_down_id:
        time.sleep(60)
        return get_updt_id (id_in_db)
    else:
        conn = sqlite3.connect(db_loc)
        c = conn.cursor()
        c.execute("select * from moz_annos where id="+str(id_in_db))
        otpt_record = c.fetchone()
        cont = otpt_record[3]                                                    ### Getting the content ###
        if otpt_record[3].find('file:///') == -1:                                ### Checking if content has file name or state and if state getting the file name ###
            c.execute("select * from moz_annos where id="+str(id_in_db-1))
            down_res = c.fetchone()
            loc_from_db = down_res[3]
            ref_loc = loc_from_db[loc_from_db.index('/')+3:]
            return ref_loc,id_in_db
        else:
            ref_loc = cont[cont.index('/')+3:]
            return ref_loc,id_in_db

firfox_prev_id = get_updt_id('init')                                     # To get the present download ID from Firefox database

while True:
    firfox_down_file_loc,firfox_down_id = get_updt_id(firfox_prev_id)

    if firfox_down_file_loc != None:
        filescan.scan_file (firfox_down_file_loc)

    firfox_prev_id = firfox_down_id