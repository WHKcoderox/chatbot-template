from datetime import datetime
import sqlite3
import os
my_dir = os.path.dirname(__file__) # for accessing files.

class ChatBot:

    def newline_to_br(string):
        for i in range(len(string)):
            if string[i] == '\n': # check for newline char
                string = string[:i] + "<br>" + string[i+1:] # replace the newline character with br tag

        return string

    def __init__(self): # when an instance/copy of ChatBot is made, this function will run. i.e. when calling the function ChatBot()
        # accepted_messages maps incoming messages to
        # list of callback functions
        self.accepted_messages = {}

        # time of instantiation
        self.birth_time = datetime.now()

        inputs_db_path = os.path.join(my_dir, 'inputs.sqlite3')
        connection = sqlite3.connect(inputs_db_path)

        cursor = connection.cursor()

        # I took this from the internet, this should work.
        tb_names = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

        # this has to be hardcoded, no way around this I suppose.
        name_callback_map = \
        {
            "greetings" : self.respond_to_greeting,
            "valedictions" : self.respond_to_departure # make sure to add commas ( , ) after each callback.
            # "add_whatever_table_name_here" : self.sample_callback
        }

        # Something like this can register all callbacks
        for table in tb_names:
            # table is probably a tuple or something, albeit of size 1.
            # just pretend the [0] wasn't there.
            responses = cursor.execute("SELECT input FROM "+table[0]+';')
            for response in responses:
            	callback = name_callback_map[table[0]]
            	self.register_callback(response[0], callback)

        connection.close() # when you're done, close the connection.

    def register_callback(self, message, callback):
        """
        Registers a callback to a message.
        """
        if message not in self.accepted_messages:
            self.accepted_messages[message] = []
        self.accepted_messages[message].append(callback)

    def respond_to_greeting(self):
        return ("Hello!")

    def respond_to_departure(self):
        return ("Nice chatting with you!")

    def respond_to_age_request(self):
        age = datetime.now() - self.birth_time
        return ("I am " + str(age.seconds) + " seconds old.")

    def respond_to_age_request_detailed(self):
        age = datetime.now() - self.birth_time
        micros = age.microseconds
        return ("Technically, I'm " + str(age.seconds) + " seconds and " +
              str(micros) + " microseconds old")

    def handle_message(self, message):
        if message not in self.accepted_messages:
            return ("Sorry, I don't understand \'" + message + "\'")
        else:
            callbacks = self.accepted_messages[message]
            for callback in callbacks:
                return callback()

# main - run whatever testing code you want here.
cbot = ChatBot()
test_msgs = ["hello", "byebye", "ahahaha"]
for test_msg in test_msgs:
    cbot.handle_message(test_msg)
