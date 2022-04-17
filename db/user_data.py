"""
This file will manage interactions with the user and their data

Sample of User Architecture for Refrence:
{
  "user_data" :
  {
    "_id": {
      "username": "Fake User",
      "password": "123",
      "email": "catslovecats@gmail.com"
    }
  }
}

OLD Mongo List Ref:
[{'_id': {'$oid': '624e03449ed2db7f77aaf5b1'},
  '0YAFQ1ABPM': {'username': 'user name 2728518203020duso2jkdna4oiha FAKE_KEY aebj0kfho1iuj5na',
                 'password': 'password 6921355629683',
                 'emails': 'test@testemail.com'}},
 {'_id': {'$oid': '624f0a9be96c27ac380a17e3'},
  '0TELC3OQMF': {'username': 'user name 9147374907469duso2jkdna4oiha FAKE_KEY aebj0kfho1iuj5na',
                 'password': 'password 234608589154',
                 'emails': 'test@testemail.com'}}
]
"""

import os
import db.db_connect as dbc
# import db.event_data as edata
import db.connect_data as cdata


AUTOCAL_HOME = os.environ["AUTOCAL_DIR"]
GET_USERS = "user_data"
USERS = "_id"
UNAME = "username"
PW = "password"
EM = "email"

# ref in other _data.py files
OK = 0
NOT_FOUND = 1
DUPLICATE = 2

client = dbc.get_client()
if client is None:
    print("Failed to connect to MongoDB.")
    exit(1)


def get_all_users():  # Note: name change
    """
    A function to return a hashmap of all users.
    (Is this new db structure to be updated for get emails?)
    """
    ret = dbc.fetch_all(GET_USERS, USERS)
    final_dict = {}
    for user_info in ret:
        new_key = user_info[USERS]
        final_dict[new_key] = {UNAME: user_info[UNAME],
                               PW: user_info[PW],
                               EM: user_info[EM]}
    # print("fetched users:", final_dict, "\n")
    return final_dict


def get_user(uid):
    """
    A function to get all a user's info given its user id
    """
    curr_users = get_all_users()
    return curr_users[uid]


def find_user(keyword):
    """
    A function to return a list of users with a username keyword
    """
    curr_users = get_all_users()
    user_list = {}
    for uid, user_info in curr_users.items():
        if keyword in user_info[UNAME]:
            user_list[uid] = user_info
    return user_list


def add_user(username, password, email=""):
    """
    Add a user to the database using username & password
    """
    new_user = {UNAME: username, PW: password, EM: email}
    return dbc.insert_doc(GET_USERS, new_user)  # new uid
# TODO: add functionality to update a user's info/pw


def log_in(username, password):
    """
    Returns uid given a user's username and password
    """
    curr_users = get_all_users()
    for uid, info in curr_users.items():
        if info[UNAME] == username and info[PW] == password:
            return uid
    return NOT_FOUND


def user_exists(uid):
    """
    A function that checks if a user exists
    """
    curr_users = get_all_users()
    if uid in curr_users.keys():
        return OK
    return NOT_FOUND


def del_user(uid):
    """ deletes a user and all related events """
    # curr_users = get_all_users()
    if user_exists(uid) is NOT_FOUND:
        return NOT_FOUND
    cdata.del_events_by_user(uid)
    dbc.del_one(GET_USERS, filters={USERS: uid})
    return OK

def user_update(doc,new_name):
    """Updates user's name ** TO DO: Add more updates"""
    if user_exists(uid) is NOT_FOUND:
        return NOT_FOUND
    res = GET_USERS._update_document_single_field(uid, UNAME, new_name, "None") # (temporary), none in position of where the "parent" would be and uid in place of doc
    return OK

def get_emails():
    """
    A function to return a list of all emails.
    """
    curr_users = get_all_users()
    em_lst = []
    for uid, info in curr_users.items():
        em_lst.append(info[EM])
    return em_lst
    # Note: USER_DATA previously refrenced


def email_exists(email):
    """
    returns True if email exists
    TODO: fix with new db structure
    """
    rec = dbc.fetch_one(GET_USERS, filters={EM: email})
    # print(f"{rec=}")
    if rec is not None:
        return OK
    return NOT_FOUND
