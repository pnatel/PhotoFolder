# PHOTO FOLDER

![Python package](https://github.com/pnatel/PhotoFolder/workflows/Python%20package/badge.svg)

Working version 1.1.1 tested in March/2020 using Python 3.5 and above

The application aim to get a list of photos from a folder and to copy a random sample to a destination folder

## How to use

- Clone the Repository: <https://github.com/pnatel/PhotoFolder.git>
- navigate to the folder and run: "pip install -r requirements.txt"
- run "python photofolder.py"

PS.: If you run the application with any argument (e.g. "python photofolder.py MY_ARGUMENT"), it will use its local test folders

## Features

- The application creates a log file with steps performed for late analysis
- The file extensions accepted cn be changed of any kind, so the application can have other purposes.
- Running the application multiple times will not overload its destination. The application prunes the destination folder based on the '''config.ini''' parameters

## The Following parameters can be changed in config.ini

```conf
[folder]
SourceFolder = /mnt/usbstorage/media/Pictures/Minhas_imagens/Guimaraes_Silva_Collection
DestinationFolder = ./pics
LogPath = ./logs/PhotoFolder.log

[ext]
FileType1 = jpg
FileType2 = jpeg
FileType3 = png
FileType4 = JPG
FileType5 = JPEG
FileType6 = PNG


[parameter]
# Size of your sample of pictures from the source folder
NumberOfPics = 100
NumberOfPics_test = 3
# not implemented
MaxNumberOfPics = 1000
# How much the folder can grow size in Megabytes
FoldersizeUpperLimit = 1000
FoldersizeUpperLimit_test = 10

NewerPhotos = datetime.now() - relativedelta(years=3)

[sort]
# 1 = Random,
# 2 = Shuffle recently,
# 3 = Shuffle oldest,
# 4 = Descendent by Date taken,
# 5 = By Location (Need to read it from pic or Google)
Criteria = 1

[loglevel]
; Level               When it’s used
; logging.DEBUG       Detailed information, typically of interest only when diagnosing problems.
; logging.INFO        Confirmation that things are working as expected.
; logging.WARNING     An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
; logging.ERROR       Due to a more serious problem, the software has not been able to perform some function.
; logging.CRITICAL    A serious error, indicating that the program itself may be unable to continue running.
level = logging.INFO

; settings for application testing and CI/CD on Github
[test]
SourceFolder = test/source/
DestinationFolder = test/destination/
LogPath = test/logs/PhotoFolder.log

```

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
