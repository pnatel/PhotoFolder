# PHOTO FOLDER

Working version 1.1 tested in 07/Dec/2019

The application aim to get a list of photos from a folder and to copy a random sample to a destination folder

## The Following parameters can be changed in config.ini:

```conf
[folder]
SourceFolder = /path/to/source/folder/
DestinationFolder = /path/to/destination/folder/

[ext]
FileType1 = jpg
FileType2 = JPEG
FileType3 = jpeg
FileType4 = JPG


[parameter]
NumberOfPics = 100
# not implemented
MaxNumberOfPics = 100
# Use folder Size in Megabytes
FoldersizeUpperLimit = 1000

NewerPhotos = datetime.now() - relativedelta(years=3)

[sort]
# 1 = Random, 
# 2 = Shuffle recently, 
# 3 = Shuffle oldest,
# 4 = Descendent by Date taken, 
# 5 = By Location (Need to read it from pic or Google)
Criteria = 1
```

## RECOMMENDATIONS:

Use pipreqs to generate the requirements.txt 
run in console or redirect output to a log file
e.g:
```bash
python3 photofolder.py
python3 photofolder.py >> log.txt
```

## Pending:
- add sftp feature so the code does NOT need to be ran from the host
- Make it run on Docker
- Send email notification and logs
- Different criterias
- House keeping and new files should perform tests:
    - Is the file I am about to copy already in the folder?
    - What is the age of the file? (in the folder) so I can remove the oldest ones 

## Some of the Research sources for reference:
https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
