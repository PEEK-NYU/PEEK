"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import json
import os
import copy

PEEK_DIR = os.environ["PEEK_DIR"]
TEST_MODE = os.environ.get("TEST_MODE") == "True"

if TEST_MODE:
    DB_DIR = f"{PEEK_DIR}/db/test_dbs"
else:
    DB_DIR = f"{PEEK_DIR}/db"

EVENT_COLLECTION = f"{DB_DIR}/events.json"
USER_COLLECTION = f"{DB_DIR}/users.json"

shell_event = {"name": "shell event name",
               "descr": "",
               "start_time": 0,  # thoughts of datetime.Ticks conversion
               "end_time": 0,
               "duration": 0,
               "location": "2 Metrotech",
               "unscheduled": False,
               "break": False,
               "owner": "",
               "attendees": []}

# Note: username is the unique key so its not in the structure
shell_user = {"username": "shell user name",
              "email": "",
              "password": "",
              "google_key": "",
              "events": []}

OK = 0
NOT_FOUND = 1
DUPLICATE = 2


def write_collection(perm_version, mem_version):
    """
    Write out the in-memory data collection in proper DB format.
    """
    with open(perm_version, 'w') as f:
        json.dump(mem_version, f, indent=4)


def read_collection(perm_version):
    """
    A function to read a colleciton off of disk.
    """
    try:
        with open(perm_version) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        print(f"{perm_version} not found.")
        return None


def get_events():
    """
    A function to return a dictionary of all events.
    """
    return read_collection(EVENT_COLLECTION)


def get_users():
    """
    A function to return a dictionary of all users.
    """
    return read_collection(USER_COLLECTION)


def add_event(event_traits):
    """
    Add a events to the events database.
    Until we are using a real DB, we have a potential
    race condition here.
    - event_traits is a collection of info for the event
    - event_traits must include "name" for now
    """
    events = get_events()
    if "name" in event_traits:
        like_events = find_name(events, event_traits["name"])
        if len(like_events) > 0:
            return DUPLICATE
    else:
        return NOT_FOUND
    if events is None:
        return NOT_FOUND
    else:
        # Note: once db is chosen this will be autogenerated
        new_event_info = copy.deepcopy(shell_event)
        for trait, value in event_traits.items():
            new_event_info[trait] = value
        # new_event_info["name"] = eventname
        # eventname doubles as a key in this case
        events[event_traits["name"]] = new_event_info
        write_collection(EVENT_COLLECTION, events)
        return OK


def add_user(username):
    """
    Add a user to the user database.
    Until we are using a real DB, we have a potential
    race condition here.
    """
    users = get_users()
    like_users = find_name(users, username)
    if users is None:
        return NOT_FOUND
    elif len(like_users) > 0:
        return DUPLICATE
    else:
        new_user_info = copy.deepcopy(shell_user)
        new_user_info["name"] = username
        users[username] = new_user_info
        write_collection(USER_COLLECTION, users)
        return OK


def find_name(collection, name):
    """
    A function that returns a list of ids...
    within a collection by "name".
    """
    found_lst = []
    for key, value in collection.items():
        if value["name"] == name:
            found_lst.append(key)
    return found_lst


# function templates/shells for integration with google cal
def get_scheduling_options(user_schedule, common_events):
    """
    Input: the user's schedule for the requested time range
    Input: list of other scheduled events of the same type/group
    Output: list of recommended event times
    """
    return
