# Demonstrate simple synchronous commands

import velox
with velox.MessageServerInterface() as msgServer:
    response = velox.IsAppRegistered('Kernel')
    if response < 0 :
        print('Could not register application.')

    x,y,z = velox.ReadChuckPosition("Microns")
    print(x,y,z)
