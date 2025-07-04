import os
fileli = []
for root, dirs, files in os.walk('.'):
    fileli += files