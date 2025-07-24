# Demonstrate Custom User Commands
#
# Custom commands are commands added to the commands.user.txt file.
# See the Velox Integration Toolkit documentation for details
#
# Because custom user commands are not part of the velox Python library,
# use the generic sendSciCommand of the MessageServer class to send the command.
#
# The code below shows two ways to call sendSciCommand: one using the msgServer
# object from the 'with' statement on the second line of code, and one using the
# full path velox.MessageServerInterface.sendSciCommand()
#
# The parameters are a string containing the name of the command and a string 
# containing any arguemnts that should be sent to the command.
# 
# rsp = msgServer.sendSciCommand('commandName', 'arguments separated by spaces')
#
# The example blow does not use a custom command, but demonstrates calling the 
# echodata test commmd to demonstrate the use os sendSciCommand

import velox
with velox.MessageServerInterface() as msgServer:
    rsp = msgServer.sendSciCommand('EchoData', 'Hello')
    print(rsp)
    rsp = velox.MessageServerInterface.sendSciCommand('echodata', 'World')
    print(rsp)
