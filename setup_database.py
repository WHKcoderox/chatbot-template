import sqlite3

def fix_single_quote(string): # SQL typically messes up when there's single quotes. The workaround is to make two single quotes.
    limit = len(string)
    i = 0
    while i < limit:
        if string[i] == '\'':
            string = string[:i+1] + string[i:] # this duplicates the single quotes.
            limit += 1
            i += 1 # the next letter becomes a single quote, so it must be ignored.
        i += 1
    return string

# this sets up a connection to the database and creates all the tables based on the inputs you put into the text file.
connection = sqlite3.connect("./inputs.sqlite3", isolation_level = None )

cursor = connection.cursor()

hardcoded_inputs_file = open("./hardcoded_inputs.txt")

curr_table = ""
for line in hardcoded_inputs_file.readlines():
    check = line.split(',')
    if len(check) > 1 and check[0] == 'T': # anything with 'T,' will register here.
        # table header. Should always come first.
        curr_table = line[2:-1] # remove the newline char and the 'T,'
        try:
            cursor.execute("CREATE TABLE " + curr_table + " (input text)")
        except sqlite3.OperationalError: # this will happen if the table already exists.
            cursor.execute("DELETE FROM " + curr_table) # clears the data already existing in the table so the new data overwrites it.
            cursor.execute("VACUUM") # frees up unused space.
    else: # word
        # important: added in inverted commas to ensure that the value you pass in is seen as a string to SQL.
        cursor.execute("INSERT INTO " + curr_table + "(input) VALUES (\'" + fix_single_quote(line[:-1]) + "\')") # again, remove the newline char.

# close file connections. commit changes.
connection.commit()
hardcoded_inputs_file.close()
connection.close()
