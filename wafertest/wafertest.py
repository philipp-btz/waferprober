#!/usr/bin/python3
import serial
import velox 
import time
import matplotlib.pyplot as plt
import os
import csv
from velox import *
# Connect to Velox Message Server
def connect_to_message_server():
    try:
        msgServer = velox.MessageServerInterface(ipaddr='129.206.177.74', targetSocket = 1412)
        print("Connected to Velox Message Server")
        return msgServer
    except Exception as e:
        print(f"Error connecting to Message Server: {e}")
        return None

# Register applications with Velox Message Server
def register_applications():
    try:
        # Register Wafer Map Application
        velox.RegisterProberAppChange("WaferMap", "WaferMapLoader", 0)
        print("WaferMap registered successfully.")
    except Exception as e:
        print(f"Error registering application: {e}")
        

# Initialize Keithley for IV scan using RS-232 communication
def init_IV(dev):
    try:
        with serial.Serial(dev, baudrate=57600)  as ser:
            ser.write(b"*RST\n")
            ser.write(b"CURR:RANG 2E-9\n")
            ser.write(b"SYST:ZCH ON\n")
            #ser-write(b"SYST:ZCORR ON\n")
            ser.write(b"ARM:COUN 1\n")
            ser.write(b"INIT\n")
            ser.write(b"CURR:RANG:AUTO ON\n")
            ser.write(b"SOUR:VOLT:RANG 500\n")
            ser.write(b"SOUR:VOLT:ILIM 2.50e-3\n")
            ser.write(b"FORM:ELEM READ,VSO\n")
            ser.write(b"SYST:ZCOR:STAT OFF\n")
            ser.write(b"SYST:ZCOR:ACQ\n")
            ser.write(b"SYST:ZCOR:STAT ON\n")
            print("Keithley initialized successfully.")
    except Exception as e:
        print(f"Error initializing Keithley: {e}")


# Read temperature from the chuck
def read_temperature_from_chuck(msgServer):
    try:
        response=msgServer.sendSciCommand("GetHeaterTemp")
        if isinstance(response,str):
            parts=response.split()
        else:
            parts=response

        if len(parts)<1:
            print(f"Error: Unexpected response: {response}")
            return None
        temperature=float(parts[0])
        print(f"Temperature: {temperature}C")
        return temperature

    except ValueError as ve:
        print(f"Error: Unable to parse temp value. Response: {response}")
        return None

    except Exception as e:
        print(f"Error reading temperature from chuck: {e}")
        return None

def get_die_info(msgServer):
    try:
        response = msgServer.sendSciCommand("ReadMapPosition2")
        print(f"ReadMapPosition2 output: {response}")
        
        # Parsing the response based on the format shown
        if isinstance(response, str):
            data = response.split()
        else:
            data=response
        if len(data) < 7:
            raise ValueError("Unexpected response format.")
        
        current_die = data[6]  # Current die
        current_subdie = data[4]  # Current sub-die
        x_position = data[2]  # X position
        y_position = data[3]  # Y position
        
        return current_die, current_subdie, x_position, y_position
    except Exception as e:
        print(f"Error getting die and sub-die positions: {e}")
        return "UnknownDie", "UnknownSubdie", "UnknownX", "UnknownY"

#Step to next sub die
def step_to_next_subdie(msgServer):
    try:
        response=msgServer.sendSciCommand("StepNextDie")
        print(f"Stepped to next subdie {response}")
        if "EndOfWafer" in response or "EndOfSubDieTable" in response:
            print("End of wafer or sub die tabel reached. Exiting....")
            return False
        return True
    except Exception as e:
        print(f"Error in stepping to next subdie {e}")
        return False

# Perform IV measurement and store results
def do_IV(dev, graph, start, stop, step, delay, is_last):
    try:
        n = int((stop - start) / step + 1)
        #timeout=None
        with serial.Serial(dev, baudrate=57600, timeout=None) as ser:
            ser.write(f"TRAC:POINTS {n}\n".encode())
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
            ser.flush()
            
            time.sleep(
            # Parse the IV data
            line = ser.readline().decode()
            if line:
                points = line.split(',')
                n = len(points)
                print(f"adding {n//2} points")
                for i in range(0, n - 1, 2):
                    try:
                        y = float(points[i])
                        x = float(points[i + 1])
                        if -500 < x < 500:
                            graph.append((x, y))
                    except ValueError:
                        print("Error parsing data point.")
            else:
                print("No data returned by instrument")
    except Exception as e:
        print(f"Error performing IV scan: {e}")

#create a folder to store IV results
def create_wafer_folder():
    base_folder_name="Wafer"
    folder_number=1
    while os.path.exists(f"{base_folder_name}{folder_number}"):
        folder_number+=1

    folder_name=f"{base_folder_name}{folder_number}"
    os.makedirs(folder_name)
    print(f"Created folder: {folder_name}")
    return folder_name

def get_unique_filename(folder, base_filename):
    file_path=os.path.join(folder, base_filename)
    if not os.path.exists(file_path):
        return file_path

    base, ext = os.path.splittext(base_filename)
    counter = 1
    while os.path.exists(file_path):
        file_path=os.path.join(folder, f"{base}_{counter}{ext}")
        counter+=1
    return file_path
        

# Save IV measurement results 
def save_iv_results(iv_data, temp, die_pos, subdie_pos, x_position, y_position,folder):
    if folder is None:
        print("Error:folder path is None. CAnnot save rsults.")
        return

    filename = f"IV_Die {die_pos} subdie {subdie_pos} X {x_position} Y {y_position}.csv"
    filepath= get_unique_filename(folder, filename)
    
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Voltage (V)", "Current (A)", "Temperature(C)", "Die Position", "Subdie Position", "X Position", "Y Position"])
        
        for x, y in iv_data:
            writer.writerow([x, y, temp, die_pos, subdie_pos, x_position, y_position])

    print(f"IV results saved to {filepath}")

# Process the IV measurement results and save them 
def sweep(dev, graph, start, stop, step, delay):
  #  graph = []  # List to store (x, y) data points

    # Perform the IV scan
    do_IV(dev, graph, start, stop, step, delay, is_last=True)
    if graph:
        initial_y = graph[0][1]
        processed_graph = [(x, y - initial_y) for x, y in graph]
        processed_graph[0] = (processed_graph[0][0], 1e-15)  
        return processed_graph
    else:
        print("No data collected during the sweeps.")
        return[]


#Probe and measure sub dies
def probe_and_measure(msgServer, device_port, folder):
    subdie_index=0
    try:
        while True:
            die_pos, subdie_pos, x_position, y_position = get_die_info(msgServer)
            temp=read_temperature_from_chuck(msgServer)
            if temp is None:
                print("Error: temperatue measurement failed")
                return
            start,stop,step,delay=0,41,1,1
            graph=[]

            iv_data=sweep(device_port, graph, start, stop, step, delay)


            if iv_data:
                save_iv_results(iv_data, temp, die_pos, subdie_pos, x_position, y_position, folder)
                print(f"Probed and measured sub die {x_position} {y_position}")
            
            if not step_to_next_subdie(msgServer):
                print("Exiting loop as end of wafer is reached")
                return
            subdie_index+= 1
    except Exception as e:
        print(f"Error probing & measuring subdie {e}")


def main():
     
    device_port = "/dev/ttyS0"  

    # Connect to Velox Message Server
    msgServer = connect_to_message_server()
    if not msgServer:
        return

    # Register applications using the new socket communication method
    register_applications()

    #init_IV(device_port)

    wafer_folder = create_wafer_folder()
    if wafer_folder is None:
        print("Error: Wafer folder is not created. Exiting..")
        return

    #probe_and_measure(msgServer, device_port, wafer_folder)

if __name__ == "__main__":
    main()

