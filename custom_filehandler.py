'''

    Philipp Bartz 2025
    
    CREDIT: some of this code is based on Sonam Sharma's code
    from her PHD thesis at the University of Heidelberg.

    This file is part of the Velox project.

'''

#####       Version 3.0       #####


import time
import os
import json
import custom_pathlibrary

class bcolors:
    HEADER = '\033[95m'
    ENDC = '\033[0m'


#TODO: check if config file is valid

def create_folder(*, path="", base_folder_name="Wafer", no_time=False, temperature=None):
    if not os.path.isdir(base_folder_name):
        timestr = time.strftime("_at_%Y_%m_%d-%H_%M_%S")
        if no_time:
            timestr = ""
        folder_name=f"data/{path}{base_folder_name}{timestr}{temperature if temperature is not None else ''}"
        os.makedirs(folder_name, exist_ok=True)
        print(f"{bcolors.HEADER}Created folder: {folder_name}{bcolors.ENDC}")
        return folder_name
    else:
        print(f"{bcolors.HEADER}Folder {base_folder_name} already exists.{bcolors.ENDC}")
        return

def save_IV(*, msgServer, store_data, iv_data_rbias, iv_data_fbias, folder, diode_Nr, logger, measurement_no=-1):
    store_data.add(name="diode_Nr", value=diode_Nr)
    if folder is None:
        logger.critical(f"Error:folder path is None. cannot save rsults.")
        return
    response = msgServer.sendSciCommand("ReadMapPosition2")
    column = response[0]
    store_data.add(name="column", value=column)
    row = response[1]
    store_data.add(name="row", value=row)
    x_POS = response[2]
    store_data.add(name="x_pos", value=x_POS)
    y_POS = response[3]
    store_data.add(name="y_pos", value=y_POS)
    subdie_NR = response[4]
    store_data.add(name="subdie_nr", value=subdie_NR)
    die_NR = response[6]
    store_data.add(name="die_nr", value=die_NR)

    plib = custom_pathlibrary.PLib()
    a_DIODES = plib.get_diode_count(msgServer=msgServer, subdie_Nr=subdie_NR, logger=logger)
    identifier, guardring_value, entrance_window =plib.get_identifier(msgServer=msgServer, logger=logger)
    store_data.add(name="a_diodes", value=a_DIODES)
    store_data.add(name="identifier", value=identifier)
    store_data.add(name="guardring_value", value=guardring_value)
    store_data.add(name="entrance_window", value=entrance_window)
    filename = f"IV_Die_{die_NR}_Subdie_{subdie_NR}_Diode_{diode_Nr}_measurement_{measurement_no}"
    filepath= f"{folder}/Die_{die_NR}/Subdie_{subdie_NR}_ADiodes_{a_DIODES}"
    filepath_with_filename = os.path.join(filepath, filename)
    logger.file(f"Saving IV results to {filepath_with_filename}")

    if not os.path.isdir(filepath):
        os.makedirs(filepath)
        logger.file(f"Created folder: {filepath}")
    
    store_data.add(name="iv_data_rbias", value=iv_data_rbias)
    store_data.add(name="iv_data_fbias", value=iv_data_fbias)
    store_data.save_for_data(folder=filepath, filename=filename)
    logger.file(f"IV results saved to {filepath_with_filename}")



class save_to_json():
    def __init__(self, *, folder=""):
        self.predefined_folder = folder
        self.settings = {}
    def add(self, *, name, value):
        self.settings[name] = value

    def chash(self):
        # This function returns a hash of the settings dict
        # It is used to check if the settings have changed
        hashstring = ""
        nonhashable_keys = ["a_diodes", "column", "die_nr", "diode_Nr", 
                            "diode_nr", "entrance_window", "guardring_value", 
                            "identifier", "iv_data_fbias", "iv_data_rbias", "row", 
                            "subdie_nr", "x_pos", "y_pos", "hash", "time_at_start", 
                            "time_at_end", "time_elapsed"]
        hashable_keys = set(self.settings.keys()) - set(nonhashable_keys)
        #print(f"Hashable keys: {hashable_keys}")
        for key in hashable_keys:
            if isinstance(self.settings[key], (str, int, float, bool, list, dict)):
                hashstring += str(self.settings[key])
                #print(f"Adding {key} to hashstring: {self.settings[key]}")
        hashed_string = str(hash(hashstring))
        self.add(name="hash", value=hashed_string)
        return

    ## This is outdated, but kept for compatibility
    def save(self, *, folder = None, logger=None):
        if folder is None:
            folder = self.predefined_folder
        if logger is not None:
            logger.critical(f"Saving settings to {folder}/settings_dump.json")
            logger.critical(f"Settings: {self.settings}")
        with open(f"{folder}/settings_dump.json", mode="w", encoding="utf-8") as write_file:
            json.dump(self.settings, write_file, sort_keys=True, indent=4)


    ## this should be used to save IV data 
    ## all Settings woll be hashed and saved to the file as well, to enable quick filtering afterwards
    def save_for_data(self, *, folder = None, filename):
        self.chash()
        with open(f"{folder}/{filename}.json", mode="w", encoding="utf-8") as write_file:
            json.dump(self.settings, write_file, sort_keys=True, indent=4)




def get_all_filenames_in_folder(*, startdir, file_extension=""):
    # This func outputs a List of all Files in a given directory and its subdirectories
    f = []
    if startdir.endswith("/"):
        startdir = startdir[0:-1]
    w = os.walk(startdir)

    for (dirpath, dirnames, filenames) in w:

        for i in filenames:
            if i.endswith(file_extension):
                f.append(f"{dirpath}/{i}")
    return f


def load_json_file(*, filepath):
    # This func loads a json file and returns the content as a dict
    if not os.path.isfile(filepath):
        print(f"Error: File {filepath} does not exist.")
        return None
    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {filepath}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while loading JSON file {filepath}: {e}")
            return None