from fflib import *
import sm2
from datetime import datetime
#print(ManifestHandler.scan_for_manifests())
#ManifestHandler.evaluate_manifest('saves/topicexample2/lessonlists/chunkmanifest.txt')
#ManifestHandler.lesson_manifest_contains_chunks('saves/topicexample2/lessonmanifest.txt')
j =ManifestHandler.get_available_chunks()