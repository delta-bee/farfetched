from fflib import *
import sm2
from datetime import datetime
#print(ManifestHandler.scan_for_manifests())
#ManifestHandler.evaluate_manifest('saves/topicexample2/lessonlists/chunkmanifest.txt')
#ManifestHandler.lesson_manifest_contains_chunks('saves/topicexample2/lessonmanifest.txt')
import assembler
chunk_paths = assembler.setup_directories()
for lesson_chunks in chunk_paths:
    assembler.populate_chunks(lesson_chunks)
for lesson_chunks in chunk_paths:
    assembler.ask_questions(lesson_chunks)