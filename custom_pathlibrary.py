'''

    Philipp Bartz 2025

    This file is part of the Velox project.

'''

#####  VERSION 3.2  #####


#import velox

class PLib:
    """
    This class contains the path library for different diode configurations.
    Each configuration is represented as a tuple of tuples, where each inner tuple
    contains the coordinates and type of the path.
    """

    # This maps the sub-die number returned by "ReadMapPosition2" to the type of diode configuration.
    dieNr_to_type = (16, 16, 16, 16,
                     16, 16, 16, 16,
                     4, 4, 4, 4, 
                     4, 4, 4, 4,
                     1, 1, 1, 1, 
                     1, 1, 1, 1,
                     )
    
    dieNr_to_identifier = ("04E10", "04E20", "04C10", "04C20",
                            "04E05", "04E15", "04C05", "04C15",
                            "02E10", "02E20", "02C10", "02C20",
                            "02E05", "02E15", "02C05", "02C15",
                            "01E10", "01E20", "01C10", "01C20",
                            "01E05", "01E15", "01C05", "01C15"
                           )

    p_1 = ((150, 416, "PATH"), (-216, 466, "PAD", "1,1"), 
           (150, 415, "PATH")
           )
    p_4 = ((150, 416, "PATH"), (-216, 366, "PAD", "1,2"), (-216, 466 , "PAD", "1,1"), 
           (150, 416, "PATH"), (516, 466, "PAD", "2,1"), (516, 366, "PAD", "2,2"), 
           (150, 416, "PATH")
           )
    p_16 = ((150, 416, "PATH"), (-216, 266, "PAD", "2,3"), (-216, 366, "PAD", "1,3"), (-216, 466, "PAD", "1,2"), (-216, 566, "PAD", "2,2"), 
            (150, 416, "PATH"), (0, 832, "PAD", "1,1"), (100, 832, "PAD", "2,1"), (200, 832, "PAD", "3,1"), (300, 832, "PAD", "4,1"), 
            (150, 416, "PATH"), (516, 566, "PAD", "3,2"), (516, 466, "PAD", "4,2"), (516, 366, "PAD", "4,3"), (516, 266, "PAD", "3,3"), 
            (150, 416, "PATH"), (300, 0, "PAD", "4,4"), (200, 0, "PAD", "3,4"),  (100, 0, "PAD", "2,4"),  (0, 0, "PAD", "1,4"), 
            (150, 416, "PATH")
            )
    p_1wholewafer = ((-216, 496, "PAD", "1,1"))

    p_1wholewafer2 = ((150, 416, "PATH"), (-216, 496, "PAD", "1,1"), 
           (150, 415, "PATH"))
    p_1_temperature = ((150, 416, "PATH"), (-216, 466, "PAD", "1,1"), 
           (150, 415, "PATH")
           )
    p_4_temperature = ((150, 416, "PATH"), (-216, 366, "PAD", "1,2"), (-216, 466 , "PAD", "1,1"), 
           (150, 416, "PATH"), (516, 466, "PAD", "2,1"), (516, 366, "PAD", "2,2"), 
           (150, 416, "PATH")
           )
    p_16_temperature = ((150, 416, "PATH"), (-216, 266, "PAD", "2,3"), (-216, 366, "PAD", "1,3"), (-216, 466, "PAD", "1,2"), (-216, 566, "PAD", "2,2"), 
            (150, 416, "PATH"), (0, 832, "PAD", "1,1"), (100, 832, "PAD", "2,1"), (200, 832, "PAD", "3,1"), (300, 832, "PAD", "4,1"), 
            (150, 416, "PATH"), (516, 566, "PAD", "3,2"), (516, 466, "PAD", "4,2"), (516, 366, "PAD", "4,3"), (516, 266, "PAD", "3,3"), 
            (150, 416, "PATH"), (340, 0, "PAD", "4,4"), (200, 0, "PAD", "3,4"),  (100, 0, "PAD", "2,4"),  (0, 0, "PAD", "1,4"), 
            (150, 416, "PATH")
            )
    
    # The _short paths are used for quick scans, when all diodes are nor needed
    p_1_short = ((150, 416, "PATH"), (-216, 466, "PAD", "1,1"), 
           (150, 415, "PATH")
           )
    p_4_short = ((150, 416, "PATH"), (-216, 366, "PAD", "1,2"), (-216, 466 , "PAD", "1,1"), 
           (150, 416, "PATH"), (516, 466, "PAD", "2,1"), (516, 366, "PAD", "2,2"), 
           (150, 416, "PATH")
           )
    p_16_short = ((150, 416, "PATH"), (-216, 266, "PAD", "2,3"), (-216, 566, "PAD", "2,2"), 
            (150, 416, "PATH"), (516, 566, "PAD", "3,2"), (516, 266, "PAD", "3,3"),  
            (150, 416, "PATH")
            )

    def __init__(self):
        pass

    def find_path(self, *, msgServer, extra="", logger):
        """
        This method returns the path corresponding to the given path name.
        extra is a placeholder for future configurations where the static prober's positions 
        might change. It is currently not used.

        """
        response = msgServer.sendSciCommand("ReadMapPosition2")
        logger.path(f"ReadMapPosition2 output: {response}")
        
        # Parsing the response based on the format shown
        if isinstance(response, str):
            data = response.split()
        else:
            data=response
        if len(data) < 7:
            raise ValueError("Unexpected response format.")
        current_subdie = data[4]  # Current sub-die


        path_name = f"p_{self.dieNr_to_type[int(current_subdie) - 1]}{extra}"
        if hasattr(self, path_name):
            logger.path(f"Path found: {path_name}: {getattr(self, path_name)}")
            return getattr(self, path_name)
        else:
            raise ValueError(f"Path '{path_name}' not found in PathLibrary.")
    
    def get_diode_count(self, *, msgServer, subdie_Nr=-1, logger):
        if subdie_Nr == -1:

            response = msgServer.sendSciCommand("ReadMapPosition2")
            logger.path(f"ReadMapPosition2 output: {response}")
        
            # Parsing the response based on the format shown
            if isinstance(response, str):
                data = response.split()
            else:
                data=response
            if len(data) < 7:
                raise ValueError("Unexpected response format.")
            subdie_Nr = data[4]  # Current sub-die
        diode_count = self.dieNr_to_type[int(subdie_Nr) - 1]
        return diode_count
    
    def get_identifier(self, *, subdie_Nr=-1, msgServer, logger):
        if subdie_Nr == -1:
            response = msgServer.sendSciCommand("ReadMapPosition2")
            logger.path(f"ReadMapPosition2 output: {response}")
        
            # Parsing the response based on the format shown
            if isinstance(response, str):
                data = response.split()
            else:
                data=response
            if len(data) < 7:
                raise ValueError("Unexpected response format.")
            subdie_Nr = data[4]
        identifier = self.dieNr_to_identifier[int(subdie_Nr) - 1]
        guardring_value = identifier[3:5]
        entrance_window = identifier[2:3]
        return identifier, guardring_value, entrance_window


        
