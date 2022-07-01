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

- The account application  

- The api application  

- The badges application

- The core application.

- The events application.  

- The general application.  

## launch and run

When launched, the embedded program will send a post request to the website to receive the different scanning type of the current event. Then, the embedded program will wait for scans and send an other post request with the current scanning type (or mode) and the badge uid. The webapp will send a response depending on the scan validity and store the scan into the database.

## account app

Handle the website Users data.
🔴 Incomplet ?

### views 🔴

- login:

- authenticate:

- authorize:

- logout:

- user_page:

## api app


Handle the scan database and the scanning requests by sending specific responses depending on the validity of the scan.
The api application handle the connection with the embedded program and handle the Scan model.

### views

- init_page:

Send the modes of the current event to the embedded program in a json format after receiving a POST request.

- scan_post_management:

Receive an UID and a mode from the embedded program in a json format after receiving a POST request. The function checks for a StudentBadge with this UID and assign his login to a new Scan object along with his other relative informations.  
If the uid sent by the scan has not StudentBadge assigned yet, the scan login is set as UNDEFINED.  
  
It also checks for the validity of the scan depending the mode amount and the number of time an UID has been scanned for the mode in the current event.

### models

- Scan:

uid: uid of the badge sent by the embedded program.  
date: date of the scan.  
mode: mode sent by the embedded program.  
login: login based on the StudentBadge that is assigned the given uid.  
validity: if the scan is valid based on the amount of the given mode.  
event: event to which the badge has been scanned.

## badges app

Handle the Badge, Student and StudentBadge models (database related to the badges and the students).  

### views

- add_student:

Render add_student.html.  
Add a StudentBadge with the StudentBadge form to the database and redirect to list_student.  
  
🔴 add_student add a student_badge with a complex form.    
Submitted variable should also be deleted (useless in html and function)    
Is refered as "add user" in the website navbar.  
Context should be in a variable outside the return line (uniformity of functions)

- update_student:

Render update_student.html.  
Update a StudentBadge with the StudentBadge form.  
  
🔴 different than add_student, might need update to look/work like add_student (divide in post and get)  
Complex form   
Context should be in a variable outside the return line (uniformity of functions)

- one_student:

Render one_student.html with a StudentBadge.

- testing_student:

🔴 idk what that is

- list_student:

Render students.html with all StudentBadge objects.

- udate_studentbadge:
 
Render update_studentbadge.html.  
Can be called on the scan page by clicking on a specific scan.  
Assign an uid to a StudentBadge and the Scan.  

🔴 Update student vs update studentbadge ?? + too much error management ?
(If login is already assigned uid, can't assign an other one)

### models

- Student:

intra_id: id of the student.  
login: login of the student.  
email: email of the student.  
displayname: 🔴 idk  
image_url: image of the student on the intranet.  
is_staff: boolean, if the student is a staff member or not.

- Badge:

serial: Badge serial.  
uid: badge uid.  
reference: Badge reference.  
badge_type: Depends on the student status (Piscineux or Student).

- StudentBadge:

student: Student model.  
badge: Badge model.  
start_at: The date of the acquisition of the badge by the student.  
end_at: The date of the requisition of the badge.  
caution_paid: The caution paid by the student for the badge.  
caution_returned: Boolean, caution returned or not.  
lost: Boolean, badge lost or not.

## core app

🔴

## events app

Handle the Event and Mode models.

### views

- events_page:

Render events.html with all Events objects.

- one_event:

Render one_event.html with a specific event, the scans related to the event
and his modes (or scanning type).

- update_event:

Render update_event.html and call mode_page.  
Update an Event object.  

- add_event:

Render add_event.html.  
Add an event and redirect to update_event.  

- delete_event:

Render delete_event.html.  
Delete an event and redirect to events_page.  

- mode_page:

This function is called by other event functions.

Add the specific modes of an event, a mode_form and an mode_error if needed
to the context given in parameter.   
Delete or add a mode for an event.  

🔴 Can be put directly in update event since its the only function that calls it

### models

🔴 Quick fix still in file. (two_hours_hence function)

- Event:

date: Event starting date.  
name: Event name.  
end: Event end date.

🔴 get_current_event return nothing if not events, and undefined behavior if multiple.

- Mode:

amount: Max valid scans possibles for the mode.  
type: Name / type of the mode.  
event: Related event for this mode.

## general app

Handle the views related to the general section, the scans and the calendar.

### views

- CalendarView:  
Infos can be found at https://github.com/huiwenhw.

- home_page: 

render home.html

- search_general: 

From the menubar : possibility to search for a specific Event object and / or StudentBadge object.  
Redirect to search_general.html and list all Event and StudentBadge objects matching the parameter given in the search bar.  

- scan_page:

Render scans.html with all the Scan objects and the last scan.  

🔴 Do we need the last scan since it is on top of the list ?

- search_scan_page:

Render search_scan.html.  
Render scans.html after a POST request with all the scans matching the event_name and login given.
  
🔴 Not used yet

- delete_scan:

Render delete_event.html.  
🔴 Pourquoi render delete_event ??  
Delete scan and redirect to scan_page.  
🔴 redirect a verifier  

## templates (html files) To do ? 🔴