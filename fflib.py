#Library for FarFetched
#Shamelessly reuse code from previous projects, for efficiency
import sys, os, time, sqlite3, sm2
from typing import List, Union, Tuple #I was told my stuff's more readable if I use this.
from datetime import datetime
required_files = ['main.py','fflib.py','__init__.py','sm2.py']
required_directories = ['assets', 'saves']
def on_error(severity='1', error_message="No error message was provided"):
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

def make_boolean(string):  # Converts string literals to booleans
    if 'bool' in str(type(string)):
        return string #Return to sender
    string = string.lower()
    if string == 'true':
        return True
    elif string == 'false':
        return False
    else:
        on_error('1', 'make_boolean was given an invalid input.')
        return None #Stupid Pycharm, nagging me.
def menu(*args):
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
def self_check():
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
    def fetch_question(path):
        #The purpose of this function is to extract the question and answer from a path.
        #It may be later updated to work with future question formats, which may have greater functionality.
        if os.path.isfile(path):
            lines = [line.strip() for line in open(path)]
            if 'FF1' in lines[0]:
                question = lines[1]
                answer = lines[2]
                return question, answer
            else:
                on_error('1', 'fetchquestion() is unable to read this file format.')
                return None
        else:
            on_error('1', 'Invalid path given to fetch_question function.')
            return None
    @staticmethod
    def strip_punctuation(string):
        discardables = ['\'', '\"', ',', ' ', ':', ';','-']  # update as needed
        for character in discardables:
            string = string.replace(character,'')
        return string
    @staticmethod
    def extract_keywords(string):
        word_list = string.split(' ')
        keywords = []
        for word in word_list:
            word = word.lower()
            word = QProc.strip_punctuation(word)
            if word:
                keywords.append(word)
        return keywords
    @staticmethod
    def is_correct(responseli, answerli):
        if not isinstance(responseli,list) or not isinstance(answerli,list):
            actual_type = type(responseli)
            if 'str' in str(actual_type):
                responseli = QProc.extract_keywords(responseli)
                answerli = QProc.extract_keywords(answerli)
            else:
                on_error('1', 'Incorrect data type given to QProc.iscorrect()')

        correct_keywords = 0
        incorrect_keywords = 0
        for keyword in answerli:
            if keyword in responseli:
                correct_keywords += 1
                #print(keyword,"is correct")
            else:
                incorrect_keywords +=1
                #print(keyword,"is incorrect")
        #The previous portion of code determines how many keywords were correct, and how many were incorrect.
        #We will now determine whether we will accept this answer.
        correctness_threshold = 0.6 #We will accept 60% or higher accuracy. Keep in mind that user will be able to override this crude algorithm.
        if correct_keywords / (correct_keywords+incorrect_keywords) >= correctness_threshold:
            return True
        else:
            return False
def topiclist():
    topicli = os.listdir('saves')
    nutopicli = [] #All of this is just to make the menu command.
    for x in topicli:
        nutopicli.append(x)
        nutopicli.append(x)
    #menu("topic1","topic1","topic2","topic2")
    param_head = "menu(\""
    param_body = '\",\"'.join(nutopicli)
    param_tail = "\")"
    complete_command = param_head + param_body + param_tail
    #Everything we've done in those lines above is set up to execute a menu command listing all of the topics.
    #Now, we'll see which one the users picks.
    try:
        choice = eval(complete_command) #Scary!
    except Exception as e:
        print(complete_command)
        print(f"An error occurred: {e}")
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
            connection.commit()
    @staticmethod
    def determine_repetitions(path: str):
        #This function should really only be used with fetch_in_database, unless you're insane.
        #Ex input: (5.0, 5, 'today', 'saves/topicexample/lessonexample/chunkexample/contentexample')
        dbcontents: List[Tuple[int]] = []
        if not os.path.exists('data.db'):
            FFMAN2.create_database() #If database does not exist, call upon the create database function.
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('''SELECT id,quality FROM logs WHERE path = ?''',(path,))
            for entry in cur:
                dbcontents.append(entry)
        repetitions = 0
        #Right now, DB Contents is a list of tuples with just one integer in them.
        for quality_tuple in dbcontents: #Increment by 1 for every entry that has the path in it.
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
    def fetch_in_database(path: str) -> List[List[Union[int,float,int,int,str]]]:
        #Input: path of file
        #Output: quality (int), easiness (float), interval (int), repetitions(int), review_datetime(str)
        output_entries: List[List[Union[int,float,int,int,str]]] = []
        dbcontents: List[Tuple[Union[int,float,str,str]]] = []
        if not os.path.exists('data.db'):
            FFMAN2.create_database() #If database does not exist, call upon the create database function.
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT quality, easiness, review_datetime, path FROM logs WHERE entry_type = "review_log" AND path = ?',(path,))
            for data in cur:
                dbcontents.append(data) #We need to close the connection ASAP, so we'll just put all of the data in this list.
        for output_entry in dbcontents:
            if output_entry:
                try:
                    #(5.0 (easiness), 5, '2025-03-02 09:12:30.654321', 'saves/topicexample/lessonexample/chunkexample/questions/q1.ffq1')
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
    def log_review_completion(path: str,correctness: int,easiness:str =None)-> None:
        if not os.path.exists('data.db'):
            FFMAN2.create_database()
        if not FFMAN2.fetch_in_database(path):
            #If there are no database entries, we use first review instead.
            sm2dict = sm2.first_review(correctness)
            easiness, interval, repetitions, review_datetime = sm2dict['easiness'], sm2dict['interval'], sm2dict['repetitions'], sm2dict['review_datetime']
            #FORMAT: id(int), entry_type(str), quality(int), easiness(float), review_datetime(str), path(str)
            with sqlite3.connect('data.db') as conn:
                cur = conn.cursor()
                cur.execute('''INSERT INTO logs (entry_type,quality,easiness,review_datetime,path) VALUES ('review_log',?,?,?,?)''',(correctness,easiness,review_datetime,path))
                conn.commit()
            return
        timestamp = datetime.utcnow()
        with sqlite3.connect('data.db') as conn:
            cur = conn.cursor()

    @staticmethod
    def scan_for_review(root='saves'):
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
    def check_if_pending_review(qpath): #This checks if a given review card was reviewed recently:
        if 'list' in str(type(qpath)):
            on_error('1', 'Incorrect usage of check pending review function')
        dbpath = 'assets/data/ffdb'
        is_pending = True #This is the default value, but will change if a record says that it's not actually pending.
        if not os.path.isfile(dbpath): #Check if database exists
            on_error('1', 'Database file not found.')
        lines = [line.strip() for line in open(dbpath)] #We will now read every line from the database
        for line in lines:
            if qpath in line: #Ignore all database entries that to not concern the file we are checking.
                line = line[1:-1] #Cut off the brackets
                line = line.replace('"','')
                line = line.replace('\'','')
                line = line.replace(' ','')
                line = line.split(',') #Turn into a list
                line[2] = make_boolean(line[2])
                line[-1] = int(line[-1])
                #print(line) #This is ugly. Really really ugly. But I don't have internet right now, so I can't google a more elegant solution.
                #Note to self; remove jank
                #In this version, we are not implementing SM2. Instead, we will just use the 1 day timer.
                #['1', 'reviewcomplete', True, 'assets/data/ffdb', 1751767635]
                rn = time.time()
                diff = rn - line[4]
                is_correct = line[2]
                if is_correct: #i.e, false was reported
                    if diff <= 86400: #If it's been a while, then say it's pending review. Otherwise, say there's no need.
                        #In v2, we'll use an algo to determine this, instead of this crude method.
                        is_pending = False
        return is_pending
    @staticmethod
    def fetchallpending():
        reviewableli = []
        allquestions =FFMAN2.scan_for_review()
        for questionfile in allquestions:
            #print(questionfile,"is being checked")
            if FFMAN2.check_if_pending_review(questionfile):
                reviewableli.append(questionfile)
                #print(questionfile,'has been accepted')
        return reviewableli
    @staticmethod
    def fetch_next_review():
        pass
def autolearn(topic='all'):
    if topic != 'all':
        return FFMAN2.scan_for_review(topic)
    elif topic == 'all':
        return FFMAN2.fetchallpending()
    else: return
class Menu:
    @staticmethod
    def main_menu():
        choice = menu("Auto-Learn", "autolearn", "Perform self-check", 'self_check')
        if choice == 'autolearn':
            questions_to_ask = autolearn('all')
            for question in questions_to_ask:
                Menu.ask_question(question)
            print("Finished asking questions.")
        elif choice == 'self_check':
            self_check()
        return 'Menu.main_menu()'
    @staticmethod
    def ask_question(path):
        question,answer = QProc.fetch_question(path)
        print(question)
        print("Please type your response:")
        response = input()
        correctness = QProc.is_correct(response,answer)
        if correctness: #i.e. True
            print("Correct! Moving to the next question...")
            FFMAN2.log_review_completion(path, True)
        else:
            print("The Algorithm™ believes your response was incorrect. Override?")
            override = menu("Override","override","Do not override","nope")
            if override == "override":
                print("Algorithm ignored. Human is supreme. Truth bends to your will.") #What the heck did I just write?
                FFMAN2.log_review_completion(path, True)
            elif override == 'nope':
                FFMAN2.log_review_completion(path, False)
        return
