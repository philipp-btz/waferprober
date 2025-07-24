import velox

with velox.MessageServerInterface() as msgServer:
  
    # FindFocus will throw an exception because we aren't properly set up yet.
    # This is to demonstrate exception handling.
    try:
        print(velox.FindFocus())
    except velox.SciException as e:
        print('We caught an exception as expected:')
        print(e)

