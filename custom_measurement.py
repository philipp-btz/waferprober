'''
    
    Philipp Bartz 2025

    CREDIT: a major part of this code is based on Sonam Sharma's code 
    from her PHD thesis at the University of Heidelberg.
    
    This file is part of the Velox project.

'''

# #####       Version 1.3       #####


import serial
import custom_filehandler as cfile
import custom_waferprober as cwafer
import time
import matplotlib.pyplot as plt
import os
import json
import typing


# Initialize Keithley for IV scan using RS-232 communication
def init_IV(*, dev, logger):
    try:
        with serial.Serial(dev, baudrate=57600)  as ser:
            ser.write(b"*RST\n")
            ser.write(b"CURR:RANG 2E-9\n")
            ser.write(b"SYST:ZCH ON\n")
            ser.write(b"ARM:COUN 1\n")
            ser.write(b"INIT\n")
            ser.write(b"CURR:RANG:AUTO ON\n")
            ser.write(b"SOUR:VOLT:RANG 500\n")
            ser.write(b"SOUR:VOLT:ILIM 2.50e-3\n")
            ser.write(b"FORM:ELEM READ,VSO\n")
            ser.write(b"SYST:ZCOR:STAT OFF\n")
            ser.write(b"SYST:ZCOR:ACQ\n")
            ser.write(b"SYST:ZCOR:STAT ON\n")
            logger.info("Keithley initialized successfully.")

    except Exception as e:
        logger.critical(f"Error initializing Keithley: {e}")



# Perform IV measurement using Keithley and store results
def do_IV(*, dev, graph = [], start, stop, step, delay, is_last=False, logger, failed_measurement_timestamps):
    measurement_successful = False
    try:
        n = int(abs(stop - start) / step +1)
        max_expected_time = n * (delay+2) + 20
        
        #with serial.Serial(dev, baudrate=57600, timeout=int(max_expected_time)) as ser:
        with serial.Serial(dev, baudrate=57600, timeout=400) as ser:
            
            ser.write(f"TRAC:POIN {n}\n".encode())
            ser.write(f"SOUR:VOLT:SWE:STAR {start}\n".encode())
            ser.write(f"SOUR:VOLT:SWE:STOP {stop}\n".encode())
            ser.write(f"SOUR:VOLT:SWE:STEP {step}\n".encode())
            ser.write(f"SOUR:VOLT:SWE:DEL {delay}\n".encode())
            ser.write(f"TRIG:COUN {n}\n".encode())
            ser.write(b"SYST:ZCH OFF\n")
            ser.write(b"SOUR:VOLT:SWE:INIT\n")
            ser.flush()
            ser.write(b"INIT\n")
            ser.write(b"TRAC:DATA?\n")
            if is_last:
                ser.write(b"SYST:ZCH ON\n")
                ser.write(b"INIT\n")
                time.sleep(3)
            ser.flush()
            
            # Parse the IV data
            line = ser.readline().decode()
            print("readline, decode")
            logger.info(f"line: {line}")
            if line:
                points = line.split(',')
                n = len(points)
                logger.info(f"adding {n//2} points")
                for i in range(0, n - 1, 2):
                    try:
                        y = float(points[i])
                        x = float(points[i + 1])
                        if -500 < x < 500 and y < 500:
                            graph.append((x, y))
                            # check if that there is contact
                            if y > 5e-12:
                                measurement_successful = True

                    except ValueError:
                        logger.error(f"Error parsing data point: {points[i]}, {points[i + 1]}")
                if measurement_successful == False:
                    failed_measurement_timestamps.append(time.time())
                    
                return graph
            else:
                logger.error("No data returned by instrument")
                return None
    except Exception as e:
        logger.critical(f"Error performing IV scan: {e}")


## evtl. für auswertung
def sweep(*, graph, logger):
    if graph:
        initial_y = graph[0][1]
        processed_graph = [(x, y - initial_y) for x, y in graph]
        processed_graph[0] = (processed_graph[0][0], 1e-15)  
        return processed_graph
    else:
        logger.measurement("No data collected during the sweeps.")
        print("No data collected during the sweeps.")
        return[]
    

def measure(*, msgServer, device_port, folder, diode_Nr, settings, logger, plotting=False, extra, measurements_per_diode, measurement_no, path_to_config_file, failed_measurement_timestamps):
    try:
        store_data = cfile.save_to_json(folder="")
        die_pos, subdie_pos, x_position, y_position, column, row = cwafer.get_die_info(msgServer=msgServer, logger=logger)
        temp=cwafer.read_temperature_from_chuck(msgServer=msgServer, logger=logger)
        store_data.add(name="temp_at_start", value=temp)
        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
        store_data.add(name="time_at_start", value=timestr)
        if temp is None:
            logger.critical("Error: temperature measurement failed")
            return
        ### Import settings from file ###

        if not os.path.isfile(path_to_config_file):
                print(f"Error: File {path_to_config_file} does not exist.")
        with open(path_to_config_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {path_to_config_file}: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred while loading JSON file {path_to_config_file}: {e}")
                return None
            finally:
                file.close()
            
        delay_fbias = data.get("delay_fbias", 1)
        delay_rbias = data.get("delay_rbias", 1)
        start_fbias = data.get("start_fbias", 0.0)
        start_rbias = data.get("start_rbias", 0.0)
        step_fbias = data.get("step_fbias", 0.2)
        step_rbias = data.get("step_rbias", 0.1)
        stop_fbias = data.get("stop_fbias", -2.5)
        stop_rbias = data.get("stop_rbias", 50)
        tag_1 = data.get("tag_1", "")
        tag_2 = data.get("tag_2", "")
        tag_3 = data.get("tag_3", "")

        
        settings.add(name="start_rbias", value=start_rbias)
        settings.add(name="stop_rbias", value=stop_rbias)
        settings.add(name="step_rbias", value=step_rbias)
        settings.add(name="delay_rbias", value=delay_rbias)
        store_data.add(name="start_rbias", value=start_rbias)
        store_data.add(name="stop_rbias", value=stop_rbias)
        store_data.add(name="step_rbias", value=step_rbias)
        store_data.add(name="delay_rbias", value=delay_rbias)

        settings.add(name="start_fbias", value=start_fbias)
        settings.add(name="stop_fbias", value=stop_fbias)
        settings.add(name="step_fbias", value=step_fbias)
        settings.add(name="delay_fbias", value=delay_fbias)
        store_data.add(name="start_fbias", value=start_fbias)
        store_data.add(name="stop_fbias", value=stop_fbias)
        store_data.add(name="step_fbias", value=step_fbias)
        store_data.add(name="delay_fbias", value=delay_fbias)
        store_data.add(name="extra", value=extra)
        store_data.add(name="tag_1", value=tag_1)
        store_data.add(name="tag_2", value=tag_2)
        store_data.add(name="tag_3", value=tag_3)
        store_data.add(name="measurements_per_diode", value=measurements_per_diode)
        store_data.add(name="measurement_no", value=measurement_no)




        iv_data_rbias = []
        iv_data_fbias = []
        iv_data_rbias = do_IV(dev=device_port, graph=iv_data_rbias, start=start_rbias, stop=stop_rbias, step=step_rbias, delay=delay_rbias, is_last=False, logger=logger, failed_measurement_timestamps=failed_measurement_timestamps)
        time.sleep(2)
        iv_data_fbias = do_IV(dev=device_port, graph=iv_data_fbias, start=start_fbias, stop=stop_fbias, step=step_fbias, delay=delay_fbias, is_last=True, logger=logger, failed_measurement_timestamps=failed_measurement_timestamps)
        logger.measurement(str("Measurement data reverse Bias: " + str(iv_data_rbias)))
        logger.measurement(str("Measurement data forward Bias: " + str(iv_data_fbias)))
        if plotting and iv_data_rbias != None:
            x_val = [x[0] for x in iv_data_rbias]
            y_val = [x[1] for x in iv_data_rbias]
            plt.plot(x_val, y_val , 'o')
            plt.yscale("log")
            plt.title("reverse bias Measurement")
            plt.xlabel("Voltage")
            plt.ylabel("Current")
            plt.show()
        if plotting and iv_data_fbias != None:
            x_val = [x[0] for x in iv_data_fbias]
            y_val = [x[1] for x in iv_data_fbias]
            plt.plot(x_val, y_val , 'o')
            #plt.yscale("log")
            plt.title("forward bias Measurement")
            plt.xlabel("Voltage")
            plt.ylabel("Current")
            plt.show() 
        temp=cwafer.read_temperature_from_chuck(msgServer=msgServer, logger=logger)
        store_data.add(name="temp_at_end", value=temp)
        timestr = time.strftime("%Y_%m_%d-%H_%M_%S")
        store_data.add(name="time_at_end", value=timestr)
        #iv_data = sweep(iv_data)
        if iv_data_rbias or iv_data_fbias:
            cfile.save_IV(msgServer=msgServer, store_data=store_data, iv_data_rbias=iv_data_rbias, iv_data_fbias=iv_data_fbias, folder=folder, diode_Nr=diode_Nr, logger=logger, measurement_no=measurement_no)
            logger.measurement(f"IV data saved for diode {diode_Nr} at die {die_pos} subdie {subdie_pos} x {x_position} y {y_position}")
            logger.measurement(f"Probed and measured sub die {x_position} {y_position}")
        else:
            logger.measurement("No Data Returned from Measurement")
                
    except Exception as e:
        logger.critical(f"Error probing & measuring subdie {e}")