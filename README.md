# WaferProber (Velox Project)

### Description
The puropse of the **Velox Project** is easy and low maintenance Operation of the KIP Waferprober.

>in case you need to contact me, consult **# Support**

---
## Special Features
1. ### Push notifications

    Push Notifications can be send to your mobile phone with *ntfy.sh* 
    
    Notifications include:
    - at the start of every run
    - at the end of the run
    - every hour to ensure the Waferprober is still running (this can be modified)
    - every logging message of importance *critical* and above

    When triggered, the logging module will send a REST API put request to the topic : `WaferproberNotifications--------EdG2HGYuxMaNoZf3eUNRWsiKie`
2. ### Test Ending Procedure

    Experience has shown that controlling the waferprober via remote can result in some weird behavior of the Keithley's serial connection.
    In order to prevent the sourcemeter to freeze or raise an ERROR

    Unfortunately I didnt find a satifying solution for this problem.

    The current workaround is a text file `activate.txt` that is checked regulary and exits the main loop when the program cannot detect `"True"`in the file.
    
    Actually stopping the run will take approx. 5 mins because we have to wait until the current IV-measurement is finished.

3. ### Pathlibrary
    The movable positioner of the waferprober is used to measure different diodes on each Sub-Die. The Pathlibrary contains all utilites and Information for this.
    - it maps the subdie numbers to diode configurations and Identifiers
    - the diode configuration is then used to determine the movement path of the positioner
    - the `"extra"`tag is used to allow for different paths for each configuration:

        *Note: the **extra** tag applies to all diode-confuguraion paths*

4. ### Analyzer
    *an in depth explanation of the analyzer will be added soon*

    To start with, the idea of the analyzer is that you load Test Data into it, filter accordingly and then calculate. All in ONE Object.   
    The key **most** important inormation the analyzer needs is the name of the slice it should work on (filter, standard error, etc)





## Installation
To install the Velox Module, consult: `Velox_Python/Velox Python readme.txt`

The installation of all other Modules is trivial


## Usage

### 1. Push notifications
Push Notifications can be send to your mobile phone with *ntfy.sh* 

# Support
This git repository is created by me, Philipp Bartz. 
In case you have any questions and I am not at KIP anymore and my KIP-email address is no longer active, feel free to reach out to me via github and create an Issue on the repo there.

>[https://github.com/philipp-btz/waferprober/settings](https://github.com/philipp-btz/waferprober/settings) is an semi up-to-date dublicate of the velox Project. 
*In case there is no other possibility to reach me, create an issue there and I will try to help*



## Authors and acknowledgment
Special Thanks to Sonam Sharma!
This Project wouldn't be possible without the Help of Konrad Briggl, Hagen Bühler and Markus Dorn.



## Project status
*active* (as of Jun 2025)


***


```
cd existing_repo
git remote add origin https://git.kip.uni-heidelberg.de/philippb/waferprober.git
git branch -M main
git push -uf origin main
