@echo off
cmd /k "cd /d newpc\scripts & activate & cd /d ..\..\ & python manage.py runserver"
run "newpc\Scripts\activate.bat"
python manage.py runserver