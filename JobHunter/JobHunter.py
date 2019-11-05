# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
#CNA 330 2nd quarter

# I work with groups & Gabe And Abdu Mohammed,
#jobhunter Assignment
#Samuel Lian slian@Student.rtc.edu
from idlelib import query

import mysql.connector
import sys
import json
import urllib.request
import os
import time
import re
import urllib3
import urllib.parse
import urllib.error
#

# Connect to database
# You should not need to edit anything in this function
from cursor import cursor


def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1',
                                   database='cna330')
    return conn

# Create the table structure
def create_tables(cursor, table):
    ## Add your code here. Starter code below
    cursor.execute('''CREATE TABLE IF NOT EXISTS JobsH (
        ID int NOT NULL PRIMARY KEY AUTO_INCREMENT, 
        Type varchar(10),
        Title varchar(100),
        Description text,
        Job_id varchar(33),
        Created_at DATE,
        Company varchar(100),
        Location varchar(50),
        How_to_apply varchar(100)); ''')
    return


# Add a new job
#insert_stmt = (
   ## "INSERT IGNORE INTO JobsH (Type, Title, Location, Description, Job_id, Company, Location) "
    #"VALUES (%(created_at)s, %(title)s, %(location)s, %(description)s, %(how_to_apply)s, %(id)s)"
#)

# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in ())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in ())

    # Add a new job here
    def add_new_job(cursor, jobdetails):
        query = cursor.excute(
            "INSERT INTO JobsH (Type,Title,Description,Job_id,Created_at,Company,Location,How_to_apply) values(10,"
            "'Full_time,C# Developer','looking for exceptionally motivated candidates',"
            " '33','2019-10-31 22:52:29', 'Microsoft Corporation','Redmond','https://www.microsoft.com/en-us/')")

    query = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('JobsH', columns, values)

    cursor.execute(query, query.values())

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ## Add your code here
    Query = ("SELECT EXISTS(SELECT * FROM JobsH WHERE %(id)s)")
    return query_sql(cursor, Query)


# Update
def delete_job(cursor, jobdetails):
    ## Add your code here
    query = "UPDATE   SET id = 1, type = ?, title = ?, description = ?, job_id = ?, created_at = ?," \
            " company = ?,location = ?, how_to_apply = ? WHERE id = 1"
    return query_sql(cursor, query)
    # delete
    job_id = get_job_id(cursor, jobdetails)
    query = '''DELETE FROM %s WHERE %s=%s''' % ("JobsH", "id", job_id)
    return query_sql(cursor, query)


# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?location=%s&description=%s" % (arg_dict[1], arg_dict[3])
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)
    except:
        print("whoops")
        pass
    return jsonpage

# Load a text-based configuration file
def load_config_file(filename):
    argument_dictionary = ""
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path = os.path.abspath(os.path.dirname(__file__))
    file_contents = 0

    jsonpage = 0
    contents = urllib.request.urlopen(query)
    response = contents.read()
    jsonpage = json.loads(response)
    for page in jsonpage:
        print(page['location'])
        page['description'] = str(page['description']).replace('\"', '')
        page['how_to_apply'] = str(page['description']).replace('\"', '')
        cursor.execute('''INSERT INTO Jobs (type, Title, Location, Description, Company, Apply_info) VALUES (
         "''' + page['created_at'] + '''",
         "''' + page['title'] + '''",
         "''' + page['location'] + '''",
         "''' + page['description'] + '''",
         "''' + page['company'] + '''",
         "''' + page['how_to_apply'] + '''")''')

    try:
        file = open(filename, "r")
        file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()

    for row in file_contents:
        argument_dictionary += row
    return argument_dictionary

# Main area of the code.
def jobhunt(cursor, arg_dict):
    jobpage = fetch_new_jobs(arg_dict)
    for job in jobpage:
        if check_if_job_exists(cursor, job):
            continue
            add_new_job(cursor, job)
    return jobpage


# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    fields = ["id", "Type", "Title", "Description," , "Job_id,Created_at", "Company", "Location,How_to_apply"]
    conn = connect_to_sql()
    cursor = conn.cursor()
    arg_dict = load_config_file(sys.argv[1]).split('\n')
    create_tables(cursor, arg_dict[0], fields)
    jobhunt(cursor, arg_dict)


if __name__ == '__main__':
    main()
