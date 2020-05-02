# PHOTO FOLDER

![Python package](https://github.com/pnatel/PhotoFolder/workflows/Python%20package/badge.svg)

Working version 1.2.1 tested in April/2020 using Python 3.5 and above

The application aim to get a list of photos from a folder and to copy a random sample to a destination folder

## How to use

- Clone the Repository: <https://github.com/pnatel/PhotoFolder.git>
- navigate to the folder and run: "pip install -r requirements.txt"
- run "python photofolder.py"
- Web version runs on main.py (BETA) hard codded to the test folders

PS.: If you run the application with any argument (e.g. "python photofolder.py MY_ARGUMENT"), it will use its local test folders

## Features

- The application creates a log file with steps performed for late analysis
- The file extensions accepted cn be changed of any kind, so the application can have other purposes.
- Running the application multiple times will not overload its destination. The application prunes the destination folder based on the '''config.ini''' parameters

## The Following parameters can be changed in config.ini

Several parameters must be changed in the file to allow the app to run smoothly.

## RECOMMENDATIONS

Run pipreqs (pip install pipreqs) in the folder of the project to generate the requirements.txt if required.
Use --force to overwrite it

## Pending

- add sftp feature so the code does NOT need to be ran from the host
- Make it run on Docker
- Send email notification and logs
- Different sorting criterias
- House keeping and new files should perform tests:
  - Is the file I am about to copy already in the folder?
    - What is the age of the file? (in the folder) so I can remove the oldest ones

## Some of the Research sources for reference

- <https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/>
- <https://wiki.python.org/moin/ConfigParserExamples>
- <https://stackabuse.com/command-line-arguments-in-python/>
