#This work is licensed under the GLP-3 license. FarFetched is free/libre open source software (FLOSS).
#For inquiries, please contact:
#- Matrix: @sl8:matrix.org
#- Email: sl8@o8.lol

from fflib import *
intro_ascii_art = r"""
  ______         ______   _       _              _ 
 |  ____|       |  ____| | |     | |            | |
 | |__ __ _ _ __| |__ ___| |_ ___| |__   ___  __| |
 |  __/ _` | '__|  __/ _ \ __/ __| '_ \ / _ \/ _` |
 | | | (_| | |  | | |  __/ || (__| | | |  __/ (_| |
 |_|  \__,_|_|  |_|  \___|\__\___|_| |_|\___|\__,_|
"""
print(intro_ascii_art)
print("FarFetched, Alpha, Commit #32")
while True:
    eval(Menu.main_menu())