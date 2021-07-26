import pymysql
import re
import config
import time
import hashlib
import os

mydb = pymysql.connect(host="localhost",
                      user=config.MYSQL_USER, password=config.MYSQL_PASS, db='mailpass')

mycursor = mydb.cursor() #cursor created

regexp = re.compile("([\w]+@[^:\n]*\.[^:\n]*):(.*)( \| .*)?\n?", )
input = input('File with combo:\n')
today = time.strftime("%Y-%m-%d")

# TODO Insert information about file to database

def get_file_hash():
    with open(input, 'rb') as f:
        fbytes = f.read()
        hash = hashlib.sha256(fbytes).hexdigest()
        return(hash)
hash = get_file_hash()
name = os.path.basename(input)
print(name, hash)
# checking if the file exist
file_exist = f"SELECT file_id from files WHERE file_hash = '{hash}'"
mycursor.execute(file_exist)
file_id = mycursor.fetchall()

if file_id == None:
    print("File don't exist in database. I'll add it.")
    create_file = f"INSERT INTO files (file_name, file_hash, date_add) VALUES ('{name}', '{hash}', '{today}')"
    mycursor.execute(create_file)
else:
    print("File already added with id:", file_id[0][0])
    file_id = file_id[0][0]
    print(file_id)


# TODO Get file_id from table with hash


# Add records from file
with open(input, 'r') as f:
    lines = f.read()
    list = regexp.finditer(lines)
    for i in list:
        mail = i.group(1)
        password = i.group(2)

        add_to_db = f'INSERT IGNORE INTO combo_valid (email, password, date_checked) VALUES ("{mail}", "{password}", "{today}")'
        mycursor.execute(add_to_db)
        print(mail, password)


mydb.commit()
mydb.close()





""" All my queries
create database mailpass;
CREATE TABLE combo_valid (combo_id int AUTO_INCREMENT, email varchar(500) NOT NULL, password varchar(200) NOT NULL, date_checked date, PRIMARY KEY (combo_id));
ALTER TABLE combo_valid ADD CONSTRAINT unique_only UNIQUE (email,password);
CREATE TABLE files (file_id int auto_increment, file_name varchar(300), file_hash char(64) UNIQUE, PRIMARY KEY (file_id));
ALTER TABLE files ADD COLUMN date_add date;
"""
