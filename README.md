# PEEK ~ (Paul, Ethan, Elizabeth, Kora)
#### This is the main repository of our Software Engineering project as part of CS-UY 4513 section C.
![](https://app.travis-ci.com/PEEK-NYU/PEEK.svg?branch=main)

#### HEROKU:  https://peek-nyu.herokuapp.com/
#### TRAVIS:  https://app.travis-ci.com/github/PEEK-NYU/PEEK

### **Note: For some of the event/break tests we included code to insert sample data at the beginning of the test. This is because the list functions for event/break look for a username that we specify in the test. So we created sample data for that specific username to ensure the test would work without having figure out the username yourself and add in data manually.**

## Project Idea:
* A website that aids users in scheduling events. Website uses existing calendar data and suggests the best time for an event.
* Story: User wants to schedule a study time. User imports an .ics file into software, types in some quick event information if wanted, and presses a button. The software then outputs an .ics file with the new event, which the user imports into their calendar software of choice.
* Advanced Features:
* * Automation of .ics import/export via google calendar login credentials
* * Software has suggested time-slots and learns the user's habits based on software use
* * Software categorizes events by type (study time, break time, etc.)
* * User can customize software's suggestions by event type

## Requirements:
**Database** 
(note: for simplicity, all ints are positive where 0 represents an uninitialized value.)

User Table
* _user_id (string) //unique database key
* username (string)  
* password (string)

Event Table
* _event_id (string) // unique database key
* eventname (string)  // imported information via <a href="https://fileinfo.com/extension/ics"> .ics </a> specific <a href="https://icalendar.readthedocs.io/en/latest/"> structures </a>
* location (string)
* start_time (datetime)
* end_time (datetime)
* description (string)

Connection Table
* _event_id (string) // unique database key
* _user_id (string) // unique database key

**Create**
1. Users can create an account with a username, password, google_key, and profile pic (username must be unique).
2. Users can create a break during which no events will be scheduled. The user would specify a given time period for the break and name the break.
3. Users can import events from their Google Calendar. These events passed in from Google Calendar have a _id, eventname, location, start_time, end_time, description, owner, and attendees
4. Users can add an event with an _id (autogenerated), eventname (required), location (optional), start_time (required), end_time (required), description (optional), owner (required), and attendees (required) passed by the user.

**Read**
1. Users can get multiple scheduled events.
2. Users can get a specific event given an event ID.
3. Users can get a list of suggested times for a given time duration.
4. Users can get their user info.
5. Users can get a break.
6. Users can get all breaks.
7. Users can get both scheduled breaks and scheduled events.
8. Get a list of users

**Update**
1. Users can change an event's properties.
2. Users can add a suggested time or a custom time to an existing event.
3. Users can change their password.
4. Users can update their account to add/modify their linked Google Calendar account.
5. Users can update the breaks.

**Delete**
1. Users can delete a given event.
2. Users can delete a given break.
3. Users can delete their account.

## Design:

**Create**
1. `/users/create/<username>` Fulfills requirement 1 of Create. Users can create an account by passing a username (required), password (required), google_key(required) and profile_pic_url (optional). Users will have all of the above data sent, stored in the database. Returns a success message + username if it works. Else returns an error message if failed (including one if username already exists)
2. `/breaks/create/<username>/<breakname>` Fulfills requirement 2 of Create. Users can create a break time during which no events will be scheduled. A username (required for owner field), breakname (required), start_time (required), and end_time (required) passed by the user. Returns a success message + breakname + _id if it works. Else returns an error message if failed
3. `/events/import/<username>/<eventname>` Fulfills requirement 3 of Create. Users can import events from their Google Calendar. The user sends a request with start_time (required) and end_time (required) and their username(required). The API server uses the user's Google API key stored in the database to get the events from Google Calendar and add to the user calendar. These events passed in from Google Calendar have an _id (autogenerated), eventname (required), location (optional), start_time (required), end_time (required), description (optional), owner (required), and attendees (required). Returns a success message and the imported event _ids if it works. Else returns an error message if failed
4. `/events/create/<username>/<eventname>` Fulfills requirement 4 of Create. Users can add an event. These events have a eventname (required), location (optional), start_time (required), end_time (required), description (optional), username (required for owner field), and attendees (required) passed by the user (for now we just require eventname and username). Users will have all of the above data sent in, stored in the database alongside an _id. The _id + eventname is returned. Else returns an error message if failed

**Read**
1. `/events/list/<username>`. Fulfills requirement 1 of Read. Users can get all scheduled events. The users must pass in a username (required). It returns a dict with the _id (required), eventname (required), location (optional), start_time (required), end_time (required), description (optional), owner (required), attendees (required) and any other properties for the events. Else returns an error message if failed
2. `/events/get/<event_id>` Fulfills requirement 2 of Read. Users can get a specific event. Users pass in an event_id (required). The result will have a  _id (required), eventname (required), location (optional), start_time (required), end_time (required), description (optional), owner (required), and attendees (required) for the event. Else returns an error message if failed
3. `/times/get/<username>` Fulfills requirement 3 of Read. Users can get a list of suggested times given a duration. Users pass in a username (required) and duration(required). The result is an list of start_time (required) and end_time(required). These times can later be used with update_event to use the chosen suggested time. Else returns an error message if failed
4. `/users/get/<username>` Fulfills requirement 4 of Read. Users can get their user info. Users pass in their username (required). Returns a username (required), and profile_pic_url (optional). Does not return a password or google_key for security reasons. Else returns an error message if failed
5. `/breaks/get/<break_id>` Fulfills requirement 5 of Read. Users can get a specific break. Users pass in an break_id (required). The result will have a  _id (required), breakname (required), start_time (required), end_time (required), and owner (required). Else returns an error message if failed
6. `/breaks/list/<username>` Fulfills requirement 6 of Read. Users can get all breaks. The users must pass in a username (required). The result will have an list/dict of breaks with _id (required), breakname (required), start_time (required), end_time (required), and owner (required) and any other properties. Else returns an error message if failed
7. `/calendar/get/<username>`  Fulfills requirement 7 of Read. Users can get all breaks and events. The users must pass in a username (required). The result will have an list/dict of events/breaks with each having  _id (required), eventname (required), location (optional), start_time (required), end_time (required), description (optional), owner (required), and attendees (required) for the events. Meanwhile the breaks have _id (required), breakname (required), start_time (required), end_time (required), and owner (required). Else returns an error message if failed
8. `/users/list` Fulfills requirement 8 of Read. Get a list of usernames (required) and profile_pics_urls (optional) back. Else returns an error message if failed

**Update**

1. `/events/update/<event_id>` Fulfills requirement 1 and 2 of Update.  Users can change an event's properties. The event is specified with event_id (required). User can specify an eventname, location, start_time, end_time, description, owner, or attendees for the events. Else returns an error message if failed
2. `/user/password/update/<username>` Fulfills requirement 3 of Update. Users can change their password. Users pass in their existing_password (required) and new_password (required) and a username (required). Returns a message if successfully changed. Returns a success message + username if it works. Else returns an error message if failed
3. `/user/google/update/<username>` Fulfills requirement 4 of Update. Users can add or update their linked Google Calendar account. Users pass in the google_key (required) and a username (required). Returns a message if successfully changed. Returns a success message + username if it works. Else returns an error message if failed
4. `/breaks/update/<break_id>` Fulfills requirement 5 of Update. Users can update their break times. The break is specified with break_id (required). User can specify an breakname, start_time, end_time, or owner. Else returns an error message if failed

**Delete**
1. `/events/delete/<event_id>` Fulfills requirement 1 of Delete. Users can delete a given event using an event_id. Users pass in an event_id (required). Returns a success message with the event_id if it works. Else returns an error message if failed (with event_id).
2. `/breaks/delete/<break_id>` Fulfills requirement 2 of Delete. Users can delete a given break using an break_id. Users pass in a break_id (required). Returns a success message with the break_id if it works. Else returns an error message if failed (with break_id)
3. `/users/delete/<username>` Fulfills requirement 3 of Delete. Users can delete a given user using a user ID. Users pass in a username (required). Returns a success message with the username if it works. Else returns an error message if failed (includes username)

**Important: all items passed into REST not in the URL are in the body of the request**
 
## Organization Founders:
#### Kora Hughes
#### Elizabeth Akindeko
#### Ethan Philpott
#### Shaoxuan Liu

## More Links:
#### Team Ref: https://docs.google.com/spreadsheets/d/1glCAWIw6jaU5CnT3hGBCVzhFlsXHqffca_ndXOUfIwY/edit#gid=0
#### Template Ref: https://github.com/gcallah/demo-repo2
#### Previous Ref: https://github.com/AlphaError/swe-demo/tree/483d66b752659eeca268a26512faefc57851544c
