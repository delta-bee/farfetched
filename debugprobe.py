from fflib import *
import sm2
from datetime import datetime
#print(ManifestHandler.scan_for_manifests())
#ManifestHandler.evaluate_manifest('saves/topicexample2/lessonlists/chunkmanifest.txt')
#ManifestHandler.lesson_manifest_contains_chunks('saves/topicexample2/lessonmanifest.txt')
topic_heap = [['Topic2/Lesson/Chunk1', 'Topic2/Lesson/Chunk2'], ['Topic2/Lesson2/Chunk3', 'Topic2/Lesson2/Chunk4']]
flattened_list = []
for topic in topic_heap:
    print(topic)
    for lesson in topic:
        print(lesson)
        flattened_list.append(os.path.split(lesson)[1])
print(flattened_list)