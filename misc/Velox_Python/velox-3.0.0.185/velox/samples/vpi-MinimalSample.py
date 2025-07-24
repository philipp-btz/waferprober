import velox

with velox.MessageServerInterface() as msgServer:

    ver, desc = velox.ReportKernelVersion()
    print('Got ', ver, 'and', desc)
    x,y,z = velox.ReadChuckPosition("Inches")
    print(x,y,z)

