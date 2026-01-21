# Data Science Professional Practicum (DSCI 560)
## Laboratory Assignment 1
### Github Repository Made by Vincent-Daniel Yun

Lab 1 covers installing Ubuntu and performing a simple web data crawl. This README was written to provide guidelines for reproducing the assignment.   
Please clone this repostory first in your ubuntu machine by using this command:

    git clone https://github.com/YUNBLAK/usc-dsci560-sp26.git

## Dependencies
There are several dependencies for this lab. Please make sure you already installed Python 3 `sudo apt install python3` and  Pip (Python Package Manager) `sudo apt install python3-pip`. Libraries that we need for this lab are:

    requests
    beautifulsoup4
    selenium
    

## Usage Case for "Get Familiar with Linux and Python"

After cloning the repository, confirm that the folder was created:

    ls

Then move into the `lab01` directory:

    cd usc-dsci560-sp26/lab01

For doing this subsection, we need to run `task_1.py` in scripts directory. Please move to `scripts` directory:

    cd scripts

Then, enter this command:

    python task_1.py



## Usage Case for "Python Web-scraping Task"
This is for scraping data from the website: https://www.cnbc.com/world/?region=world. 
Enter this command in `usc-dsci560-sp26/lab01/scripts` directory:

    python web_scraper.py

Then you can see a html file named `web_data.html` stored in `usc-dsci560-sp26/lab01/data/raw_data`


