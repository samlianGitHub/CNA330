# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
#CNA 330 2nd quarter
.
# I work with groups & Gabe And Abdu Mohammed, 
#jobhunter Assignment
#Samuel Lian slian@Student.rtc.edu
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

def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                   host='127.0.0.1',
                                   database='cna330')
    return conn


# Create the table structure
def create_tables(cursor, table):


    cursor.execute('CREATE TABLE IF NOT EXISTS JobHunter (ID integer,Type varchar(10),Title varchar(100),Description Text,'
                     'Job_id varchar(20),Created_at TIMESTAMP,Company varchar(100),'
                   "Location varchar(100),How_to_apply varchar(100)")

# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor


# Add a new job here
def add_new_job(cursor, jobdetails):
    query = cursor.excute("INSERT INTO job(Type,Title,Description,Job_id,Created_at,Company,Location,How_to_apply) values(10,"
                  "'Full_time,C# Developer','looking for exceptionally motivated candidates',"
                  " '33','2019-10-31 22:52:29', 'Microsoft Corporation','Redmond','https://www.microsoft.com/en-us/')")

    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in ())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in ())

    query = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('job', columns, values)

    cursor.execute(query, query.values())


# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ## Add your code here
    #query = "SELECT * FROM job ;"
   # return query_sql(cursor, query)

    check_Query = ("SELECT EXISTS(SELECT * FROM Jobs WHERE %(id)s)")
    return query_sql(cursor, check_Query)

# Update
def delete_job(cursor, jobdetails):
    ## Add your code here
    query = "UPDATE   SET id = 1, type = ?, title = ?, description = ?, job_id = ?, created_at = ?," \
            " company = ?,location = ?, how_to_apply = ? WHERE id = 1"
    return query_sql(cursor, query)
#delete
    job_id = get_job_id(cursor, jobdetails)
    query = '''DELETE FROM %s WHERE %s=%s''' % ("jobs", "id", job_id)
    return query_sql(cursor, query)


# Grab new jobs from a website
# refrence https://stackoverflow.com/questions/20299088/print-web-page-source-code-in-python
def fetch_new_jobs(cursor, arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?description=&location=washington"
    query = "https://jobs.github.com/positions.json?" + "location=seattle "      # Add arguments here

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


# Load a text-based configuration file
def load_config_file(filename):
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
    jobdetails = {'host': '127.0.0.1',
                  'user': "root",
                  'password': '',
                  'db': 'cna330'}
    return argument_dictionary,jobdetails
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req= urllib.request.Request(url,data)
    return argument_dictionary


# Main area of the code.
def jobhunt(arg_dict):
    # Fetch jobs from website
   
    jobpage = fetch_new_jobs(arg_dict)
    #print(jobpage)
    with urllib.request.urlopen("https://jobs.github.com/positions.json?location=seattle") as url:
        json_data = json.loads(url.read().decode())
    # print(json_data)
    sing = (json.dumps(json_data, indent=4, sort_keys=True))
    with open('job.txt', "w") as text_file:
        text_file.write(sing)
        # print(sing)
        with open('job.txt', 'r') as searchfile:
            for line in searchfile:
                if re.search(r'"id"', line, re.M | re.I):
                    print(line)
        with open('job.txt', 'r') as searchfile:
            for line in searchfile:
                if re.search(r'"type"', line, re.M | re.I):
                    print(line)

        with open('job.txt', 'r') as searchfile:
            for line in searchfile:
                if re.search(r'"description"', line, re.M | re.I):
                    print(line)
    ##ref:https://stackoverflow.com/questions/30326562/regular-expression-match-everything-after-a-particular-word?rq=1
        ## Add in your code here to check if the job already exists in the DB

def already_exist(cursor):
        text = 'job.txt'
        cursor.execute("SELECT job_id, COUNT(*) FROM jobinfo WHERE job_id = %s GROUP BY job_id", (text,))

        msg = cursor.fetchone()
        if msg:
            print('already exists')

        if not msg:
            print('It does not exist')
    ## Add in your code here to notify the user of a new posting
def new_psoting():
    saved_time_file = 'last time check.txt'
    url = 'https://jobs.github.com/positions.json?location=seattle'

    request = urllib.request
    if os.path.exists(saved_time_file):
        """ If we've previously stored a time, get it and add it to the request"""
        last_time = open(saved_time_file, 'r').read()
        urllib3.make_headers("If-Modified-Since", last_time)

    try:
        response = urllib.request.urlopen(url)  # Make the reques
    except urllib.request.HTTPError as err:
        if err.code == 304:
            print("Nothing new.")
            sys.exit(0)
        raise  # some other http error (like 404 not found etc); re-raise it.

    last_modified = response.info().get('Last-Modified', False)
    if last_modified:
        open(saved_time_file, 'w').write('last_modified')
    else:
        print("Server did not provide a last-modified property. Continuing...")
    ## EXTRA CREDIT: Add your code to delete old entries
def delete_old(cursor, conn):
    try:
        sql="DELETE FROM jobinfo WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 DAY)"

        try:
            cursor.execute(sql)
            conn.commit()
            print("Deleted Older Data from database")

        except:
            conn.rollback()
            print("Cann't delete older data")
            cursor.close()

    except:
                print("localserver not connected")

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "table")
    # Load text file and store arguments into dictionary
    arg_dict = 0
    while (1):
        jobhunt(arg_dict)
        time.sleep(3600)  # Sleep for 1h


if __name__ == '__main__':
    main()
