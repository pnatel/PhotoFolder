# PHOTO FOLDER

| MASTER  | DEVELOPMENT  | DOCKER  |
|:-------:|:------------:|:-------:|
| ![Engine Testing](https://github.com/pnatel/PhotoFolder/workflows/Engine%20Testing/badge.svg?branch=master)  | ![Engine Testing](https://github.com/pnatel/PhotoFolder/workflows/Engine%20Testing/badge.svg?branch=Development)  | ![Engine Testing](https://github.com/pnatel/PhotoFolder/workflows/Engine%20Testing/badge.svg?branch=docker)  |
| ![Webserver Testing](https://github.com/pnatel/PhotoFolder/workflows/Webserver%20Testing/badge.svg?branch=master)  | ![Webserver Testing](https://github.com/pnatel/PhotoFolder/workflows/Webserver%20Testing/badge.svg?branch=Development)  | ![Webserver Testing](https://github.com/pnatel/PhotoFolder/workflows/Webserver%20Testing/badge.svg?branch=docker)  |

The application aim to get a list of photos from a folder and to copy a random sample to a destination folder.

## A bit of history

I am a bit of a IT hoarder, and I like to use or to give use to the things I have. One day, I was in the garage trying to make sense of the mess, when I found my old Android tablet, an Acer A500, that is collecting dust with the rest of my collection of IT stuff that is old enough for me to NOT want to use it, but still works,  so I can't throw in a bin...
Anyway, I charged the tablet and downloaded a Photo Frame app, after setup, I put the tablet to work in my living room and it kept changing the pictures happily over the day reminding us of the cool moments of our life.
(To Be Continue...)

## How to use

- Clone the Repository: <https://github.com/pnatel/PhotoFolder.git>
- navigate to the folder and run: "pip install -r requirements.txt"
- run "python FileModule.py"

### Web Version

- Web version runs on main.py pre-set to test folders, run:

> python main.py

- And visit <http://localhost:23276>
- there is a page for configuration changes
  - Recommended Changes:
    > test_mode = False
    >
    > SourceFolder = /Path/to/your/photos

## Running on Docker

> $ docker build --tag=photo_folder_manager <https://github.com/pnatel/PhotoFolder.git#docker>
>
> $ docker run  -d --name photo_folder_manager -p 23276:23276 --mount source=PHOTO_POOL_FOLDER, target=/source photo_folder_manager

I also have the image saved in Docker Hub (<https://hub.docker.com/r/pnatel/photo_folder_manager>):
> $ docker pull pnatel/photo_folder_manager

Only change required in the config is `test_mode = False`

### Docker on Raspberry Pi

- There is a Dockerfile for the Pi in the arm folder, you don't need to clone the Repo if you want to use this file
- Docker Hub also has a prebuilt image look for the ARM tag

> $ docker pull pnatel/photo_folder_manager:armv7

## Features

- The application creates a log file with steps performed for late analysis
- The file extensions accepted cn be changed of any kind, so the application can have other purposes.
- Running the application multiple times will not overload its destination. The application prunes the destination folder based on the `config.ini` parameters

## Parameters can be changed in config.ini

Several parameters must be changed in the file to allow the app to customise its usage to your liking.

## RECOMMENDATIONS

Run pipreqs (pip install pipreqs) in the folder of the project to generate the requirements.txt if required.
Use --force to overwrite it

## Pending

- add sftp feature so the code does NOT need to be ran from the host
- Send email notification and logs
- Different sorting criterias
- House keeping and new files should perform tests:
  - Is the file I am about to copy already in the folder?
    - What is the age of the file? (in the folder) so I can remove the oldest ones

## Some of the Research sources for reference

- <https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/>
- <https://wiki.python.org/moin/ConfigParserExamples>
- <https://stackabuse.com/command-line-arguments-in-python/>
- There are references in the files itself
- Google, Bing and whatever finds me an answer to move forward
