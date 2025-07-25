#Library for FarFetched
import sys, os, time, sqlite3, sm2, assembler
from typing import List, Union, Tuple, TypeVar #I was told my stuff's more readable if I use this.
from datetime import datetime

from assembler import strip_punctuation

required_files = ['main.py','fflib.py','data.db','sm2.py']
required_directories = ['saves']
def on_error(severity: str or int='1', error_message: str="No error message was provided") -> None:
    #For severity, if it's 0, it won't stop the game, if it's 1, it will stop the game.
    print("Uh oh, an impossible state has occurred.")
    print(error_message)
    if severity == int(severity):
        severity = str(severity)
    if severity == '0':
        print("The program has self repaired, and will continue. Yay!")
        return
    else:
        print("The program cannot continue like this, and will now exit.")
        sys.exit()

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
def get_immediate_child_directories(path: str) -> list[str]:
    return [os.path.join(path,directory) for directory in os.listdir(path) if os.path.isdir(os.path.join(path, directory))]

def strip_path(path: str) -> str:
    """
    It is given a path, and it will return the last part of the path.
    Ex: /home/user/file.txt -> file.txt
    :param path: The path to be stripped.
    :return str: The last part of the path.:
    """
    return path.split(os.sep)[-1]

def make_boolean(string: str) -> bool or str:  # Converts string literals to booleans
    if 'bool' in str(type(string)):
        return string #Return to sender
    string = string.lower()
    if string == 'true':
        return True
    elif string == 'false':
        return False
    else:
        on_error('1', 'make_boolean was given an invalid input.')
        sys.exit()
def menu(*args) -> str:
    #Example input: "Eat the Burger","eat","Don't eat the burger","nah"
    #It will display the user "Eat the Burger" and then "Don't eat the burger"
    #And then this function will return with either "eat" or "nah" depending on what the user selected.

    #This crates a list "argli" that stores all the arguments given to the function.
    argli = list(args)
    #We make sure that we have an even number of arguments, if not, we crash the program.
    if (len(argli)%2) == 1:
        on_error('1', "Menu: Odd number of arguments were provided.")

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
def self_check() -> None:
    #We will deploy os.walk() to crawl the contents of the current directory.
    fileli = []
    dirli = []
    for root, dirs, files in os.walk('.'):
        fileli += files
        dirli += dirs
    #Now, we will check that all needed files and directories were found.
    files_missing = False
    dirs_missing = False
    for file in required_files:
        if file not in fileli:
            print(file,"not found. It may be required for proper program operation.")
            if file == 'data.db':
                print("Automatically created new database!")
                FFMAN2.create_database()
            files_missing = True
    for directory in required_directories:
        if directory not in dirli:
            print(directory, "directory not found. It may be required for proper program operation.")
            dirs_missing = True
    if not files_missing and not dirs_missing:
        print("Self check complete: No problems detected by the scanner.")
    else:
        print("Self check complete: Some issues were detected.")
class QProc:
    @staticmethod
    def fetch_question(path: str) -> tuple[str,str] or None:
        """
        This function will extract the question and answer from a path.
        :param path: This is the path to the question file.
        :return: This function will return a tuple containing the question and answer, or None if the path is invalid (like if it contains no question or answer).
        """
        #The purpose of this function is to extract the question and answer from a path.
        if os.path.isfile(path) and os.path.getsize(path) != 0:
            lines = []
            with open(path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        lines.append(line)

            if not lines or len(lines) != 2 or all(line == '' for line in lines):
                return None
            else:
                question = lines[0]
                answer = lines[1]
                return question, answer
        else:
            on_error('1', 'Invalid path given to fetch_question function.')
            sys.exit()
    @staticmethod
    def strip_punctuation(string: str) -> str:
        discardables = ['\'', '\"', ',', ' ', ':', ';','-','.','/']
        for character in discardables:
            string = string.replace(character,'')
        return string
    @staticmethod
    def extract_keywords(string: str) -> list[str]:
        word_list = string.split(' ')
        keywords = []
        for word in word_list:
            word = word.lower()
            word = QProc.strip_punctuation(word)
            if word:
                keywords.append(word)
        return keywords
    @staticmethod
    def is_perfect(responseli: list or str, answerli: list or str) -> bool:
        if not isinstance(responseli,list) or not isinstance(answerli,list):
            actual_type = type(responseli)
            if 'str' in str(actual_type):
                responseli = QProc.extract_keywords(responseli)
                answerli = QProc.extract_keywords(answerli)
            else:
                on_error('1', 'Incorrect data type given to QProc.is_perfect()')

        correct_keywords = 0
        incorrect_keywords = 0
        for keyword in answerli:
            if keyword in responseli:
                correct_keywords += 1
            else:
                incorrect_keywords +=1
        #The previous portion of code determines how many keywords were correct, and how many were incorrect.
        #We will now determine whether we will accept this answer as perfect.
        correctness_threshold = 0.8 #We will accept 80% or higher accuracy.
        if correct_keywords / (correct_keywords+incorrect_keywords) >= correctness_threshold:
            return True
        else:
            return False
def topic_list() -> str:
    topic_directory_list = os.listdir('saves')
    new_topic_list = [] #All of this is just to make the menu command.
    for x in topic_directory_list:
        new_topic_list.append(x)
        new_topic_list.append(x)
    #menu("topic1","topic1","topic2","topic2")
    param_head = "menu(\""
    param_body = '\",\"'.join(new_topic_list)
    param_tail = "\")"
    complete_command = param_head + param_body + param_tail
    #Everything we've done in those lines above is set up to execute a menu command listing all of the topics.
    #Now, we'll see which one the users picks.
    try:
        choice = eval(complete_command) #Scary!
    except Exception as e:
        print(complete_command)
        print(f"An error occurred: {e}")
        on_error('1','topic_list has suffered an error, now exiting.')
        sys.exit()
    topic_path_head = 'saves/'
    return topic_path_head +str(choice) #This program speaks in paths. Therefore, we will return the relative path, instead of merely the directory name.
    #This is a terrible way to do it, but at least we can list out the topics now.
    #Step 2: Have something on the other end of this
class FFMAN2: #Handles the translation between the "database" and the rest of the program.
    @staticmethod
    def create_database() -> None:
        with sqlite3.connect('data.db') as connection:
            cursor = connection.cursor()
            command = '''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_type TEXT,
                    quality INTEGER,
                    easiness REAL,
                    review_datetime TEXT,
                    path TEXT
                )''' #We are not including repetitions because I'd rather calculate that myself, and Interval could get messed up if the user reviews the card beyond the program's desired review date.
            cursor.execute(command)
            other_command = '''CREATE TABLE IF NOT EXISTS learned (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_path TEXT,
                    chunk_path TEXT,
                    lesson_path TEXT,
                    topic_path TEXT
                )''' #I'm not sure if I'm going to use all of those columns.
            cursor.execute(other_command)
            connection.commit()
    @staticmethod
    def check_if_completed(learned_path) -> bool: #Currently only supports chunks.
        if not os.path.exists('data.db'):
            FFMAN2.create_database()
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute(
                '''SELECT * FROM learned WHERE chunk_path = ?''',
                (learned_path,)
            )
            cur_contents = [x for x in cur]
            if cur_contents:
                return True
            else:
                return False
    @staticmethod
    def determine_repetitions(path: str) -> int:
        #This function should really only be used with fetch_in_database, unless you're insane.
        #Ex input: (5.0, 5, 'today', 'saves/topicexample/lessonexample/chunkexample/questions/q1.ffq1')
        db_contents: List[Tuple[int]] = []
        if not os.path.exists('data.db'):
            FFMAN2.create_database() #If database does not exist, call upon the create database function.
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('''SELECT id,quality FROM logs WHERE path = ?''',(path,))
            for entry in cur:
                db_contents.append(entry)
        repetitions = 0
        #Right now, DB Contents is a list of tuples with just one integer in them.
        for quality_tuple in db_contents: #Increment by 1 for every entry that has the path in it.
            #print(quality_tuple[0])This seems like it's going in order. If it's not, we'll figure out soon enough.
            review_quality = quality_tuple[1]
            if review_quality > 2:
                repetitions += 1
            else:
                repetitions = 0 #If the review quality is 2 or lower, then it doesn't count, because the response was incorrect.
        return repetitions
    @staticmethod
    def determine_interval(review_datetime: str) -> int:
        #Ex input: 2025-07-14 22:33:09.344286
        dt = datetime.strptime(review_datetime, "%Y-%m-%d %H:%M:%S.%f")
        past_timestamp = dt.timestamp()
        current_timestamp = time.time()
        return int((current_timestamp-past_timestamp)//86400)
    @staticmethod
    def determine_easiness(path: str) -> float:
        data = FFMAN2.fetch_in_database(path)
        return data[-1][1]
    @staticmethod
    def fetch_in_database(path: str) -> List[List[Union[int,float,int,int,str]]]:
        #Input: path of file
        #Output: quality (int), easiness (float), interval (int), repetitions(int), review_datetime(str)
        output_entries: List[List[Union[int,float,int,int,str]]] = []
        dbcontents: List[Tuple[Union[int,float,str,str]]] = []
        if not os.path.exists('data.db'):
            FFMAN2.create_database() #If database does not exist, call upon the create database function.
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT quality, easiness, review_datetime, path FROM logs WHERE entry_type = "review_log" AND path = ? ORDER BY id ASC',(path,))
            for data in cur:
                dbcontents.append(data) #We need to close the connection ASAP, so we'll just put all of the data in this list.
        for output_entry in dbcontents:
            if output_entry:
                try:
                    #We are repacking the contents of cur (database cursor) into a list, so that we may return the contents.
                    quality = int(output_entry[0])
                    easiness = float(output_entry[1])
                    review_datetime = str(output_entry[2])
                    interval = FFMAN2.determine_interval(review_datetime)
                    repetitions = FFMAN2.determine_repetitions(path)
                    output_entries.append([quality,easiness,interval,repetitions,review_datetime])
                except (ValueError or IndexError) as e:
                    on_error('1', f'Data type error happened when Fetch in Database tried to repack a database entry. Check Database integrity.{str(e)}')
        return output_entries

    @staticmethod
    def log_review_completion(path: str,correctness: int)-> None:
        if not os.path.exists('data.db'):
            FFMAN2.create_database()
        if not os.path.exists(path): on_error('1','Invalid path given to log_review_completion') #If path doesn't exist, throw error.
        if not FFMAN2.fetch_in_database(path):#If there are no database entries, we use first review instead.
            sm2dict = sm2.first_review(correctness)
            easiness, interval, repetitions, review_datetime = sm2dict['easiness'], sm2dict['interval'], sm2dict['repetitions'], sm2dict['review_datetime']
        else: #If there are database entries, we need to do a bit more work. review( quality, easiness, interval, repetitions, review_datetime=None )
            quality = correctness
            easiness = FFMAN2.determine_easiness(path)
            repetitions = FFMAN2.determine_repetitions(path)
            sm2dict = sm2.review(quality,easiness,repetitions)
            #sm2dict has format: {'easiness': 1.4000000000000001, 'interval': 6, 'repetitions': 2, 'review_datetime': '2025-07-21 06:05:35'}
            easiness, interval, repetitions, review_datetime = sm2dict['easiness'], sm2dict['interval'], sm2dict['repetitions'], sm2dict['review_datetime']
        #FORMAT: id(int), entry_type(str), quality(int), easiness(float), review_datetime(str), path(str)
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute(
                '''INSERT INTO logs (entry_type,quality,easiness,review_datetime,path) VALUES ('review_log',?,?,?,?)''',
                (correctness, easiness, review_datetime, path))
            conn.commit()
        return

    @staticmethod
    def scan_for_review(root: str='saves') -> list:
        question_paths = []
        for root, dirs, file in os.walk(root):
            if file:
                for filename in file:
                    if 'ffq1' in filename:
                        question_path = (str(root)+'/'+str(filename)) #add relative path
                        #print(question_path,"is being scanned for database entries")
                        if FFMAN2.check_if_pending_review(question_path):
                            question_paths.append(question_path)
        return question_paths
    @staticmethod
    def check_if_pending_review(question_path: str) -> bool: #This checks if a given review card was reviewed recently:
        data = FFMAN2.fetch_in_database(question_path)
        if data:
            most_recent_timestamp = data[-1][4]
            unix_timestamp = int(datetime.strptime(most_recent_timestamp, '%Y-%m-%d %H:%M:%S.%f').timestamp())
            right_now = str(datetime.utcnow())
            unix_now = int(datetime.strptime(right_now, '%Y-%m-%d %H:%M:%S.%f').timestamp())
            #If unix_timestamp is less than unix_now, that means that it's pending, as it's in the past.
            return unix_timestamp < unix_now
        else:
            return True

    @staticmethod
    def fetch_all_pending() -> list:
        reviewable_list = []
        all_questions =FFMAN2.scan_for_review()
        for question_file in all_questions:
            if FFMAN2.check_if_pending_review(question_file):
                reviewable_list.append(question_file)
        return reviewable_list

    @staticmethod
    def log_chunk_completion(chunk_path: str) -> None:
        if not os.path.exists('data.db'):
            FFMAN2.create_database()
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute(
                '''INSERT INTO learned (chunk_path) VALUES (?)''',
                (chunk_path,)
            )

class ManifestHandler: #This will handle the processing of manifests and whatnot.
    @staticmethod
    def scan_for_manifests(directory: str = 'saves') -> List[List[str]]: #Scans for manifests in the saves directory, returns paths
        lesson_manifest_list = []
        chunk_manifest_list = []
        for root, dirs, files in os.walk(directory):
            #print(files)
            if 'manifest' in str(files) and '.txt' in str(files):
                filename = files[0]
                if str(root).count(os.path.sep) == 1: #We're just going to count the amount of slashes or whatever to know if it's a chunk manifest or a lesson manifest.
                    lesson_manifest_list.append(os.path.join(root,filename))
                elif str(root).count(os.path.sep) == 2:
                    chunk_manifest_list.append(os.path.join(root,filename))
                else:
                    on_error(1,'Scan_for_manifests believes that the saves directory is faulty.')
        return [lesson_manifest_list,chunk_manifest_list]
    @staticmethod
    def evaluate_manifest(manifest_path: str,completed_paths: list = [str]):
        completed_paths = [strip_path(path) for path in completed_paths]
        accessible_paths = [] #Note: Completed paths are ones that the user has already learned. Accessible ones are the ones that the user is now able to learn.
        with open(manifest_path) as manifest:
            for clause in manifest:
                #[Lesson] "REQUIRES" [Lesson_Dependency1], [Lesson_Dependency2], [Lesson_Dependency3], etc
                clause = clause.replace(',','')
                clause = clause.replace('\n','')
                clause_as_list = clause.split(' ')
                clause_as_list = [clause for clause in clause_as_list if clause]
                if len(clause_as_list) == 2:
                    accessible_paths.append(clause_as_list[0]) #If there is no dependencies, unlock it.
                else:
                    accessible_or_not = True
                    for dependency in clause_as_list[2: ]:
                        if dependency not in completed_paths:
                            accessible_or_not = False
                    if accessible_or_not:
                        accessible_paths.append(clause_as_list[0])
            return accessible_paths

    @staticmethod
    def get_available_chunks() -> List[str]:
        """
        Returns a list of chunk manifests for
        """
        #Step 1: Get all lesson manifests in topic directory
        lesson_manifests = ManifestHandler.scan_for_manifests()[0]
        #Step 2: Remove lesson manifests that do not have any accessible lessons
        valid_lesson_manifests = [lesson_manifest for lesson_manifest in lesson_manifests if ManifestHandler.evaluate_manifest(lesson_manifest)]

        #Step 3: If the lesson manifest in the topic directory is valid, then the topic directory is valid.
        valid_topic_directories = [os.path.split(valid_lesson_manifest)[0] for valid_lesson_manifest in valid_lesson_manifests]
        if not valid_topic_directories:
            return []
        # We now need to find a valid chunk manifest (which is found within a lesson directory, as opposed to the lesson manifest which is in the topic directory)

        #Step 4: Get all lesson directories within valid topic directories.
        lesson_directories = [get_immediate_child_directories(valid_topic_directory) for valid_topic_directory in valid_topic_directories]
        #> [['saves/TopicExample/LessonExample'], ['saves/Topic/Lesson']]
        if isinstance(lesson_directories[0],list):
            lesson_directories = flatten_list(lesson_directories)
        #Step 5: Check if these lesson directories have a valid chunk manifest inside of them
        valid_lesson_directories = [lesson_path for lesson_path in lesson_directories if ManifestHandler.scan_for_manifests(lesson_path)[1]]

        #Step 6: Get available chunks from these directories and return them.
        available_chunk_manifests = []
        for directory in valid_lesson_directories:
            chunk_manifests = ManifestHandler.scan_for_manifests(directory)[1]
            for manifest in chunk_manifests:
                if manifest:
                    chunk_manifests = ManifestHandler.evaluate_manifest(manifest)
                    chunk_manifests = [os.path.join(directory,manifest) for manifest in chunk_manifests] #God bless list comprehensions. Sorry if this function has too many of them, but I'm learning this stuff and weaving it into my brain the more I use them.
                    available_chunk_manifests = available_chunk_manifests + chunk_manifests
        return available_chunk_manifests
class Menu:
    @staticmethod
    def answer_questions(topic: str = 'all') -> List[str]:
        if topic != 'all':
            return FFMAN2.scan_for_review(topic)
        else:
            return FFMAN2.fetch_all_pending()


    @staticmethod
    def main_menu() -> str:
        choice = menu("Learn a lesson","learn_lesson","Make new lesson","create_new_lesson","Answer Questions", "answer_questions", "Perform self-check", 'self_check',"Exit the program", 'exit')
        if choice == 'answer_questions':
            questions_to_ask = Menu.answer_questions('all')
            for question in questions_to_ask:
                Menu.ask_question(question)
            print("Finished asking questions.")
        else:
            eval('Menu.'+choice+'()')
        return 'Menu.main_menu()'
    @staticmethod
    def exit():
        print("Exiting program...")
        exit()
    @staticmethod
    def create_new_lesson():
        assembler.main()
    @staticmethod
    def self_check():
        self_check() #Just an alias
    @staticmethod
    def ask_question(path: str) -> bool: #True if they got it correct, False if they didn't.
        if not QProc.fetch_question(path):
            raise Exception(f'Question fetch failed, as there is no question at the given path. {path}')
        question,answer = QProc.fetch_question(path)
        print(question)
        print("Please type your response:")
        response = input()
        print('The answer was:',answer)
        if not response:
            #Didn't even try. Lowest possible score.
            print("You did not provide an answer. Program will assume an incorrect answer.")
            FFMAN2.log_review_completion(path,0)
            return False
        else:
            is_perfect = QProc.is_perfect(response, answer)
        if is_perfect:
            print("Perfect score! Moving to the next question...")
            FFMAN2.log_review_completion(path, 5)
        else:
            print("The Algorithm™ believes your response was imperfect.")
            print("Please type in your score from 1-5. (5/5 is perfect)") #0/5 is reserved for when user doesn't even try.
            while True:
                manual_score = input()
                if manual_score.isnumeric() and int(manual_score) in range(1,6):
                    manual_score = int(manual_score)
                    FFMAN2.log_review_completion(path,manual_score)
                    if int(manual_score) >= 3:
                        return True
                    else:
                        return False
                else:
                    print("Your input is invalid. Try again.")
    @staticmethod
    def display_lesson(lesson_path):
        with open(lesson_path) as text_file:
            for line in text_file:
                print(line)
            print("Press ENTER to continue to questions.")
            input()

    @staticmethod
    def learn_lesson() -> bool or str:
        """
        It has ManifestHandler get available chunks, checks if it's pending with check if completed,
        has Menu display the lesson, and then scans for questions, and has ask_question ask the questions.
        In the event that the questions it discovers are invalid, it will discard the error and remove the question from the list.
        :return:
        """
        print("Alright! Time to learn something new.")
        available_chunk_manifests = ManifestHandler.get_available_chunks()
        def has_content_file(chunk_directory:str) -> bool or str:
            content_path = os.path.join(chunk_directory,'content.txt')
            if not os.path.exists(content_path) or '.txt' not in content_path:
                return False
            else:
                return content_path


        for chunk_dir in available_chunk_manifests:
            chunk_path = has_content_file(chunk_dir)
            if chunk_path and not FFMAN2.check_if_completed(chunk_path): #Check that chunk_path isn't blank and that it's hasn't already been completed.
                Menu.display_lesson(chunk_path)
                question_list = FFMAN2.scan_for_review(os.path.split(chunk_dir)[0])
                for question in question_list: #Ask all questions in this chunk, don't stop until they get it all correct at least once.
                    while question_list:
                        try:
                            Menu.ask_question(question)
                        except Exception as e:
                            pass
                        finally:
                            question_list.remove(question)
                #Now they've answered all of the questions!
                #So we'll log that the chunk is complete.
                FFMAN2.log_chunk_completion(chunk_path)




