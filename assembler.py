import os
from typing import List, Union, Tuple, TypeVar, Optional
normal_cwd = os.getcwd()
#You guys ever wonder if this will ever actually take off? If it does, I'd be so happy.
#Maintaining this code might be pain though. I need to write better documentation...
#I HATE YOU ASSEMBLER.PY, YOU HYDRA OF BUGS.
def get_immediate_child_directories(path: str) -> list[str]:
    """
    Given a string representing a path, this function will return a list of all of the immediate child directories.
    :param path: A string representing a path.
    :return: A list of strings, representing the paths of the immediate child directories.:
    """
    return [os.path.join(path,directory) for directory in os.listdir(path) if os.path.isdir(os.path.join(path, directory))]

def strip_path(path: str, list_index: int) -> str:
    """
    :param path: A string representing a path. Ex. Topic2/Lesson/Chunk1
    :param list_index: The index of the list that you want to strip from the path. Ex. 2 for Chunk, 1 for Lesson, 0 for Topic.
    :return: The chunk name, without the path. Ex. Chunk1
    """
    return path.split(os.sep)[list_index]

def flatten_list(nested_list: List[List[TypeVar]]) -> List[TypeVar]:
    """
    :param nested_list: A list of lists.
    :return flattened_list: A list of strings, or of lists.:

    Note: If it is given a list that does not contain any lists, it will return the original list.
    """

    while any(isinstance(item,list) for item in nested_list):
        flattened_list = []
        for item in nested_list:
            if isinstance(item,list):
                flattened_list.extend(item)
            else:
                flattened_list.append(item)
        nested_list = flattened_list
    #I think my AI code completer made this. I don't really understand it, but it passes the tests.
    #:shrug:
    return nested_list


def strip_punctuation(string: str) -> str: #Slightly modified version found in FFLIB.py, it allows spaces.
    """
    Removes common punctuation from a string.
    Returns a string with the punctuation removed.
    :param string:
    :return:
    """
    discardables = ['\'', '\"', ',', ':', ';', '-', '.','/','!','?']
    for character in discardables:
        string = string.replace(character, '')
    return string
def if_not_exist_create_it(path: str or tuple[str], *args) -> None:
    """
    This function will check if a directory exists. If it doesn't, it will create it.
    It can be given a string, or a tuple of strings.
    In the event it is given a tuple, it will join the strings with os.sep.
    Raises an error if it has something other than a string or tuple of strings.
    :param path:
    :param args:
    :return None:
    """
    #This function can be called with if_not_exist_create_it(pathpart1,pathpart2), for the sake of simplifying code outside of this function.
    #So... we'll handle the args.
    if args and isinstance(path,tuple):
        raise TypeError("if_not_exist_create_it: The path parameter cannot be a tuple if additional arguments are given.") #I am NOT handling that kind of crappy input. In fact, if that garbage is passed to this function, something went wrong upstream.
    elif args:
        path = os.path.join(path,*args)
    if not isinstance(path,tuple) and not isinstance(path,str):
        raise TypeError("if_not_exist_create_it: The path parameter must be a string or a tuple of strings.")
    elif isinstance(path,tuple):
        path = os.path.join(*path)
    if not os.path.exists(path):
        os.mkdir(path)
    return None
def setup_directories(hierarchy: List[List[str]] = [['Topic'], ['Lesson', 'Lesson2'], [['Chunk1', 'Chunk2'], ['Chunk3', 'Chunk4']]]) -> List[List[str]]: #default val for debugging
    """
    This function will create the directory tree for the user's custom lesson.
    :param hierarchy:
    :return: This returns a list of lists. The top level list is the list of lessons, and the second level list is the list of chunks in that lesson.

    In detail, this function will create the following directory structure:
    Topic contains lesson folders, each with chunk folders.

    When called, it:
        Checks for a save folder. If it doesn't exist, it creates it.
        Checks for the topic folder. If it doesn't exist, it creates it.

    """
    chunk_path_list: List[List[str]] = []
    try:
        #Move present working directory to the save folder, that's the only place that this script should be poking around in...
        if_not_exist_create_it(normal_cwd,'saves')
        #Create topic directory in the saves folder
        topic = hierarchy[0][0]
        if_not_exist_create_it('saves',topic)
        #Create lesson folders and their chunks
        lesson_list = hierarchy[1]
        print(hierarchy)
        for i,lesson_dir in enumerate(lesson_list): #Look, Mom, I learned a new function!
            lesson_path = os.path.join('saves',topic,lesson_dir) #topic/lesson_path
            #Create lesson directories
            if not os.path.exists(lesson_path):
                os.mkdir(lesson_path)
            chunk_paths_in_lesson = []
            lesson_chunk_list = hierarchy[2][i] #['Chunk1', 'Chunk2']
            for chunk_dir in lesson_chunk_list:
                chunk_path = os.path.join(topic,lesson_dir,chunk_dir)
                if_not_exist_create_it('saves',chunk_path)
                chunk_paths_in_lesson.append(chunk_path)
            chunk_path_list.append(chunk_paths_in_lesson)
    except NameError as e:
        print("Oh no. Failed to create directories.",e)
    return chunk_path_list
def populate_chunks(chunk_list: List[str]) -> None:
    """
    In each chunk directory, we'll create a content.txt file, with contents specified by the user.

    :param chunk_list: A flat list of chunk paths. Ex. ['Topic2/Lesson/Chunk1', 'Topic2/Lesson/Chunk2']
    :return: None
    """
    list_of_content_file_paths = []
    list_of_content_file_contents = []
    for chunk in chunk_list:
        if 'saves' not in chunk.split(os.sep):
            chunk = os.path.join('saves',chunk)
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
            list_of_content_file_paths.append(content_file_path)
            content_input_as_string = "\n".join(content_input)
            list_of_content_file_contents.append(content_input_as_string)
    write_contents_to_drive(list_of_content_file_paths,list_of_content_file_contents)
    return
def write_contents_to_drive(list_of_paths: List[str],list_of_contents: List[str]) -> None:
    """
    In each path, we'll write the contents to the file.
    Each path should correspond to the content of the same index in the list_of_contents list.
    Both parameters should be lists of strings.
    If the length of both lists are not equal, this function will raise an error.
    If there is already a text file at the path, this function will overwrite it.
    :param list_of_paths:
    :param list_of_contents:
    :return None:
    """
    if not len(list_of_paths) == len(list_of_contents):
        raise ValueError("Write contents to drive: The length of the list of paths and the list of contents must be equal.")
    for path,content in zip(list_of_paths,list_of_contents):
        with open(path,'w') as file:
            file.write(content)
    return None
def ask_questions(chunk_list: List[str]) -> None:
    for chunk in chunk_list:
        if 'saves' not in chunk.split(os.sep):
            chunk = os.path.join('saves',chunk)
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
def lesson_manifest_creator(user_input: List[List[str]]) -> None:
    #user_input = [['Topic'], ['Lesson', 'Lesson2'], [['Chunk1', 'Chunk2'], ['Chunk3', 'Chunk4']]]
    print(f"LIST OF LESSONS:{str(user_input[1])}")
    list_of_manifest_declarations = [] #Hey, I've been getting good at this self explanatory variable name stuff. Maybe I'll make docstrings for these functions too.
    for lesson in user_input[1]: #PSST! user_input[1] is just the lesson list. And not lesson paths. Just lesson names.
        print(f"For lesson \"{lesson}\", please tell me if requires any other lesson to be learned first.")
        print("Type in the lesson name(s) that need to be learned before this, and then press enter. Type DONE when you're done entering lesson names.")
        dependency_list = []
        while True:
            entry = input()
            if entry.upper() == "DONE":
                break
            else:
                if entry.lower() == lesson.lower():
                    print("Lesson can't depend on itself, silly. Try again.")
                    continue
                elif entry in user_input[1]:
                    dependency_list.append(entry)
                else:
                    print("Unknown lesson. Try again.")
        #Now we've got the list of dependencies, so we'll put it in the format that manifesthandler will understand.
        lesson_manifest_declaration = lesson + ' REQUIRES ' + ' '.join(dependency_list)
        #In case you're lost, for each lesson, we're generating this manifest statement ex."Lesson2 REQUIRES Lesson", and adding it to the topic directory, along with the statements of every other lesson.
        list_of_manifest_declarations.append(lesson_manifest_declaration)
    manifest_text_file_contents = "\n".join(list_of_manifest_declarations)
    #And finally, we write this darn manifest to the directory tree.
    topic = user_input[0][0] #Yeah, it's List[List[str]]. Weird how I thought that would be more understandable.
    topic_path = os.path.join(normal_cwd,'saves',topic)
    #if not os.path.exists(topic_path):
    with open(os.path.join(topic_path,'lessonmanifest.txt'),'w') as manifest_file:
        manifest_file.write(manifest_text_file_contents)
    return None

def chunk_manifest_creator(lesson_chunks:List[List[str]]) -> None:
    #Copying and pasting the code for lesson_manifest creator was a mistake. I'm just going to rewrite all of this.
    """
    Create a manifest file for all of the chunks in each lesson.

    :param lesson_chunks: A list of lists. The top level list is the list of lessons, and the second level list is the list of chunks in that lesson.
        Ex. [['Topic2/Lesson/Chunk1', 'Topic2/Lesson/Chunk2'], ['Topic2/Lesson2/Chunk3', 'Topic2/Lesson2/Chunk4']]
        Note that the "chunks" are relative paths, not just the chunk names.
    :return: None
    """
    for chunk_paths_in_lesson in lesson_chunks:
        chunk_names_in_lesson = [strip_path(chunk,2) for chunk in chunk_paths_in_lesson]
        list_of_manifest_declarations = []
        for chunk in chunk_paths_in_lesson:
            chunk_name = strip_path(chunk,2)
            print(f"For chunk \"{chunk_name}\", please tell me if requires any other chunk to be learned first.")
            print("Type in the chunk name(s) that need to be learned before this, and then press enter. Type DONE when you're done entering chunk names.")
            print(f"Chunk names in this lesson: {chunk_names_in_lesson}")
            dependency_list = [] #Note: This shouldn't be shared across lessons. That'll break something downstream.
            while True:
                entry = input()
                if entry.upper() == "DONE":
                    break
                elif entry == chunk_name:
                    print("Chunk can't depend on itself, silly. Try again.")
                    continue
                elif entry in chunk_names_in_lesson:
                    dependency_list.append(entry)
                else:
                    print("Unknown chunk. Try again.")
            chunk_without_path = os.path.split(chunk)[1]
            list_of_manifest_declarations.append(chunk_without_path + ' REQUIRES ' + ' '.join(dependency_list))
        #Now, we have all of the chunk dependencies in this individual lesson.
        #We'll convert this list into a string, and then write that string to the lesson directory.
        manifest_content = "\n".join(list_of_manifest_declarations)
        topic_name = strip_path(chunk,0)
        lesson_name = strip_path(chunk,1)
        file_target = os.path.join(normal_cwd,'saves',topic_name,lesson_name,'chunkmanifest.txt')
        with open(file_target,'w') as manifest_file:
            manifest_file.write(manifest_content)
def orchestrate_creation() -> None:
    """
    This function will orchestrate the creation of the directory tree and content files.
    It used to be the main function, but I've split it up into smaller functions for easier debugging.
    Good luck debugging it. I'm sorry, but I didn't write the easiest to maintain code...
    :return:
    """
    print("Welcome to FarFetched's Assembler!")
    print("This program will help you assemble your own custom lessons for FarFetched.")
    print("Please note that this program is still in development. It may not work as intended.")
    user_inputs = get_user_input()
    print("Chunk names complete.")
    print("Please wait while the program attempts to create the directory tree that you've outlined...")
    chunk_paths: List[List[str]] = setup_directories(user_inputs)
    for lesson_paths in chunk_paths:
        populate_chunks(lesson_paths)
    for lesson_chunks in chunk_paths:
        ask_questions(lesson_chunks)
    lesson_manifest_creator(user_inputs)
    chunk_manifest_creator(chunk_paths)
    chunk_paths_flat_list: List[str] = flatten_list(chunk_paths)
    print("Assembly complete. You can now find your new topic in the \"saves\" folder.")
    #Now we've got all of the content. Now we need to ask for the chunk's questions
def get_user_input() -> List[List[str]]:
    # Now we'll ask the user about the layout of their lesson.
    user_inputs = []  # But we'll store what the user inputted in this list, so that the user can change their mind later.
    print("What is the name of your topic? Ex. Introduction to Python Programming")
    while True:
        topic_name = input()
        if not topic_name == strip_punctuation(topic_name):
            topic_name = strip_punctuation(topic_name)
            print(f"Topic name cannot contain some punctuation. Your new topic name is {topic_name}.")
            user_inputs.append([topic_name])
            break
        if os.path.exists(os.path.join('saves', topic_name)):
            print(f"Topic name \"{topic_name}\" already exists. Please choose a different name.")
        else:
            user_inputs.append([topic_name])
            break
    # We need to keep directory commands and user inputs on the same index.

    # Next step: Get all of the lesson directories.
    print("Now we need all of the lesson names for your topic. Ex. Datatype: Lists")
    print("Put in a lesson name, and then hit ENTER. Once you're done entering lesson names, type \"DONE\" .")
    lesson_names = []
    while True:
        user_input = input()
        if user_input.upper() == "DONE" and lesson_names:
            break
        else:
            lesson_names.append(user_input)
    user_inputs.append(lesson_names)
    print("Lesson names complete.")

    # Now, for each lesson, we'll ask for each of the chunks in the lesson.
    chunk_names: List[List[str]] = []
    for lesson in lesson_names:
        chunk_list_in_lesson = []
        print(f'For the lesson \"{lesson}\". please list all chunks. Ex. List Indexing')
        print("Again, ENTER to submit one chunk name, DONE when you're finished.")
        while True:
            user_input = input()
            if user_input.upper() == "DONE" and chunk_list_in_lesson:  # Do not allow the user to input no lessons. It'll crash it.
                break
            else:
                chunk_list_in_lesson.append(user_input)
        chunk_names.append(chunk_list_in_lesson)
    user_inputs.append(chunk_names)
    return user_inputs
def discover_topics():
    pass
def menu(*args) -> str:
    """
    This function will display a menu, and then return the user's selection.
    Example: menu("Eat the Burger","eat","Don't eat the burger","nah")
    If the user selects "Eat the Burger", it will return "eat"
    Input must be an even number of strings.
    :param args:
    :return:
    """
    #This crates a list "argli" that stores all the arguments given to the function.
    argli = list(args)
    #We make sure that we have an even number of arguments, if not, we crash the program.
    if (len(argli)%2) == 1:
        raise ValueError("Menu: Odd number of arguments were provided.")

    #The even arguments are added to displaylist
    displaylist = [argli[i] for i in range(len(argli)) if i%2 == 0]
    #And the odd ones are added to varlist
    varlist = [argli[i] for i in range(len(argli)) if i%2 == 1]

    #This will make something like:
    '''
    [1]: Eat the Burger
    [2]: Don't eat the burger
    '''
    for i in range(len(displaylist)):
        bracket_thing = "[" + str(i+1) + "]:" #Example: [2]:
        print(bracket_thing,displaylist[i])


    # This list is for which numbers we should accept as an input
    valid_numbers = [str(x + 1) for x in range(len(displaylist))] #Example: [1, 2]

    #This asks the user for their selection, and will loop again if they provide an invalid choice
    while True:
        selection = str(input())
        if selection in valid_numbers:
            break
        else:
            print("Menu: Invalid selection. Try again.")

    #Now we have the user's selection, and we need to fetch from varlist the corresponding thing to return.
    selection = int(selection)- 1 #Lists start at 0, but the menu we displayed starts at 1, so we need to correct for this.
    return varlist[selection]
def menu_translator(options: List[str]) -> str:
    """
    This function will translate a list of strings a list of options into a format that menu() understands.
    It will then call menu() with the options.
    It will return the result of menu(), which is one of the strings that have been provided in options.
    :param options:  A list of strings.
    :return: The string that was chosen by the user.
    """
    doubled_list = options*2
    return menu(*doubled_list)
def fetch_topics() -> dict[str:str] or None:
    """
    This function will fetch all of the topics that have been created.
    It returns a dictionary where the keys are the display names, and the values are the paths.
    The display name is merely the name of the topic folder.
    :return: Dictionary of topic names and topic paths, with display names as keys and paths as values.

    Behavior:
    Gets the list of topic paths from get_immediate_child_directories pointed at the saves folder.
    Does the save thing, but trims off the rest of the path, to get the directory name.
    Zips these two lists into a dictionary, and returns it.
    """
    display_topic_list = [os.path.split(topic_path)[1] for topic_path in get_immediate_child_directories(os.path.join(normal_cwd, 'saves'))]
    path_topic_list = [topic_path for topic_path in get_immediate_child_directories(os.path.join(normal_cwd, 'saves'))]
    display_and_path_dict = dict(zip(display_topic_list, path_topic_list))
    return display_and_path_dict
def fetch_user_desired_topic_path() -> Optional[str]:
    """
    This function will display a menu that allows the user to edit a topic.
    It returns a path, a string, that corresponds to the path of the topic that the user has chosen.
    :return: A string that corresponds to the path of the topic that the user has chosen, or None if the user has not created any topics yet.
    Behavior:
    Calls fetch_topics() to get a dictionary of topic names and topic paths.
    If the dictionary is empty, it will return None.
    Otherwise, it will display a menu of topic names, and then return the path of the topic that the user has chosen.
    """
    topic_and_path_dict = fetch_topics()
    if not topic_and_path_dict:
        return None
    display_topic_list = list(topic_and_path_dict.keys())
    print("Which topic would you like to edit?")
    user_topic_name_choice = menu_translator(display_topic_list)
    user_topic_path_choice = topic_and_path_dict.get(user_topic_name_choice)
    if user_topic_name_choice not in display_topic_list or user_topic_path_choice not in topic_and_path_dict.values():
        raise ValueError("Downstream error in fetch_user_desired_topic_path: menu_translator returned a value that was not in the topic_and_path_dict. This should never happen. Please report this error to the developer.")
    return user_topic_path_choice
def ask_user_edit_type() -> List[str]:
    """
    This function will ask the user what type of edit they want to make.
    It returns a string that corresponds to the type of edit that the user has chosen.
    :return: A list of two strings, where the first string is the type of edit, and the second string is the target type.
        Valid types of edit: ["add_new","edit_existing","delete_existing","rename_existing"]
        Valid target types: ["topic","lesson","chunk"]
    Behavior:
    Defines the display version of the operation options for the menu, and their corresponding machine names.
    Uses menu_translator() to display the menu with the display options, and then does the same with the target type.
    """
    #Get operation type
    print("What type of edit would you like to make?")
    operation_menu_options = ["add_new","edit_existing","delete_existing","rename_existing"]
    operation_menu_display_options = ["Add new", "Edit existing", "Delete existing", "Rename existing"]
    display_and_path_dict = dict(zip(operation_menu_display_options, operation_menu_options))
    user_operation_edit_type_choice = menu_translator(operation_menu_display_options)
    operation_type = display_and_path_dict.get(user_operation_edit_type_choice)

    print("What type of thing would you like to edit?")
    #Now, we get the target of their operation (Chunk, Lesson, Topic)
    target_menu_options = ["topic","lesson","chunk"]
    target_menu_display_options = ["Topic", "Lesson", "Chunk"]
    display_and_path_dict = dict(zip(target_menu_display_options, target_menu_options))
    user_target_edit_type_choice = menu_translator(target_menu_display_options)
    target_type = display_and_path_dict.get(user_target_edit_type_choice)
    return [operation_type, target_type]
def editor():
    print("Welcome to FarFetched's Editor!")
    print("Fetching topics...")
    user_desired_topic_path = fetch_user_desired_topic_path()
    if not user_desired_topic_path:
        print("Sorry, you don't seem to have any topics yet.")
        print("Make some with create new topic.")
        print("Editor will now exit.")
        return
    print(user_desired_topic_path)
    return

def main():
    print("Welcome to FarFetched's Lesson Manager.")
    editor()
    while True:
        menu("Create a new topic","new_topic","Edit topic","editor","Exit","exit")
        if menu() == "new_topic":
            orchestrate_creation()
        elif menu() == "exit":
            break
        elif menu() == "editor":
            pass
if __name__ == '__main__':
    main()