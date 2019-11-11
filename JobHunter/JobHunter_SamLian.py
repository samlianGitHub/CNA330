# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# Fall 2019 CNA 330
#Samuel Lian , slian@student.rtc.edu
# Sources come from Robin Cunanan , I work with him and he help me a lot
# # I work with groups & A lot help from Robin Cunanan
# #jobhunter Assignment
# #

import mysql.connector
import json
import urllib.request
import time
from datetime import datetime


# Connect to database
# You may need to edit the connect function based on your local settings.
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cna330')
    return conn

# Create the table structure
def create_tables(cursor, table):
    # Creates table
    cursor.execute('''CREATE TABLE IF NOT EXISTS JobsHunter (id INT PRIMARY KEY auto_increment, 
    Type varchar(10), 
    Title varchar(100), 
    Description text CHARSET utf8,
    Job_id varchar(50), 
    Created_at DATE, Company varchar(100), 
    Location varchar(50), 
    How_to_apply varchar(300)); ''')
    return

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, Newquery):
    cursor.execute(Newquery)
    return cursor

# Add a new job
def add_new_job(cursor, jobdetails):
    # extract all required columns
    type = jobdetails['type']
    created_at = time.strptime(jobdetails['created_at'], "%a %b %d %H:%M:%S %Z %Y")  # The Sources code come from https://www.programiz.com/python-programming/datetime/strftime & https://docs.python.org/3/library/datetime.html
    company = jobdetails['company']
    location = jobdetails['location']
    title = jobdetails['title']
    description = jobdetails['description']
    how_to_apply = jobdetails['how_to_apply']
    job_id = jobdetails['id']


    Newquery = cursor.execute("INSERT INTO JobsHunter(Type, "
                              "Title, Description, "
                              "Job_id, Created_at, "
                              "Company, Location, "
                              "How_to_apply" ") "
               "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (type, title, description, job_id, created_at, company, location, how_to_apply))  # The Sources code come from https https://stackoverflow.com/questions/20818155/not-all-parameters-were-used-in-the-sql-statement-python-mysql/20818201#20818201
    return query_sql(cursor, Newquery)

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    job_id = jobdetails['id']
    query = "SELECT * FROM JobsHunter WHERE Job_id = \"%s\"" % job_id
    return query_sql(cursor, query)

# Deletes job
# The Sources code come from  https://www.tutorialspoint.com/mysql/mysql-delete-query.htm
def delete_job(cursor, jobdetails):
    job_id = jobdetails['id']
    query = "DELETE FROM JobsHunter WHERE Job_id = \"%s\"" % job_id
    return query_sql(cursor, query)

# Grab new jobs from a website, Parses JSON code and inserts the data into a list of dictionaries
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?location=seattle"  # "https://jobs.github.com/positions.json?" + "location=seattle" ## Add arguments here #Use & after seattle to do &description=python&full_time=no this is how to chain
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()  # it Loads from config file
        jsonpage = json.loads(response) # checks database, any jobs that find
    except:
        pass
    return jsonpage

# Load a text-based configuration file, not function needed per Zak
"""def load_config_file(filename):  
    argument_dictionary = 0
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path = os.path.abspath(os.path.dirname(__file__))
    file = 0
    file_contents = 0
    try:
        file = open(filename, "r")
        file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()
    ## Add in information for argument dictionary
    return argument_dictionary"""

# Main area of the code.
def jobhunt(arg_dict, cursor):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict)  # Gets github website and holds the json data in it as a list
    # use below print statement to view list in json format
    # print(jobpage)
    add_or_delete_job(jobpage, cursor)


# This will add or delete jobpage
def add_or_delete_job(jobpage, cursor):
    # Add your code here to parse the job page
    for jobdetails in jobpage:  # EXTRACTS EACH JOB FROM THE JOB LIST
        # Add in your code here to check if the job already exists in the DB
        check_if_job_exists(cursor, jobdetails)
        is_job_found = len(cursor.fetchall()) > 0  # https://stackoverflow.com/questions/2511679/python-number-of-rows-affected-by-cursor-executeselect

        #job file
        if is_job_found:  #
            # DELETE JOB
            # EXTRA CREDIT: Add your code to delete old entries
            now = datetime.now()
            job_date = datetime.strptime(jobdetails['created_at'], "%a %b %d %H:%M:%S %Z %Y")
            if (now - job_date).days > 30:  # https://stackoverflow.com/questions/46563442/check-if-dates-on-a-list-are-older-than-2-days
                print("Delete job: " +
                      jobdetails["title"] +
                      " from " + jobdetails["company"] +
                      ", Created at: " + jobdetails["created_at"] +
                      ", JobID: " + jobdetails['id'])
                delete_job(cursor, jobdetails)
        else:
            # INSERT JOB
            # Add in your code here to notify the user of a new posting
            print("New job is found: " +
                  jobdetails["title"] +
                  " from " + jobdetails["company"] +
                  ", Created at: " + jobdetails["created_at"] +
                  ", JobID: " + jobdetails['id'])
            add_new_job(cursor, jobdetails)


# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Important, rest are supporting functions
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "table")
    # Load text file and store arguments into dictionary
    arg_dict = 0
    while(1):  # Infinite Loops.
        jobhunt(arg_dict, cursor)  # arg_dict is argument dictionary,
        time.sleep(3600)  # Sleep for 1h, this is ran every hour.
# Sleep does a rough cycle count, system is not entirely accurate
if __name__ == '__main__':
    main()

