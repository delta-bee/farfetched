import os
from fflib import *
question,answer = fetch_question('saves/topicexample/lessonexample/chunkexample/questions/q1')
keywords = extract_keywords("\"Last night, as I strolled through the park, I noticed a beautiful fountain; its water danced gracefully in the moonlight, creating a mesmerizing display—truly a sight to behold! Suddenly, a gentle breeze whispered through the trees, and I thought, 'What a perfect moment to cherish!\'\"")
print(keywords)