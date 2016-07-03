Time sheet parser
-----------------

Creates an ical file from the files used at the University of Applied Sciences Chur for planning the time tables.

Usage
-----

 1. Export the time sheet to CSV
 2. Export the ical file the given lecturer

    ```bash
    ./time-sheet-parser.py --lecturer "Weichselbraun Albert" timetable.csv > timetable.ics
    ```

 3. Import the .ics file into Outlook or Thunderbird (Thunderbird: activate the **Today Pane** and drag & drop the file into the pane).
