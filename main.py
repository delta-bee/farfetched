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
print("FarFetched, Pre-alpha  Commit #13")
choice = menu("Auto-Learn","autolearn","View Topics","topiclist","Perform self-check",'self_check')
try:
    exec(choice + "()")
except NameError:
    on_logic_error(1,'Function not found: ' + str(choice))