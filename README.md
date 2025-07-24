# WaferProber (Velox Project)

### Description
The purpose of the **Velox Project** is easy and low maintenance Operation of the KIP Waferprober.

>in case you need to contact me, consult [# Support](#Support)

---
# General Structure of the repository 
- `archive/` : contains Sonam Sharma's original code and her original measurements
- `data/` : here are the folders for each measurement run. Measurements are stored in the subfolders as per the Die and Subdie number. The time in the folder name is the time at the start of the measurement run. The Folder also contains the **logging** file(s) of the run, as well as the **settings** with wich the run was executed.   
***NOTE: the `settings_dump.json`file is created at the End of the run, so any changes of the test-Settings are not saved there and will not be tracable   
This folder is not synced by git***  

- `data_storage/` : has the exact same structure as `data/`, but is used to store the data long term. When you have finished a successful run, you can copy the data from `data/` to `data_storage/`. 
- `global_logs/` : contains logs made by the ***Task Scheduler***. You can change the desired size and number of backup log files in `custom_logging.py`.
- `misc/` : contains:
    - `Keithley_Model_6487_Manual.pdf` : the manual of the Keithley 6487 Sourcemeter
    - `Velox_Python/` : contains the Velox Python Module, which is used to control the Waferprober
    - `Remote Interface.pdf` : the manual to the Velox Python Module
    - other manuals and documentation for the waferprober
- `python_tools/` : a python library that contains some useful tools for analyzing and processing IV measurements  
this is made by Tiancheng Zhong and provided to me by Hagen Wolfgang Bühler
- `task_list/` : contains the task cue for the Task Scheduler
- `activate.txt` : a text file that is used to control the ending procedure of the Waferprober.  
    - if it contains `"True"`, the program will run
    - if it contains `"Pause"`, the program will pause at save points and wait until it is resumed with "True" or ultimately stopped
    - if it contains anything else, the program will stop after the current IV-measurement is finished
- `custom_[...].py` : contains the custom modules used in operating the Waferprober and analyzing the data.
- `waferprober.ipynb` : the Jupyter Notebook that is used to run the Waferprober.  
    - it contains the main loop that controls the Waferprober
    - it contains the Task Scheduler, which is used to schedule tasks and settings
- `WaferMap_neu_[...].png` : a quick sketch for the physical position of the pixels and pads on the Subdies. The number in the filename corresponds to the number of pixels on the Subdie.  


# How to run the waferprober
1. Make sure the controlling computer is connected to the Waferprober and the Keithley 6487 Sourcemeter!
2. Ensure that activate.txt contains `"True"`
3. Calibrate the Positioner to the paths in the Pathlibrary.   
When using the original paths, the reference point is the center of the lower left Pad.  
(see `WaferMap_neu_16.png` for the position of the pads)
4. Put your settings file in the `task_list/` directory. It does not need to contain all settings of the example file, most of them have fallback/default values that are used in case they are not specified in the settings file.
5. Open the `waferprober.ipynb` Jupyter Notebook and run the first cell to import the necessary modules.
6. Run the second cell to start the Task Scheduler.   
The Task Scheduler will automatically execute the tasks in the `task_list/` directory in alphanumeric order.      
The Task Scheduler will run until the `activate.txt` file contains anything else than `"True"` or `"Pause"`. It will log all important information to the `global_logs/` directory.   

***The Waferprober is somehow able do un-calibrate itself. This only happened once so far but you should pay attention to the calibration, even during a test run*!**     
(i just wasted 3 weeks of machine time because of this. The contact hight of the Chuck drifted down until the measurement was only noise. In the specs of the waferprober it says that the chuck is self calibating but somehow that time it didnt work.)

# How to analyze the data
There is no ultimate way to analyze the data and for most types of analysis, you have to write custom code.    
When you want to analyze IV Curves, you can use the `custom_analyzer.py` module.:
- create a new Dataset with `custom_analyzer.py` and load the desired measurement files into it (`custom_analyzer.Dataset.add_files(...)`).  
You can use `custom_analyzer.get_all_filenames(...)` get a list of all filepaths that you can put into the Dataset.
- Filter the data according to your needs with `custom_analyzer.Dataset.filter(...).`    
this creates a data slice that can be filtered further with `custom_analyzer.Dataset.filter_slice(...)`.
- *[more will follow soon]*




## Special Features
1. ### Task Scheduler and Settings
    As the name suggests, the Task Scheduler is used to schedule tasks.  
    The Goal hereby is the fully autonomous operation of the Waferprober for as little maintenance as possible

    #### Tasks
    the Tasks are executed alphanumerically.  
    `01_task.json` is executed before `02_task.json`and so on

    #### Settings 
    `task_list/finished/example_setting_file.json` cotains an example.  
    There are some restrictions with the settings, mainly because of the Keithley 6487. You can find its manual in `misc/Keithley_Model_6487_Manual.pdf`.  



2. ### Push notifications

    Push Notifications can be send to your mobile phone with *ntfy.sh* 
    
    Notifications include:
    - at the start of every run
    - at the end of the run
    - every 4 hours to ensure the Waferprober is still running (this can be modified)
    - when there are more than 7 Measurements per hour that are just noise
    - every logging message of importance *critical* and above

    When triggered, the logging module will send a REST API put request to the topic : `WaferproberNotifications--------EdG2HGYuxMaNoZf3eUNRWsiKie`
3. ### Test Ending Procedure

    Experience has shown that controlling the waferprober via remote can result in some weird behavior of the Keithley's serial connection.
    In order to prevent the sourcemeter to freeze or raise an ERROR

    Unfortunately I didnt find a satifying solution for this problem.

    The current workaround is a text file `activate.txt` that is checked regulary and exits the main loop when the program cannot detect `"True"`in the file.

    When there is `"Pause"`in the text file, the program will pause at save points and wait until it is resumed with "True" or ultimately stopped.  

    Actually stopping the run will take approx. 5 mins because we have to wait until the current IV-measurement is finished. 

4. ### Pathlibrary
    The movable positioner of the waferprober is used to measure different diodes on each Sub-Die. The Pathlibrary contains all utilites and Information for this.
    - it maps the subdie numbers to diode configurations and Identifiers
    - the diode configuration is then used to determine the movement path of the positioner
    - the `"extra"`tag is used to allow for different paths for each configuration:

        *Note: the **extra** tag applies to all diode-confuguraion paths*

5. ### Analyzer
    *an in depth explanation of the analyzer will be added soon*

    To start with, the idea of the analyzer is that you load Test Data into it, filter accordingly and then calculate. All in ONE Object.   
    The key **most** important inormation the analyzer needs is the name of the slice it should work on (filter, standard error, etc)





## Installation
To install the Velox Module, consult: `misc/Velox_Python/Velox Python readme.txt`

The installation of all other Modules is trivial


## Usage

### 1. Push notifications
Push Notifications can be send to your mobile phone with *ntfy.sh* 

# Support
This git repository is created by me, Philipp Bartz. 
In case you have any questions and I am not at KIP anymore and my KIP-email address is no longer active, feel free to reach out to me via github and create an Issue on the repo there.

>[https://github.com/philipp-btz/waferprober/settings](https://github.com/philipp-btz/waferprober/settings) is an semi up-to-date dublicate of the velox Project. 
*In there is no other possibility to reach me, create an issue there and I will try to help*



## Authors and acknowledgment
Special Thanks to Sonam Sharma!
This Project wouldn't be possible without the Help of Konrad Briggl, Hagen Bühler and Markus Dorn.



## Project status
*active* (as of Jul 2025)


***



## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://git.kip.uni-heidelberg.de/philippb/waferprober.git
git branch -M main
git push -uf origin main