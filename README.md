Manly Mustache Contest - 2013 Edition
=====================================
What is it?
-----------
This is the source code used to run the [Manly Mustache Contest](http://mustache.chryso.net) (2013 Edition).

The contest is meant to correspond to No-shave November and [Movember](http://us.movember.com) as a way to raise awareness for men's health issues.

The contest begins on November 1st, where each participating gentleman must be clean shaven (with photographic evidence).

It is a work-in-progress, but takes care of the basics of participation such as voting and image submission.

Instructions to get it running
------------------------------
* Make a virtualenv in checked out dir: ```virtualenv-2.7 ve```
* Activate your ve: ```source ve/bin/activate```
* Install requirements: ```pip install -r requirements.txt```
* Set up migrations: ```cd mustache; ./manage.py schemamigration --initial voting```
* Sync your database: ```./manage.py syncdb```
* Run migration: ```./manage.py migrate voting```
* Try out test server: ```./manage.py runserver```

To Do
-----
* [x] Randomize listing
* [x] Login to vote
* [x] Comments on submissions
* [ ] Vote across all gentlemen at once instead of one at a time
* [ ] Quick look at your current votes
* [ ] Jump to any gentleman
* [ ] Add LESS
* [ ] Convert Bootstrap to LESS
* [ ] Allow non-participating users to convert to participating?
