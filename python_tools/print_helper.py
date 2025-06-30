class bcolors:                                                                                                                                                                            
    OK = '\033[92m'
    INFO = '\033[94m'
    WARNING = '\033[33m'
    ERROR = '\033[31m'
    ENDC = '\033[0m'
    def __init__(self):
       print(f"{self.INFO}Initiated an instance of the class bcolors!{self.ENDC}")
    def example(self):
       print(self.OK+"GOOD"+      self.ENDC)
       print(self.WARNING+"WARNING"+ self.ENDC)
       print(self.INFO+"INFO"+    self.ENDC)
       print(self.ERROR+"ERROR"+   self.ENDC)
        
class my_symbol:
    LINE1='****************************************\n'
    LINE2='========================================\n' 

if __name__=="__main__":
    test=bcolors()
    test.example()
    exit()
