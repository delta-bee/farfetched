import os
from fflib import *
response = QProc.extract_keywords("The dog jumped over the bush.")
answer = QProc.extract_keywords("The dog leaped over the tree.")
v = QProc.is_correct(response, answer)
print(QProc.is_correct("The dog ate", "The Cat ate"))