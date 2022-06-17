# Badger: `webapp`

## Summary

ToDo

## Setup

- Create and activate a python3 virtual environement:
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```
- Install the dependencies:
```sh
$ pip install -r requirements.txt
```
- Create and populate a `.env` file from the template:
```sh
$ cp template.env .env
```

## Manual

This project is a web application designed to keep track of scan requests from badges linked to students during an event.
The scans can have different values depending on the event to keep track of drinks, presences or else.

The project is divided into 6 applications :

- The account application:
Handle the website Users data

- The api application:
Handle the scan database and the scanning requests by sending specific responses depending on the validity of the scan.

- The badges application:
Handle the database related to badges and students.

- The core application.

- The events application:
Hanle the database related to the events and his scanning types.

- The pages application:
Render the different html pages and handle the website requests.
The html files can be found in the template folder.

### launch and run

When launched, the embedded program will send a post request to the website to receive the different scanning type of the current event. Then, the embedded program will wait for scans and send an other post request with the current scanning type (or mode) and the badge uid. The webapp will send a response depending on the scan validity and store the scan into the database.

### account app

### api app

### badges app

### core app

### events app

### pages app

The pages application is divided based on the different databases. Each databases type has a view file that handle the requests from their respective pages.
The urls.py file shows which url is linked to which function in the views.

- admin_views

#### login:

#### authenticate:

#### authorize:

#### logout:

#### user_page:

- badges_views

#### add_student:

POST:
Add a StudentBadge to the database and redirect to list_student
ELSE:
Render add_student.html

🔴 add_student (in add user) add a student_badge with a complicated form. Submitted variable should also be deleted (useless in html and function)
Context should be in a variable outside the return line (uniformity of functions)

#### update_student:

ALL:
Render update_student.html
Update the StudentBadge

🔴 different than add_student, might need update to look/work like add_student (divide in post and get)
Context should be in a variable outside the return line (uniformity of functions)

#### one_student:

ALL:
Render one_student.html with a specific StudentBadge

#### testing_student:

🔴 idk what that is

#### list_student:

ALL:
Render students.html with all StudentBadge objects

#### udate_studentbadge:

POST:
Can be called on the scan page by clicking on a specific scan.
Assign an uid to a StudentBadge.

ALL:
Render update_studentbadge.html

🔴 Update student vs update studentbadge ?? + too much error management ?
(If login is already assigned uid, can't assign an other one)

- calendar_views

Infos can be found at https://github.com/huiwenhw

- event_views

#### events_page:

ALL:
Render events.html with all Events objects

#### one_event:

ALL:
Render one_event.html with a specific event, the scans related to the event
and his modes (or scanning type)

#### update_event:

POST:
Update an Event object.

ALL:
Render update_event.html and call mode_page.

#### add_event:

POST:
Add an event and redirect to update_event.
ALL:
Render add_event.html.

🔴 Submit variable useless

#### delete_event:

POST:
Delete an event and redirect to events_page.
ALL:
Render delete_event.html.

#### mode_page:

This function is called by other page functions.

POST:
Delete or add a mode for an event.
ALL:
Add the specific modes of an event, a mode_form and an mode_error if needed
to the context given in parameter.

🔴 Can be put directly in update event since its the only function that calls it

- general_views

#### home_page: 

render home.html

#### search_general: 

POST:
From the menubar : possibility to search for a specific Event object and / or StudentBadge object.
Redirect to search_general.html and list all Event and StudentBadge objects matching the parameter given in the search bar.

🔴 Users should be modified to students

- scan views

#### scan_page:

ALL:
Render scans.html with all the Scan objects and the last scan.

🔴 Do we need the last scan since it is on top of the list ?

#### scan_page:

#### scan_page:

#### scan_page:

#### scan_page:

## templates (html files)


POST:
Can redirect to : events_page, students_page

- events_page : render events_page.html

GET:
List all Event objects with their name and dates.

POST:
The update button redirect to the update_event page and the delete button delete the chosen Event object.

The one_event page is rendered if clicking on the event name.

- one_event : render one_event.html

GET:
List the scans of the event and his different modes.

POST:
The update button redirect to the update_event page.

- user_page : render user.html

GET:
List all User objects with their information.

- calendar_page : render calendar.html

🔴 Infos missing



- mode_page : called by update_event

GET:
List every mode of the Event object with the id parameter.

POST:
Possibility to add and delete a mode for an Event object.

- update_event : render update_event.html

GET:
Render the Event form for the specified Event object and his list of modes (see mode_page).

POST:
Update the Event object and redirect to the events_page (events.html).

- add_event : render add_event.html

GET:
Render an Event form to submit.

POST:
The add modes button redirect to the update_event page to add the different modes and save the new submitted Event object.

- delete_event : render delete_event.html

GET:
Confirmation page to delete the chosen event.

POST:
Delete the chosen event and redirect to event_pages.

🔴 Scan pages to add to pages part !!


- base.html: Render the menubar to redirect to the differents locations

