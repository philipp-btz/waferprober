"""
Velox Message Server Interface
To simplify calls from the SCI commands, many of the class methods are
defined as static.  Some class variables are required to support a
connection to the Message Server, but the individual SCI commands
do not maintain a reference to the MessageServer object. Several
class global variables are used to maintain state.
Registration with the Message Server is handled in the __init__.
"""
import re
import socket
import sys
from collections import namedtuple
from os.path import basename

REGISTRATION_MESSAGE_TEMPLATE = "FCN=1:RegisterProberApp:{0} {0} 0\n"
GET_ALL_COMMANDS_MESSAGE = "FCN=1:GetCommands:\n"

class SciException(Exception):
    """ Contains fields for:
        code : The Error Number as a string
        description : The error description
        __str__, __repr__ : A formatted description of the exception """
    def __init__(self, cmd, code, description):
        self.command = cmd
        self.code = str(code)
        self.description = description

    def __repr__(self):
        return 'Error # {0} "{1}"'.format(self.code, self.description)

    def __str__(self):
        return 'Error # {0} "{1}"'.format(self.code, self.description)


class MessageServerInterface(object):

    def __init__(self, ipaddr = 'localhost', targetSocket = 1412):
        """ Initialize a socket and register with the velox message server.
            Uses the python script name as the application name to register.
        """
        global mySocket, myBytesReceived, myResponse, myCurrentCommand

        try:
            appName = basename(sys.argv[0])     # get the script name being executed
            appName = appName.replace(' ', '_') # make sure there are no spaces in the name
            registrationMessage = REGISTRATION_MESSAGE_TEMPLATE.format(appName)

            myCurrentCommand = 1
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.connect((ipaddr, targetSocket))

            #register with message server
            mySocket.send(registrationMessage.encode())
            myBytesReceived = 0
            myResponse = mySocket.recv(200)
        except ConnectionRefusedError:
            errormessage = ('Error: The connection to the Velox Message Server was refused.'
                            ' It probably is not running on IP [' 
                            + str(ipaddr) + '] on Socket [' + str(targetSocket) + '].'
                            ' Start Velox or examine IP Address and Socket parameters.')

            raise Exception(errormessage)
        pass

    def __enter__(self):
        return self
        pass

    def __exit__(self, type, value, traceback):
        """ Close the socket connected to the message server """
        global mySocket
        mySocket.close()
        pass

    def _getcommands(self):
        ''' Return a list of all commands known to the Velox Message Server '''
        global mySocket, myBytesReceived, myResponse
        mySocket.send(GET_ALL_COMMANDS_MESSAGE.encode())
        myBytesReceived = 0
        myResponse = mySocket.recv(60000)
        message = str(myResponse.decode('utf-8'))
        # parse the list
        commands = message.split(':')[2].split(';')

        # split the list into parsed tuples
        SimpleCommandTuple = namedtuple('SimpleCommandTuple', 'section, name, number, timeout')
        scilist = []
        for x in commands:
            parts = x.split(' ')
            scilist.append(SimpleCommandTuple(parts[0], parts[1], int(parts[2]),int(parts[3])))
        return scilist
        pass

    @staticmethod
    def __parseReturnValues(valueString):
        """ The values come back from the SCI command as a string separated by spaces,
            but with embedded strings as well.  Separate the values. """

        results = []   # the values parsed to be returned
        remainingValues = valueString   # holds all values still to be parsed
        while remainingValues:
            if remainingValues.startswith('"'):     # we have a string
                parts = remainingValues.split('"', 2)
                parts.pop(0)
                results.append(parts.pop(0).strip())    # get the string
                parts.pop(0)
            else:   # get value separated by a space
                parts = remainingValues.split(' ', 1)
                results.append(parts.pop(0))

            if len(parts) > 0:
                remainingValues = parts[0].strip()  # get the rest of the values
            else:
                remainingValues = None

        return results
        pass

    @staticmethod
    def __convertReturnValues(responses):
        """ The responses are all strings.  Use the hints from the SCI Command definition
            to convert them to the proper types """
        pass

    @staticmethod
    def __parseSciCommandResponse(response):
        """ The response from Message Server has the form
            Rsp=<ID>:<Return Code>:<Return Value>
            Split the response on the : character, then split up the return values """

        message = str(response.decode('utf-8')[:-2])

        # we may have 0 or more values
        partsCount = message.count(':')+1
        if partsCount == 2:
            command, code = re.split(":", message)
            values = '';
        else:
            command, code, values = re.split(":", message)
            values = values.strip()

        if message.startswith('Rsp='):
            values = MessageServerInterface.__parseReturnValues(values)

        commandNumber = command.split('=')[1]
        return int(commandNumber), int(code), values

    @staticmethod
    def __sendSynchronousCommand(commandName, message=''):
        global mySocket, myBytesReceived, myResponse, myCurrentCommand

        try:
            myCurrentCommand += 1       # increment the commend number
            if myCurrentCommand == 0 or myCurrentCommand > 999:
                myCurrentCommand = 1
            messageToSend = 'Cmd={}:{}:{}\n'.format(myCurrentCommand,commandName,message)
            mySocket.send(messageToSend.encode())
            myBytesReceived = 0
            myResponse = mySocket.recv(500)

        except Exception as e:
            raise Exception('Unable to communicate with Velox Message Server. Start Velox.' + e)

        cmd, code, values = MessageServerInterface.__parseSciCommandResponse(myResponse)

        # if the response code is not 0, raise an exception
        if code:
            parameters = ' '.join(values)
            raise SciException(cmd, code, parameters)

        return values
        pass

    @staticmethod
    def sendSciCommand(commandName, *args, **kwargs):
        """ If the parameter rparams is passed, it is the full command parameter string and should be used.
            Otherwise, join the other arguments into a string separated by spaces and send that.
            The rparams is used for legacy scripts converted from Pascal or Basic or other cases 
            where you want to send the command parameters as a single string.  """

        if 'rparams' in kwargs: # use the raw parameter string if provided
            commandParameters = kwargs['rparams']
        else: # use the positional arguments and build the parameter string
            commandParameters = ' '.join(str(x) for x in args)
        return MessageServerInterface.__sendSynchronousCommand(commandName, commandParameters)
