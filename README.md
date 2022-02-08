# PEEK ~ (Paul, Ethan, Elizabeth, Kora)
#### This is the main repository of our Design/Software Engineering project as part of CS-UY 4513 and CS-UY 4523.
![](https://app.travis-ci.com/PEEK-NYU/PEEK.svg?branch=overhauled)

![peekdemo](https://github.com/PEEK-NYU/PEEK/blob/overhauled/images/peekcalendar%20page%201.png)

#### HEROKU:  https://peek-nyu.herokuapp.com/
#### GITHUB ACTIONS: (tbd)


## Project Idea:
* A website that aids users in scheduling events. Website uses existing calendar data and suggests the best time for an event.
* Story: User wants to schedule a study time. User imports an .ics file into software, types in some quick event information if wanted, and presses a button. The software then outputs an .ics file with the new event, which the user imports into their calendar software of choice.
  * user can also login to access their previously stored calendar information
* Advanced Features:
  * Automation of .ics import/export via google calendar login credentials
  * Software has suggested time-slots and learns the user's habits based on software use
  * Software categorizes events by type (study time, break time, etc.)
  * User can customize software's suggestions by event type
  * Extra Data: user profile images, complex event data (particpants), recurring events


## UI Overview
* Homepage
  * if not logged-in
    * log-in button (navigates to login page)
  * if is logged-in
    * log-out button
    * list of current calendar information (edit links/ui for each event shown that navigate to event edit page)
    * account info button (navigates to account page)
    * some calendar navigation tools (tbd)
* Login Page
  * text boxes for username and password input
  * login button to submit text box info (takes you back to home page on success)
* Account page
  * text boxes for username, new password, and existing password
  * submit button to change
* Event Search Page
  * search bar for keyword lookup with search button
  * similar calendar info layout as homepage
* Event Edit Page
  * shows labeled text boxes for all event info
     * current info stored in database is in default fields
  * submit button for event info


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
* start_time (datetime)
* end_time (datetime)
* location (string)
* description (string)

Connection Table  // used to refrence which events are owned (viewable/editable) by which users
* _event_id (string) // unique database key
* _user_id (string) // unique database key

**Create**
* Users can create an account with a username and password
* Users can create an event - also updates via .ics file import
  * eventname (required)
  * start_time (required)
  * end_time (required)
  * location (optional)
  * description (optional)

**Read**
* Users can get their user info
  * User Name
  * Password
* Users can get a list of all events and its subsequent event information
  * Event Name
  * Start Time
  * End Time
  * Location
  * Description
* Users can search for events by a keyword.

**Update**
* Users can change their user info
  * User Name
  * Password
* Users can edit the information for a specific event
  * Event Name
  * Start Time
  * End Time
  * Location
  * Description

**Delete**
* Users can delete their account (along with account information)
* Users can delete an event.

## Design:

**Create**
1. `/users/create/<_user_id>` Users can create an account by passing a *username* and *password* (both required). Users will have all of the above data sent, stored in the database. Returns a success message + the associated *_user_id* (autogenerated) if it works. Else returns an error message if failed (including one if username already exists)
2. `/events/import/<calendar>` Logged-in users can import events from their personal calendar via .ics file upload. All event information available is imported into the database. Returns a success message and a list of the imported event *_event_id*'s if it works. Else returns an error message if failed
3. `/events/create/<event>` Logged-in users can create new events by filling out a form of event info: *eventname* (required), *start time* (required), *end time* (required), *location* (optional), *description* (optional). Returns a success message and the associated _event_id if it works. Else returns an error message if failed

**Read**
1. `/users/get/<_user_id>` Logged-in users can get their user information. The API will return a dict with *username* and *password*.
2. `/events/get/<_user_id>` Logged-in users can get all scheduled events under their account. The API will return a list of dicts with the *eventname*, *start_time*, *end_time*, *location*, *description* (aka event information). Else returns an error message if there are no events and returns an error message if failed.
3. `/events/get/<eventname>` Logged-in users can get a specific event by passing in a keyword. The API will return a list of dicts (with event information) such that all returned events' *eventnames* contain the keyword. Else returns an error message if there are no events and returns an error message if failed.
4. `/times/get/<_user_id>` Logged-in users can get a list of suggested event times. Users pass in a *date_range* (start, end date - required) and *duration*(required). The API will return a list of *start_time* (required) and *end_time* (required) pairs (tuples). These times can later be used with *create_event* to create an event at the chosen suggested time. Else returns an error message if failed

**Update**
1. `/events/update/<_event_id>` Logged-in users can change the properties of an event they own: *eventname*, *location*, *start_time*, *end_time*, *description*. Database will update said event accordingly and return a success message with the associated *_event_id*. Else returns an error message if failed
2. `/users/update/<_user_id>` Users can change their user information: *username* and *password*. Users pass in their *username* and or their *new_password* (required) and confirm this change with their *existing_password* (required). Returns a message if successfully changed. Returns a success message and *_user_id* if it works. Else returns an error message if the old and new passwords match, returns an error message if the input existing_password does not match the present state of the database, and returns an error message if failed.

**Delete**
1. `/events/delete/<eventname>` Users can delete a given event be searching its *eventname* keyword in tandem with **get_event**. Users pass in an *keyword* (required) and have the option to delete a given event with said keyword in its *eventname* that is also owned by the user. Returns a success message if it works. Else returns an error message and the associated *eventname* if it failed.
2. `/breaks/delete/<_user_id>` Logged-in users can delete their own account via UI. Returns a success message with the if it works. Else returns an error message along with the *_user_id* if failed.

> Important: all items passed into REST not in the URL are in the body of the request

## Organization Founders:
#### Kora Hughes
#### Elizabeth Akindeko
#### Shaoxuan Liu
#### Ethan Philpott

## More Links:
#### Team Ref: https://docs.google.com/spreadsheets/d/1glCAWIw6jaU5CnT3hGBCVzhFlsXHqffca_ndXOUfIwY/edit#gid=0
#### Template Ref: https://github.com/gcallah/demo-repo2
#### Previous Ref: https://github.com/AlphaError/swe-demo/tree/483d66b752659eeca268a26512faefc57851544c
