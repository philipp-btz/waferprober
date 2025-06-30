from datetime import datetime,timedelta
class timer_helper:
    time_zero=0
    def __init__(self):
        self.time_zero=datetime(1995,1,1)  #this is the reference time of CERN ROOT
    def test(self):
        print("this is a test")
    
    def time_to_int(self,time):
        return (time-self.time_zero).total_seconds()
    
    def int_to_time(self,time_delta_seconds):
        return self.time_zero+timedelta(seconds=time_delta_seconds)