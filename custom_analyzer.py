'''

    Philipp Bartz 2025

    This file is part of the Velox project.
'''

#####       Version 2.1       #####

import os
import time
import json
import matplotlib.pyplot as plt
import numpy as np
import typing
import math
from scipy.optimize import curve_fit
import statistics
import typing



'''
From:
A model based DC analysis of SiPM breakdown voltages
Ferenc Nagy, Gyula Hegyesi, Gábor Kalinka, József Molnár
Institute for Nuclear Research, Hungarian Academy of Sciences, Bem ter 18/c, Debrecen H-4026, Hungary
https://doi.org/10.1016/j.nima.2017.01.002
term (10) (p. 4)
'''
def diode_fit(V, sig, mean, A, h):
    '''
    V > Voltage
    sig > standard deviation
    mean > mean V01 Voltage
    A > Amplitude
    h > hysteresis
    '''
    y = []
    for i in V:
        factor1 = 2 - (h/(sig**2)) * (i-mean)
        fraction_top = (i-mean) ** 2
        fraction_bottom = 2 * sig * sig
        factor2 = math.exp(-1 * (fraction_top / fraction_bottom))
        y2 = A * factor1 * factor2
        y.append(y2)
    return y






'''
    this class contains analysis and data handling utilities for the JSON data collected by the Velox project.
'''
class Dataset():


    def __init__(self, *, description: typing.Optional[str] = None) -> None:
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.data: typing.Dict[str, typing.Dict[str, typing.Any]] = {}  # the raw data from all selected json files. For more, conslt Dataset.add_files()
        self.slices: typing.Dict[str, typing.Dict[str, typing.Any]] = {}    # the data sliced by different parameters. For more, consult Dataset.filter()
        self.description = description


    # In case, the dataset consists of only one slice, you dont have to specify the slicename, it will be picked automatically.
    # If there are multiple slices, you have to specify the slicename.
    def _slicename_provider(self, *, slicename: typing.Optional[str] = None) -> str:
        if slicename is None and len(self.slices) == 1:
            return list(self.slices.keys())[0]
        elif slicename is None and len(self.slices) > 1:
            raise ValueError("You must specify a slicename when there are multiple slices.")
        else:
            return str(slicename) 

    def add_files(self, *, files: typing.List[typing.Any] = [], only_measurements: bool = True) -> None:
        try:
            if only_measurements:
                for i in files:
                    if not os.path.isfile(i):
                        raise FileNotFoundError(f"File {i} does not exist.")
                    if i.endswith(".json") and "IV_" in i:
                        with open(i, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            self.data[i] = data
            else:
                for i in files:
                    if not os.path.isfile(i):
                        raise FileNotFoundError(f"File {i} does not exist.")
                    if i.endswith(".json"):
                        with open(i, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            self.data[i] = data
            return
        except Exception as e:
            print(f"Error loading files: {e}")
            return
        
    def get_times_at_start(self) -> typing.List[str]:
        starttimes: typing.List[str] = []
        for filename, data in self.data.items():
            if "time_at_start" in data:
                starttimes.append(data["time_at_start"])
            else:
                print(f"Warning: 'starttime' not found in {filename}")
        return starttimes

    # this function lets you get all entries with the specified key from all data loaded into the Dataset.
    def get(self, *, key : str, pretty : bool = False) -> typing.List[typing.Tuple[str, typing.Any]]:
        output: typing.List[typing.Tuple[str, typing.Any]] = []
        if pretty:
            for filename, data in self.data.items():
                if str(key) in data:
                    output.append((filename, data[str(key)]))
                else:
                    print(f"Warning: '{key}' not found in {filename}")
        else:
            for filename, data in self.data.items():
                if str(key) in data:
                    output.append(data[str(key)])
                else:
                    print(f"Warning: '{key}' not found in {filename}")
        return output

    # same as Dataset.get(...) but for a specific slice
    def get_from_slice(self, *, slicename: typing.Optional[str] = None, key : str, pretty : bool = False) -> typing.List[typing.Tuple[str, typing.Any]]:
        slicename = self._slicename_provider(slicename=slicename)
        output: typing.List[typing.Tuple[str, typing.Any]] = []
        if pretty == True:
            for filename, data in self.slices[slicename].items():
                if str(key) in data:
                    output.append((filename, data[str(key)]))
                else:
                    print(f"Warning: '{key}' not found in {filename}")
        else:
            for filename, data in self.slices[slicename].items():
                if str(key) in data:
                    output.append(data[str(key)])
                else:
                    print(f"Warning: '{key}' not found in {filename}")
        return output
    
    '''
    this function filters the data based on a parameter and a range or value.
    the filtered data is stored in the slices dictionary
    an extra function to filter slices, not the whole dataset is Dataset.filter_slice(...)
    the range parameter is inclusive
    
    it will return the name of the slice and the filtered data.
    '''
    def filter(self, *, 
               parameter: str, 
               range: typing.Optional[typing.List[float]] = None, 
               value: typing.Optional[typing.Union[float, str, int]] = None, 
               slicename: typing.Optional[str] = None) -> typing.Tuple[str, typing.Dict[typing.Any, typing.Any]]:
        if range is not None and value is not None:
            raise ValueError("You can only specify either 'range' or 'value', not both.")
        if range is None and value is None:
            raise ValueError("You must specify either 'range' or 'value'.")
        if slicename is None:
            slicename = f"filter_{parameter}_range_{range}_value_{value}"
        else:
            slicename = str(slicename)
        slice = {}
        if range is not None:
            if not isinstance(range, list) or len(range) != 2:
                raise ValueError("Range must be a list with two elements.")
            min_val, max_val = range
            for filename, data in self.data.items():
                if parameter in data and min_val <= data[parameter] <= max_val:
                    slice[filename] = data
            self.slices[slicename] = slice
        elif value is not None:
            for filename, data in self.data.items():
                if parameter in data and data[parameter] == value:
                    slice[filename] = data
            self.slices[slicename] = slice

        else:
            raise ValueError("Either range or value must be provided.")

        return slicename, slice

    '''
    like Dataset.filter(...) this functiun filters data based on a parameter and a range or value.
    the DIFFERENCE is that Dataset.filter_slices(...) is used to further filter existing slices.
    the range parameter is inclusive
    '''
    def filter_slice(self, *, 
                     target_slice_name: typing.Optional[str] = None, 
                     parameter: str, 
                     range: typing.Optional[typing.List[float]] = None, 
                     value: typing.Optional[typing.Union[float, str, int]] = None, 
                     name: typing.Optional[str] = None) -> typing.Tuple[str, typing.Dict[typing.Any, typing.Any]]:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        if name is None:
            name = target_slice_name
        if target_slice_name not in self.slices:
            raise ValueError(f"Slice '{target_slice_name}' does not exist.")
        if range is not None and value is not None:
            raise ValueError("You can only specify either 'range' or 'value', not both.")
        if range is None and value is None:
            raise ValueError("You must specify either 'range' or 'value'.")
        target_slice = self.slices[target_slice_name]
        new_slice = {}

        if range is not None:
            if not isinstance(range, list) or len(range) != 2:
                raise ValueError("Range must be a list with two elements.")
            min_val, max_val = range
            for filename, data in target_slice.items():
                
                if parameter in data and min_val <= target_slice[filename][parameter] <= max_val:
                    new_slice.update({filename: {parameter: data}})


            self.slices[name] = new_slice

        elif value is not None:
            for filename, data in target_slice.items():
                if parameter in data and target_slice[filename][parameter] == value:
                    new_slice.update({filename: data})
            self.slices[name] = new_slice

        else:
            raise ValueError("Either range or value must be provided.")
        
        return name, new_slice

    def get_slice(self, *, target_slice_name: typing.Optional[str] = None) -> dict:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        if target_slice_name not in self.slices:
            raise ValueError(f"Slice '{target_slice_name}' does not exist.")
        target_slice = self.slices[target_slice_name]
        return target_slice
    
    # this function returns the total number of entries in a data slice
    def get_size(self, *, target_slice_name: typing.Optional[str] = None) -> int:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        if target_slice_name not in self.slices:
            raise ValueError(f"Slice '{target_slice_name}' does not exist.")
        target_slice = self.slices[target_slice_name]
        return len(target_slice)


    # this function returns the values of a data slice
    def get_vals(self, *, 
                 target_slice_name: typing.Optional[str] = None, 
                 rbias_only: bool = False, 
                 fbias_only: bool = False) -> typing.Dict[float, typing.List[float]]: # this function returns the values of a data slice
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        if rbias_only and fbias_only:
            raise ValueError("You can only specify either 'rbias_only' or 'fbias_only', not both.")
        target_slice = self.slices[target_slice_name]
        vals = {}
        if not rbias_only:
            for measurement in target_slice:
                if "iv_data_fbias" in target_slice[measurement]:
                    for x, y in target_slice[measurement]["iv_data_fbias"]:
                        if x not in vals:
                            vals[x] = [y]
                        else:
                            vals[x].append(y)
        if not fbias_only:
            for measurement in target_slice:
                if "iv_data_rbias" in target_slice[measurement]:
                    for x, y in target_slice[measurement]["iv_data_rbias"]:
                        if x not in vals:
                            vals[x] = [y]
                        else:
                            vals[x].append(y)
        target_slice["vals"] = vals
        return vals


    # this function calculates the mean of y vales of a data slice
    def get_slice_mean(self, *, target_slice_name: typing.Optional[str] = None, rbias_only: bool = False, fbias_only: bool = False) -> typing.Dict[float, float]: 
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        if hasattr(target_slice, "vals"):
            vals = target_slice["vals"]
        else:
            vals = self.get_vals(target_slice_name=target_slice_name, rbias_only=rbias_only, fbias_only=fbias_only)
        mean = {}
        for x, y in vals.items():
            mean[x] = sum(y) / len(y)
        target_slice["mean"] = mean
        return mean
    
    # this function calculates the standard deviation of y vales of a data slice
    def get_slice_std(self, *, target_slice_name: typing.Optional[str] = None, rbias_only: bool = False, fbias_only: bool = False) -> typing.Dict[float, float]:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        if hasattr(target_slice, "vals"):
            vals = target_slice["vals"]
        else:
            vals = self.get_vals(target_slice_name=target_slice_name, rbias_only=rbias_only, fbias_only=fbias_only)
        
        std = {}
        for x, y in vals.items():
            mean = sum(y) / len(y)
            variance = sum((i - mean) ** 2 for i in y) / (len(y) - 1)
            std[x] = np.sqrt(variance)
        target_slice["std"] = std
        return std 

    # this function calculates the standard error of y vales of a data slice
    def get_slice_se(self, *, target_slice_name: typing.Optional[str] = None, rbias_only: bool = False, fbias_only: bool = False) -> typing.Dict[float, float]:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        if hasattr(target_slice, "vals"):
            vals = target_slice["vals"]
        else:
            vals = self.get_vals(target_slice_name=target_slice_name, rbias_only=rbias_only, fbias_only=fbias_only)
        
        std = self.get_slice_std(target_slice_name=target_slice_name, rbias_only=rbias_only, fbias_only=fbias_only)
        se = {}
        for x, std in std.items():
            se[x] = std / np.sqrt(len(vals[x]))
        target_slice["se"] = se
        return se
    
    def get_slice_median(self, *, 
                       target_slice_name: typing.Optional[str] = None,
                       rbias_only: bool = False,
                       fbias_only: bool = False) -> typing.Dict[float, float]:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        if hasattr(target_slice, "vals"):
            vals = target_slice["vals"]
        else:
            vals = self.get_vals(target_slice_name=target_slice_name, rbias_only=rbias_only, fbias_only=fbias_only)

        median = {}
        for x, y in vals.items():
            median[x] = statistics.median(y)
        target_slice["median"] = median
        return median

    def get_slice_mode(self, *,
                       target_slice_name: typing.Optional[str] = None,
                       rbias_only: bool = False,
                       fbias_only: bool = False) -> typing.Dict[float, float]:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        if hasattr(target_slice, "vals"):
            vals = target_slice["vals"]
        else:
            vals = self.get_vals(target_slice_name=target_slice_name, rbias_only=rbias_only, fbias_only=fbias_only)

        mode = {}
        for x, y in vals.items():
            mode[x] = statistics.mode(y)
        target_slice["mode"] = mode
        return mode

    def export_slice(self, *, 
                     target_slice_name: typing.Optional[str] = None, 
                     filename: typing.Optional[str] = None, 
                     folder: typing.Optional[str] = None) -> str:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        if target_slice_name not in self.slices:
            raise ValueError(f"Slice '{target_slice_name}' does not exist.")
        if folder is None:
            folder = os.getcwd()
        if filename is None:
            filename = f"{target_slice_name}.json"
        with open(os.path.join(folder, filename), 'w', encoding='utf-8') as file:
            json.dump(self.slices[target_slice_name], file, indent=4,sort_keys=True)
        return os.path.join(folder, filename)
    

    # This function cleans the data in a slice by removing entries with outliers in the rbias data.
    def clean_slice_data_rbias(self, *, 
                        target_slice_name: typing.Optional[str] = None,
                        verbose: bool = False,
                        files: bool = False,
                        taken: bool = False,
                        reverse: bool = False) -> None: #when reverse is True, it will keep the entries with outliers and removing the ones that would otherwise pass
        if not os.path.isdir("figs/outliers") and files:
            os.makedirs("figs/outliers")
        if not os.path.isdir("figs/taken") and files and taken:
            os.makedirs("figs/taken")
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        cleaned_t_s = {}
        print("len target_slice", len(target_slice))
        print(f"Cleaning slice {target_slice_name} with {len(target_slice)} entries")
        for filename, data in target_slice.items():
            if "iv_data_rbias" in data:
                rbias_data = data["iv_data_rbias"]
                if len(rbias_data) > 20:
                    reason = ""
                    low_V_Threshhold = False
                    single_HV_value_over_thresh = False
                    i = []
                    j = []
                    for x, y in rbias_data:
                        i.append(x)
                        j.append(y)
                        if 5<= x <= 15 and y > 5e-7:
                            low_V_Threshhold = True
                        elif 40 <= x <= 50 and y > 1e-11:
                            single_HV_value_over_thresh = True
                        else:
                            pass
                    if not low_V_Threshhold and single_HV_value_over_thresh:
                        # print(f"Keeping {filename} in slice {target_slice_name}")
                        if not reverse:
                            cleaned_t_s[filename] = data
                        if files and taken:
                            fig = plt.figure(figsize=(16, 9))
                            plt.plot(i,j, label=filename)
                            plt.title(f"taken {data['temp_at_start']}C in {filename}")
                            plt.yscale("log")
                            plt.xlabel("Voltage (V)")
                            plt.ylabel("Current (A)")
                            plt.grid(True)
                            plt.axhline(0, color='black')
                            plt.axhline(1e-6, color='r')
                            plt.axvline(0, color='black')
                            plt.legend()
                            plt.savefig(os.path.join("figs/taken", f"{target_slice_name}_{filename.replace('/', '+')}_{time.strftime('%Y_%m_%d-%H_%M_%S')}.png"), bbox_inches='tight', dpi=300)
                            plt.close(fig)
                    else:
                        if reverse:
                            cleaned_t_s[filename] = data
                        if verbose:
                            print(f"Removing {filename} from slice {target_slice_name} due to outliers in rbias data")
                        if files:# and single_HV_value_over_thresh: #TODO: remove single_HV_value_over_thresh, it only needed for testing
                            fig = plt.figure(figsize=(16, 9))
                            plt.plot(i,j, label=filename)
                            reason = ""
                            if low_V_Threshhold:
                                reason += " Low Voltage Outliers "
                            if not single_HV_value_over_thresh:
                                reason += " High Voltage Outliers "
                            plt.title(f"{data['temp_at_start']}C Outliers {reason} in {filename}")
                            plt.yscale("log")
                            plt.xlabel("Voltage (V)")
                            plt.ylabel("Current (A)")
                            plt.grid(True)
                            plt.axhline(0, color='black')
                            plt.axhline(1e-6, color='r')
                            plt.axvline(0, color='black')
                            plt.legend()
                            plt.savefig(os.path.join("figs/outliers", f"{target_slice_name}_{filename.replace('/', '+')}_{time.strftime('%Y_%m_%d-%H_%M_%S')}.png"), bbox_inches='tight', dpi=300)
                            plt.close(fig)
                        pass
                else:
                    if verbose:
                        print(f"Removing {filename} from slice {target_slice_name} due to insufficient number of rbias measurement-points ({len(rbias_data)})")
                    pass
            else:
                if verbose:
                    print(f"Removing {filename} from slice {target_slice_name} due to missing 'iv_data_rbias' key")
                pass
        try:
            slice_yield = len(cleaned_t_s) / len(target_slice)
        except ZeroDivisionError:
            slice_yield = 0
        print("len cleaned_t_s", len(cleaned_t_s))
        print(f"Yield of cleaned slice {target_slice_name}: {slice_yield:.2%}")
        if slice_yield < 0.5:
            print(f"Warning: Yield of cleaned slice {target_slice_name} is below 50% ({slice_yield:.2%}), consider adjusting the cleaning criteria.")
        self.slices[target_slice_name] = cleaned_t_s
        return



    '''
    This function gets the nth derivative of the means of a data slice
    '''
    #TODO calculate errors for derivatives
    def get_nth_derivative(self, *, 
                            target_slice_name: typing.Optional[str] = None, 
                            n: int = 1, rbias_only: bool = False, fbias_only: bool = False,
                            force_calculations: bool = False) -> typing.Dict[float, float]:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        if n < 1:
            raise ValueError("n must be greater than or equal to 1.")
        
        if n < 1:
            raise ValueError("n must be greater than or equal to 1.")
        elif n == 1:
            target_slice = self.slices[target_slice_name]
            if "mean" not in target_slice:
                self.get_slice_mean(target_slice_name=target_slice_name, 
                                    rbias_only=rbias_only, 
                                    fbias_only=fbias_only)
            mean = target_slice["mean"]
            print(f"mean: {mean}")
            x_vals = sorted(mean.keys())
            y_vals = [mean[x] for x in x_vals]
            if force_calculations == False and f"derivative_{n}" in target_slice:
                print(f"1st derivative already calculated, returning cached value.")
                return target_slice[f"derivative_{n}"]
            slopes = []
            # Calculate the first derivative (slope) using finite differences
            for i in range(len(y_vals)-1):
                dy_dx = (y_vals[i + 1] - y_vals[i]) / (x_vals[i + 1] - x_vals[i])
                slopes.append(dy_dx)
            # Create a dictionary with x values as keys and slopes as values
            derivative = dict(zip(x_vals, slopes))
            print(f"Calculated 1st derivative for {target_slice_name} with n={n}")
            print(f"1st derivative: {derivative}")
            target_slice[f"derivative_{n}"] = derivative

            return derivative
        elif n >= 2:
            target_slice = self.slices[target_slice_name]
            if f"derivative_{n-1}" not in target_slice:
                self.get_nth_derivative(target_slice_name=target_slice_name, rbias_only=rbias_only, fbias_only=fbias_only, n=n-1, force_calculations=force_calculations)
            values = target_slice[f"derivative_{n-1}"]
            print(f"mean: {values}")
            x_vals = sorted(values.keys())
            y_vals = [values[x] for x in x_vals]
            if force_calculations == False and f"derivative_{n}" in target_slice:
                print(f"{n} derivative already calculated, returning cached value.")
                return target_slice[f"derivative_{n}"]
            slopes = []
            # Calculate the first derivative (slope) using finite differences
            for i in range(len(y_vals) - 1):
                dy_dx = (y_vals[i + 1] - y_vals[i]) / (x_vals[i + 1] - x_vals[i])
                slopes.append(dy_dx)
            # Create a dictionary with x values as keys and slopes as values
            derivative = dict(zip(x_vals, slopes))
            print(f"Calculated {n} derivative for {target_slice_name}")
            print(f"{n} derivative: {derivative}")
            target_slice[f"derivative_{n}"] = derivative

            return derivative
        else:
            raise NotImplementedError("This ist not implemented. Only n=1 and n>1 are supported.")

    '''
    this function returns a list of all Current values (I) at a given Voltage (V) for a specific slice.
    '''
    def get_I_at_V(self, *, target_slice_name: str, voltage: float) -> list:
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        I_list = []
        for filename, data in target_slice.items():
            IV_data_fbias = data["iv_data_fbias"]
            if IV_data_fbias is not None:
                for v, i in IV_data_fbias:
                    if v == voltage:
                        I_list.append(i)
            IV_data_rbias = data["iv_data_rbias"]
            if IV_data_rbias is not None:
                for v, i in IV_data_rbias:
                    if v == voltage:
                        I_list.append(i)
        return I_list

    def fit_graph(self, *, target_slice_name, 
                  function = diode_fit, 
                  rbias_only: bool = False, 
                  fbias_only: bool = False, 
                  force_calculations: bool = False):
        print("Fit4567890")
        target_slice_name = self._slicename_provider(slicename=target_slice_name)
        target_slice = self.slices[target_slice_name]
        derivative = self.get_nth_derivative(target_slice_name=target_slice_name, n=3, rbias_only=rbias_only, fbias_only=fbias_only, force_calculations=force_calculations)
        xdata = np.array(list(derivative.keys()))
        ydata = np.array(list(derivative.values()))
        xdata = np.array(list(derivative.keys()))
        ydata = np.array(list(derivative.values()))
        popt, pcov = curve_fit(function, xdata, ydata)
        print(f"popt: {popt}")
        target_slice[f"fit_with_{function.__name__}"] = popt
        fitted_y = function(xdata, *popt)
        print(f"fitted_y: {fitted_y}")
        fitted_xy = dict(zip(xdata, fitted_y))
        fitted_y = function(xdata, *popt)
        print(f"fitted_y: {fitted_y}")
        fitted_xy = dict(zip(xdata, fitted_y))
        target_slice[f"fitted_xy"] = fitted_xy

        return fitted_xy



def get_all_filenames(*, startdir: str) -> typing.List[str]:
    f = []
    if startdir[-1] == "/":
        startdir = startdir[0:-1]
    w = os.walk(startdir)
    for (dirpath, dirnames, filenames) in w:
        for i in filenames:
            f.append(f"{dirpath}/{i}")
    return f


# This class is used to create and plot graphs based on the data collected
class Graph():
    def __init__(self, *, 
                 x: typing.Optional[typing.List[float]] = None, y: typing.Optional[typing.List[float]] = None, 
                 title: typing.Optional[str] = None, 
                 xlabel: typing.Optional[str] = None, 
                 ylabel: typing.Optional[str] = None, 
                 err_y: typing.Optional[typing.List[float]] = None, 
                 yscale = "symlog", 
                 xscale = "linear",
                 xmin = None,
                 xmax = None) -> None:
        self.x = x
        self.y = y
        self.x_help = []
        self.y_help = []
        self.err_y = err_y
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.yscale = yscale
        self.xscale = xscale
        self.created_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.x_1st = []
        self.y_1st = []
        self.x_2nd = []
        self.y_2nd = []
        self.x_3rd = []
        self.y_3rd = []
        self.xmin = xmin
        self.xmax = xmax

        return
    '''
    def plot(self) -> None:
        if self.x is None or self.y is None:
            raise ValueError("x and y values must be set before plotting.")
        elif len(self.x) != len(self.y):
            raise ValueError("x and y must have the same length.")
        else:
            pass
        fig = plt.figure()
        if self.err_y is not None and isinstance(self.err_y, list) and len(self.err_y) == len(self.y):
            plt.errorbar(self.x, self.y, yerr=self.err_y, fmt='o', capsize=5, label='Data')
        else:
            plt.plot(self.x, self.y, marker='o', linestyle='-', label='Data')
        if self.x_help != [] and self.y_help != []:
            plt.plot(self.x_help, self.y_help, marker='x', linestyle='--', color='red', label='Help Line')
    
        plt.title(str(self.title) if self.title else "Graph")
        plt.yscale(self.yscale)
        plt.xscale(self.xscale)
        plt.xlabel(str(self.xlabel) if self.xlabel else "Voltage (V)")
        plt.ylabel(str(self.ylabel) if self.ylabel else "Current (A)")
        plt.grid(True)
        fig.set_facecolor('w')
        plt.show()

        return
    '''




    # this function saves the graph to a file.
    def save(self, *, folder: typing.Optional[str] = None, label='Data',  to_stdout: bool = False,  close_fig: bool = True, fig: typing.Optional[plt.figure] = None):
        plt.ioff()
        filename = f"graph_{self.title}.png"
        if not os.path.isdir(str(folder)):
            os.makedirs(str(folder))
        #if self.x is None or self.y is None:
            #raise ValueError("x and y values must be set before plotting.")
        else:
            pass

        if fig is None:
            fig = plt.figure()

        # plotting main data (optional)
        if self.y is not None and self.x is not None:
            if self.err_y is not None and isinstance(self.err_y, list) and len(self.err_y) == len(self.y):
                if len(self.x) != len(self.y):
                    raise ValueError("x and y must have the same length.")
                else:
                    plt.errorbar(self.x, self.y, yerr=self.err_y, fmt='o', capsize=5, label=label)
            else:
                if len(self.x) != len(self.y):
                    raise ValueError("x and y must have the same length.")
                else:
                    plt.plot(self.x, self.y, marker='o', linestyle='-', label=label)
        else:
            print("Plotting data without main values")

        # plotting auxilary lines
        if self.x_help != [] and self.y_help != []:
            plt.plot(self.x_help, self.y_help, marker='x', linestyle='--', color='red', label='Help Line')
        if self.x_1st != [] and self.y_1st != []:
            print("Plotting 1st derivative")
            plt.plot(self.x_1st, self.y_1st, marker='x', linestyle='--', color='red', label='1st Derivative')
            plt.legend()
        if self.x_2nd != [] and self.y_2nd != []:
            print("Plotting 2nd derivative")
            plt.plot(self.x_2nd, self.y_2nd, marker='x', linestyle='--', color='green', label='2nd Derivative')
            plt.legend()
        if self.x_3rd != [] and self.y_3rd != []:
            print("Plotting 3rd derivative")
            plt.plot(self.x_3rd, self.y_3rd, marker='x', linestyle='--', color='yellow', label='3rd Derivative')
            plt.legend()

        plt.title(str(self.title) if self.title else "Graph")
        plt.yscale(self.yscale)
        plt.xscale(self.xscale)
        plt.xlim(left=self.xmin, right=self.xmax)
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')   
        plt.xlabel(str(self.xlabel) if self.xlabel else "Voltage (V)")
        plt.ylabel(str(self.ylabel) if self.ylabel else "Current (A)")
        plt.grid(True)
        fig.set_facecolor('w')
        if to_stdout:
            plt.show()
        else:
            fig.savefig(os.path.join(folder, filename) if folder else filename, bbox_inches='tight', dpi=300)
            if close_fig:
                plt.close(fig)
            print(f"Graph saved to {os.path.join(folder, filename) if folder else filename}")
        return fig

    '''
    this function unpacks the data given from Dataset()
    it can unpack x and y values (mode "x_y") or x and error y values (mode "x_err_y")
    '''
    def unpack_dict(self, *, data: dict, mode: str = "x_y"): 

        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary.")
        if len(data) == 0:
            raise ValueError("Data dictionary is empty.")
        
        if mode == "x_y":
            x = []
            y = []  
            for key, value in data.items():
                x.append(key)
                y.append(value)
            self.x = x
            self.y = y
        elif mode == "x_err_y":
            err_y = []
            x = []
            for key, value in data.items():
                x.append(key)
                err_y.append(value)
            if self.x is None:
                self.x = x
            elif self.x == x:
                print(f"x values match")
            else:
                raise ValueError("x values do not match.")
            self.err_y = err_y
        elif mode == "helpline":
            self.x_help = []
            self.y_help = []
            for key, value in data.items():
                self.x_help.append(key)
                self.y_help.append(value)
        elif mode == "1st_derivative":
            self.x_1st = []
            self.y_1st = []
            for key, value in data.items():
                self.x_1st.append(key)
                self.y_1st.append(value)
        elif mode == "2nd_derivative":
            self.x_2nd = []
            self.y_2nd = []
            for key, value in data.items():
                self.x_2nd.append(key)
                self.y_2nd.append(value)
        elif mode == "3rd_derivative":
            self.x_3rd = []
            self.y_3rd = []
            for key, value in data.items():
                self.x_3rd.append(key)
                self.y_3rd.append(value)

        else:
            raise ValueError("Mode Error")

        return
    





#TODO: 3rd derivative curve fitting using sonams root script
#TODO: graph fitting
#TODO: single measurement error
#TODO: whole wafer tests --> gradient over whole wafer?#








