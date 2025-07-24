# Demonstrate Die Stepping in WaferMap

import velox

def perform_measurement(die):
    if die.CurSite > 0:
        print(f'Measure at die <{die[0], die[1]}> subdie {die.CurSite} of {die.LastSiteIndex}')
    else:
        print(f'Measure at die <{die[0], die[1]}>')

with velox.MessageServerInterface() as msgServer:
    try:
        rsp = velox.IsAppRegistered('Kernel')
        print('IsAppRegistered Kernel: %s' % rsp)


        rsp = velox.StepFirstDie()
        perform_measurement(rsp)

        while(True):
            rsp = velox.StepNextDie()
            perform_measurement(rsp)

        x,y,z = velox.ReadChuckPosition('Y','H', 'D')
        print('The Chuck is at <%s,%s,%s>'% (x, y, z))

    except velox.SciException as e:
        if (e.code == '703'):
            print('Die Stepping Completed')
        elif e.code == '512':
            print('There was an error. The error code was %s.' % e.code)
            print('This may mean that the WaferMAp application is not running.')
            print('Make sure that the WaferMap application is running and try again.')
            print(e)
        else:
            print('We caught an exception with error code %s as:' % e.code)
            print(e)

