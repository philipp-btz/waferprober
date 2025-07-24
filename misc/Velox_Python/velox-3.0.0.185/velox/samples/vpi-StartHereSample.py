# import velox will choose the correct version of the library 
# based on the version of Python being executed
import velox

# import sys for this example, but it is not required for VPI
import sys

# print the version of Python that is running, just to see that it is working
print('Using Python Version ' + sys.version)

# Connect to the message server using a 'with' statement.
# The application name registered with the Velox Message Server 
# will be the name of our script. Keep a reference to 
# the object returned by velox.MessageServerInterface 
# - in this example, we call it msgServer

# the parameters to MessageServerInterface are optional. 
# For a local connection, you can leave them blank. If 
# connecting to a remote machine, add keyword parameters and set the 
# address and socket
# velox.MessageServerInterface(ipaddr='localhost',targetSocket=1412)

with velox.MessageServerInterface() as msgServer:
    # as long as the connection was successful, we can send some commands.
    # if it was not successful, an exception is thrown.

    # try some SCI Command Examples

    # The SCI commands in the velox module have docstrings to describe 
    # their function, inputs, and outputs. 
    # You can print them from a Python command to see what the function does. 

    # print the docstring for the ReportKernelVersion command
    # ReportKernelVersion returns 2 values. 
    # here is the description of the command
    
    print(velox.ReportKernelVersion.__doc__)

    # SCI commands return a namedtuple if multiple values are returned. 
    # ReportKernelVersion returns a version number and a description. 
    # You can acess the return values by name or by indexing the tuple.

    v = velox.ReportKernelVersion()
    print('The kernel version is', v.Version, 'and', v.Description)
    print('The kernel version array is', v[0], 'and', v[1])

    # a more convenient example is to unpack the tuple into variables 
    # as part of the function call.
    # here we get variables named ver and desc and use them directly
    ver, desc = velox.ReportKernelVersion()
    print('Got ', ver, 'and', desc)

    # The Echo Data command just returns its own first input.  
    # Echo data only returns the first string in the parameter list.
    # To get a string with spaces to display, we need to add double quotes.
    # Try it both ways to see the difference. The first one below does 
    # what we expect. The second only prints the first word. 
    # The third assigns a return value to a variable

    print(velox.EchoData('"Hi World"'))
    print(velox.EchoData("Hi World"))
    evalue = velox.EchoData("Echo_This")

    # ReadChuckPosition returns 3 values. Here we print the entire tuple
    # to show the tuple name and the names of the 3 return values
    print(velox.ReadChuckPosition("Microns"))

    # it is possible to send raw command strings with the 
    # sendSciCommand function.
    # it isn't recommended, but in some cases, it might be necessary. 
    # it is much easier and 'safer' to use the defined SCI functions.
    # note that this is a function of MessageServerInterface, 
    # not a velox module function
    
    print(msgServer.sendSciCommand("echodata", rparams='"RawHello Velox"'))
