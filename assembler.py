import os
import sqlite3
from typing import List, Union, Tuple
def setup_directories(hierarchy: List[List[str]] = [['Topic'], ['Lesson', 'Lesson2'], [['Chunk1', 'Chunk2'], ['Chunk3', 'Chunk4']]]) -> List[List[str]]: #default val for debugging
    #We'll put this in one big ol try statement. If it fails, I don't want it to make me a half-baked directory tree.
    chunk_path_list: List[List[str]] = []
    try:
        #Move present working directory to the save folder, that's the only place that this script should be poking around in...
        if not os.path.exists('saves'):
            #I'd call on self_check in FFlib, but I want this to be independent of the rest of FarFetched, because FFlib is entering into function cancer territory.
            os.mkdir('saves')
        os.chdir('saves')
        #Create topic directory in the saves folder
        topic = hierarchy[0][0]
        if not os.path.exists(topic):
            os.mkdir(topic)
        #Create lesson folders and their chunks
        lesson_list = hierarchy[1]
        for i,lesson_dir in enumerate(lesson_list): #Look, Mom, I learned a new function!
            lesson_path = os.path.join(topic,lesson_dir) #topic/lesson_path

            #Create lesson directories
            if not os.path.exists(lesson_path):
                os.mkdir(lesson_path)
            chunk_paths_in_lesson = []
            lesson_chunk_list = hierarchy[2][i] #['Chunk1', 'Chunk2']
            for chunk_dir in lesson_chunk_list:
                chunk_path = os.path.join(topic,lesson_dir,chunk_dir)
                if not os.path.exists(chunk_path):
                    os.mkdir(chunk_path)
                chunk_paths_in_lesson.append(chunk_path)
            chunk_path_list.append(chunk_paths_in_lesson)
    except NameError as e:
        print("Oh no. Failed to create directories.",e)
    return chunk_path_list
def populate_chunks(chunk_list: List[str]) -> None:
    for chunk in chunk_list:
        if os.path.exists(chunk):
            chunk_without_path = os.path.split(chunk)[1]
            print(f"Please now give me the contents of the chunk named \"{chunk_without_path}\". DONE when you're finished providing all of the lines.")
            #Previously, we allowed DONE in all cases. Now, we'll only accept all uppercase, because we don't want to prematurely terminate the input
            content_input = []
            while True:
                new_input_line = input()
                if new_input_line == "DONE":
                    break
                else:
                    content_input.append(new_input_line)
            #Now we've got their input, we will write it to content.txt
            content_file_path = os.path.join(chunk,'content.txt')
            with open(content_file_path,'w') as file:
                as_string = ''
                for line in content_input:
                    as_string += line +'\n'
                file.write(as_string)
    return
def ask_questions(chunk_list: List[str]) -> None:
    for chunk in chunk_list:
        if os.path.exists(chunk):
            print(f"Please now give me a question for the chunk {chunk}")
            #Previously, we allowed DONE in all cases. Now, we'll only accept all uppercase, because we don't want to prematurely terminate the input
            question: str = input() + '\n'
            print("Now, give me the correct answer.")
            answer: str = input() + '\n'

            #Now we've got their input, we'll create the questions folder now.
            os.mkdir(os.path.join(chunk,'questions'))
            #Now we've got their input, we will write it to content.txt
            content_file_path = os.path.join(chunk,'questions','question.ffq1')
            with open(content_file_path,'w') as file:
                file.write(question)
                file.write(answer)
def main():
    # Step 1, check for all database files.
    dir_contents = os.listdir()
    db_files = [file for file in dir_contents if '.db' in file and file != 'data.db']
    # Step 2, if there are database files (from previous assembly attempts), ask user if they wish to load them.
    if db_files:
        print("Possible assembler database detected. Would you like to open it?")
        #Work on this later.

    #Now we'll ask the user about the layout of their lesson.
    user_inputs = [] #But we'll store what the user inputted in this list, so that the user can change their mind later.
    print("What is the name of your topic? Ex. Introduction to Python Programming")
    topic_name = input()
    user_inputs.append([topic_name])
    #We need to keep directory commands and user inputs on the same index.

    #Next step: Get all of the lesson directories.
    print("Now we need all of the lesson names for your topic. Ex. Datatype: Lists")
    print("Put in a lesson name, and then hit ENTER. Once you're done entering lesson names, type \"DONE\" .")
    lesson_names = []
    while True:
        user_input = input()
        if user_input.upper() == "DONE":
            break
        else:
            lesson_names.append(user_input)
    user_inputs.append(lesson_names)
    print("Lesson names complete.")

    #Now, for each lesson, we'll ask for each of the chunks in the lesson.
    chunk_names: List[List[str]] = []
    for lesson in lesson_names:
        chunk_list_in_lesson = []
        print(f'For the lesson \"{lesson}\". please list all chunks. Ex. List Indexing')
        print("Again, ENTER to submit one chunk name, DONE when you're finished.")
        while True:
            user_input = input()
            if user_input.upper() == "DONE":
                break
            else:
                chunk_list_in_lesson.append(user_input)
        chunk_names.append(chunk_list_in_lesson)
    user_inputs.append(chunk_names)
    print("Chunk names complete.")
    print("Please wait while the program attempts to create the directory tree that you've outlined...")
    chunk_paths = setup_directories(user_inputs)
    for lesson_paths in chunk_paths:
        populate_chunks(lesson_paths)
    for lesson_chunks in chunk_paths:
        ask_questions(lesson_chunks)
    #Now we've got all of the content. Now we need to ask for the chunk's quesitons
if __name__ == '__main__':
    main()
else:
    print("WARNING! Assembler shouldn't be run as a module, unless you are debugging.")