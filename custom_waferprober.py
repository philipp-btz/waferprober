'''

    Philipp Bartz 2025

    CREDIT: some of this code is based on Sonam Sharma's code
    from her PHD thesis at the University of Heidelberg.

    This file is part of the Velox project.

'''

# #####       Version 1.0       #####


import velox


# Connect to Velox Message Server
def connect_to_message_server(*, ip, logger):
    try:
        msgServer = velox.MessageServerInterface(ipaddr = ip, targetSocket = 1412)
        logger.waferprober(f"Connected to Velox Message Server at {ip}.")
        return msgServer
    except Exception as e:
        logger.waferprober(f"Error connecting to Velox Message Server: {e}")

        return None
    

# Register applications with Velox Message Server
def register_applications(*, logger):
    try:
        # Register Wafer Map Application
        velox.RegisterProberAppChange("WaferMap", "WaferMapLoader", "0")
        logger.waferprober("WaferMap application registered successfully.")
    except Exception as e:
        logger.critical(f"Error registering WaferMap application: {e}")

#function to read the prober status
def read_prober_status(*, msgServer, logger):
    try:
        response=msgServer.sendSciCommand("ReadProberStatus")
        logger.waferprober(f"Prober Status: {response}")
        return response
    except Exception as e:
        logger.error(f"Error reading prober status: {e}")
        return None
    

def set_heater_temp(*, msgServer, temperature, logger):
    try:
        command=f"SetHeaterTemp {temperature}"
        response=msgServer.sendSciCommand("SetHeaterTemp", str(temperature) , "C")
        logger.waferprober(f"Set heater temperature to {temperature}C")


    except Exception as e:
        logger.error(f"Error setting heater temperature: {e}")

#Function to set camera and motor to quiet mode
def set_quiet_mode(*, msgServer, quiet_mode=True, logger):
    try:
        if quiet_mode == True:
            scope_response=msgServer.sendSciCommand("SetCameraQuiet", 1)
            motor_response=msgServer.sendSciCommand("EnableMotorQuiet", 1)
            logger.quiet(f"Motor Quiet Mode ENabled")
        elif quiet_mode == "AUTO":
            chuck_response = msgServer.sendSciCommand("SetChuckMode", 2, 2, 2, 2, 2, 1)
            probe_response = msgServer.sendSciCommand("SetProbeMode", 1, 2, 2, 2, 2, 1)
            scope_response = msgServer.sendSciCommand("SetScopeMode", 1, 2)
            logger.quiet(f"AUTO Motot Quiet Mode enabled")
            logger.quiet(f"Scope quiet mode response: {scope_response}")
            logger.quiet(f"Probe quiet mode response: {probe_response}")
            logger.quiet(f"Chuck quiet mode response: {chuck_response}")
        else:
            scope_response=msgServer.sendSciCommand("SetCameraQuiet", 0)
            motor_response=msgServer.sendSciCommand("EnableMotorQuiet", 0)
            logger.quiet(f"Motor Quiet Mode DISabled")
    except Exception as e:
        logger.error(f"Error setting quiet mode: {e}")
        return None

# this is used to set the motor quiet mode only
def set_quiet_mode_motor(*, msgServer, quiet_mode=True, logger):
    try:
        if quiet_mode == True:
            motor_response=msgServer.sendSciCommand("EnableMotorQuiet", 1)
            logger.quiet(f"Motor Quiet Mode ENabled {motor_response}")
        else:
            motor_response=msgServer.sendSciCommand("EnableMotorQuiet", 0)
            logger.quiet(f"Motor Quiet Mode DISabled {motor_response}")
    except Exception as e:
        logger.error(f"Error setting quiet mode: {e}")
        return None

# this is used to set the scope quiet mode only
def set_quiet_mode_scope(*, msgServer, quiet_mode=True, logger):
    try:
        if quiet_mode == True:
            scope_response=msgServer.sendSciCommand("SetCameraQuiet", 1)
            logger.quiet(f"Scope Quiet Mode ENabled {scope_response}")
        else:
            scope_response=msgServer.sendSciCommand("SetCameraQuiet", 0)
            logger.quiet(f"Scope Quiet Mode DISabled {scope_response}")
    except Exception as e:
        logger.error(f"Error setting quiet mode: {e}")
        return None


# Read temperature from the chuck
def read_temperature_from_chuck(*, msgServer, logger):
    try:
        response=msgServer.sendSciCommand("GetHeaterTemp")
        if isinstance(response,str):
            parts=response.split()
        else:
            parts=response

        if len(parts)<1:
            logger.error(f"Error: Unexpected response format: {response}")
            return None
        temperature=float(parts[0])
        logger.waferprober(f"Temperature: {temperature}C")
        return temperature

    except ValueError as ve:
        logger.error(f"Error: Unable to parse temperature value. Response: {ve}")
        return None

    except Exception as e:
        logger.critical(f"Error reading temperature from chuck: {e}")
        return None
    

def get_die_info(*, msgServer, logger):
    try:
        response = msgServer.sendSciCommand("ReadMapPosition2")
        logger.waferprober(f"ReadMapPosition2 output: {response}")
        
        # Parsing the response based on the format shown
        if isinstance(response, str):
            data = response.split()
        else:
            data=response
        if len(data) < 7:
            raise ValueError("Unexpected response format.")
        column = data[0]  # column number
        row = data[1]  # row number
        current_die = data[6]  # Current die
        current_subdie = data[4]  # Current sub-die
        x_position = data[2]  # X position
        y_position = data[3]  # Y position
        return current_die, current_subdie, x_position, y_position, column, row
    except Exception as e:
        logger.error(f"Error getting die and sub-die positions: {e}")
        return "UnknownDie", "UnknownSubdie", "UnknownX", "UnknownY", "UnknownColumn", "UnknownRow"



#Step to next sub die
def step_to_next_subdie(*, msgServer, logger):
    try:
        response=msgServer.sendSciCommand("StepNextDie")
        logger.waferprober(f"Stepped to next subdie: {response}")
        if "EndOfWafer" in response or "EndOfSubDieTable" in response:
            logger.waferprober("End of wafer or sub die table reached. Exiting....")
            return False
        return True
    except Exception as e:
        logger.critical(f"Error stepping to next subdie: {e}")
        return False
    
def set_home(*, msgServer, logger, offset = False):
    logger.critical(f"Setting new Home Position")
    if offset == False:
        response = msgServer.sendSciCommand("SetProbeHome", "1", "0")
    else:
        position = msgServer.sendSciCommand("ReadProbePosition", "1")
        homex = float(position[2])
        homey = float(position[3])

def get_chuck_temperature(*, msgServer, logger):
    try:
        response = msgServer.sendSciCommand("GetHeaterTemp")
        if isinstance(response, str):
            parts = response.split()
        else:
            parts = response
        if len(parts) < 1:
            logger.error(f"Error: Unexpected response format: {response}")
            return None
        temperature = float(parts[0])
        logger.waferprober(f"Chuck Temperature: {temperature}C")
        return temperature
    except Exception as e:
        logger.critical(f"Error reading chuck temperature: {e}")
        return None

def set_scope_light(*, msgServer, light_on=True, logger):
    try:
        if light_on:
            response = msgServer.sendSciCommand("SetMicroLight", 1)
            logger.waferprober("Scope light turned ON")
        else:
            response = msgServer.sendSciCommand("SetMicroLight", 0)
            logger.waferprober("Scope light turned OFF")
        return response
    except Exception as e:
        logger.error(f"Error controlling scope light: {e}")
        return None
