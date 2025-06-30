from  velox.vxmessageserver import *
from decimal import Decimal
from collections import namedtuple

"""
Velox SCI Commands
This module provides a function interface to the Cascade Microtech Velox software suite. 
The module was auto-generated from the commands.info.xml file on 2019-08-16.  
737 SCI commands were found and included.

To use this module, your code must import the veloxsci.py module.
Create a connection to the Velox Message Server using the 'with MessageServerInterface():' 
command as shown in the sample below.

The Velox Message Server must be running prior to establishing a connection. 
To start the Message Server, run Velox.

The sample code to use this module is:

import velox
with velox.MessageServerInterface() as msgServer:

    # Your Code: try some SCI Commands - such as:
    response = velox.ReportKernelVersion()
    print ('The kernel version is', response.Version, 'and', response.Description)
    
"""
def EchoData(TestCmd:str=""):
    """
    Test Command for the Kernel Communication. Like a ping command, the given text
    string is returned unchanged.
    API Status: published
    Args:
        TestCmd:str = "Test"
    Returns:
        TestRsp:str
    Command Timeout: 5000
    Example:EchoData Test
    """
    rsp = MessageServerInterface.sendSciCommand("EchoData",TestCmd)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ReportKernelVersion(Module:str=""):
    """
    Returns the version information of the kernel or the control box code. The
    "Version" value contains version number and revision level of the actual Kernel
    implementation. The text string contains a code description, version number and
    the revision date.
    API Status: published
    Args:
        Module:str = "K"
    Returns:
        Version:Decimal
        Description:str
    Command Timeout: 5000
    Example:ReportKernelVersion K
    """
    rsp = MessageServerInterface.sendSciCommand("ReportKernelVersion",Module)
    global ReportKernelVersion_Response
    if not "ReportKernelVersion_Response" in globals(): ReportKernelVersion_Response = namedtuple("ReportKernelVersion_Response", "Version,Description")
    return ReportKernelVersion_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def ReadProberStatus():
    """
    Returns an actual status information of the prober.
    API Status: published
    Returns:
        FlagsBusy:int
        FlagsContact:int
        Mode:str
        IsQuiet:int
    Command Timeout: 5000
    Example:ReadProberStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProberStatus")
    global ReadProberStatus_Response
    if not "ReadProberStatus_Response" in globals(): ReadProberStatus_Response = namedtuple("ReadProberStatus_Response", "FlagsBusy,FlagsContact,Mode,IsQuiet")
    return ReadProberStatus_Response(int(rsp[0]),int(rsp[1]),str(rsp[2]),int(rsp[3]))

def EnableMotorQuiet(WantQuietModeOn:int="", Stage:str=""):
    """
    Toggles the motor power for quiet probing. In most applications this feature is
    not required. However, for special measurements it may be necessary to reduce
    the noise of the system. Quiet on turns off the motor power for all stages (or
    the one specified with the optional parameter). Quiet off will turn on the motor
    power of all stages (or the one specified with the optional parameter) for
    subsequent movements. A move command will also turn on the motor power of the
    moved stage automatically. For automatical switching of the quiet mode refer to
    Auto Quiet functionality.  Sending 'EnableMotorQuiet 1' will enable the quiet
    mode for all stages. Sending 'EnableMotorQuiet 1 C' will only enable the quiet
    mode for the chuck stage. Sending 'EnableMotorQuiet 1 1' will only enable the
    quiet mode for the Positioner1 stage. Sending 'EnableMotorQuiet 0 S' will only
    disable the quiet mode for the scope stage.
    API Status: published
    Args:
        WantQuietModeOn:int = 0
        Stage:str = "None"
    Command Timeout: 10000
    Example:EnableMotorQuiet 1
    """
    MessageServerInterface.sendSciCommand("EnableMotorQuiet",WantQuietModeOn,Stage)


def SetChuckVacuum(WantChuckVacuumOn:int=""):
    """
    Toggles the chuck vacuum on (1) or off (0). Can return vacuum timeout error for
    stations with wafer vacuum sensors in case no wafer was detected.
    API Status: published
    Args:
        WantChuckVacuumOn:int = 0
    Command Timeout: 10000
    Example:SetChuckVacuum 1
    """
    MessageServerInterface.sendSciCommand("SetChuckVacuum",WantChuckVacuumOn)


def SetMicroLight(WantIlluminatorOn:int=""):
    """
    Toggles the microscope light channel of the peripheral output board and all
    cameras. Notifications: 7
    API Status: published
    Args:
        WantIlluminatorOn:int = 2
    Command Timeout: 5000
    Example:SetMicroLight 1
    """
    MessageServerInterface.sendSciCommand("SetMicroLight",WantIlluminatorOn)


def SetBeaconStatus(FlagsMode:int="", PulseWidthRed:int="", PulseWidthGreen:int="", PulseWidthYellow:int="", PulseWidthBlue:int="", PulseWidthWhite:int=""):
    """
    This command controls the beacon channel of the peripheral output board. All
    lights can be switched on, off, or blinking. Setting an interval to zero means,
    that the corresponding light will be statically on or off. The minimum blinking
    interval is 50ms.
    API Status: published
    Args:
        FlagsMode:int = 0
        PulseWidthRed:int = 1000
        PulseWidthGreen:int = 0
        PulseWidthYellow:int = 0
        PulseWidthBlue:int = 0
        PulseWidthWhite:int = 0
    Command Timeout: 5000
    Example:SetBeaconStatus 1 1000
    """
    MessageServerInterface.sendSciCommand("SetBeaconStatus",FlagsMode,PulseWidthRed,PulseWidthGreen,PulseWidthYellow,PulseWidthBlue,PulseWidthWhite)


def SetOutput(Channel:int="", WantOutputOn:int="", PulseTime:int=""):
    """
    Controls the Velox output channel signals. It can be used to activate/deactivate
    outputs.
    API Status: published
    Args:
        Channel:int = 1
        WantOutputOn:int = 0
        PulseTime:int = -1
    Command Timeout: 5000
    Example:SetOutput 4 0
    """
    MessageServerInterface.sendSciCommand("SetOutput",Channel,WantOutputOn,PulseTime)


def StopAllMovements():
    """
    Stops all Prober movements immediately. The response status value of any pending
    movement will signify that the stop command was executed.
    API Status: published
    Command Timeout: 5000
    Example:StopAllMovements
    """
    MessageServerInterface.sendSciCommand("StopAllMovements")


def InkDevice(FlagsInker:int="", PulseWidth:int=""):
    """
    Inks the current device under test. The range of PulseWidth is 20ms to 2000ms.
    For correct function, the inkers have to be linked to default outputs.
    API Status: published
    Args:
        FlagsInker:int = 0
        PulseWidth:int = 50
    Command Timeout: 10000
    Example:InkDevice 1 40
    """
    MessageServerInterface.sendSciCommand("InkDevice",FlagsInker,PulseWidth)


def ReadProbeSetup():
    """
    Returns the current positioner configuration.  The output pattern is:  1. Type
    Positioner 1 2. Type Positioner 2 3. Type Positioner 3 4. Type Positioner 4 5.
    Type Positioner 5 6. Axis Positioner 1 (Bit 0: XY, Bit 1: Z) 7. Axis Positioner
    2 (Bit 0: XY, Bit 1: Z) 8. Axis Positioner 3 (Bit 0: XY, Bit 1: Z) 9. Axis
    Positioner 4 (Bit 0: XY, Bit 1: Z) 10. Axis Positioner 5 (Bit 0: XY, Bit 1: Z)
    11. Type Positioner 6 12. Axis Positioner 6 (Bit 0: XY, Bit 1: Z)
    API Status: published
    Returns:
        TypePositioner1:int
        TypePositioner2:int
        TypePositioner3:int
        TypePositioner4:int
        TypePositioner5:int
        AxisPositioner1:int
        AxisPositioner2:int
        AxisPositioner3:int
        AxisPositioner4:int
        AxisPositioner5:int
        TypePositioner6:int
        AxisPositioner6:int
    Command Timeout: 5000
    Example:ReadProbeSetup
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbeSetup")
    global ReadProbeSetup_Response
    if not "ReadProbeSetup_Response" in globals(): ReadProbeSetup_Response = namedtuple("ReadProbeSetup_Response", "TypePositioner1,TypePositioner2,TypePositioner3,TypePositioner4,TypePositioner5,AxisPositioner1,AxisPositioner2,AxisPositioner3,AxisPositioner4,AxisPositioner5,TypePositioner6,AxisPositioner6")
    return ReadProbeSetup_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]),int(rsp[10]),int(rsp[11]))

def ReadSystemStatus():
    """
    Returns the system options which are currently enabled at the prober.
    API Status: published
    Returns:
        Name:str
        System:str
        ChuckXY:int
        ChuckZ:int
        ChuckTheta:int
        ScopeXY:int
        ScopeZ:int
        EdgeSensor:int
        OperationalMode:str
        Turret:int
        TemperatureChuck:int
        AuxSiteCount:int
        PlatenXY:int
        PlatenZ:int
        LoaderGateState:str
        NucleusType:str
    Command Timeout: 10000
    Example:ReadSystemStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadSystemStatus")
    global ReadSystemStatus_Response
    if not "ReadSystemStatus_Response" in globals(): ReadSystemStatus_Response = namedtuple("ReadSystemStatus_Response", "Name,System,ChuckXY,ChuckZ,ChuckTheta,ScopeXY,ScopeZ,EdgeSensor,OperationalMode,Turret,TemperatureChuck,AuxSiteCount,PlatenXY,PlatenZ,LoaderGateState,NucleusType")
    return ReadSystemStatus_Response(str(rsp[0]),str(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),str(rsp[8]),int(rsp[9]),int(rsp[10]),int(rsp[11]),int(rsp[12]),int(rsp[13]),str(rsp[14]),str("" if len(rsp) < 16 else ' '.join(rsp[15:])))

def SetExternalMode(Mode:str=""):
    """
    If 'R' is sent, it sets the external mode of the kernel. This disables most of
    the control box functions (except the LOCAL function key). Otherwise, this
    command re-enables all functions of the control box.
    API Status: published
    Args:
        Mode:str = "L"
    Command Timeout: 5000
    Example:SetExternalMode L
    """
    MessageServerInterface.sendSciCommand("SetExternalMode",Mode)


def SetStageLock(Stage:str="", WantStageLock:int="", Application:str=""):
    """
    Enables or disables the stage lock functionality. Stages which are locked can't
    be moved in any way. If the joystick controller is locked, the display and the
    keys are deactivated. The name of the application can be stored by using the
    Application Name parameter and is shown in lock-caused error messages.
    API Status: published
    Args:
        Stage:str = "0"
        WantStageLock:int = 1
        Application:str = ""
    Command Timeout: 10000
    Example:SetStageLock C 0 WaferMap
    """
    MessageServerInterface.sendSciCommand("SetStageLock",Stage,WantStageLock,Application)


def ReadSensor(Channel:int="", Type:str=""):
    """
    Returns the actual status of the specified input channel, output channel or edge
    sensor. The signal table is described in the Hardware Manual. Each used IO-board
    has 16 channels (max. 4 IO-boards are supported), what results in a domain of 64
    channel numbers. Beyond this range there are pseudo channels, which are used for
    special purposes. Pseudo channels:
    API Status: published
    Args:
        Channel:int = 1
        Type:str = "Input"
    Returns:
        IsSensorOn:int
    Command Timeout: 10000
    Example:ReadSensor 11 I
    """
    rsp = MessageServerInterface.sendSciCommand("ReadSensor",Channel,Type)
    return int(rsp[0])

def GetStageLock(Stage:str=""):
    """
    Reads whether stages or joystick controller are locked.
    API Status: published
    Args:
        Stage:str = "0"
    Returns:
        Locks:int
        Application:str
    Command Timeout: 10000
    Example:GetStageLock C
    """
    rsp = MessageServerInterface.sendSciCommand("GetStageLock",Stage)
    global GetStageLock_Response
    if not "GetStageLock_Response" in globals(): GetStageLock_Response = namedtuple("GetStageLock_Response", "Locks,Application")
    return GetStageLock_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def SetBackSideMode(WantBackSideMode:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command sets bottomside mode. In this mode the Z axis is reverse and the
    command MoveChuckLoad is not allowed.
    API Status: internal
    Args:
        WantBackSideMode:int = 0
    Command Timeout: 5000
    Example:SetBackSideMode 1
    """
    MessageServerInterface.sendSciCommand("SetBackSideMode",WantBackSideMode)


def GetBackSideMode():
    """
    Returns the current side mode.
    API Status: published
    Returns:
        IsBackSideModeOn:int
    Command Timeout: 5000
    Example:GetBackSideMode
    """
    rsp = MessageServerInterface.sendSciCommand("GetBackSideMode")
    return int(rsp[0])

def SetDarkMode(WantSetDarkMode:int=""):
    """
    Switches off all LEDs on the Control Box, on the positioners, and on the screen
    of the Control Box and also the light of the cameras.
    API Status: published
    Args:
        WantSetDarkMode:int = 0
    Command Timeout: 5000
    Example:SetDarkMode 1
    """
    MessageServerInterface.sendSciCommand("SetDarkMode",WantSetDarkMode)


def GetDarkMode():
    """
    Returns the current mode of the light sources.
    API Status: published
    Returns:
        IsDarkMode:int
    Command Timeout: 5000
    Example:GetDarkMode
    """
    rsp = MessageServerInterface.sendSciCommand("GetDarkMode")
    return int(rsp[0])

def DockChuckCamera(ConnectCamera:str="", Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Connect or disconnect the chuck camera to the chuck stage. The command is only
    available for the Prober type PA300BEP.
    API Status: internal
    Args:
        ConnectCamera:str = "ParkPos"
        Velocity:Decimal = 100
    Command Timeout: 300000
    Example:DockChuckCamera P 75
    """
    MessageServerInterface.sendSciCommand("DockChuckCamera",ConnectCamera,Velocity)


def ReadCBoxStage():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current selected stage of the joystick controller.
    API Status: internal
    Returns:
        Stage:str
    Command Timeout: 5000
    Example:ReadCBoxStage
    """
    rsp = MessageServerInterface.sendSciCommand("ReadCBoxStage")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetCBoxStage(Stage:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the current stage of the joystick controller.
    API Status: internal
    Args:
        Stage:str = "Chuck"
    Command Timeout: 5000
    Example:SetCBoxStage C
    """
    MessageServerInterface.sendSciCommand("SetCBoxStage",Stage)


def ReadCBoxPosMonConf(Stage:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current setting of the joystick controllers position monitor for the
    secified stage.
    API Status: internal
    Args:
        Stage:str = "Chuck"
    Returns:
        PosRef:str
        Unit:str
    Command Timeout: 5000
    Example:ReadCBoxPosMonConf C
    """
    rsp = MessageServerInterface.sendSciCommand("ReadCBoxPosMonConf",Stage)
    global ReadCBoxPosMonConf_Response
    if not "ReadCBoxPosMonConf_Response" in globals(): ReadCBoxPosMonConf_Response = namedtuple("ReadCBoxPosMonConf_Response", "PosRef,Unit")
    return ReadCBoxPosMonConf_Response(str(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def SetCBoxPosMonConf(Stage:str="", PosRef:str="", Unit:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Configures the joystick controller position monitor for the secified stage.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        PosRef:str = "Zero"
        Unit:str = "Microns"
    Command Timeout: 5000
    Example:SetCBoxPosMonConf C Z Y
    """
    MessageServerInterface.sendSciCommand("SetCBoxPosMonConf",Stage,PosRef,Unit)


def ReadCBoxCurrSpeed(Stage:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current speed of the joystick controller for the specified stage.
    API Status: internal
    Args:
        Stage:str = "Chuck"
    Returns:
        CBoxSpeed:str
    Command Timeout: 5000
    Example:ReadCBoxCurrSpeed C
    """
    rsp = MessageServerInterface.sendSciCommand("ReadCBoxCurrSpeed",Stage)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetCBoxCurrSpeed(Stage:str="", CBoxSpeed:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the current speed of the joystick controller for the specified stage.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        CBoxSpeed:str = "Speed4"
    Command Timeout: 5000
    Example:SetCBoxCurrSpeed C 3
    """
    MessageServerInterface.sendSciCommand("SetCBoxCurrSpeed",Stage,CBoxSpeed)


def MoveChuckAsync(XValue:Decimal="", YValue:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the chuck stage to the specified X,Y position without waiting for the move
    to be finished If chuck Z is in contact height or higher, the chuck will drop to
    separation.
    API Status: internal
    Args:
        XValue:Decimal = 0
        YValue:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Command Timeout: 5000
    Example:MoveChuckAsync 5000. 5000. R Y 100
    """
    MessageServerInterface.sendSciCommand("MoveChuckAsync",XValue,YValue,PosRef,Unit,Velocity,Comp)


def MoveScopeAsync(XValue:Decimal="", YValue:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the scope stage to the specified X,Y position without waiting for the move
    to be finished.
    API Status: internal
    Args:
        XValue:Decimal = 0
        YValue:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Command Timeout: 5000
    Example:MoveScopeAsync 5000 5000 R Y 100
    """
    MessageServerInterface.sendSciCommand("MoveScopeAsync",XValue,YValue,PosRef,Unit,Velocity,Comp)


def MoveProbeAsync(Probe:int="", XValue:Decimal="", YValue:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the probe stage to the specified X,Y position without waiting for the move
    to be finished.
    API Status: internal
    Args:
        Probe:int = 1
        XValue:Decimal = 0
        YValue:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Returns:
        ProbeEcho:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeAsync",Probe,XValue,YValue,PosRef,Unit,Velocity,Comp)
    return int(rsp[0])

def ReadChuckStatus():
    """
    Returns the current chuck status. Every bit in the bit fields works like a
    boolean value: One &lt;1&gt; means true/on and zero &lt;0&gt; means false/off.
    Its counted from LSB to MSB.   - _FlagsInit_: X, Y, Z, Theta - _FlagsMode_:
    HasOvertravel, HasAutoZ, HasInterlock, ContactSearch, IsContactSet,
    EdgeInterlock, QuietContact, IsLocked - _FlagsLimit_: XHigh, XLow, YHigh, YLow,
    ZHigh, ZLow, ThetaHigh, ThetaLow - _FlagsMoving_: X, Y, Z, Theta  All parameters
    are provided as indirect access (e.g. first bit of M_pvecFlagsInit can be
    accessed by M_pbIsInitX).
    API Status: published
    Returns:
        FlagsInit:int
        FlagsMode:int
        FlagsLimit:int
        FlagsMoving:int
        Comp:str
        IsVacuumOn:int
        PresetHeight:str
        LoadPos:str
        IsLiftDown:int
        CameraConnection:str
        IsQuiet:int
    Command Timeout: 5000
    Example:ReadChuckStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckStatus")
    global ReadChuckStatus_Response
    if not "ReadChuckStatus_Response" in globals(): ReadChuckStatus_Response = namedtuple("ReadChuckStatus_Response", "FlagsInit,FlagsMode,FlagsLimit,FlagsMoving,Comp,IsVacuumOn,PresetHeight,LoadPos,IsLiftDown,CameraConnection,IsQuiet")
    return ReadChuckStatus_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),str(rsp[4]),int(rsp[5]),str(rsp[6]),str(rsp[7]),int(rsp[8]),str(rsp[9]),int(rsp[10]))

def ReadChuckPosition(Unit:str="", PosRef:str="", Comp:str=""):
    """
    Returns the current chuck stage position in X, Y and Z.
    API Status: published
    Args:
        Unit:str = "Microns"
        PosRef:str = "Home"
        Comp:str = "Default"
    Returns:
        X:Decimal
        Y:Decimal
        Z:Decimal
    Command Timeout: 5000
    Example:ReadChuckPosition Y Z
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckPosition",Unit,PosRef,Comp)
    global ReadChuckPosition_Response
    if not "ReadChuckPosition_Response" in globals(): ReadChuckPosition_Response = namedtuple("ReadChuckPosition_Response", "X,Y,Z")
    return ReadChuckPosition_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def ReadChuckHeights(Unit:str=""):
    """
    Returns the current settings used for the chuck Z movement. `Contact` is the
    contact-height from zero in default compensation. The other heights are relative
    to this. If no contact is set, the value will be -1.
    API Status: published
    Args:
        Unit:str = "Microns"
    Returns:
        Contact:Decimal
        Overtravel:Decimal
        AlignDist:Decimal
        SepDist:Decimal
        SearchGap:Decimal
    Command Timeout: 5000
    Example:ReadChuckHeights Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckHeights",Unit)
    global ReadChuckHeights_Response
    if not "ReadChuckHeights_Response" in globals(): ReadChuckHeights_Response = namedtuple("ReadChuckHeights_Response", "Contact,Overtravel,AlignDist,SepDist,SearchGap")
    return ReadChuckHeights_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]))

def InitChuck(FlagsInit:int="", FlagsDirection:int="", FlagsMoveRange:int=""):
    """
    Machine Coordinate System: Chuck X Y Z Theta  - _FlagsInit_: X, Y, Z, Theta -
    _FlagsDirection_: X, Y, Z, Theta (true means plus direction) - _FlagsMoveRange_:
    X, Y, Z, Theta   All flags can be accessed by indirect members.  Initializes the
    chuck stage and resets current coordinate system. Should be used only in cases
    when the reported coordinates do not correspond to real position of mechanics.
    Find Move Range starts the initialization in the defined direction and then
    moves to the other limit and finds the whole range of the axes.
    API Status: published
    Args:
        FlagsInit:int = 0
        FlagsDirection:int = 0
        FlagsMoveRange:int = 0
    Command Timeout: 150000
    Example:InitChuck 7 0 0
    """
    MessageServerInterface.sendSciCommand("InitChuck",FlagsInit,FlagsDirection,FlagsMoveRange)


def MoveChuck(XValue:Decimal="", YValue:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    Moves the chuck stage to the specified X,Y position. If chuck Z is in contact
    height or higher, Interlock and Auto Z flags will be analyzed and stage will
    behave correspondingly - can move to separation first or return an error:
    API Status: published
    Args:
        XValue:Decimal = 0
        YValue:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Command Timeout: 30000
    Example:MoveChuck 5000. 5000. R Y 100
    """
    MessageServerInterface.sendSciCommand("MoveChuck",XValue,YValue,PosRef,Unit,Velocity,Comp)


def MoveChuckIndex(XSteps:int="", YSteps:int="", PosRef:str="", Velocity:Decimal=""):
    """
    Moves the chuck stage in index steps. This command modifies Die Home Position.
    API Status: published
    Args:
        XSteps:int = 0
        YSteps:int = 0
        PosRef:str = "Home"
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MoveChuckIndex 1 1 R 100
    """
    MessageServerInterface.sendSciCommand("MoveChuckIndex",XSteps,YSteps,PosRef,Velocity)


def MoveChuckSubsite(XValue:Decimal="", YValue:Decimal="", Unit:str="", Velocity:Decimal=""):
    """
    Moves the chuck stage to the specified X, Y sub-site position. Die home position
    is defined by destination position of last successful MoveChuck or
    MoveChuckIndex commands. MoveChuckVelocity does not touch die home position. If
    you have moved chuck with MoveChuckVelocity, "MoveChuckSubsite 0 0" will move it
    back to die home position.
    API Status: published
    Args:
        XValue:Decimal = 0
        YValue:Decimal = 0
        Unit:str = "Microns"
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MoveChuckSubsite 200 200 Y 100
    """
    MessageServerInterface.sendSciCommand("MoveChuckSubsite",XValue,YValue,Unit,Velocity)


def MoveChuckContact(Velocity:Decimal=""):
    """
    Performs a movement of chuck Z axis to preset contact height or will return
    error if no contact height is set.
    API Status: published
    Args:
        Velocity:Decimal = 100
    Command Timeout: 60000
    Example:MoveChuckContact 100
    """
    MessageServerInterface.sendSciCommand("MoveChuckContact",Velocity)


def MoveChuckAlign(Velocity:Decimal=""):
    """
    Moves the chuck Z axis to the align height. If no Contact height is set will
    return an error.
    API Status: published
    Args:
        Velocity:Decimal = 100
    Command Timeout: 60000
    Example:MoveChuckAlign 100
    """
    MessageServerInterface.sendSciCommand("MoveChuckAlign",Velocity)


def MoveChuckSeparation(Velocity:Decimal=""):
    """
    Moves the chuck Z axis to the separation height. Returns error if no Contact
    height is set.
    API Status: published
    Args:
        Velocity:Decimal = 100
    Command Timeout: 60000
    Example:MoveChuckSeparation 100
    """
    MessageServerInterface.sendSciCommand("MoveChuckSeparation",Velocity)


def MoveChuckLoad(LoadPosition:str=""):
    """
    Moves the Chuck stage in X, Y, Z and Theta to the load position.
    API Status: published
    Args:
        LoadPosition:str = "First"
    Command Timeout: 60000
    Example:MoveChuckLoad 0
    """
    MessageServerInterface.sendSciCommand("MoveChuckLoad",LoadPosition)


def MoveChuckZ(Height:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    Moves the chuck Z axis to the specified height. If contact is set, only moves up
    to contact height will be allowed. If overtravel is enabled - up to overtravel
    height.
    API Status: published
    Args:
        Height:Decimal = 0
        PosRef:str = "Zero"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Command Timeout: 60000
    Example:MoveChuckZ 1000. R Y 67
    """
    MessageServerInterface.sendSciCommand("MoveChuckZ",Height,PosRef,Unit,Velocity,Comp)


def SearchChuckContact(Height:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    Moves the chuck Z axis to the specified height and sets contact. The move stops
    immediately if the Contact Sensor ( Edge Sensor) is triggered. If no contact has
    been found and an old one was set before the old contact will not get lost, it
    will be reset.
    API Status: published
    Args:
        Height:Decimal = 100
        PosRef:str = "Relative"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Returns:
        ContactHeight:Decimal
    Command Timeout: 60000
    Example:SearchChuckContact 1000 R Y 10
    """
    rsp = MessageServerInterface.sendSciCommand("SearchChuckContact",Height,PosRef,Unit,Velocity,Comp)
    return Decimal(rsp[0])

def MoveChuckVelocity(PolarityX:str="", PolarityY:str="", PolarityZ:str="", VelocityX:Decimal="", VelocityY:Decimal="", VelocityZ:Decimal=""):
    """
    Moves the chuck stage in velocity mode. The motion continues until the
    StopChuckMovement command is received, or the end limit is reached.
    API Status: published
    Args:
        PolarityX:str = "Fixed"
        PolarityY:str = "Fixed"
        PolarityZ:str = "Fixed"
        VelocityX:Decimal = 100
        VelocityY:Decimal = 0
        VelocityZ:Decimal = 0
    Command Timeout: 30000
    Example:MoveChuckVelocity + + 0 100 30 0
    """
    MessageServerInterface.sendSciCommand("MoveChuckVelocity",PolarityX,PolarityY,PolarityZ,VelocityX,VelocityY,VelocityZ)


def StopChuckMovement(FlagsStop:int=""):
    """
    Stops chuck movement for the given axis. Notifications: 31 / 32 / 5
    API Status: published
    Args:
        FlagsStop:int = 15
    Command Timeout: 5000
    Example:StopChuckMovement 7
    """
    MessageServerInterface.sendSciCommand("StopChuckMovement",FlagsStop)


def SetChuckMode(Overtravel:int="", AutoZ:int="", Interlock:int="", ContactSearch:int="", EdgeInterlock:int="", QuietContact:int=""):
    """
    Mode manages the way the chuck behaves when it is in contact height. Chuck mode
    is made from 6 flags and you can control all of them using this command. Every
    flag can be turned on by using value 1 or turned off by using value 0. If you do
    not want to change a flag - use value of 2.
    API Status: published
    Args:
        Overtravel:int = 2
        AutoZ:int = 2
        Interlock:int = 2
        ContactSearch:int = 2
        EdgeInterlock:int = 2
        QuietContact:int = 2
    Command Timeout: 5000
    Example:SetChuckMode 2 2 2 2 2 2
    """
    MessageServerInterface.sendSciCommand("SetChuckMode",Overtravel,AutoZ,Interlock,ContactSearch,EdgeInterlock,QuietContact)


def SetChuckHome(Mode:str="", Unit:str="", XValue:Decimal="", YValue:Decimal=""):
    """
    Sets wafer and die home position, which can be used later as coordinate system
    for movements.
    API Status: published
    Args:
        Mode:str = "0"
        Unit:str = "Microns"
        XValue:Decimal = 0
        YValue:Decimal = 0
    Command Timeout: 5000
    Example:SetChuckHome 0 Y
    """
    MessageServerInterface.sendSciCommand("SetChuckHome",Mode,Unit,XValue,YValue)


def SetChuckIndex(XValue:Decimal="", YValue:Decimal="", Unit:str=""):
    """
    Sets the wafer index size. Normally the size of one die.
    API Status: published
    Args:
        XValue:Decimal = 0
        YValue:Decimal = 0
        Unit:str = "Microns"
    Command Timeout: 5000
    Example:SetChuckIndex 5000. 5000. Y
    """
    MessageServerInterface.sendSciCommand("SetChuckIndex",XValue,YValue,Unit)


def SetChuckHeight(PresetHeight:str="", Mode:str="", Unit:str="", Value:Decimal=""):
    """
    Defines the predefined contact height and corresponding gaps for overtravel,
    align and separation. A predefined contact search gap is able to write. No data
    in the optional parameters sets contact height at current position. If Mode is
    '0', contact height can be set at current position. The levels O, A, S and T
    support no Mode '0'. If Mode is 'V' and no value for height is specified -
    default 0 will be used, what potentially can be not what you expect. If Mode is
    'R', contact height can be invalidated. The levels O, A, S and T support no Mode
    'R'.
    API Status: published
    Args:
        PresetHeight:str = "Contact"
        Mode:str = "0"
        Unit:str = "Microns"
        Value:Decimal = 0
    Command Timeout: 5000
    Example:SetChuckHeight C V Y 5000.
    """
    MessageServerInterface.sendSciCommand("SetChuckHeight",PresetHeight,Mode,Unit,Value)


def ReadChuckIndex(Unit:str=""):
    """
    The command gets the current die size which is stored in the kernel.
    API Status: published
    Args:
        Unit:str = "Microns"
    Returns:
        IndexX:Decimal
        IndexY:Decimal
    Command Timeout: 5000
    Example:ReadChuckIndex Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckIndex",Unit)
    global ReadChuckIndex_Response
    if not "ReadChuckIndex_Response" in globals(): ReadChuckIndex_Response = namedtuple("ReadChuckIndex_Response", "IndexX,IndexY")
    return ReadChuckIndex_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def MoveChuckTransfer():
    """
    Moves the Chuck to the Transfer Position. If the movement starts in Load
    Position (where it's possible to pull out the chuck) the handling of the Add On
    Platen or the Pin Chuck is integrated.
    API Status: published
    Command Timeout: 60000
    Example:MoveChuckTransfer
    """
    MessageServerInterface.sendSciCommand("MoveChuckTransfer")


def MoveChuckLift(SetLift:int=""):
    """
    Moves the chuck to the upper (0) or lower = lifted (1) position. This initiates
    motion only, the actual movement may take some seconds.
    API Status: published
    Args:
        SetLift:int = 1
    Command Timeout: 10000
    Example:MoveChuckLift 1
    """
    MessageServerInterface.sendSciCommand("MoveChuckLift",SetLift)


def SetChuckThermoScale(ScaleX:Decimal="", ScaleY:Decimal=""):
    """
    Thermo drifts of the wafer will be compensated. The compensation is not
    persistent, (power off - this compensation is deleted). The algorithm works as
    an additional one.  This is for an iterative usage, so:  1. `ResetProber H` 2.
    `SetChuckThermoScale 1.5 1.5` 3. `SetChuckThermoScale 1.5 1.5`  will result in a
    scale of 2.25 in both directions. The thermal scale can also be reset using the
    command 'SetChcukThermoValue 20 C'
    API Status: published
    Args:
        ScaleX:Decimal = 1
        ScaleY:Decimal = 1
    Command Timeout: 5000
    Example:SetChuckThermoScale 1.000005 1.0000045
    """
    MessageServerInterface.sendSciCommand("SetChuckThermoScale",ScaleX,ScaleY)


def ReadChuckThermoScale():
    """
    Read the linear scaling value of the chuck.
    API Status: published
    Returns:
        ScaleX:Decimal
        ScaleY:Decimal
    Command Timeout: 5000
    Example:ReadChuckThermoScale
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckThermoScale")
    global ReadChuckThermoScale_Response
    if not "ReadChuckThermoScale_Response" in globals(): ReadChuckThermoScale_Response = namedtuple("ReadChuckThermoScale_Response", "ScaleX,ScaleY")
    return ReadChuckThermoScale_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def SetChuckThermoValue(Temperature:Decimal="", Unit:str="", ExpCoeffX:Decimal="", ExpCoeffY:Decimal=""):
    """
    Set a temperature and optional the expansion coefficient. The temperature for
    normal level is 20 degree. The scaling factor at this temperature is 1.0. If you
    set the temperature directly the controller calculates the stage difference in
    the coordinate system. For the calculation use the set coefficient of expansion
    from the controller. The default coefficient of expansion is based on silicon:
    2.33E-06 1/K.
    API Status: published
    Args:
        Temperature:Decimal = 0
        Unit:str = "Celsius"
        ExpCoeffX:Decimal = 0
        ExpCoeffY:Decimal = 0
    Command Timeout: 5000
    Example:SetChuckThermoValue 250 C 2.43 2.32
    """
    MessageServerInterface.sendSciCommand("SetChuckThermoValue",Temperature,Unit,ExpCoeffX,ExpCoeffY)


def ReadChuckThermoValue(Unit:str=""):
    """
    Read the current temperature (either set or calculated) for the thermal scaling.
    With SetChuckThermoScale in use, the value will be calculated by the current
    scale and the expansion factor of silicium. The temperature that is read with
    this command is not identical to the current chuck temperature.
    API Status: published
    Args:
        Unit:str = "Celsius"
    Returns:
        Temperature:Decimal
        ExpCoeffX:Decimal
        ExpCoeffY:Decimal
    Command Timeout: 5000
    Example:ReadChuckThermoValue C
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckThermoValue",Unit)
    global ReadChuckThermoValue_Response
    if not "ReadChuckThermoValue_Response" in globals(): ReadChuckThermoValue_Response = namedtuple("ReadChuckThermoValue_Response", "Temperature,ExpCoeffX,ExpCoeffY")
    return ReadChuckThermoValue_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def GetChuckTableID(TableName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Return the TableID Number of the stored chuck table or create a new table. The
    ID Number is unique for the name and the chuck. The table itself has a string
    name, this name is not case sensitive. This command has to be used before all
    other table commands can be used. Accesses to the table is possible only with an
    ID Number (name dependet).
    API Status: internal
    Args:
        TableName:str = "ChuckTable"
    Returns:
        TableID:int
    Command Timeout: 5000
    Example:GetChuckTableID ChuckTable
    """
    rsp = MessageServerInterface.sendSciCommand("GetChuckTableID",TableName)
    return int(rsp[0])

def MoveChuckTablePoint(TableID:int="", PointID:int="", Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Move the chuck to the next stored table site.
    API Status: internal
    Args:
        TableID:int = 0
        PointID:int = 0
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MoveChuckTablePoint 3 10 67
    """
    MessageServerInterface.sendSciCommand("MoveChuckTablePoint",TableID,PointID,Velocity)


def ReadChuckTablePoint(TableID:int="", PointID:int="", Unit:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Read back the table site information for this point from the Kernel.
    API Status: internal
    Args:
        TableID:int = 0
        PointID:int = 0
        Unit:str = "Microns"
    Returns:
        CoordX:Decimal
        CoordY:Decimal
        CoordSystem:str
    Command Timeout: 5000
    Example:ReadChuckTablePoint 10 250 Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckTablePoint",TableID,PointID,Unit)
    global ReadChuckTablePoint_Response
    if not "ReadChuckTablePoint_Response" in globals(): ReadChuckTablePoint_Response = namedtuple("ReadChuckTablePoint_Response", "CoordX,CoordY,CoordSystem")
    return ReadChuckTablePoint_Response(Decimal(rsp[0]),Decimal(rsp[1]),str("" if len(rsp) < 3 else ' '.join(rsp[2:])))

def SetChuckTablePoint(TableID:int="", PointID:int="", CoordX:Decimal="", CoordY:Decimal="", Unit:str="", CoordSystem:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set one point of the chuck table inside of the Kernel. If there is still a point
    with this index loaded, the Kernel returns an error. Number of positions and
    number of tables are dependet on the internal memory. All positions are stored
    persistent, that means after switching power on or off the positions are still
    available. The table starts with point number 1 and ends with the ID 16. The
    table can contain 65535 points with the ID 0 up to 65534. Overwriting of
    position points is not possible. The point has to be deleted before other values
    are set.
    API Status: internal
    Args:
        TableID:int = 0
        PointID:int = 0
        CoordX:Decimal = 0
        CoordY:Decimal = 0
        Unit:str = "Microns"
        CoordSystem:str = "HomeSystem"
    Returns:
        ValidPoint:int
    Command Timeout: 5000
    Example:SetChuckTablePoint 10 12000.0 2344.0 Y F
    """
    rsp = MessageServerInterface.sendSciCommand("SetChuckTablePoint",TableID,PointID,CoordX,CoordY,Unit,CoordSystem)
    return int(rsp[0])

def ClearChuckTablePoint(TableID:int="", StartPoint:int="", EndPoint:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Clear one or a range of chuck table site points in the in the Kernel. If Start
    Point is -1 or negative the whole table will be deleted.
    API Status: internal
    Args:
        TableID:int = 0
        StartPoint:int = -1
        EndPoint:int = 0
    Returns:
        ClearNumber:int
        ValidNumber:int
    Command Timeout: 5000
    Example:ClearChuckTablePoint 5 10 15
    """
    rsp = MessageServerInterface.sendSciCommand("ClearChuckTablePoint",TableID,StartPoint,EndPoint)
    global ClearChuckTablePoint_Response
    if not "ClearChuckTablePoint_Response" in globals(): ClearChuckTablePoint_Response = namedtuple("ClearChuckTablePoint_Response", "ClearNumber,ValidNumber")
    return ClearChuckTablePoint_Response(int(rsp[0]),int(rsp[1]))

def AttachAmbientWafer(MoveTimeMs:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command is moved to slowly attach a wafer that is at ambient temperature while
    the chuck is hot.     The command acts similar to MoveChuckTransfer when moving
    out of Load 2 but will use a much slower Z velocity.     This is only supported
    for BnR-machines (CM300 and Summit200) at the moment.
    API Status: internal
    Args:
        MoveTimeMs:Decimal = 30000
    Command Timeout: 300000
    Example:AttachAmbientWafer
    """
    MessageServerInterface.sendSciCommand("AttachAmbientWafer",MoveTimeMs)


def ReadThetaStatus():
    """
    Returns the actual status of the chuck Theta axis.
    API Status: published
    Returns:
        IsInit:int
        FlagsLimit:int
        IsMoving:int
    Command Timeout: 5000
    Example:ReadThetaStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadThetaStatus")
    global ReadThetaStatus_Response
    if not "ReadThetaStatus_Response" in globals(): ReadThetaStatus_Response = namedtuple("ReadThetaStatus_Response", "IsInit,FlagsLimit,IsMoving")
    return ReadThetaStatus_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]))

def ReadThetaPosition(Unit:str="", PosRef:str=""):
    """
    Returns the actual Theta position.
    API Status: published
    Args:
        Unit:str = "Degrees"
        PosRef:str = "Home"
    Returns:
        Position:Decimal
    Command Timeout: 5000
    Example:ReadThetaPosition D Z
    """
    rsp = MessageServerInterface.sendSciCommand("ReadThetaPosition",Unit,PosRef)
    return Decimal(rsp[0])

def InitTheta(FlagsDoPlus:int="", FlagsMoveRange:int=""):
    """
    Performs an initialization move and resets the coordinate system of the Theta
    axis.
    API Status: published
    Args:
        FlagsDoPlus:int = 0
        FlagsMoveRange:int = 0
    Command Timeout: 120000
    Example:InitTheta 0 0
    """
    MessageServerInterface.sendSciCommand("InitTheta",FlagsDoPlus,FlagsMoveRange)


def MoveTheta(Position:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal=""):
    """
    Moves the chuck Theta axis to the specified position. The positive direction is
    counter-clockwise.
    API Status: published
    Args:
        Position:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Degrees"
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MoveTheta 1000. R E
    """
    MessageServerInterface.sendSciCommand("MoveTheta",Position,PosRef,Unit,Velocity)


def MoveThetaVelocity(Polarity:str="", Velocity:Decimal=""):
    """
    Moves the chuck Theta axis in velocity mode. The positive direction is counter-
    clockwise. The motion continues until the StopThetaMovement command is received,
    or the end limit (error condition) is reached. This command is mostly used for
    joystick movements that do not have a target destination.
    API Status: published
    Args:
        Polarity:str = "Fixed"
        Velocity:Decimal = 0
    Command Timeout: 240000
    Example:MoveThetaVelocity + 67
    """
    MessageServerInterface.sendSciCommand("MoveThetaVelocity",Polarity,Velocity)


def StopThetaMovement():
    """
    Stops any type (velocity, position etc.) of chuck Theta axis movement. This is
    treated as a smooth stop rather than an emergency stop.
    API Status: published
    Command Timeout: 5000
    Example:StopThetaMovement
    """
    MessageServerInterface.sendSciCommand("StopThetaMovement")


def SetThetaHome(Mode:str="", Unit:str="", Position:Decimal=""):
    """
    Sets the chuck Theta position to home. This position is usable as reference
    position for other commands.
    API Status: published
    Args:
        Mode:str = "0"
        Unit:str = "Degrees"
        Position:Decimal = 0
    Command Timeout: 5000
    Example:SetThetaHome 0
    """
    MessageServerInterface.sendSciCommand("SetThetaHome",Mode,Unit,Position)


def ScanChuckZ(ZDistance:Decimal="", TriggerEveryNthCycle:int="", Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Starts moving the chuck from the current position with Velocity [%] over
    ZDistance (sign is important, as a negative sign will move chuck down during
    scan) - Predefined camera trigger pulses (TTL active high for at least 5us) will
    be sent during the scan every passed number of BnR cyclics (800us per cyclic)
    until the ZDistance has been reached.  Command returns number of positions and
    all compensated Z Positions from Zero, where the trigger was sent.
    API Status: internal
    Args:
        ZDistance:Decimal = 1000
        TriggerEveryNthCycle:int = 3
        Velocity:Decimal = 10
    Returns:
        NumberOfPositions:int
        TriggerPositions:str
    Command Timeout: 60000
    Example:ScanChuckZ 300 3 1.5
    """
    rsp = MessageServerInterface.sendSciCommand("ScanChuckZ",ZDistance,TriggerEveryNthCycle,Velocity)
    global ScanChuckZ_Response
    if not "ScanChuckZ_Response" in globals(): ScanChuckZ_Response = namedtuple("ScanChuckZ_Response", "NumberOfPositions,TriggerPositions")
    return ScanChuckZ_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def MoveChuckZSafe():
    """
    Moves the chuck Z axis to a z height considered safe. This is either the lower
    Z-Fence or the kernel setup item Chuck:SafeTransferHeight (which ever is larger)
    API Status: published
    Command Timeout: 60000
    Example:MoveChuckZSafe
    """
    MessageServerInterface.sendSciCommand("MoveChuckZSafe")


def SetPlatenMode(Overtravel:int="", AutoZ:int="", Interlock:int="", AutoZFollow:int="", AutoQuiet:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The mode manages the way the platen behaves when it is in contact height. Platen
    mode is made up from 5 flags and the user can control all of them by using this
    command. Every flag can be turned on by setting value 1 or turned off by setting
    value 0. If no change for a flag is wanted, use the value of 2.
    API Status: internal
    Args:
        Overtravel:int = 2
        AutoZ:int = 2
        Interlock:int = 2
        AutoZFollow:int = 2
        AutoQuiet:int = 2
    Command Timeout: 5000
    Example:SetPlatenMode 2 2 2 2 2
    """
    MessageServerInterface.sendSciCommand("SetPlatenMode",Overtravel,AutoZ,Interlock,AutoZFollow,AutoQuiet)


def MovePlatenLift(SetLift:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the platen to the high (0) or low = lifted (1) position. This initiates
    motion; the actual movement may take some seconds.
    API Status: internal
    Args:
        SetLift:int = 1
    Command Timeout: 10000
    Example:MovePlatenLift 1
    """
    MessageServerInterface.sendSciCommand("MovePlatenLift",SetLift)


def SearchPlatenContact(Height:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", CompLayer:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Searches contact height using the edge sensor using a z movement of the platen
    stage
    API Status: internal
    Args:
        Height:Decimal = 0
        PosRef:str = "Zero"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        CompLayer:str = "Default"
    Returns:
        ContactHeight:Decimal
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("SearchPlatenContact",Height,PosRef,Unit,Velocity,CompLayer)
    return Decimal(rsp[0])

def ReadPlatenStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current platen status.
    API Status: internal
    Returns:
        FlagsInit:int
        FlagsMode:int
        FlagsLimit:int
        FlagsMoving:int
        Comp:str
        PresetHeight:str
        IsLiftDown:int
    Command Timeout: 10000
    Example:ReadPlatenStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadPlatenStatus")
    global ReadPlatenStatus_Response
    if not "ReadPlatenStatus_Response" in globals(): ReadPlatenStatus_Response = namedtuple("ReadPlatenStatus_Response", "FlagsInit,FlagsMode,FlagsLimit,FlagsMoving,Comp,PresetHeight,IsLiftDown")
    return ReadPlatenStatus_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),str(rsp[4]),str(rsp[5]),int(rsp[6]))

def ReadPlatenPosition(Unit:str="", PosRef:str="", Comp:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current position of the platens X, Y and Z axes. The default
    compensation is the currently selected compensation for the stage.
    API Status: internal
    Args:
        Unit:str = "Microns"
        PosRef:str = "Home"
        Comp:str = "Default"
    Returns:
        X:Decimal
        Y:Decimal
        Z:Decimal
    Command Timeout: 10000
    Example:ReadPlatenPosition Y Z
    """
    rsp = MessageServerInterface.sendSciCommand("ReadPlatenPosition",Unit,PosRef,Comp)
    global ReadPlatenPosition_Response
    if not "ReadPlatenPosition_Response" in globals(): ReadPlatenPosition_Response = namedtuple("ReadPlatenPosition_Response", "X,Y,Z")
    return ReadPlatenPosition_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def ReadPlatenHeights(Unit:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the actual settings for the probe Z movement.
    API Status: internal
    Args:
        Unit:str = "Microns"
    Returns:
        Contact:Decimal
        Overtravel:Decimal
        AlignDist:Decimal
        SepDist:Decimal
    Command Timeout: 10000
    Example:ReadPlatenHeights Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadPlatenHeights",Unit)
    global ReadPlatenHeights_Response
    if not "ReadPlatenHeights_Response" in globals(): ReadPlatenHeights_Response = namedtuple("ReadPlatenHeights_Response", "Contact,Overtravel,AlignDist,SepDist")
    return ReadPlatenHeights_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]))

def InitPlaten(FlagsInit:int="", FlagsDirection:int="", FlagsMoveRange:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Initializes the platens X, Y and Z axes. Currently the initialization in
    negative direction and the move range scan are not supported.
    API Status: internal
    Args:
        FlagsInit:int = 0
        FlagsDirection:int = 0
        FlagsMoveRange:int = 0
    Command Timeout: 120000
    Example:InitPlaten 4
    """
    MessageServerInterface.sendSciCommand("InitPlaten",FlagsInit,FlagsDirection,FlagsMoveRange)


def MovePlatenZ(Height:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the platen Z axis to the specified height. If contact is set, only moves
    up to contact height will be allowed. If overtravel is enabled - up to
    overtravel height.
    API Status: internal
    Args:
        Height:Decimal = 0
        PosRef:str = "Zero"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Command Timeout: 30000
    Example:MovePlatenZ 1000. R Y 67
    """
    MessageServerInterface.sendSciCommand("MovePlatenZ",Height,PosRef,Unit,Velocity,Comp)


def MovePlatenContact(Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Performs a movement of platen Z axis to preset contact height or returns an
    error, if no contact height is set.
    API Status: internal
    Args:
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MovePlatenContact 100
    """
    MessageServerInterface.sendSciCommand("MovePlatenContact",Velocity)


def MovePlatenAlign(Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the platen Z axis to the align height. If no contact height is set, the
    command will return an error.
    API Status: internal
    Args:
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MovePlatenAlign 100
    """
    MessageServerInterface.sendSciCommand("MovePlatenAlign",Velocity)


def MovePlatenSeparation(Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the platen Z axis to the separation height. If no contact height is set,
    the command will return an error.
    API Status: internal
    Args:
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MovePlatenSeparation 100
    """
    MessageServerInterface.sendSciCommand("MovePlatenSeparation",Velocity)


def MovePlatenVelocity(PolarityX:str="", PolarityY:str="", PolarityZ:str="", VelocityX:Decimal="", VelocityY:Decimal="", VelocityZ:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the platen stage in velocity mode. The motion continues until the
    StopPlatenMovement command is received, or the software fence is reached.
    API Status: internal
    Args:
        PolarityX:str = "Fixed"
        PolarityY:str = "Fixed"
        PolarityZ:str = "Fixed"
        VelocityX:Decimal = 100
        VelocityY:Decimal = 0
        VelocityZ:Decimal = 0
    Command Timeout: 240000
    Example:MovePlatenVelocity + + 0 67 50 0
    """
    MessageServerInterface.sendSciCommand("MovePlatenVelocity",PolarityX,PolarityY,PolarityZ,VelocityX,VelocityY,VelocityZ)


def StopPlatenMovement(FlagsStop:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Stops the movement of a set of platen axes immediately.
    API Status: internal
    Args:
        FlagsStop:int = 7
    Command Timeout: 10000
    Example:StopPlatenMovement 4
    """
    MessageServerInterface.sendSciCommand("StopPlatenMovement",FlagsStop)


def SetPlatenHeight(PresetHeight:str="", Mode:str="", Unit:str="", Value:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Defines the predefined contact height and corresponding gaps for overtravel,
    align and separation height. A command without data sets contact height at
    current position.
    API Status: internal
    Args:
        PresetHeight:str = "Contact"
        Mode:str = "0"
        Unit:str = "Microns"
        Value:Decimal = 0
    Command Timeout: 10000
    Example:SetPlatenHeight C V Y 5000
    """
    MessageServerInterface.sendSciCommand("SetPlatenHeight",PresetHeight,Mode,Unit,Value)


def ReadManualPlatenState():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Reads the current status of the manual platen. THis is only supported for
    Nucleus and Summit200.
    API Status: internal
    Returns:
        IsUp:int
        IsDown:int
        IsSafe:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadManualPlatenState")
    global ReadManualPlatenState_Response
    if not "ReadManualPlatenState_Response" in globals(): ReadManualPlatenState_Response = namedtuple("ReadManualPlatenState_Response", "IsUp,IsDown,IsSafe")
    return ReadManualPlatenState_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]))

def ReadScopeStatus():
    """
    Returns the current scope status.
    API Status: published
    Returns:
        FlagsInit:int
        FlagsLimit:int
        FlagsMoving:int
        Comp:str
        IsScopeLiftUp:int
        PresetHeight:str
        IsScopeLight:int
        FlagsMode:int
        IsQuiet:int
    Command Timeout: 5000
    Example:ReadScopeStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeStatus")
    global ReadScopeStatus_Response
    if not "ReadScopeStatus_Response" in globals(): ReadScopeStatus_Response = namedtuple("ReadScopeStatus_Response", "FlagsInit,FlagsLimit,FlagsMoving,Comp,IsScopeLiftUp,PresetHeight,IsScopeLight,FlagsMode,IsQuiet")
    return ReadScopeStatus_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),str(rsp[3]),int(rsp[4]),str(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]))

def ReadScopePosition(Unit:str="", PosRef:str="", Comp:str=""):
    """
    Returns the actual scope stage position in X, Y and Z. The default Compensation
    Mode is the currently activated compensation mode of the kernel.
    API Status: published
    Args:
        Unit:str = "Microns"
        PosRef:str = "Home"
        Comp:str = "Default"
    Returns:
        X:Decimal
        Y:Decimal
        Z:Decimal
    Command Timeout: 5000
    Example:ReadScopePosition Y Z
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopePosition",Unit,PosRef,Comp)
    global ReadScopePosition_Response
    if not "ReadScopePosition_Response" in globals(): ReadScopePosition_Response = namedtuple("ReadScopePosition_Response", "X,Y,Z")
    return ReadScopePosition_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def ReadScopeHeights(Unit:str=""):
    """
    Returns the actual settings of the focus height, align gap, and separation gap
    for the scope Z axis.
    API Status: published
    Args:
        Unit:str = "Microns"
    Returns:
        FocusHeight:Decimal
        AlignDist:Decimal
        SepDist:Decimal
    Command Timeout: 5000
    Example:ReadScopeHeights Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeHeights",Unit)
    global ReadScopeHeights_Response
    if not "ReadScopeHeights_Response" in globals(): ReadScopeHeights_Response = namedtuple("ReadScopeHeights_Response", "FocusHeight,AlignDist,SepDist")
    return ReadScopeHeights_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def InitScope(FlagsInit:int="", FlagsDirection:int="", FlagsMoveRange:int=""):
    """
    Initializes the microscope stage in X, Y and Z. The Axis default is all axes and
    the Direction default is XY in minus and Z in plus. Should be used only in cases
    when the reported coordinates do not correspond to real position of mechanics.
    Find Move Range starts the initialization in the defined direction and then
    moves to the other limit and finds the whole range of the axes.
    API Status: published
    Args:
        FlagsInit:int = 0
        FlagsDirection:int = 0
        FlagsMoveRange:int = 0
    Command Timeout: 240000
    Example:InitScope 3 0 0
    """
    MessageServerInterface.sendSciCommand("InitScope",FlagsInit,FlagsDirection,FlagsMoveRange)


def MoveScope(XValue:Decimal="", YValue:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    Moves the microscope stage to the specified X,Y position relative to the per
    PosRef specified reference position.
    API Status: published
    Args:
        XValue:Decimal = 0
        YValue:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Command Timeout: 70000
    Example:MoveScope 5000 5000 R Y 100
    """
    MessageServerInterface.sendSciCommand("MoveScope",XValue,YValue,PosRef,Unit,Velocity,Comp)


def MoveScopeIndex(XSteps:int="", YSteps:int="", PosRef:str="", Velocity:Decimal=""):
    """
    Moves the microscope stage in index steps. If no PositionReference byte is
    passed the scope will step relative to the wafer home position. ('R' means the
    step relative to current position).
    API Status: published
    Args:
        XSteps:int = 0
        YSteps:int = 0
        PosRef:str = "Home"
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MoveScopeIndex 1 1 R 100
    """
    MessageServerInterface.sendSciCommand("MoveScopeIndex",XSteps,YSteps,PosRef,Velocity)


def MoveScopeZ(Height:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    Moves the microscope Z axis to the specified height. Default velocity is 100%.
    API Status: published
    Args:
        Height:Decimal = 0
        PosRef:str = "Zero"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Command Timeout: 120000
    Example:MoveScopeZ 1000. R Y 67
    """
    MessageServerInterface.sendSciCommand("MoveScopeZ",Height,PosRef,Unit,Velocity,Comp)


def SetScopeMode(QuietMode:int="", FollowMode:int=""):
    """
    Scope mode is made up of two flags which can be controlled using this command.
    Each flag can be turned on by using value 1 or turned off by using value 0. If
    you do not want to change a flag, use value of 2.
    API Status: published
    Args:
        QuietMode:int = 2
        FollowMode:int = 2
    Command Timeout: 5000
    Example:SetScopeMode 2 2
    """
    MessageServerInterface.sendSciCommand("SetScopeMode",QuietMode,FollowMode)


def MoveScopeVelocity(PolarityX:str="", PolarityY:str="", PolarityZ:str="", VelocityX:Decimal="", VelocityY:Decimal="", VelocityZ:Decimal=""):
    """
    Moves the microscope stage in velocity mode. The motion continues until the
    StopScopeMovement command is received, or the end limit (error condition) is
    reached. Axes parameter: '+' move this axis in plus direction '-' move this axis
    in minus direction '0' Do not change this axis
    API Status: published
    Args:
        PolarityX:str = "Fixed"
        PolarityY:str = "Fixed"
        PolarityZ:str = "Fixed"
        VelocityX:Decimal = 100
        VelocityY:Decimal = 0
        VelocityZ:Decimal = 0
    Command Timeout: 30000
    Example:MoveScopeVelocity + + 0 67 100 0
    """
    MessageServerInterface.sendSciCommand("MoveScopeVelocity",PolarityX,PolarityY,PolarityZ,VelocityX,VelocityY,VelocityZ)


def StopScopeMovement(FlagsStop:int=""):
    """
    Stops scope movement for the given axis. A smooth stop is executed, no emergency
    stop.
    API Status: published
    Args:
        FlagsStop:int = 7
    Command Timeout: 5000
    Example:StopScopeMovement 7
    """
    MessageServerInterface.sendSciCommand("StopScopeMovement",FlagsStop)


def SetScopeHome(Mode:str="", Unit:str="", XValue:Decimal="", YValue:Decimal=""):
    """
    Sets the scope Home position in X and Y. It identifies the scope coordinate
    system for later movements. Usually this position is identical to the die home
    location.
    API Status: published
    Args:
        Mode:str = "0"
        Unit:str = "Microns"
        XValue:Decimal = 0
        YValue:Decimal = 0
    Command Timeout: 5000
    Example:SetScopeHome 0 Y
    """
    MessageServerInterface.sendSciCommand("SetScopeHome",Mode,Unit,XValue,YValue)


def SetScopeIndex(XValue:Decimal="", YValue:Decimal="", Unit:str=""):
    """
    Sets the microscope index size. Normally set in relation to the wafer index
    size.
    API Status: published
    Args:
        XValue:Decimal = 0
        YValue:Decimal = 0
        Unit:str = "Microns"
    Command Timeout: 5000
    Example:SetScopeIndex 5000. 5000. Y
    """
    MessageServerInterface.sendSciCommand("SetScopeIndex",XValue,YValue,Unit)


def SetScopeHeight(PresetHeight:str="", Mode:str="", Unit:str="", Value:Decimal=""):
    """
    This command defines scope focus height and the corresponding gaps for alignment
    or separation. No data sets focus height at current position.
    API Status: published
    Args:
        PresetHeight:str = "Contact"
        Mode:str = "0"
        Unit:str = "Microns"
        Value:Decimal = 0
    Command Timeout: 5000
    Example:SetScopeHeight F 0 Y
    """
    MessageServerInterface.sendSciCommand("SetScopeHeight",PresetHeight,Mode,Unit,Value)


def ReadScopeIndex(Unit:str=""):
    """
    Returns the actual scope stage index values in X and Y.
    API Status: published
    Args:
        Unit:str = "Microns"
    Returns:
        IndexX:Decimal
        IndexY:Decimal
    Command Timeout: 5000
    Example:ReadScopeIndex Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeIndex",Unit)
    global ReadScopeIndex_Response
    if not "ReadScopeIndex_Response" in globals(): ReadScopeIndex_Response = namedtuple("ReadScopeIndex_Response", "IndexX,IndexY")
    return ReadScopeIndex_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def MoveScopeFocus(Velocity:Decimal=""):
    """
    Moves the microscope stage to the specified X,Y position relative to the per
    PosRef specified reference position.
    API Status: published
    Args:
        Velocity:Decimal = 100
    Command Timeout: 25000
    Example:MoveScopeFocus 100
    """
    MessageServerInterface.sendSciCommand("MoveScopeFocus",Velocity)


def MoveScopeAlign(Velocity:Decimal=""):
    """
    Moves the Scope Z axis to the alignment height. If no focus height is set an
    error will bereturned.
    API Status: published
    Args:
        Velocity:Decimal = 100
    Command Timeout: 10000
    Example:MoveScopeAlign 100
    """
    MessageServerInterface.sendSciCommand("MoveScopeAlign",Velocity)


def MoveScopeSeparation(Velocity:Decimal=""):
    """
    Moves the scope Z axis to the separation height. Returns an error if no focus
    height is set.
    API Status: published
    Args:
        Velocity:Decimal = 100
    Command Timeout: 60000
    Example:MoveScopeSeparation 100
    """
    MessageServerInterface.sendSciCommand("MoveScopeSeparation",Velocity)


def MoveScopeLift(SetLift:int=""):
    """
    Moves the microscope lift to the lower (0) or upper = lifted (1) position. This
    initiates the motion only, the actual movement may take some seconds.
    API Status: published
    Args:
        SetLift:int = 1
    Command Timeout: 10000
    Example:MoveScopeLift 1
    """
    MessageServerInterface.sendSciCommand("MoveScopeLift",SetLift)


def ReadTurretStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current status of the motorized turret.
    API Status: internal
    Returns:
        IsMoving:int
    Command Timeout: 5000
    Example:ReadTurretStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadTurretStatus")
    return int(rsp[0])

def SelectLens(Lens:int=""):
    """
    Parfocality and para-centricity are adjusted according to the stored values.
    This can be used with manual turrets to compensate for XYZ differences between
    lenses.
    API Status: published
    Args:
        Lens:int = 1
    Command Timeout: 30000
    Example:SelectLens 1
    """
    MessageServerInterface.sendSciCommand("SelectLens",Lens)


def GetScopeTable(TableName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Return the TableID Number of the stored chuck table or create a new table. The
    ID Number is unique for the name and the chuck. The table itself has a string
    name, this name is not case sensitive. This command has to be used before all
    other table commands can be used. Accesses to the table is possible only with an
    ID Number (name dependet).
    API Status: internal
    Args:
        TableName:str = "ScopeTable"
    Returns:
        TableID:int
    Command Timeout: 5000
    Example:GetScopeTable ScopeTable
    """
    rsp = MessageServerInterface.sendSciCommand("GetScopeTable",TableName)
    return int(rsp[0])

def MoveScopeTablePoint(TableID:int="", PointID:int="", Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the microscope stage to the specified X,Y position relative to the per
    PosRef specified reference position.
    API Status: internal
    Args:
        TableID:int = 0
        PointID:int = 0
        Velocity:Decimal = 100
    Command Timeout: 30000
    Example:MoveScopeTablePoint 10 5 67
    """
    MessageServerInterface.sendSciCommand("MoveScopeTablePoint",TableID,PointID,Velocity)


def ReadScopeTablePoint(TableID:int="", PointID:int="", Unit:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Read back the scope table site Information for this point from the Kernel.
    API Status: internal
    Args:
        TableID:int = 0
        PointID:int = 0
        Unit:str = "Microns"
    Returns:
        CoordX:Decimal
        CoordY:Decimal
        CoordSystem:str
    Command Timeout: 5000
    Example:ReadScopeTablePoint 2 10 Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeTablePoint",TableID,PointID,Unit)
    global ReadScopeTablePoint_Response
    if not "ReadScopeTablePoint_Response" in globals(): ReadScopeTablePoint_Response = namedtuple("ReadScopeTablePoint_Response", "CoordX,CoordY,CoordSystem")
    return ReadScopeTablePoint_Response(Decimal(rsp[0]),Decimal(rsp[1]),str("" if len(rsp) < 3 else ' '.join(rsp[2:])))

def ReadCurrentLens():
    """
    Returns the number of the current microscope lens.
    API Status: published
    Returns:
        Lens:int
    Command Timeout: 5000
    Example:ReadCurrentLens
    """
    rsp = MessageServerInterface.sendSciCommand("ReadCurrentLens")
    return int(rsp[0])

def SetScopeTablePoint(TableID:int="", PointID:int="", CoordX:Decimal="", CoordY:Decimal="", Unit:str="", CoordSystem:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set one point of the scope table inside of the Kernel. If there is still a point
    with this index loaded, the Kernel returns an error. Number of positions and
    number of tables are dependet on the internal memory. All positions are stored
    persistent, that means after switching power on or off the positions are still
    available. The table starts with point number 1 and ends with the ID 16. The
    table can contain 65535 points with the ID 0 up to 65534. Overwriting of
    position points is not possible. The point has to be deleted before other values
    are set.
    API Status: internal
    Args:
        TableID:int = 0
        PointID:int = 0
        CoordX:Decimal = 0
        CoordY:Decimal = 0
        Unit:str = "Microns"
        CoordSystem:str = "HomeSystem"
    Returns:
        ValidPoint:int
    Command Timeout: 5000
    Example:SetScopeTablePoint 10 10 8992.5 7883.0 Y H
    """
    rsp = MessageServerInterface.sendSciCommand("SetScopeTablePoint",TableID,PointID,CoordX,CoordY,Unit,CoordSystem)
    return int(rsp[0])

def ClearScopeTablePoint(TableID:int="", StartPoint:int="", EndPoint:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Clear one or a range of scope table site points in the Kernel. If Start Point is
    -1 or negative the whole table will be deleted.
    API Status: internal
    Args:
        TableID:int = 0
        StartPoint:int = -1
        EndPoint:int = 0
    Returns:
        ClearNumber:int
        ValidNumber:int
    Command Timeout: 5000
    Example:ClearScopeTablePoint 2 10 15
    """
    rsp = MessageServerInterface.sendSciCommand("ClearScopeTablePoint",TableID,StartPoint,EndPoint)
    global ClearScopeTablePoint_Response
    if not "ClearScopeTablePoint_Response" in globals(): ClearScopeTablePoint_Response = namedtuple("ClearScopeTablePoint_Response", "ClearNumber,ValidNumber")
    return ClearScopeTablePoint_Response(int(rsp[0]),int(rsp[1]))

def ReadScopeSiloCount():
    """
    Returns the number of silos in the scope fence. Will be zero if no silos are
    configured.
    API Status: published
    Returns:
        Count:int
    Command Timeout: 5000
    Example:ReadScopeSiloCount
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeSiloCount")
    return int(rsp[0])

def ReadProbeStatus(Probe:int=""):
    """
    Returns the current positioner's status.
    API Status: published
    Args:
        Probe:int = 1
    Returns:
        ProbeEcho:int
        FlagsInit:int
        FlagsMode:int
        FlagsLimit:int
        FlagsMoving:int
        Comp:str
        Side:str
        PresetHeight:str
        IsLiftUp:int
        IsQuiet:int
    Command Timeout: 5000
    Example:ReadProbeStatus 1
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbeStatus",Probe)
    global ReadProbeStatus_Response
    if not "ReadProbeStatus_Response" in globals(): ReadProbeStatus_Response = namedtuple("ReadProbeStatus_Response", "ProbeEcho,FlagsInit,FlagsMode,FlagsLimit,FlagsMoving,Comp,Side,PresetHeight,IsLiftUp,IsQuiet")
    return ReadProbeStatus_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),str(rsp[5]),str(rsp[6]),str(rsp[7]),int(rsp[8]),int(rsp[9]))

def ReadProbePosition(Probe:int="", Unit:str="", PosRef:str="", Comp:str=""):
    """
    Returns the actual positioner's position in X, Y and Z. The default Compensation
    Mode is the currently activated compensation mode of the kernel.
    API Status: published
    Args:
        Probe:int = 1
        Unit:str = "Microns"
        PosRef:str = "Home"
        Comp:str = "Default"
    Returns:
        ProbeEcho:int
        X:Decimal
        Y:Decimal
        Z:Decimal
    Command Timeout: 5000
    Example:ReadProbePosition 1 Y Z
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbePosition",Probe,Unit,PosRef,Comp)
    global ReadProbePosition_Response
    if not "ReadProbePosition_Response" in globals(): ReadProbePosition_Response = namedtuple("ReadProbePosition_Response", "ProbeEcho,X,Y,Z")
    return ReadProbePosition_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]))

def ReadProbeHeights(Probe:int="", Unit:str=""):
    """
    Returns the actual settings for the probe Z movement.
    API Status: published
    Args:
        Probe:int = 1
        Unit:str = "Microns"
    Returns:
        ProbeEcho:int
        Contact:Decimal
        Overtravel:Decimal
        AlignDist:Decimal
        SepDist:Decimal
    Command Timeout: 5000
    Example:ReadProbeHeights 1 Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbeHeights",Probe,Unit)
    global ReadProbeHeights_Response
    if not "ReadProbeHeights_Response" in globals(): ReadProbeHeights_Response = namedtuple("ReadProbeHeights_Response", "ProbeEcho,Contact,Overtravel,AlignDist,SepDist")
    return ReadProbeHeights_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]))

def OrientProbe(Probe:int="", Side:str=""):
    """
    Defines the orientation of the positioner's coordinate system and turns the
    Y-axis of the probe coordinate system.
    API Status: published
    Args:
        Probe:int = 1
        Side:str = "Left"
    Returns:
        ProbeEcho:int
    Command Timeout: 5000
    Example:OrientProbe 1 R
    """
    rsp = MessageServerInterface.sendSciCommand("OrientProbe",Probe,Side)
    return int(rsp[0])

def InitProbe(Probe:int="", FlagsInit:int="", FlagsDirection:int="", FlagsMoveRange:int="", FlagsInitInPlace:int=""):
    """
    Performs an initialization move and resets the coordinate system of the given
    positioner.
    API Status: published
    Args:
        Probe:int = 1
        FlagsInit:int = 0
        FlagsDirection:int = 0
        FlagsMoveRange:int = 0
        FlagsInitInPlace:int = 0
    Returns:
        ProbeEcho:int
    Command Timeout: 120000
    Example:InitProbe 1 7 0 0
    """
    rsp = MessageServerInterface.sendSciCommand("InitProbe",Probe,FlagsInit,FlagsDirection,FlagsMoveRange,FlagsInitInPlace)
    return int(rsp[0])

def MoveProbe(Probe:int="", XValue:Decimal="", YValue:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    Moves a defined positioner to a X, Y position relative to a per PosRef specified
    reference position. Notifications: 51 / 52 / 5
    API Status: published
    Args:
        Probe:int = 1
        XValue:Decimal = 0
        YValue:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbe 1 1000. 1000. R Y 100
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbe",Probe,XValue,YValue,PosRef,Unit,Velocity,Comp)
    return int(rsp[0])

def MoveProbeIndex(Probe:int="", XSteps:int="", YSteps:int="", PosRef:str="", Velocity:Decimal=""):
    """
    Moves a defined positioner to a X, Y position relative to a per PosRef specified
    reference position. Notifications: 51 / 52 / 5
    API Status: published
    Args:
        Probe:int = 1
        XSteps:int = 0
        YSteps:int = 0
        PosRef:str = "Home"
        Velocity:Decimal = 100
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbeIndex 1 1 1 R 100
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeIndex",Probe,XSteps,YSteps,PosRef,Velocity)
    return int(rsp[0])

def MoveProbeContact(Probe:int="", Velocity:Decimal=""):
    """
    Moves the given ProbeHeads Z axis to the preset contact height. If no contact
    height is set, the kernel will return a 'Contact height not set' error.
    API Status: published
    Args:
        Probe:int = 1
        Velocity:Decimal = 100
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbeContact 1 100
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeContact",Probe,Velocity)
    return int(rsp[0])

def MoveProbeAlign(Probe:int="", Velocity:Decimal=""):
    """
    Moves the given ProbeHeads Z axis to the align height.
    API Status: published
    Args:
        Probe:int = 1
        Velocity:Decimal = 100
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbeAlign 1 100
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeAlign",Probe,Velocity)
    return int(rsp[0])

def MoveProbeSeparation(Probe:int="", Velocity:Decimal=""):
    """
    Moves a defined positioner to a X, Y position relative to a per PosRef specified
    reference position. Notifications: 51 / 52 / 5
    API Status: published
    Args:
        Probe:int = 1
        Velocity:Decimal = 100
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbeSeparation 1 100
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeSeparation",Probe,Velocity)
    return int(rsp[0])

def MoveProbeZ(Probe:int="", Height:Decimal="", PosRef:str="", Unit:str="", Velocity:Decimal="", Comp:str=""):
    """
    Moves a given ProbeHeads Z axis to a defined Z height.
    API Status: published
    Args:
        Probe:int = 1
        Height:Decimal = 0
        PosRef:str = "Zero"
        Unit:str = "Microns"
        Velocity:Decimal = 100
        Comp:str = "Default"
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbeZ 1 1000. R Y 67
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeZ",Probe,Height,PosRef,Unit,Velocity,Comp)
    return int(rsp[0])

def MoveProbeLift(Probe:int="", SetLift:int=""):
    """
    Moves the positioner to the lower (0) or upper = lifted (1) position. The
    command initiates the motion only, the whole movement may take some seconds.
    API Status: published
    Args:
        Probe:int = 1
        SetLift:int = 1
    Returns:
        ProbeEcho:int
    Command Timeout: 10000
    Example:MoveProbeLift 1
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeLift",Probe,SetLift)
    return int(rsp[0])

def MoveProbeVelocity(Probe:int="", PolarityX:str="", PolarityY:str="", PolarityZ:str="", VelocityX:Decimal="", VelocityY:Decimal="", VelocityZ:Decimal=""):
    """
    '+' Move this axis into plus direction '-' Move this axis into minus direction
    '0' Do not change this axis
    API Status: published
    Args:
        Probe:int = 1
        PolarityX:str = "Fixed"
        PolarityY:str = "Fixed"
        PolarityZ:str = "Fixed"
        VelocityX:Decimal = 100
        VelocityY:Decimal = 0
        VelocityZ:Decimal = 0
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbeVelocity 1 + + Z 67 100 0
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeVelocity",Probe,PolarityX,PolarityY,PolarityZ,VelocityX,VelocityY,VelocityZ)
    return int(rsp[0])

def StopProbeMovement(Probe:int="", FlagsStop:int=""):
    """
    Stops positioner movement for the given axes immediately. A smooth stop is
    performed.
    API Status: published
    Args:
        Probe:int = 1
        FlagsStop:int = 7
    Returns:
        ProbeEcho:int
    Command Timeout: 5000
    Example:StopProbeMovement 1 7
    """
    rsp = MessageServerInterface.sendSciCommand("StopProbeMovement",Probe,FlagsStop)
    return int(rsp[0])

def SetProbeMode(Probe:int="", Overtravel:int="", AutoZ:int="", Interlock:int="", AutoZFollow:int="", AutoQuiet:int=""):
    """
    The mode manages the way the chuck behaves when it is in contact height.
    Positioner mode is made up from 5 flags and the user can control all of them by
    using this command. Every flag can be turned on by setting value 1, or turned
    off by setting value 0. Use the value 2 if no change for a flag is needed.
    API Status: published
    Args:
        Probe:int = 1
        Overtravel:int = 2
        AutoZ:int = 2
        Interlock:int = 2
        AutoZFollow:int = 2
        AutoQuiet:int = 2
    Returns:
        ProbeEcho:int
    Command Timeout: 5000
    Example:SetProbeMode 1 2 2 2 2
    """
    rsp = MessageServerInterface.sendSciCommand("SetProbeMode",Probe,Overtravel,AutoZ,Interlock,AutoZFollow,AutoQuiet)
    return int(rsp[0])

def SetProbeHome(Probe:int="", Mode:str="", Unit:str="", XValue:Decimal="", YValue:Decimal=""):
    """
    Sets the positioner's Home position in X and Y. This position identifies the
    probe coordinate system for later movements. Usually this position is identical
    to the die home position.
    API Status: published
    Args:
        Probe:int = 1
        Mode:str = "0"
        Unit:str = "Microns"
        XValue:Decimal = 0
        YValue:Decimal = 0
    Returns:
        ProbeEcho:int
    Command Timeout: 5000
    Example:SetProbeHome 1 0 Y
    """
    rsp = MessageServerInterface.sendSciCommand("SetProbeHome",Probe,Mode,Unit,XValue,YValue)
    return int(rsp[0])

def SetProbeIndex(Probe:int="", XValue:Decimal="", YValue:Decimal="", Unit:str=""):
    """
    Sets the positioner's index size or the location of the reference die relative
    to the home die.
    API Status: published
    Args:
        Probe:int = 1
        XValue:Decimal = 0
        YValue:Decimal = 0
        Unit:str = "Microns"
    Returns:
        ProbeEcho:int
    Command Timeout: 5000
    Example:SetProbeIndex 1 1000. 1000. Y
    """
    rsp = MessageServerInterface.sendSciCommand("SetProbeIndex",Probe,XValue,YValue,Unit)
    return int(rsp[0])

def SetProbeHeight(Probe:int="", PresetHeight:str="", Mode:str="", Unit:str="", Value:Decimal=""):
    """
    Defines the predefined contact height and corresponding gaps for overtravel,
    align, load and separation height. No data sets contact height at current
    position.
    API Status: published
    Args:
        Probe:int = 1
        PresetHeight:str = "Contact"
        Mode:str = "0"
        Unit:str = "Microns"
        Value:Decimal = 0
    Returns:
        ProbeEcho:int
    Command Timeout: 5000
    Example:SetProbeHeight 1 C 0 Y
    """
    rsp = MessageServerInterface.sendSciCommand("SetProbeHeight",Probe,PresetHeight,Mode,Unit,Value)
    return int(rsp[0])

def ReadProbeIndex(Probe:int="", Unit:str=""):
    """
    Returns the current positioner's wafer index values or the current positioner's
    index positions for X and Y.
    API Status: published
    Args:
        Probe:int = 1
        Unit:str = "Microns"
    Returns:
        ProbeEcho:int
        IndexX:Decimal
        IndexY:Decimal
    Command Timeout: 5000
    Example:ReadProbeIndex 1 Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbeIndex",Probe,Unit)
    global ReadProbeIndex_Response
    if not "ReadProbeIndex_Response" in globals(): ReadProbeIndex_Response = namedtuple("ReadProbeIndex_Response", "ProbeEcho,IndexX,IndexY")
    return ReadProbeIndex_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def SetProbeLED(Probe:int="", NewLEDState:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set the positioner LED On or Off.
    API Status: internal
    Args:
        Probe:int = 1
        NewLEDState:int = 0
    Returns:
        ProbeEcho:int
        LEDState:int
    Command Timeout: 5000
    Example:SetProbeLED 1 1
    """
    rsp = MessageServerInterface.sendSciCommand("SetProbeLED",Probe,NewLEDState)
    global SetProbeLED_Response
    if not "SetProbeLED_Response" in globals(): SetProbeLED_Response = namedtuple("SetProbeLED_Response", "ProbeEcho,LEDState")
    return SetProbeLED_Response(int(rsp[0]),int(rsp[1]))

def GetProbeTableID(Probe:int="", TableName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the ID of a stored probe table or creates a new table. The ID is unique
    for the name and the probe. The table itself has a string name. This name is not
    case sensitive. The command has to be used before all other table commands can
    be used. Access to tables is possible only with an ID Number (name dependent).
    API Status: internal
    Args:
        Probe:int = 1
        TableName:str = "ProbeTable"
    Returns:
        ProbeEcho:int
        TableID:int
    Command Timeout: 5000
    Example:GetProbeTableID 1 ProbeTable
    """
    rsp = MessageServerInterface.sendSciCommand("GetProbeTableID",Probe,TableName)
    global GetProbeTableID_Response
    if not "GetProbeTableID_Response" in globals(): GetProbeTableID_Response = namedtuple("GetProbeTableID_Response", "ProbeEcho,TableID")
    return GetProbeTableID_Response(int(rsp[0]),int(rsp[1]))

def MoveProbeTablePoint(Probe:int="", TableID:int="", PointID:int="", Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves a defined positioner to a X, Y position relative to a per PosRef specified
    reference position. Notifications: 51 / 52 / 5
    API Status: internal
    Args:
        Probe:int = 1
        TableID:int = 1
        PointID:int = 1
        Velocity:Decimal = 100
    Returns:
        ProbeEcho:int
    Command Timeout: 30000
    Example:MoveProbeTablePoint 3 14 10 67
    """
    rsp = MessageServerInterface.sendSciCommand("MoveProbeTablePoint",Probe,TableID,PointID,Velocity)
    return int(rsp[0])

def ReadProbeTablePoint(Probe:int="", TableID:int="", PointID:int="", Unit:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Reads the data from a point of a stored table in the Kernel.
    API Status: internal
    Args:
        Probe:int = 1
        TableID:int = 0
        PointID:int = 0
        Unit:str = "Microns"
    Returns:
        ProbeEcho:int
        CoordX:Decimal
        CoordY:Decimal
        CoordSystem:str
    Command Timeout: 5000
    Example:ReadProbeTablePoint 2 4 10 Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbeTablePoint",Probe,TableID,PointID,Unit)
    global ReadProbeTablePoint_Response
    if not "ReadProbeTablePoint_Response" in globals(): ReadProbeTablePoint_Response = namedtuple("ReadProbeTablePoint_Response", "ProbeEcho,CoordX,CoordY,CoordSystem")
    return ReadProbeTablePoint_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),str("" if len(rsp) < 4 else ' '.join(rsp[3:])))

def SetProbeTablePoint(Probe:int="", TableID:int="", PointID:int="", CoordX:Decimal="", CoordY:Decimal="", Unit:str="", CoordSystem:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets one point of a ProbeHeads table inside the Kernel. If there is still a
    point with this index loaded, the Kernel returns an error. Number of positions
    and number of tables are dependet on the internal memory. All positions are
    stored persistent, that means after switching power on or off the positions are
    still available. The table starts with point number 1 and ends with the ID 16.
    The table can contain 65535 points with the ID 0 up to 65534. Overwriting of
    position points is not possible. The point has to be deleted before other values
    are set.
    API Status: internal
    Args:
        Probe:int = 1
        TableID:int = 0
        PointID:int = 0
        CoordX:Decimal = 0
        CoordY:Decimal = 0
        Unit:str = "Microns"
        CoordSystem:str = "HomeSystem"
    Returns:
        ProbeEcho:int
        ValidPoint:int
    Command Timeout: 5000
    Example:SetProbeTablePoint 3 12 10 8992.5 7883.0 Y Z M
    """
    rsp = MessageServerInterface.sendSciCommand("SetProbeTablePoint",Probe,TableID,PointID,CoordX,CoordY,Unit,CoordSystem)
    global SetProbeTablePoint_Response
    if not "SetProbeTablePoint_Response" in globals(): SetProbeTablePoint_Response = namedtuple("SetProbeTablePoint_Response", "ProbeEcho,ValidPoint")
    return SetProbeTablePoint_Response(int(rsp[0]),int(rsp[1]))

def ClearProbeTablePoint(Probe:int="", TableID:int="", StartPoint:int="", EndPoint:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Clear one or a range of ProbeHead table site points in the Kernel. If StartPoint
    is a negative value, the whole table will be deleted.
    API Status: internal
    Args:
        Probe:int = 1
        TableID:int = 0
        StartPoint:int = -1
        EndPoint:int = 0
    Returns:
        ProbeEcho:int
        ClearNumber:int
        ValidNumber:int
    Command Timeout: 5000
    Example:ClearProbeTablePoint 3 4 10 15
    """
    rsp = MessageServerInterface.sendSciCommand("ClearProbeTablePoint",Probe,TableID,StartPoint,EndPoint)
    global ClearProbeTablePoint_Response
    if not "ClearProbeTablePoint_Response" in globals(): ClearProbeTablePoint_Response = namedtuple("ClearProbeTablePoint_Response", "ProbeEcho,ClearNumber,ValidNumber")
    return ClearProbeTablePoint_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]))

def MoveScopeSilo(Index:int=""):
    """
    Move the scope to the reference position of the given silo. The reference
    position should be - if not defined otherwise - 200 um above the safe z-height
    in the center of the scope.
    API Status: published
    Args:
        Index:int = 1
    Command Timeout: 70000
    Example:MoveScopeSilo 1
    """
    MessageServerInterface.sendSciCommand("MoveScopeSilo",Index)


def SetScopeSiloReference(Index:int="", X:Decimal="", Y:Decimal="", Z:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set the reference position of a silo. The next time the scope moves to this
    silo, it woll go to this position. The Referenceposition must be inside the silo
    in xy and above the lower Z-Fence of the silo.  Setting the reference position
    directly on the fence in x, y or z typically leads to errors. Try to keep a
    safety margin.
    API Status: internal
    Args:
        Index:int = 1
        X:Decimal = 0
        Y:Decimal = 0
        Z:Decimal = 0
    Command Timeout: 5000
    Example:SetScopeSiloReference 1 1000 2000 3000
    """
    MessageServerInterface.sendSciCommand("SetScopeSiloReference",Index,X,Y,Z)


def AlignChuckTheta(XDistance:Decimal="", YDistance:Decimal="", PosRef:str=""):
    """
    This command causes a chuck Theta axis rotation to align the wafer to the chuck
    X,Y movements.     It can be used to perform a two point alignment with
    P1(X1,Y1) and P2(X2,Y2) as two points on a wafer street line.     The units of
    the distances are not important - but both distances should use the same unit.
    If one or both distances are zero, the command does not return an error and
    instead ignore this alignment
    API Status: published
    Args:
        XDistance:Decimal = 0
        YDistance:Decimal = 0
        PosRef:str = "Relative"
    Command Timeout: 10000
    Example:AlignChuckTheta 10000 10 R
    """
    MessageServerInterface.sendSciCommand("AlignChuckTheta",XDistance,YDistance,PosRef)


def AlignScopeTheta(XDistance:Decimal="", YDistance:Decimal="", PosRef:str=""):
    """
    This command causes a virtual rotation of the scope coordinate system to align
    the scope to the chuck X,Y axis or/and to the wafer alignment. It can be used to
    perform a two point alignment with the points P1(X1,Y1) and P2(X2,Y2).
    Calculation of X and Y distances:
    API Status: published
    Args:
        XDistance:Decimal = 0
        YDistance:Decimal = 0
        PosRef:str = "Relative"
    Command Timeout: 10000
    Example:AlignScopeTheta 10000 10 R
    """
    MessageServerInterface.sendSciCommand("AlignScopeTheta",XDistance,YDistance,PosRef)


def AlignProbeTheta(Probe:int="", XDistance:Decimal="", YDistance:Decimal="", PosRef:str=""):
    """
    This command causes a rotation of the coordinate system of given probe to align
    the probe to the chuck X,Y axis or/and to the wafer alignment. It can be used to
    perform a two point alignment with the points P1(X1,Y1) and P2(X2,Y2).
    Calculation of Y and Y distances:
    API Status: published
    Args:
        Probe:int = 1
        XDistance:Decimal = 0
        YDistance:Decimal = 0
        PosRef:str = "Relative"
    Returns:
        ProbeEcho:int
    Command Timeout: 10000
    Example:AlignProbeTheta 1 10000 10 R
    """
    rsp = MessageServerInterface.sendSciCommand("AlignProbeTheta",Probe,XDistance,YDistance,PosRef)
    return int(rsp[0])

def AlignCardTheta(Angle:Decimal="", Unit:str="", PosRef:str=""):
    """
    This command causes a rotation of the chuck coordinate system to align the chuck
    X, Y axis to the probecard.     The polarity of the data determines a left or a
    right rotation of the chuck coordinate system.
    API Status: published
    Args:
        Angle:Decimal = 0
        Unit:str = "Degrees"
        PosRef:str = "Relative"
    Command Timeout: 10000
    Example:AlignCardTheta 2.5 D R
    """
    MessageServerInterface.sendSciCommand("AlignCardTheta",Angle,Unit,PosRef)


def ReadCardTheta(Unit:str=""):
    """
    Returns the angle between the chuck-coordinate-system and the probecard-
    coordinate-system.
    API Status: published
    Args:
        Unit:str = "Degrees"
    Returns:
        Angle:Decimal
    Command Timeout: 5000
    Example:ReadCardTheta D
    """
    rsp = MessageServerInterface.sendSciCommand("ReadCardTheta",Unit)
    return Decimal(rsp[0])

def ReadChuckTheta(Unit:str=""):
    """
    Returns the current chuck alignment angle which is identical to the current
    value of theta rotation.
    API Status: published
    Args:
        Unit:str = "Degrees"
    Returns:
        Angle:Decimal
    Command Timeout: 5000
    Example:ReadChuckTheta D
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckTheta",Unit)
    return Decimal(rsp[0])

def ReadScopeTheta(Unit:str=""):
    """
    Returns the scope's alignment angle, which is the angle between the chuck
    coordinate system and the scope coordinate system.
    API Status: published
    Args:
        Unit:str = "Degrees"
    Returns:
        Angle:Decimal
    Command Timeout: 5000
    Example:ReadScopeTheta D
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeTheta",Unit)
    return Decimal(rsp[0])

def ReadProbeTheta(Probe:int="", Unit:str=""):
    """
    Returns the actual positioner's alignment angle, which is the angle between the
    chuck coordinate system and the positioner coordinate system.
    API Status: published
    Args:
        Probe:int = 1
        Unit:str = "Degrees"
    Returns:
        ProbeEcho:int
        Angle:Decimal
    Command Timeout: 5000
    Example:ReadProbeTheta 1 D
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbeTheta",Probe,Unit)
    global ReadProbeTheta_Response
    if not "ReadProbeTheta_Response" in globals(): ReadProbeTheta_Response = namedtuple("ReadProbeTheta_Response", "ProbeEcho,Angle")
    return ReadProbeTheta_Response(int(rsp[0]),Decimal(rsp[1]))

def ReadJoystickSpeeds(Stage:str="", Axis:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the preset speeds, which are used by the joystick controller for moving a
    single stage. The speeds can be read for XY, for Z and for Theta axis
    separately. Jog timing and index timing are the times, the joystick controller
    waits between two single jog or index moves.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "X"
    Returns:
        JogTime:Decimal
        Speed2:Decimal
        Speed3:Decimal
        Speed4:Decimal
        IndexTime:Decimal
    Command Timeout: 5000
    Example:ReadJoystickSpeeds S Z
    """
    rsp = MessageServerInterface.sendSciCommand("ReadJoystickSpeeds",Stage,Axis)
    global ReadJoystickSpeeds_Response
    if not "ReadJoystickSpeeds_Response" in globals(): ReadJoystickSpeeds_Response = namedtuple("ReadJoystickSpeeds_Response", "JogTime,Speed2,Speed3,Speed4,IndexTime")
    return ReadJoystickSpeeds_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]))

def SetJoystickSpeeds(Stage:str="", JogTime:Decimal="", Speed2:Decimal="", Speed3:Decimal="", Speed4:Decimal="", IndexTime:Decimal="", Axis:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the preset speeds, which are used by the joystick controller for moving a
    single stage. After setting, the speeds can be selected by pressing the Speed n
    buttons at the controller. The speeds must be set separately for XY, for Z and
    for Theta axis. Jog timing and index timing are the times, the joystick
    controller waits between two single jog or index moves.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        JogTime:Decimal = 0
        Speed2:Decimal = 0
        Speed3:Decimal = 0
        Speed4:Decimal = 0
        IndexTime:Decimal = 0
        Axis:str = "X"
    Command Timeout: 5000
    Example:SetJoystickSpeeds S 10 20 30 40 50 Z
    """
    MessageServerInterface.sendSciCommand("SetJoystickSpeeds",Stage,JogTime,Speed2,Speed3,Speed4,IndexTime,Axis)


def SetLoaderGate(Open:int=""):
    """
    Opens or closes the loader gate. Automatic handling systems can load wafers to
    the chuck through the gate.
    API Status: published
    Args:
        Open:int = 0
    Command Timeout: 5000
    Example:SetLoaderGate 0
    """
    MessageServerInterface.sendSciCommand("SetLoaderGate",Open)


def ReadWaferStatus():
    """
    Returns whether the system detected a wafer. This feature can be used if the
    probe station is equipped with a vacuum sensor and while vacuum is activated.
    API Status: published
    Returns:
        SensedByVac:str
    Command Timeout: 5000
    Example:ReadWaferStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadWaferStatus")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ReadContactCount(Stage:str=""):
    """
    Returns the number of times this stage moved to contact since the last time the
    counter was reset.
    API Status: published
    Args:
        Stage:str = "Chuck"
    Returns:
        Count:int
    Command Timeout: 5000
    Example:ReadContactCount C
    """
    rsp = MessageServerInterface.sendSciCommand("ReadContactCount",Stage)
    return int(rsp[0])

def ResetContactCount(Stage:str=""):
    """
    Resets the contact counter for the specified stage to zero. Notifications: 23
    API Status: published
    Args:
        Stage:str = "Chuck"
    Command Timeout: 5000
    Example:ResetContactCount C
    """
    MessageServerInterface.sendSciCommand("ResetContactCount",Stage)


def SetManualMode(Enable:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command enables the manual mode on Elite/Summit/S300 systems. This mode
    will allow to move the chuck using the knobs.
    API Status: internal
    Args:
        Enable:int = 1
    Command Timeout: 10000
    Example:SetManualMode 1
    """
    MessageServerInterface.sendSciCommand("SetManualMode",Enable)


def GetManualMode():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command returns the state of the manual mode on Elite/Summit/S300 stations.
    API Status: internal
    Returns:
        Enable:int
    Command Timeout: 10000
    Example:GetManualMode 1
    """
    rsp = MessageServerInterface.sendSciCommand("GetManualMode")
    return int(rsp[0])

def GetAxisReverse(Stage:str="", Axis:str=""):
    """
    Allows reading if an axis is reverse.
    API Status: published
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
    Returns:
        IsReverse:int
    Command Timeout: 5000
    Example:GetAxisReverse C X
    """
    rsp = MessageServerInterface.sendSciCommand("GetAxisReverse",Stage,Axis)
    return int(rsp[0])

def EnableEdgeSensor(EdgeSensor:int="", Enable:int=""):
    """
    Enables/disables the use of an edge sensor.
    API Status: published
    Args:
        EdgeSensor:int = 1
        Enable:int = 1
    Command Timeout: 5000
    Example:EnableEdgeSensor 1 1
    """
    MessageServerInterface.sendSciCommand("EnableEdgeSensor",EdgeSensor,Enable)


def SetTypedOutput(Channel:str="", WantOutputOn:int="", PulseTime:int=""):
    """
    Controls the kernel valve driver signals and can be used to drive the outputs.
    API Status: published
    Args:
        Channel:str = "NoSensor"
        WantOutputOn:int = 0
        PulseTime:int = -1
    Command Timeout: 5000
    Example:SetTypedOutput WaferVacuum 1
    """
    MessageServerInterface.sendSciCommand("SetTypedOutput",Channel,WantOutputOn,PulseTime)


def ReadTypedSensor(Channel:str=""):
    """
    Returns the status of the specified input channel, output channel, or edge
    sensor.
    API Status: published
    Args:
        Channel:str = "NoSensor"
    Returns:
        IsSensorOn:int
    Command Timeout: 10000
    Example:ReadTypedSensor EmoIn I
    """
    rsp = MessageServerInterface.sendSciCommand("ReadTypedSensor",Channel)
    return int(rsp[0])

def MoveCoolDownPosition():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the chuck to the cool down position that is defined in KernelSetup. The
    cooldown position is used to move the chuck away in XY while the robot is in the
    chamber and tries to get a hot wafer.
    API Status: internal
    Command Timeout: 30000
    Example:MoveCoolDownPosition
    """
    MessageServerInterface.sendSciCommand("MoveCoolDownPosition")


def ReadJoystickSpeedsCycle(Stage:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command reads the cycling speeds - these are the speeds that are used by
    the USB joystick when cycling through the speeds. Can be setup in ControlCenter.
    API Status: internal
    Args:
        Stage:str = "Chuck"
    Returns:
        CycleJog:int
        CycleSpeed2:int
        CycleSpeed3:int
        CycleSpeed4:int
        CycleIndex:int
    Command Timeout: 5000
    Example:ReadJoystickSpeedsCycle S
    """
    rsp = MessageServerInterface.sendSciCommand("ReadJoystickSpeedsCycle",Stage)
    global ReadJoystickSpeedsCycle_Response
    if not "ReadJoystickSpeedsCycle_Response" in globals(): ReadJoystickSpeedsCycle_Response = namedtuple("ReadJoystickSpeedsCycle_Response", "CycleJog,CycleSpeed2,CycleSpeed3,CycleSpeed4,CycleIndex")
    return ReadJoystickSpeedsCycle_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]))

def SetJoystickSpeedsCycle(Stage:str="", CycleJog:int="", CycleSpeed2:int="", CycleSpeed3:int="", CycleSpeed4:int="", CycleIndex:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command sets the cycling speeds - these are the speeds that are used by the
    USB joystick when cycling through the speeds. Can be setup in ControlCenter.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        CycleJog:int = 0
        CycleSpeed2:int = 0
        CycleSpeed3:int = 0
        CycleSpeed4:int = 0
        CycleIndex:int = 0
    Command Timeout: 5000
    Example:SetJoystickSpeedsCycle C 1 1 1 1 1
    """
    MessageServerInterface.sendSciCommand("SetJoystickSpeedsCycle",Stage,CycleJog,CycleSpeed2,CycleSpeed3,CycleSpeed4,CycleIndex)


def SendAUCSCommand(Command:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command allows sending low level AUCS commands to the ECX box stage. Only
    applies to Elite/Summit/S300 stations.
    API Status: internal
    Args:
        Command:str = ""
    Returns:
        Response:str
    Command Timeout: 60000
    Example:SendAUCSCommand "MM 1 0 INIT 0"
    """
    rsp = MessageServerInterface.sendSciCommand("SendAUCSCommand",Command)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ReadCompensationStatus(Stage:str="", Compensation:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command allows reading if a specific type of compensation is enabled or
    disabled. Returns an error if this type of compensation is not available for
    this stage.
    API Status: internal
    Args:
        Stage:str = "None"
        Compensation:str = "None"
    Returns:
        Enabled:int
        Active:int
    Command Timeout: 5000
    Example:ReadCompensationStatus C A
    """
    rsp = MessageServerInterface.sendSciCommand("ReadCompensationStatus",Stage,Compensation)
    global ReadCompensationStatus_Response
    if not "ReadCompensationStatus_Response" in globals(): ReadCompensationStatus_Response = namedtuple("ReadCompensationStatus_Response", "Enabled,Active")
    return ReadCompensationStatus_Response(int(rsp[0]),int(rsp[1]))

def RegisterNotification(NotificationCode:int="", WantNotification:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Deprecated. All Kernel notifications are now enabled by default.
    API Status: internal
    Args:
        NotificationCode:int = 0
        WantNotification:int = 1
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("RegisterNotification",NotificationCode,WantNotification)


def AlertNotification(NotificationId:int="", Value1:Decimal="", Value2:Decimal="", Value3:Decimal=""):
    """
    This is not a regular command. Asynchronous notifications will be sent from the
    Kernel controller to the host system only. All notifications can be switched off
    and on, except the Prober reset notification (ID01).  /warning This is a stub
    implementation without appropriate handling
    API Status: published
    Args:
        NotificationId:int = 0
        Value1:Decimal = 0
        Value2:Decimal = 0
        Value3:Decimal = 0
    Command Timeout: 5000
    Example:AlertNotification 31 195000 160000 0
    """
    MessageServerInterface.sendSciCommand("AlertNotification",NotificationId,Value1,Value2,Value3)


def SetCompensationStatus(Stage:str="", Compensation:str="", Status:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Enables or disables a compensation mode for the specified stage
    API Status: internal
    Args:
        Stage:str = "None"
        Compensation:str = "None"
        Status:int = -1
    Command Timeout: 5000
    Example:SetCompensationStatus C A 1
    """
    MessageServerInterface.sendSciCommand("SetCompensationStatus",Stage,Compensation,Status)


def GetControllerInfo(ControllerInfo:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command gets the value "Value" for the parameter "Parameter". The unit is
    parameter specific.
    API Status: internal
    Args:
        ControllerInfo:str = "Unknown"
    Returns:
        Value:Decimal
    Command Timeout: 1000
    Example:GetControllerInfo HasScanChuckZ
    """
    rsp = MessageServerInterface.sendSciCommand("GetControllerInfo",ControllerInfo)
    return Decimal(rsp[0])

def SetOperationalMode(OperationalMode:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    In unprotected mode a number of security features like software fence and
    initialization necessity are deactivated.          Unprotected mode is
    deactivated automatically after 5 minutes. Sending 'SetOperationalMode U'
    anytime before resets the timer back to 5 minutes. It is not necessary to
    deactivate it before.  **WARNING**: If unprotected mode is enabled, even the
    most basic safety- and sanity-checks are skipped. Any movement may cause
    irreparable damage to the prober or attached hardware.
    API Status: internal
    Args:
        OperationalMode:str = "ProtectedMode"
    Command Timeout: 5000
    Example:SetOperationalMode P
    """
    MessageServerInterface.sendSciCommand("SetOperationalMode",OperationalMode)


def GetNanoChamberState():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Get the currently configured Nano-chamber-state.
    API Status: internal
    Returns:
        NanoChamberState:str
    Command Timeout: 1000
    """
    rsp = MessageServerInterface.sendSciCommand("GetNanoChamberState")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetNanoChamberState(NanoChamberState:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set the NanoChamber-state.
    API Status: internal
    Args:
        NanoChamberState:str = "Free"
    Command Timeout: 1000
    """
    MessageServerInterface.sendSciCommand("SetNanoChamberState",NanoChamberState)


def SetCameraCool(State:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Allows to force activate/deactivate the camera cool output or to let it be set
    automatically by purge control.
    API Status: internal
    Args:
        State:int = 2
    Command Timeout: 10000
    Example:SetCameraCool 0
    """
    MessageServerInterface.sendSciCommand("SetCameraCool",State)


def ActivateChuckVacuum():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Activates the chuck vacuum and forces it to be on. This command ignores the
    vacuum sensor and timeout.
    API Status: internal
    Command Timeout: 10000
    Example:ActivateChuckVacuum
    """
    MessageServerInterface.sendSciCommand("ActivateChuckVacuum")


def ReadMatrixValues(Stage:str="", MatrixIndexX:int="", MatrixIndexY:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command returns a point from the matrix compensation table for the
    specified axis from the kernel. All command parameters are mandatory.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        MatrixIndexX:int = 0
        MatrixIndexY:int = 0
    Returns:
        XVal:Decimal
        YVal:Decimal
    Command Timeout: 5000
    Example:ReadMatrixValues C 0 0
    """
    rsp = MessageServerInterface.sendSciCommand("ReadMatrixValues",Stage,MatrixIndexX,MatrixIndexY)
    global ReadMatrixValues_Response
    if not "ReadMatrixValues_Response" in globals(): ReadMatrixValues_Response = namedtuple("ReadMatrixValues_Response", "XVal,YVal")
    return ReadMatrixValues_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def SetMatrixValues(Stage:str="", MatrixIndexX:int="", MatrixIndexY:int="", XVal:Decimal="", YVal:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Downloads a point of the matrix compensation table for a specified stage to the
    kernel. All command parameters are mandatory.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        MatrixIndexX:int = 0
        MatrixIndexY:int = 0
        XVal:Decimal = 0
        YVal:Decimal = 0
    Command Timeout: 5000
    Example:SetMatrixValues C 0 0 5000.0 5000.0 2500.0
    """
    MessageServerInterface.sendSciCommand("SetMatrixValues",Stage,MatrixIndexX,MatrixIndexY,XVal,YVal)


def ReadMEAStatus(Stage:str="", Type:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Reads if the MEA file for a stage is loaded/enabled (Nucleus legacy stations
    only)
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Type:int = 0
    Returns:
        Enable:int
    Command Timeout: 5000
    Example:ReadMEAStatus C 0
    """
    rsp = MessageServerInterface.sendSciCommand("ReadMEAStatus",Stage,Type)
    return int(rsp[0])

def LoadMEAFile(Stage:str="", Type:int="", Load:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Load the MEA file for a stage (Nucleus legacy stations only)
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Type:int = 0
        Load:int = 0
    Command Timeout: 5000
    Example:LoadMEAFile C 0 1
    """
    MessageServerInterface.sendSciCommand("LoadMEAFile",Stage,Type,Load)


def ReadSoftwareLimits(Stage:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The command returns the positions of the actual software limits (end of move
    range) for each axis of the specified stage in microns. If the Theta stage is
    selected Z1 and Z2 include the values for the Theta limits.
    API Status: internal
    Args:
        Stage:str = "Chuck"
    Returns:
        ZLowValue:Decimal
        ZHighValue:Decimal
        X1Value:Decimal
        Y1Value:Decimal
        X2Value:Decimal
        Y2Value:Decimal
        X3Value:Decimal
        Y3Value:Decimal
        X4Value:Decimal
        Y4Value:Decimal
    Command Timeout: 5000
    Example:ReadSoftwareLimits C
    """
    rsp = MessageServerInterface.sendSciCommand("ReadSoftwareLimits",Stage)
    global ReadSoftwareLimits_Response
    if not "ReadSoftwareLimits_Response" in globals(): ReadSoftwareLimits_Response = namedtuple("ReadSoftwareLimits_Response", "ZLowValue,ZHighValue,X1Value,Y1Value,X2Value,Y2Value,X3Value,Y3Value,X4Value,Y4Value")
    return ReadSoftwareLimits_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]),Decimal(rsp[6]),Decimal(rsp[7]),Decimal(rsp[8]),Decimal(rsp[9]))

def SetSoftwareFence(Stage:str="", AuxID:int="", FenceForm:str="", XBase:Decimal="", YBase:Decimal="", XDist:Decimal="", YDist:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command sets types and dimensions of technological software fences. It can
    also be used for enabling and disabling the software fence.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        AuxID:int = 0
        FenceForm:str = "None"
        XBase:Decimal = 0
        YBase:Decimal = 0
        XDist:Decimal = 0
        YDist:Decimal = 0
    Command Timeout: 10000
    Example:SetSoftwareFence C 0 R 5000 5000 25000 25000
    """
    MessageServerInterface.sendSciCommand("SetSoftwareFence",Stage,AuxID,FenceForm,XBase,YBase,XDist,YDist)


def GetSoftwareFence(Stage:str="", AuxID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command reads the type and the dimensions of an actual set technological
    software fence. In case of a rectangular software fence, X and Y coordinates of
    the four edge points of the fence are given back. In case of a circular software
    fence, X and Y coordinates of the center point and the radius are given back.
    All other return values are filled with zeros. All position values are in
    microns from zero.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        AuxID:int = 0
    Returns:
        FenceForm:str
        XValue1:Decimal
        YValue1:Decimal
        XValue2:Decimal
        YValue2:Decimal
        XValue3:Decimal
        YValue3:Decimal
        XValue4:Decimal
        YValue4:Decimal
    Command Timeout: 10000
    Example:GetSoftwareFence C
    """
    rsp = MessageServerInterface.sendSciCommand("GetSoftwareFence",Stage,AuxID)
    global GetSoftwareFence_Response
    if not "GetSoftwareFence_Response" in globals(): GetSoftwareFence_Response = namedtuple("GetSoftwareFence_Response", "FenceForm,XValue1,YValue1,XValue2,YValue2,XValue3,YValue3,XValue4,YValue4")
    return GetSoftwareFence_Response(str(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]),Decimal(rsp[6]),Decimal(rsp[7]),Decimal(rsp[8]))

def GetZFence(Stage:str="", CompLayer:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This commands reads if the Z-Fence is activated and the currently set Z-fence
    values for the specified stage.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        CompLayer:str = "Default"
    Returns:
        Enabled:int
        ZLow:Decimal
        ZHigh:Decimal
    Command Timeout: 10000
    Example:GetZFence S
    """
    rsp = MessageServerInterface.sendSciCommand("GetZFence",Stage,CompLayer)
    global GetZFence_Response
    if not "GetZFence_Response" in globals(): GetZFence_Response = namedtuple("GetZFence_Response", "Enabled,ZLow,ZHigh")
    return GetZFence_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def SetZFence(Stage:str="", Enabled:int="", ZLow:Decimal="", ZHigh:Decimal="", CompLayer:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This commands sets Z-Fence and the Z-fence values for the specified stage.
    Values are stored uncompensated internally and set default compensated as
    default.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Enabled:int = 0
        ZLow:Decimal = 0
        ZHigh:Decimal = 0
        CompLayer:str = "Default"
    Command Timeout: 10000
    Example:SetZFence S 1 5000 10000
    """
    MessageServerInterface.sendSciCommand("SetZFence",Stage,Enabled,ZLow,ZHigh,CompLayer)


def ResetProber(Mode:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Restarts the Prober and replaces the current configuration with a formerly
    written recovery file. If no recovery file was written, the configuration is
    reset to the version of the last Prober restart. For ProberBench electronics,
    'H' will restart the Operating system, 'S' will only restart the Kernel
    application. For Windows Kernel, 'H' and 'S' are identical.
    API Status: internal
    Args:
        Mode:str = "S"
    Command Timeout: 20000
    Example:ResetProber S
    """
    MessageServerInterface.sendSciCommand("ResetProber",Mode)


def ResetCBox(ResetMode:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Reboots the operation system inside the Joystick Controller and restarts the
    functionality. The restart will need a time of around 20 seconds.
    API Status: internal
    Args:
        ResetMode:str = "S"
    Command Timeout: 20000
    Example:ResetCBox S
    """
    MessageServerInterface.sendSciCommand("ResetCBox",ResetMode)


def ReadStageLocations(Stage:str="", LocationType:str="", AuxID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The Home Position on the Chuck or ProbeHead Z axis is also called contact
    height. The Home Position on the Scope Z axis is also called focus height.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        LocationType:str = "Center"
        AuxID:int = 0
    Returns:
        X:Decimal
        Y:Decimal
        Z:Decimal
    Command Timeout: 5000
    Example:ReadStageLocations C C 0
    """
    rsp = MessageServerInterface.sendSciCommand("ReadStageLocations",Stage,LocationType,AuxID)
    global ReadStageLocations_Response
    if not "ReadStageLocations_Response" in globals(): ReadStageLocations_Response = namedtuple("ReadStageLocations_Response", "X,Y,Z")
    return ReadStageLocations_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def GetDataIterator(ShowAll:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns a data stream handle which represents a data stream of setup parameters.
    and requires the GetNextDatum command.
    API Status: internal
    Args:
        ShowAll:int = 0
    Returns:
        IdentityToken:int
        SizeNoAll:int
    Command Timeout: 10000
    Example:GetDataIterator 1
    """
    rsp = MessageServerInterface.sendSciCommand("GetDataIterator",ShowAll)
    global GetDataIterator_Response
    if not "GetDataIterator_Response" in globals(): GetDataIterator_Response = namedtuple("GetDataIterator_Response", "IdentityToken,SizeNoAll")
    return GetDataIterator_Response(int(rsp[0]),int(rsp[1]))

def GetNextDatum(IdentityToken:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the next parameter from the data stream. Fields are separated by a
    colon. Structure of the response parameter Value:
    Path_Path:Name:Description:Value
    API Status: internal
    Args:
        IdentityToken:int = 0
    Returns:
        IsLastDatum:int
        DatumCode:int
        Attributes:int
        PathNameDescrValue:str
    Command Timeout: 10000
    Example:GetNextDatum 0
    """
    rsp = MessageServerInterface.sendSciCommand("GetNextDatum",IdentityToken)
    global GetNextDatum_Response
    if not "GetNextDatum_Response" in globals(): GetNextDatum_Response = namedtuple("GetNextDatum_Response", "IsLastDatum,DatumCode,Attributes,PathNameDescrValue")
    return GetNextDatum_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),str("" if len(rsp) < 4 else ' '.join(rsp[3:])))

def SetDatum(PathNameAndValue:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the value of a parameter. An empty parameter string saves the whole
    configuration to non-volatile memory. Fields are separated by a colon.
    API Status: internal
    Args:
        PathNameAndValue:str = ""
    Command Timeout: 20000
    Example:SetDatum Chuck:AlignGap:25
    """
    MessageServerInterface.sendSciCommand("SetDatum",PathNameAndValue)


def GetDatum(PathName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns a value string. The Value string consists of the value and the
    description. The Locator only consists of the path and the name. All fields are
    separated by a colon.  Structure of the command parameter Locator:
    Path_Path:Name Structure of the response parameter Value: Value:Description
    API Status: internal
    Args:
        PathName:str = ""
    Returns:
        Attributes:int
        DatumCode:int
        ValueDesc:str
    Command Timeout: 5000
    Example:GetDatum Chuck:AlignGap
    """
    rsp = MessageServerInterface.sendSciCommand("GetDatum",PathName)
    global GetDatum_Response
    if not "GetDatum_Response" in globals(): GetDatum_Response = namedtuple("GetDatum_Response", "Attributes,DatumCode,ValueDesc")
    return GetDatum_Response(int(rsp[0]),int(rsp[1]),str("" if len(rsp) < 3 else ' '.join(rsp[2:])))

def SetRecoveryDatum(PathNameAndValue:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the value of a parameter. An empty parameter string saves the whole
    configuration to non-volatile memory. Fields are separated by a colon.
    API Status: internal
    Args:
        PathNameAndValue:str = ""
    Command Timeout: 5000
    Example:SetRecoveryDatum Chuck:AlignGap:25
    """
    MessageServerInterface.sendSciCommand("SetRecoveryDatum",PathNameAndValue)


def TraceStart(Controller:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Activates the motion recording. The recording parameters are set in dynamic
    kernel setup.
    API Status: internal
    Args:
        Controller:str = "Chuck"
    Command Timeout: 10000
    Example:TraceStart C
    """
    MessageServerInterface.sendSciCommand("TraceStart",Controller)


def TraceStatus(Controller:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Checks the motion recording status for one stage.
    API Status: internal
    Args:
        Controller:str = "Chuck"
    Returns:
        IsReady:int
        SizeCh0Raw:int
        SizeCh0Comp:int
        SizeCh1Raw:int
        SizeCh1Comp:int
        SizeCh2Raw:int
        SizeCh2Comp:int
        SizeCh3Raw:int
        SizeCh3Comp:int
    Command Timeout: 10000
    Example:TraceStatus C
    """
    rsp = MessageServerInterface.sendSciCommand("TraceStatus",Controller)
    global TraceStatus_Response
    if not "TraceStatus_Response" in globals(): TraceStatus_Response = namedtuple("TraceStatus_Response", "IsReady,SizeCh0Raw,SizeCh0Comp,SizeCh1Raw,SizeCh1Comp,SizeCh2Raw,SizeCh2Comp,SizeCh3Raw,SizeCh3Comp")
    return TraceStatus_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]))

def TraceGetData(Controller:str="", Channel:int="", PointOne:int="", IsCompress:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Get a collection of five data pairs. A pair is the index and the value of a
    recording point. If the stream is empty or at the end the index is 1 and the
    value 0. The index is relative to the start of the motion recording. The
    recording is clocked by the motion controller cycle. The cycle time is contained
    in the Kernel setup. In the raw stream all recorded trace points are contained.
    But in the compressed stream only the non-linear depending trace points are
    contained. To reload the recording points the stream must be reset to the first
    recording point.
    API Status: internal
    Args:
        Controller:str = "Chuck"
        Channel:int = 0
        PointOne:int = 1
        IsCompress:int = 1
    Returns:
        Point1:int
        Value1:int
        Point2:int
        Value2:int
        Point3:int
        Value3:int
        Point4:int
        Value4:int
        Point5:int
        Value5:int
    Command Timeout: 10000
    Example:TraceGetData C 0 0 1
    """
    rsp = MessageServerInterface.sendSciCommand("TraceGetData",Controller,Channel,PointOne,IsCompress)
    global TraceGetData_Response
    if not "TraceGetData_Response" in globals(): TraceGetData_Response = namedtuple("TraceGetData_Response", "Point1,Value1,Point2,Value2,Point3,Value3,Point4,Value4,Point5,Value5")
    return TraceGetData_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]))

def TraceSetDataPosition(Controller:str="", Channel:int="", NewPos:int="", IsCompress:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the index position in the raw or compressed stream for the next call of the
    command TraceGetData.
    API Status: internal
    Args:
        Controller:str = "Chuck"
        Channel:int = 0
        NewPos:int = 0
        IsCompress:int = 1
    Command Timeout: 10000
    Example:TraceSetDataPosition C 0 1000 1
    """
    MessageServerInterface.sendSciCommand("TraceSetDataPosition",Controller,Channel,NewPos,IsCompress)


def TraceStop(Controller:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Stops the motion recording.
    API Status: internal
    Args:
        Controller:str = "Chuck"
    Command Timeout: 10000
    Example:TraceStop C
    """
    MessageServerInterface.sendSciCommand("TraceStop",Controller)


def SetZProfilePoint(Stage:str="", XValue:Decimal="", YValue:Decimal="", ZGap:Decimal="", PosRef:str="", Unit:str="", ZProfileType:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set a point for the Z height profile. If this profile is enabled, the Z height
    depends on a X and Y coordinate. The Z value is a gap to the current Z height.
    Positive values are elevated spots, negative values are hollows. The height
    profile is used to adjust the Z height. The adjusted Z height at a X and Y
    position is derivated from the nearest profile point. The Z contact level will
    be calculated from the contact height and the stored Z gap at this point.  See
    GetZProfilePoint for details.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        XValue:Decimal = 0
        YValue:Decimal = 0
        ZGap:Decimal = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        ZProfileType:int = 0
    Returns:
        ValueCount:int
    Command Timeout: 5000
    Example:SetZProfilePoint C 5000 5000 -3 H Y
    """
    rsp = MessageServerInterface.sendSciCommand("SetZProfilePoint",Stage,XValue,YValue,ZGap,PosRef,Unit,ZProfileType)
    return int(rsp[0])

def ReadZProfilePoint(Stage:str="", Index:int="", PosRef:str="", Unit:str="", ZProfileType:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Get a single point and the corresponding Z gap of the Z height profile.  The
    different z profiles are:  - transient: meant to be used on a per-wafer-basis,
    default - persistent: configured once, stays in memory - persistent-offset: same
    as persistent, active when offset is enabled - scratch: not used internaly. Can
    be used to translate KernelDatums <-> ZProfile-Points
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Index:int = 0
        PosRef:str = "Home"
        Unit:str = "Microns"
        ZProfileType:int = 0
    Returns:
        XValue:Decimal
        YValue:Decimal
        ZGap:Decimal
        ValueCount:int
    Command Timeout: 5000
    Example:ReadZProfilePoint C 1 H
    """
    rsp = MessageServerInterface.sendSciCommand("ReadZProfilePoint",Stage,Index,PosRef,Unit,ZProfileType)
    global ReadZProfilePoint_Response
    if not "ReadZProfilePoint_Response" in globals(): ReadZProfilePoint_Response = namedtuple("ReadZProfilePoint_Response", "XValue,YValue,ZGap,ValueCount")
    return ReadZProfilePoint_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),int(rsp[3]))

def ClearZProfile(Stage:str="", ZProfileType:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Clears all profile points. See GetZProfile for type description.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        ZProfileType:int = 0
    Command Timeout: 5000
    Example:ClearZProfile C
    """
    MessageServerInterface.sendSciCommand("ClearZProfile",Stage,ZProfileType)


def ReadScopeSilo(Index:int=""):
    """
    Returns the definition of a silo. If the type is rectangle, center means
    _Point1_. If the type is circle, the meaning of Pos2X and Pos2Y is undefined.
    API Status: published
    Args:
        Index:int = 1
    Returns:
        Type:str
        CenterX:Decimal
        CenterY:Decimal
        Radius:Decimal
        Pos2X:Decimal
        Pos2Y:Decimal
        ZHigh:Decimal
        RefX:Decimal
        RefY:Decimal
        RefZ:Decimal
    Command Timeout: 5000
    Example:ReadScopeSilo 1
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeSilo",Index)
    global ReadScopeSilo_Response
    if not "ReadScopeSilo_Response" in globals(): ReadScopeSilo_Response = namedtuple("ReadScopeSilo_Response", "Type,CenterX,CenterY,Radius,Pos2X,Pos2Y,ZHigh,RefX,RefY,RefZ")
    return ReadScopeSilo_Response(str(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]),Decimal(rsp[6]),Decimal(rsp[7]),Decimal(rsp[8]),Decimal(rsp[9]))

def NewProjectFile(FileName:str=""):
    """
    Alerts applications if the project file was changed.
    API Status: published
    Args:
        FileName:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("NewProjectFile",FileName)


def SaveProjectFile(FileName:str=""):
    """
    Alerts applications to save the current project.  This notification _MUST_ only
    be invoked by CommonCommands. Sending this notification directly _WILL_ give
    erroneous results.
    API Status: published
    Args:
        FileName:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("SaveProjectFile",FileName)


def NewAccessLevel(AccessLevel:str="", UserName:str="", VeloxLocked:int=""):
    """
    Alerts applications of new access level.
    API Status: published
    Args:
        AccessLevel:str = "Engineer"
        UserName:str = ""
        VeloxLocked:int = 0
    Command Timeout: 5000
    Example:NewAccessLevel 1
    """
    MessageServerInterface.sendSciCommand("NewAccessLevel",AccessLevel,UserName,VeloxLocked)


def LicenseInfo(AnnualEnabled:int="", AnnualDaysLeft:int="", VeloxProEnabled:int="", VueTrackEnabled:int="", VueTrack4PEnabled:int="", ReAlignEnabled:int="", AutomationEnabled:int="", IdToolsEnabled:int="", IVistaEnabled:int="", IVistaProEnabled:int="", LaserCutterEnabled:int="", SiPToolsEnabled:int="", AutoRfEnabled:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifys the listener about the licensed Velox features. Is sent cyclically by
    CommonCommands.
    API Status: internal
    Args:
        AnnualEnabled:int = 1
        AnnualDaysLeft:int = 460
        VeloxProEnabled:int = 0
        VueTrackEnabled:int = 0
        VueTrack4PEnabled:int = 0
        ReAlignEnabled:int = 0
        AutomationEnabled:int = 0
        IdToolsEnabled:int = 0
        IVistaEnabled:int = 0
        IVistaProEnabled:int = 0
        LaserCutterEnabled:int = 0
        SiPToolsEnabled:int = 0
        AutoRfEnabled:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("LicenseInfo",AnnualEnabled,AnnualDaysLeft,VeloxProEnabled,VueTrackEnabled,VueTrack4PEnabled,ReAlignEnabled,AutomationEnabled,IdToolsEnabled,IVistaEnabled,IVistaProEnabled,LaserCutterEnabled,SiPToolsEnabled,AutoRfEnabled)


def RegisterProberAppChange(AppName:str="", SecName:str="", NewRegistered:int=""):
    """
    Alerts applications that an application is registered or unregistered on
    MsgServer.
    API Status: published
    Args:
        AppName:str = "SharedTest"
        SecName:str = "SharedTest"
        NewRegistered:int = 1
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("RegisterProberAppChange",AppName,SecName,NewRegistered)


def AlignmentModeChange(AlignmentMode:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Alerts applications of a change of the current alignment mode
    API Status: internal
    Args:
        AlignmentMode:str = "OnAxis"
    Command Timeout: 5000
    Example:AlignmentModeChange OnAxis
    """
    MessageServerInterface.sendSciCommand("AlignmentModeChange",AlignmentMode)


def KernelConnectionStatus(ControllerNum:int="", Type:str="", Result:str="", Desc:str=""):
    """
    An example of Kernel Connection Status is &quot;Windows Socket Error Number and
    Error Description.&quot;
    API Status: published
    Args:
        ControllerNum:int = 1
        Type:str = "Socket"
        Result:str = "Disconnected"
        Desc:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("KernelConnectionStatus",ControllerNum,Type,Result,Desc)


def KernelCompensationStatusChange(Stage:str="", Compensation:str="", Enabled:int="", Active:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Alerts applications that a Kernel compensation has changed.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Compensation:str = "None"
        Enabled:int = 0
        Active:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("KernelCompensationStatusChange",Stage,Compensation,Enabled,Active)


def KernelCompensationLevelChange(Stage:str="", Comp:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Alerts applications that a Kernel compensation level has changed.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Comp:str = "None"
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("KernelCompensationLevelChange",Stage,Comp)


def MoveZCombinedStatusChange(Status:str="", PlatenSafe:int="", Height:Decimal="", HeightMax:Decimal="", HeightRelative:Decimal="", SafeHeight:Decimal="", Message:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifies about changes in the combined-z-move-system
    API Status: internal
    Args:
        Status:str = "Off"
        PlatenSafe:int = 0
        Height:Decimal = 0
        HeightMax:Decimal = 0
        HeightRelative:Decimal = 0
        SafeHeight:Decimal = 0
        Message:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("MoveZCombinedStatusChange",Status,PlatenSafe,Height,HeightMax,HeightRelative,SafeHeight,Message)


def MachineStateChange(MachineState:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifies about changes in the machine state
    API Status: internal
    Args:
        MachineState:str = "Off"
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("MachineStateChange",MachineState)


def ChuckVacuumChangeRequest(VacuumState:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifies if the user requests a chuck vacuum change
    API Status: internal
    Args:
        VacuumState:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("ChuckVacuumChangeRequest",VacuumState)


def SoftwareStopChangedNotify(SoftwareStopState:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifies if software stop was activated or deactivated
    API Status: internal
    Args:
        SoftwareStopState:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("SoftwareStopChangedNotify",SoftwareStopState)


def KernelQuietModeChange(IsQuiet:int="", Stage:str="", IsStageQuiet:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Informs if the overall quiet mode changes and about changes of single stages
    API Status: internal
    Args:
        IsQuiet:int = 0
        Stage:str = "None"
        IsStageQuiet:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("KernelQuietModeChange",IsQuiet,Stage,IsStageQuiet)


def ConfigurationChanged(ParameterChanged:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifies that a configuration item has changed by some application
    API Status: internal
    Args:
        ParameterChanged:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("ConfigurationChanged",ParameterChanged)


def ScopeWorkingStageChanged(ScopeWorkingStage:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Informs that a new working stage is active
    API Status: internal
    Args:
        ScopeWorkingStage:int = -1
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("ScopeWorkingStageChanged",ScopeWorkingStage)


def BnR_AxisNotify(Stage:str="", Axis:str="", State:str="", AdditionalStateInfo:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notify the user Interface and Kernel if the state of the axis has changed.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
        State:str = "NotExisting"
        AdditionalStateInfo:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_AxisNotify",Stage,Axis,State,AdditionalStateInfo)


def BnR_StageNotify(Stage:str="", State:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notify the listener that the stage status has changed.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        State:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_StageNotify",Stage,State)


def BnR_InputNotify(Channel:str="", State:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notify the listener that the state of an input channel has changed.
    API Status: internal
    Args:
        Channel:str = "0"
        State:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_InputNotify",Channel,State)


def BnR_OutputNotify(Channel:str="", State:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notify the listener that the state of an output channel has changed.
    API Status: internal
    Args:
        Channel:str = "0"
        State:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_OutputNotify",Channel,State)


def BnR_AxisStatusNotify(Stage:str="", Axis:str="", Initialized:int="", PositiveLimit:int="", NegativeLimit:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifys the listener that an axis status has changed. Currently used to notify
    the Kernel about the init state of a BnR axis.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
        Initialized:int = 0
        PositiveLimit:int = 0
        NegativeLimit:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_AxisStatusNotify",Stage,Axis,Initialized,PositiveLimit,NegativeLimit)


def AutoXYModeChange(AutoXYModeOn:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sent by Spectrum if Automation was enabled or disabled. This can be AutoXY,
    AutoZ or VueTrack. Handled by WaferMap to ensure that automation is executed
    when stepping.
    API Status: internal
    Args:
        AutoXYModeOn:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("AutoXYModeChange",AutoXYModeOn)


def ZoomLevelChange(ZoomLevel:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sent by OpticalControl when the AZoom zoom level is changed. Spectrum should
    handle this so it doesn't have to poll OpticalControl for the current zoom
    level.
    API Status: internal
    Args:
        ZoomLevel:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("ZoomLevelChange",ZoomLevel)


def BnR_AnalogIONotify(AnalogIO:str="", ValuePercent:Decimal="", UnderOverflow:int="", Error:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notify the listener that the state or value of an analog input or output channel
    has changed.
    API Status: internal
    Args:
        AnalogIO:str = "AO_PurgeDewPoint"
        ValuePercent:Decimal = 0
        UnderOverflow:int = 0
        Error:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_AnalogIONotify",AnalogIO,ValuePercent,UnderOverflow,Error)


def BnR_ControllerInfoNotify(ControllerNum:int="", ControllerInfo:str="", Value:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notifies the listener about changed controller info. Currently used to inform
    Toolbar about the battery state of the BnR controller.
    API Status: internal
    Args:
        ControllerNum:int = 1
        ControllerInfo:str = "BatteryOK"
        Value:Decimal = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_ControllerInfoNotify",ControllerNum,ControllerInfo,Value)


def BnR_PositionNotify(Stage:str="", XorT:Decimal="", Y:Decimal="", Z:Decimal="", CommandedXorT:Decimal="", CommandedY:Decimal="", CommandedZ:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notification is sent by BnR controller if a axis position has changed. Currently
    used to notify the Kernel about the new axis position.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        XorT:Decimal = 0
        Y:Decimal = 0
        Z:Decimal = 0
        CommandedXorT:Decimal = 0
        CommandedY:Decimal = 0
        CommandedZ:Decimal = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_PositionNotify",Stage,XorT,Y,Z,CommandedXorT,CommandedY,CommandedZ)


def BnR_InfoNotify(InfoType:str="", Info:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Generic Information Notification
    API Status: internal
    Args:
        InfoType:str = ""
        Info:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("BnR_InfoNotify",InfoType,Info)


def WMNewCurrentDie(DieX:int="", DieY:int="", XFromHome:Decimal="", YFromHome:Decimal="", CurSite:int="", LastSiteIndex:int=""):
    """
    Alerts applications that WaferMap has a new position.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
        XFromHome:Decimal = 0
        YFromHome:Decimal = 0
        CurSite:int = 1
        LastSiteIndex:int = 1
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("WMNewCurrentDie",DieX,DieY,XFromHome,YFromHome,CurSite,LastSiteIndex)


def WMSetupChange():
    """
    Alerts applications that a wafer's parameters have been changed.
    API Status: published
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("WMSetupChange")


def ButtonPress(TargetIdent:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sent when button instrumented for guided workflow is pressed. The TargetIdent is
    the identifier for the button as defined for the guided workflow.
    API Status: internal
    Args:
        TargetIdent:int = 0
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("ButtonPress",TargetIdent)


def CryoCmdReady(State:str="", Error:int="", ErrorDescription:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sent when the cooling or heating process was terminated successfully or
    incorrectly. Returns the status with which the process was finished (IDLE, COLD,
    COOL DOWN, WARMUP) and sends the error code and error message.
    API Status: internal
    Args:
        State:str = "IDLE"
        Error:int = 0
        ErrorDescription:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("CryoCmdReady",State,Error,ErrorDescription)


def VMProjectLoaded():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notification sent when Spectrum VS project has finished loading.
    API Status: internal
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("VMProjectLoaded")


def VMProbeCardData(Access:str="", FileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notification is sent when a probe card file is loaded.
    API Status: internal
    Args:
        Access:str = "L"
        FileName:str = ""
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("VMProbeCardData",Access,FileName)


def TTLTestDone():
    """
    Alerts applications that the TTL Test is ready.
    API Status: published
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("TTLTestDone")


def PSStateChanged(State:str="", SubState:str="", Message:str="", Error:int=""):
    """
    Notification sent when VeloxPro changes its running state.
    API Status: published
    Args:
        State:str = "Unknown"
        SubState:str = "Unknown"
        Message:str = ""
        Error:int = 0
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("PSStateChanged",State,SubState,Message,Error)


def PSProgressChanged(ProgressPercent:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notification sent during wafer stepping process. It updates the progress
    information. 'Progress' is the relationship of dies tested to dies to be tested.
    API Status: internal
    Args:
        ProgressPercent:Decimal = 0
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("PSProgressChanged",ProgressPercent)


def PSLoaderUsage(UseLoader:int="", UseAutoWafer:int="", WaferSizes:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notification is sent to notify the listener about usage of Loader, usage of
    fully/semiautomatic mode and supported wafer sizes of process station.
    API Status: internal
    Args:
        UseLoader:int = 0
        UseAutoWafer:int = 0
        WaferSizes:str = ""
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("PSLoaderUsage",UseLoader,UseAutoWafer,WaferSizes)


def LoaderMessage(Message:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Notification is sent by loader to display a message on the process station.
    API Status: internal
    Args:
        Message:str = ""
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("LoaderMessage",Message)


def OpenProjectDialog(ProjectFilename:str="", Option:int=""):
    """
    Asks if the current project should be saved and then brings up the Open Project
    window which opens the selected project file if the user clicks ok.
    API Status: published
    Args:
        ProjectFilename:str = ""
        Option:int = 0
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("OpenProjectDialog",ProjectFilename,Option)


def SaveProjectAsDialog():
    """
    Brings up the Save Project window which saves the project if the user clicks ok.
    API Status: published
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("SaveProjectAsDialog")


def LoginDialog(LevelToOffer:str=""):
    """
    Brings up the Login window and sends a New Access Level alert if the user enters
    a valid password.
    API Status: published
    Args:
        LevelToOffer:str = "1"
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("LoginDialog",LevelToOffer)


def GetStatus():
    """
    Returns the current software status. The server holds and maintains the software
    status. Status can be changed by using any of the following commands:
    BeginProbing, LoginDialog, AbortProbing, SetExternalMode, PauseProbing,
    UnloadWafer, ResumeProbing
    API Status: published
    Returns:
        DummyCommonMode:int
        RunningMode:str
        AccessLevel:str
        ExternalMode:int
        LicenseDaysLeft:int
        MKH:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetStatus")
    global GetStatus_Response
    if not "GetStatus_Response" in globals(): GetStatus_Response = namedtuple("GetStatus_Response", "DummyCommonMode,RunningMode,AccessLevel,ExternalMode,LicenseDaysLeft,MKH")
    return GetStatus_Response(int(rsp[0]),str(rsp[1]),str(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]))

def LicensingDialog():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Brings up the Licensing window.
    API Status: internal
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("LicensingDialog")


def GetLicenseInfo():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current license information.
    API Status: internal
    Returns:
        AnnualEnabled:int
        AnnualDaysLeft:int
        VeloxProEnabled:int
        VueTrackEnabled:int
        VueTrack4PEnabled:int
        ReAlignEnabled:int
        AutomationEnabled:int
        IdToolsEnabled:int
        IVistaEnabled:int
        IVistaProEnabled:int
        LaserCutterEnabled:int
        SiPToolsEnabled:int
        AutoRfEnabled:int
        SecsGemEnabled:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetLicenseInfo")
    global GetLicenseInfo_Response
    if not "GetLicenseInfo_Response" in globals(): GetLicenseInfo_Response = namedtuple("GetLicenseInfo_Response", "AnnualEnabled,AnnualDaysLeft,VeloxProEnabled,VueTrackEnabled,VueTrack4PEnabled,ReAlignEnabled,AutomationEnabled,IdToolsEnabled,IVistaEnabled,IVistaProEnabled,LaserCutterEnabled,SiPToolsEnabled,AutoRfEnabled,SecsGemEnabled")
    return GetLicenseInfo_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]),int(rsp[10]),int(rsp[11]),int(rsp[12]),int(rsp[13]))

def GetProjectFile():
    """
    Returns the current project file.
    API Status: published
    Returns:
        ProjectFilename:str
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetProjectFile")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ReportSoftwareVersion():
    """
    Returns the Velox software version as string.
    API Status: published
    Returns:
        SoftwareVersion:str
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("ReportSoftwareVersion")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def OpenProject(ProjectFilename:str=""):
    """
    The OpenProject command opens the specified project.
    API Status: published
    Args:
        ProjectFilename:str = ""
    Command Timeout: 15000
    """
    MessageServerInterface.sendSciCommand("OpenProject",ProjectFilename)


def IsAppRegistered(Application:str=""):
    """
    Checks the server to see if the application "AppName" is registered with the
    server.
    API Status: published
    Args:
        Application:str = ""
    Returns:
        IsAppRegistered:int
    Command Timeout: 5000
    Example:IsAppRegistered WaferMap
    """
    rsp = MessageServerInterface.sendSciCommand("IsAppRegistered",Application)
    return int(rsp[0])

def SaveProject(ProjectFilename:str=""):
    """
    Saves the current data to the project file.
    API Status: published
    Args:
        ProjectFilename:str = ""
    Command Timeout: 15000
    """
    MessageServerInterface.sendSciCommand("SaveProject",ProjectFilename)


def GetSoftwarePath(PathType:str=""):
    """
    Returns the path for either the applications/data or project files.
    API Status: published
    Args:
        PathType:str = "User"
    Returns:
        SoftwarePath:str
    Command Timeout: 5000
    Example:GetSoftwarePath User
    """
    rsp = MessageServerInterface.sendSciCommand("GetSoftwarePath",PathType)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def CCSelectLens(Lens:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Internal AZoom Helper Command.
    API Status: internal
    Args:
        Lens:int = 1
    Command Timeout: 10000
    Example:CCSelectLens 1
    """
    MessageServerInterface.sendSciCommand("CCSelectLens",Lens)


def CCReadCurrentLens():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Internal AZoom Helper Command. Probably no longer used.
    API Status: internal
    Returns:
        Lens:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("CCReadCurrentLens")
    return int(rsp[0])

def CCMoveAuxSite(AuxID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command calls the Kernel command MoveAuxSite to move the chuck to the
    position of a given AUX site. For the transfer move a safe height is used. If
    AUX ID is set to 0, the target of the move is the wafer site. If the flag 'Auto
    Align by Spectrum' in ControlCenter-SystemSetup-Aux Sites is True, the Spectrum
    command AlignAux is executed after MoveAuxSite to align the site automatically.
    The flag is only visible, if the aux site type is CalSubstrate and Spectrum is
    installed. AUX ID in the response is the ID of the new active site.
    API Status: internal
    Args:
        AuxID:int = 1
    Command Timeout: 200000
    """
    MessageServerInterface.sendSciCommand("CCMoveAuxSite",AuxID)


def ExecuteCleaningSequence(SequenceName:str="", AllowMediaReuse:int="", SkipAlignAux:int="", SkipReturnMove:int=""):
    """
    This command moves to the single cleaning site, executes CleanProbeTip, moves to
    the contact verify site, and then moves to contact. Returns an error if the
    clean or verify sites aren't defined.
    API Status: published
    Args:
        SequenceName:str = ""
        AllowMediaReuse:int = 0
        SkipAlignAux:int = 0
        SkipReturnMove:int = 0
    Command Timeout: 1800000
    Example:ExecuteCleaningSequence "DeepClean"
    """
    MessageServerInterface.sendSciCommand("ExecuteCleaningSequence",SequenceName,AllowMediaReuse,SkipAlignAux,SkipReturnMove)


def GetAlignmentMode():
    """
    Get the active alignment mode (either on axis or off axis).
    API Status: published
    Returns:
        AlignmentMode:str
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetAlignmentMode")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetAlignmentMode(AlignmentMode:str=""):
    """
    Sets the active alignment mode (either on axis or off axis).
    API Status: published
    Args:
        AlignmentMode:str = "OnAxis"
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("SetAlignmentMode",AlignmentMode)


def GetLoginData(CmdUserName:str=""):
    """
    Gets the Velox user data: name, full name, group, access level.     If the
    commanded user name is empty, the data of the current user will be responded
    API Status: published
    Args:
        CmdUserName:str = ""
    Returns:
        UserName:str
        LongUserName:str
        UserGroup:str
        AccessLevel:str
        VeloxLocked:int
    Command Timeout: 5000
    Example:GetLoginData
    """
    rsp = MessageServerInterface.sendSciCommand("GetLoginData",CmdUserName)
    global GetLoginData_Response
    if not "GetLoginData_Response" in globals(): GetLoginData_Response = namedtuple("GetLoginData_Response", "UserName,LongUserName,UserGroup,AccessLevel,VeloxLocked")
    return GetLoginData_Response(str(rsp[0]),str(rsp[1]),str(rsp[2]),str(rsp[3]),int(rsp[4]))

def NucleusInitChuck():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Brings up message box to warn user of chuck initialization for Nucleus stations.
    Allows user to OK/Cancel.
    API Status: internal
    Command Timeout: 1000
    """
    MessageServerInterface.sendSciCommand("NucleusInitChuck")


def ShutdownVeloxWithSave():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Brings up message box to allow saving project before shutting down Velox. Allows
    user to OK/Cancel.
    API Status: internal
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("ShutdownVeloxWithSave")


def WinCalAutoCal():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalAutoCal command to WinCal.
    API Status: internal
    Command Timeout: 300000
    """
    MessageServerInterface.sendSciCommand("WinCalAutoCal")


def WinCalCheckAutoRFStability(AllowMove:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalCheckAutoRFStability command to WinCal.
    API Status: internal
    Args:
        AllowMove:int = 0
    Returns:
        StabilityPassed:int
    Command Timeout: 300000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalCheckAutoRFStability",AllowMove)
    return int(rsp[0])

def WinCalCloseRFStabilityReport():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalCloseRFStabilityReport command to WinCal.
    API Status: internal
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("WinCalCloseRFStabilityReport")


def WinCalMoveToIssRef(IssIdx:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalMoveToIssRef command to WinCal to move to the specified ISS
    reference.     The ISS index is the IssIdxMap index as returned from
    WinCalGetIssListForAuxSite.
    API Status: internal
    Args:
        IssIdx:int = 0
    Command Timeout: 60000
    """
    MessageServerInterface.sendSciCommand("WinCalMoveToIssRef",IssIdx)


def WinCalVerifyIssRefLocAtHome(IssIdx:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalVerifyIssRefLocAtHome command to WinCal and returns AllRefAtHome
    as 1 if stage and positioners at home.
    API Status: internal
    Args:
        IssIdx:int = 0
    Returns:
        AllRefAtHome:int
    Command Timeout: 60000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalVerifyIssRefLocAtHome",IssIdx)
    return int(rsp[0])

def WinCalGetIssForAuxSite(AuxID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalGetIssForAuxSite command to WinCal and returns the ISS
    information for the given aux site ID.
    API Status: internal
    Args:
        AuxID:int = 0
    Returns:
        IssIdx:int
        IssPN:str
        IssDescription:str
        IssEnabled:int
        AuxSiteName:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetIssForAuxSite",AuxID)
    global WinCalGetIssForAuxSite_Response
    if not "WinCalGetIssForAuxSite_Response" in globals(): WinCalGetIssForAuxSite_Response = namedtuple("WinCalGetIssForAuxSite_Response", "IssIdx,IssPN,IssDescription,IssEnabled,AuxSiteName")
    return WinCalGetIssForAuxSite_Response(int(rsp[0]),str(rsp[1]),str(rsp[2]),int(rsp[3]),str("" if len(rsp) < 5 else ' '.join(rsp[4:])))

def WinCalGetNameAndVersion():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalGetNameAndVersion command to WinCal.
    API Status: internal
    Returns:
        ServerName:str
        Version:str
        MajorVersion:int
        MinorVersion:int
        Revision:int
        Build:int
    Command Timeout: 30000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetNameAndVersion")
    global WinCalGetNameAndVersion_Response
    if not "WinCalGetNameAndVersion_Response" in globals(): WinCalGetNameAndVersion_Response = namedtuple("WinCalGetNameAndVersion_Response", "ServerName,Version,MajorVersion,MinorVersion,Revision,Build")
    return WinCalGetNameAndVersion_Response(str(rsp[0]),str(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]))

def WinCalMonitorNoMove():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalMonitorNoMove command to WinCal. Triggers WinCal to measure the
    monitor portion of the current calibration setup.
    API Status: internal
    Returns:
        MonitorPassed:int
    Command Timeout: 300000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalMonitorNoMove")
    return int(rsp[0])

def WinCalValidateAdvanced(ProbeSpacing:Decimal="", ResetTrace:int="", AllowMove:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalValidateAdvanced command to WinCal. Performs the validation step of
    the currently selected calibration setup.     Resets the model used in WinCal
    for validataion.
    API Status: internal
    Args:
        ProbeSpacing:Decimal = 130
        ResetTrace:int = 1
        AllowMove:int = 1
    Returns:
        ValidationPassed:int
    Command Timeout: 300000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalValidateAdvanced",ProbeSpacing,ResetTrace,AllowMove)
    return int(rsp[0])

def WinCalMeasureMonitorReference(AllowMove:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalMeasureMonitorReference command to WinCal.
    API Status: internal
    Args:
        AllowMove:int = 0
    Command Timeout: 300000
    """
    MessageServerInterface.sendSciCommand("WinCalMeasureMonitorReference",AllowMove)


def WinCalGetNumValidationPorts():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalGetNumValidationPorts command to WinCal.
    API Status: internal
    Returns:
        NumValidationPorts:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetNumValidationPorts")
    return int(rsp[0])

def WinCalSetNumValidationPorts(NumValidationPorts:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalSetNumValidationPorts command to WinCal.
    API Status: internal
    Args:
        NumValidationPorts:int = 2
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("WinCalSetNumValidationPorts",NumValidationPorts)


def WinCalGetNumMonitoringPorts():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalGetNumMonitoringPorts command to WinCal.
    API Status: internal
    Returns:
        NumMonitoringPorts:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetNumMonitoringPorts")
    return int(rsp[0])

def WinCalSetNumMonitoringPorts(NumMonitoringPorts:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalSetNumMonitoringPorts command to WinCal.
    API Status: internal
    Args:
        NumMonitoringPorts:int = 2
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("WinCalSetNumMonitoringPorts",NumMonitoringPorts)


def WinCalGetNumRepeatabilityPorts():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalGetNumRepeatabilityPorts command to WinCal.
    API Status: internal
    Returns:
        NumRepeatabilityPorts:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetNumRepeatabilityPorts")
    return int(rsp[0])

def WinCalSetNumRepeatabilityPorts(NumRepeatabilityPorts:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalSetNumRepeatabilityPorts command to WinCal.
    API Status: internal
    Args:
        NumRepeatabilityPorts:int = 2
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("WinCalSetNumRepeatabilityPorts",NumRepeatabilityPorts)


def WinCalValidate():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalValidate command to WinCal. Performs the validation step of the
    currently selected calibration setup in WinCal.
    API Status: internal
    Returns:
        ValidationPassed:int
    Command Timeout: 300000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalValidate")
    return int(rsp[0])

def WinCalGetValidationSetup(Port:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends CalGetValidationSetup command to WinCal. Returns calibration setup
    parameters.
    API Status: internal
    Args:
        Port:int = 1
    Returns:
        StandardType:str
        StandardPorts:int
        StandardCompareType:int
        StructureType:str
        PostCorrect:int
        PostCorrectMatching:int
        AutoConfigure:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetValidationSetup",Port)
    global WinCalGetValidationSetup_Response
    if not "WinCalGetValidationSetup_Response" in globals(): WinCalGetValidationSetup_Response = namedtuple("WinCalGetValidationSetup_Response", "StandardType,StandardPorts,StandardCompareType,StructureType,PostCorrect,PostCorrectMatching,AutoConfigure")
    return WinCalGetValidationSetup_Response(str(rsp[0]),int(rsp[1]),int(rsp[2]),str(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]))

def WinCalAutoCalNoValidation(ProbeSpacing:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalAutoCalNoValidation command to WinCal. Performs an AutoCal
    without the validation step
    API Status: internal
    Args:
        ProbeSpacing:Decimal = 130
    Command Timeout: 300000
    """
    MessageServerInterface.sendSciCommand("WinCalAutoCalNoValidation",ProbeSpacing)


def WinCalHideAllWindows():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalHideAllWindows command to WinCal. This minimizes all the WinCal
    windows
    API Status: internal
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("WinCalHideAllWindows")


def WinCalGetReferenceStructureInfo(IssIdx:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalGetReferenceStructureInfo command to WinCal. Given the WinCal ISS
    index it will return a string with the reference information
    API Status: internal
    Args:
        IssIdx:int = 0
    Returns:
        ReferenceInfo:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetReferenceStructureInfo",IssIdx)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def WinCalSystemSetupHasUnappliedChanges(ShowErrors:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalSystemSetupHasUnappliedChanges command to WinCal. Returns true
    if WinCal has unapplied changes
    API Status: internal
    Args:
        ShowErrors:int = 0
    Returns:
        HasUnappliedChanges:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalSystemSetupHasUnappliedChanges",ShowErrors)
    return int(rsp[0])

def WinCalRecordIssRefAtCurrentLoc(IssIdx:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the CalRecordIssRefAtCurrentLoc command to WinCal. Record the ISS,
    indicated by the index, reference as being the current location
    API Status: internal
    Args:
        IssIdx:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("WinCalRecordIssRefAtCurrentLoc",IssIdx)


def SaveProjectAsTemplateDialog():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Brings up the Save Project as Template window which saves the project template
    if the user clicks ok.
    API Status: internal
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("SaveProjectAsTemplateDialog")


def CreateProjectFromTemplateDialog():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Brings up the New Project from Template dialog which allows the user to select a
    template and create a new project.
    API Status: internal
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("CreateProjectFromTemplateDialog")


def WinCalGetNumPortsAndProbes():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns Max Ports and Number of probes connected to a port
    API Status: internal
    Returns:
        MaxPorts:int
        NumPortsConnectedtoProbes:int
    Command Timeout: 1000
    Example:WinCalGetNumPortsAndProbes
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetNumPortsAndProbes")
    global WinCalGetNumPortsAndProbes_Response
    if not "WinCalGetNumPortsAndProbes_Response" in globals(): WinCalGetNumPortsAndProbes_Response = namedtuple("WinCalGetNumPortsAndProbes_Response", "MaxPorts,NumPortsConnectedtoProbes")
    return WinCalGetNumPortsAndProbes_Response(int(rsp[0]),int(rsp[1]))

def WinCalGetProbeInfoForPort(VnaPortNum:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the properties from one probe, based on the passed in index. Pass in a
    physical VNA port number that is less than or equal to Max Probes from the call
    to CalGetNumPortsAndProbes
    API Status: internal
    Args:
        VnaPortNum:int = 1
    Returns:
        IsSelected:int
        BaseProbe:str
        Options:str
        PhysicalOrient:str
        IsDual:int
        IsSymmetric:int
        SignalConfig:str
        SelectedPitch:int
    Command Timeout: 1000
    Example:WinCalGetProbeInfoForPort 1
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalGetProbeInfoForPort",VnaPortNum)
    global WinCalGetProbeInfoForPort_Response
    if not "WinCalGetProbeInfoForPort_Response" in globals(): WinCalGetProbeInfoForPort_Response = namedtuple("WinCalGetProbeInfoForPort_Response", "IsSelected,BaseProbe,Options,PhysicalOrient,IsDual,IsSymmetric,SignalConfig,SelectedPitch")
    return WinCalGetProbeInfoForPort_Response(int(rsp[0]),str(rsp[1]),str(rsp[2]),str(rsp[3]),int(rsp[4]),int(rsp[5]),str(rsp[6]),int(rsp[7]))

def GetMachineState():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the current state of the machine.
    API Status: internal
    Returns:
        MachineState:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetMachineState")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ShowAboutDialog(Pid:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Shows the help about dialog for the given application
    API Status: internal
    Args:
        Pid:int = -1
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("ShowAboutDialog",Pid)


def ShowSplashScreen(Pid:int="", TimeoutMs:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Shows the splash screen for the given application
    API Status: internal
    Args:
        Pid:int = -1
        TimeoutMs:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("ShowSplashScreen",Pid,TimeoutMs)


def CloseSplashScreen(Pid:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Closes the splash screen for the given application
    API Status: internal
    Args:
        Pid:int = -1
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("CloseSplashScreen",Pid)


def GetLastFourProjects():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the last four project files that were opened.
    API Status: internal
    Returns:
        ProjectFile1:str
        ProjectFile2:str
        ProjectFile3:str
        ProjectFile4:str
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetLastFourProjects")
    global GetLastFourProjects_Response
    if not "GetLastFourProjects_Response" in globals(): GetLastFourProjects_Response = namedtuple("GetLastFourProjects_Response", "ProjectFile1,ProjectFile2,ProjectFile3,ProjectFile4")
    return GetLastFourProjects_Response(str(rsp[0]),str(rsp[1]),str(rsp[2]),str("" if len(rsp) < 4 else ' '.join(rsp[3:])))

def WinCalExecuteCommand(Command:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends the WinCalExecuteCommand command to WinCal and returns the response
    string.
    API Status: internal
    Args:
        Command:str = ""
    Returns:
        Response:str
    Command Timeout: 300000
    """
    rsp = MessageServerInterface.sendSciCommand("WinCalExecuteCommand",Command)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetDemoMode(TurnOnDemoMode:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The DemoMode is not supported anymore. Use ChangeDemoRsp to install a demo mode.
    This command will return an error if its called with any other parameter as 0.
    API Status: internal
    Args:
        TurnOnDemoMode:int = 1
    Command Timeout: 5000
    Example:SetDemoMode 0
    """
    MessageServerInterface.sendSciCommand("SetDemoMode",TurnOnDemoMode)


def ChangeDemoRsp(Param:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Override a command with a demo response. The command will not reach its
    destination but the supplied demo response will be returned. An active overide
    for a command will be removed if the provided timeout is negative. Format:  [ID]
    [Time] [ErrorCode]:[Response]  - Id: command id in hex withoud leding 0x - Time:
    time in ms between command and response, negativ to reset demo mode for this
    command - Errorcode: 0 for success, everything else indicates an error -
    Response: response string
    API Status: internal
    Args:
        Param:str = ""
    Command Timeout: 5000
    Example:ChangeDemoRsp 31 200 0:5000.0 5000.0 8500
    """
    MessageServerInterface.sendSciCommand("ChangeDemoRsp",Param)


def GetDemoMode():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The DemoMode is not supported anymore. Use ChangeDemoRsp to install a demo mode.
    This command will always return 0.
    API Status: internal
    Returns:
        DemoModeOn:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDemoMode")
    return int(rsp[0])

def ResetNetworkPort(Param:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    (Re)sets the IP address and listen port of the socket to which the NetworkDriver
    tries to connect to (IP address and listen port of Kernel socket). Dummy
    implementation for Kernel to support backwards.
    API Status: internal
    Args:
        Param:str = ""
    Command Timeout: 10000
    Example:ResetNetworkPort 192.168.3.1 10000
    """
    MessageServerInterface.sendSciCommand("ResetNetworkPort",Param)


def GetNDriverClientStatus(ClientNum:int="", Param:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets status information about the connection NetworkDriver to Kernel. Socket
    Error is the Windows socket error, Description the Windows socket error
    description. If Socket Error is 0, the description 'Registered' informs that the
    Kernel is ready to receive Remote Commands.
    API Status: internal
    Args:
        ClientNum:int = 1
        Param:str = ""
    Returns:
        Response:str
    Command Timeout: 5000
    Example:GetNDriverClientStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetNDriverClientStatus",ClientNum,Param)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def OverrideCommandTimeout(CmdID:int="", TimeoutMilliSec:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command allows specifying a separate command timeout for a single instance
    of a command. This is especially useful if the application that receives a
    command knows how long a command will take.  This command had been added for
    SoakTime-handling of StepNextDie. A safe guess for the timeout of StepNextDie is
    5s.
    API Status: internal
    Args:
        CmdID:int = 0
        TimeoutMilliSec:int = 1000
    Command Timeout: 5000
    Example:OverrideCommandTimeout 3234 20000
    """
    MessageServerInterface.sendSciCommand("OverrideCommandTimeout",CmdID,TimeoutMilliSec)


def ShutdownVelox(IgnorePID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Shutdown all Velox applications in an ordered fashion. When this command returns
    success, all non-mandatory apps are closed and the mandatory ones will follow
    shortly
    API Status: internal
    Args:
        IgnorePID:int = 0
    Command Timeout: 120000
    Example:ShutdownVelox
    """
    MessageServerInterface.sendSciCommand("ShutdownVelox",IgnorePID)


def InitializationDone(CommandGroup:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Registration of an application can be delayed. To trigger this behavior,
    RegisterProberApp has to be called with flag 3 set (0x04). From
    RegisterProberApp to the time this command is sent, the application can send
    commands but can't receive commands. This is necessary because some application
    have to communicate with others during initialization and can not handle
    commands properly during this time.  The command group is necessary because of
    architectural reasons (By design, the command receiver does not now the sender
    of a command).
    API Status: internal
    Args:
        CommandGroup:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("InitializationDone",CommandGroup)


def StepFirstZProfilePoint(XPos:Decimal="", YPos:Decimal="", NumberOfPoints:int="", NumberOfEPoints:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command goes to the first Z Profile Point, adjusts Z (in the automatic mode
    only) and pauses after it (even in the automatic mode)
    API Status: internal
    Args:
        XPos:Decimal = 0
        YPos:Decimal = 0
        NumberOfPoints:int = 0
        NumberOfEPoints:int = 0
    Command Timeout: 60000
    Example:StepFirstZProfilePoint 10000 20000 5 5
    """
    MessageServerInterface.sendSciCommand("StepFirstZProfilePoint",XPos,YPos,NumberOfPoints,NumberOfEPoints)


def StepNextZProfilePoint(Point:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command calculates a delta value for the current point and then moves to
    the specified point (if it's presented) or to the next one. Note, that in case
    of the automatic Z detecting a return ZDelta parameter is a value for the
    current point, but in case of the semiautomatic mode the command returns ZDelta
    as a value for a previous tested point. If the profiling is finished this
    command will return #807 error (End of the profile). Point indices are started
    from 1 (1 is first, 2 is second, and so on).
    API Status: internal
    Args:
        Point:int = 0
    Returns:
        XPos:Decimal
        YPos:Decimal
        Delta:Decimal
        CurPoint:int
        NumberOfPoints:int
        NumberOfEPoints:int
    Command Timeout: 60000
    Example:StepNextZProfilePoint 1
    """
    rsp = MessageServerInterface.sendSciCommand("StepNextZProfilePoint",Point)
    global StepNextZProfilePoint_Response
    if not "StepNextZProfilePoint_Response" in globals(): StepNextZProfilePoint_Response = namedtuple("StepNextZProfilePoint_Response", "XPos,YPos,Delta,CurPoint,NumberOfPoints,NumberOfEPoints")
    return StepNextZProfilePoint_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]))

def SetZProfileOptions(ProfileMode:str="", SepSpeed:Decimal="", ProfileSensor:str="", Stage:str="", SearchSpeed:Decimal="", Gap:Decimal="", Units:str="", ClearElectronics:int="", ClearRefZ:int="", Inaccuracy:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets some Z Profile Program Options remotely.
    API Status: internal
    Args:
        ProfileMode:str = "S"
        SepSpeed:Decimal = 25
        ProfileSensor:str = "E"
        Stage:str = "C"
        SearchSpeed:Decimal = 50
        Gap:Decimal = 10
        Units:str = "Y"
        ClearElectronics:int = 1
        ClearRefZ:int = 1
        Inaccuracy:Decimal = 0
    Command Timeout: 10000
    Example:SetZProfileOptions S 25 E C 50 10 Y 1 1 0
    """
    MessageServerInterface.sendSciCommand("SetZProfileOptions",ProfileMode,SepSpeed,ProfileSensor,Stage,SearchSpeed,Gap,Units,ClearElectronics,ClearRefZ,Inaccuracy)


def GetZProfileOptions():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Return predefined settings of the Z Profile Program.
    API Status: internal
    Returns:
        ProfileMode:str
        SepSpeed:Decimal
        ProfileSensor:str
        Stage:str
        SearchSpeed:Decimal
        Gap:Decimal
        Units:str
        ClearElectronics:int
        ClearRefZ:int
        Inaccuracy:Decimal
    Command Timeout: 10000
    Example:GetZProfileOptions
    """
    rsp = MessageServerInterface.sendSciCommand("GetZProfileOptions")
    global GetZProfileOptions_Response
    if not "GetZProfileOptions_Response" in globals(): GetZProfileOptions_Response = namedtuple("GetZProfileOptions_Response", "ProfileMode,SepSpeed,ProfileSensor,Stage,SearchSpeed,Gap,Units,ClearElectronics,ClearRefZ,Inaccuracy")
    return GetZProfileOptions_Response(str(rsp[0]),Decimal(rsp[1]),str(rsp[2]),str(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]),str(rsp[6]),int(rsp[7]),int(rsp[8]),Decimal(rsp[9]))

def OpenZProfileFile(FileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command opens the file inside of the Z Profiling.
    API Status: internal
    Args:
        FileName:str = ""
    Returns:
        NumberOfPoints:int
        NumberOfEPoints:int
    Command Timeout: 240000
    Example:OpenZProfileFile Profile1
    """
    rsp = MessageServerInterface.sendSciCommand("OpenZProfileFile",FileName)
    global OpenZProfileFile_Response
    if not "OpenZProfileFile_Response" in globals(): OpenZProfileFile_Response = namedtuple("OpenZProfileFile_Response", "NumberOfPoints,NumberOfEPoints")
    return OpenZProfileFile_Response(int(rsp[0]),int(rsp[1]))

def SaveZProfileFile(FileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Saves the current profile in the specified file.
    API Status: internal
    Args:
        FileName:str = ""
    Returns:
        NumberOfPoints:int
        NumberOfEPoints:int
    Command Timeout: 10000
    Example:SaveZProfileFile Profile1
    """
    rsp = MessageServerInterface.sendSciCommand("SaveZProfileFile",FileName)
    global SaveZProfileFile_Response
    if not "SaveZProfileFile_Response" in globals(): SaveZProfileFile_Response = namedtuple("SaveZProfileFile_Response", "NumberOfPoints,NumberOfEPoints")
    return SaveZProfileFile_Response(int(rsp[0]),int(rsp[1]))

def ReadZProfile(NewOrigin:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Read a profile from the ProberBench Electronics II to the application. Return a
    number of available points.
    API Status: internal
    Args:
        NewOrigin:str = "Z"
    Returns:
        NumberOfPoints:int
    Command Timeout: 10000
    Example:ReadZProfile H
    """
    rsp = MessageServerInterface.sendSciCommand("ReadZProfile",NewOrigin)
    return int(rsp[0])

def SetZProfile():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Uploads the current profile to the ProberBench Electronics II. Returns a number
    of written points.
    API Status: internal
    Returns:
        NumberOfPoints:int
    Command Timeout: 10000
    Example:SetZProfile
    """
    rsp = MessageServerInterface.sendSciCommand("SetZProfile")
    return int(rsp[0])

def CloseZProfiling():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Closes the Z-Profiling application.
    API Status: internal
    Command Timeout: 5000
    Example:CloseZProfiling
    """
    MessageServerInterface.sendSciCommand("CloseZProfiling")


def SetZProfileStartPoint(X:Decimal="", Y:Decimal="", PosRef:str="", Units:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets new start point for the profile. All points of the profile will be shifted
    accordingly.
    API Status: internal
    Args:
        X:Decimal = 0
        Y:Decimal = 0
        PosRef:str = "Z"
        Units:str = "Y"
    Command Timeout: 10000
    Example:SetZProfileStartPoint 0 0 H Y
    """
    MessageServerInterface.sendSciCommand("SetZProfileStartPoint",X,Y,PosRef,Units)


def GetZProfilingStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns a status of the profiling process. If this status is true it means the
    process is started.
    API Status: internal
    Returns:
        Started:int
    Command Timeout: 10000
    Example:GetZProfilingStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetZProfilingStatus")
    return int(rsp[0])

def StopZProfiling():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Stops the profiling process.
    API Status: internal
    Command Timeout: 10000
    Example:StopZProfiling
    """
    MessageServerInterface.sendSciCommand("StopZProfiling")


def SetZProfileOrigin(Pos:str="", X:Decimal="", Y:Decimal="", Z:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets an origin for the profile. If the origin position is H the command ignores
    X and Y parameters. If Z is None the command clears Z value of the origin.
    Otherwise it tries to extract a double value from the string and set it.
    API Status: internal
    Args:
        Pos:str = "H"
        X:Decimal = 0
        Y:Decimal = 0
        Z:str = "None"
    Command Timeout: 10000
    Example:SetZProfileOrigin H 0 0 None
    """
    MessageServerInterface.sendSciCommand("SetZProfileOrigin",Pos,X,Y,Z)


def GetZProfileOrigin():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the current parameters of the profile origin. If the origin Z has no value
    the return string for it will be None, otherwise it consists a double value of
    the profile Z.
    API Status: internal
    Returns:
        Pos:str
        X:Decimal
        Y:Decimal
        Z:str
    Command Timeout: 10000
    Example:GetZProfileOrigin
    """
    rsp = MessageServerInterface.sendSciCommand("GetZProfileOrigin")
    global GetZProfileOrigin_Response
    if not "GetZProfileOrigin_Response" in globals(): GetZProfileOrigin_Response = namedtuple("GetZProfileOrigin_Response", "Pos,X,Y,Z")
    return GetZProfileOrigin_Response(str(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),str("" if len(rsp) < 4 else ' '.join(rsp[3:])))

def StartZProfiling():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command works in the automatic mode only. It starts the profiling process,
    profiles the entire wafer and then returns a number of tested points. This
    command does upload the current profile to the ProberBench Electronics II. To do
    it please use SetZProfile command
    API Status: internal
    Command Timeout: 10000
    Example:StartZProfiling
    """
    MessageServerInterface.sendSciCommand("StartZProfiling")


def ZProfileWafer():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command works in the automatic mode only. It starts the profiling process,
    profiles the entire wafer and then returns a number of tested points. This
    command does upload the current profile to the ProberBench Electronics II. To do
    it please use SetZProfile command
    API Status: internal
    Returns:
        NumberOfPoints:int
        NumberOfEPoints:int
    Command Timeout: 36000000
    Example:ZProfileWafer
    """
    rsp = MessageServerInterface.sendSciCommand("ZProfileWafer")
    global ZProfileWafer_Response
    if not "ZProfileWafer_Response" in globals(): ZProfileWafer_Response = namedtuple("ZProfileWafer_Response", "NumberOfPoints,NumberOfEPoints")
    return ZProfileWafer_Response(int(rsp[0]),int(rsp[1]))

def GetZProfileStartPoint(PosRef:str="", Units:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current start point of the profile by using given units and a
    reference position.
    API Status: internal
    Args:
        PosRef:str = "Z"
        Units:str = "Y"
    Returns:
        X:Decimal
        Y:Decimal
    Command Timeout: 10000
    Example:GetZProfileStartPoint H Y
    """
    rsp = MessageServerInterface.sendSciCommand("GetZProfileStartPoint",PosRef,Units)
    global GetZProfileStartPoint_Response
    if not "GetZProfileStartPoint_Response" in globals(): GetZProfileStartPoint_Response = namedtuple("GetZProfileStartPoint_Response", "X,Y")
    return GetZProfileStartPoint_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def AddZProfilePoint(X:Decimal="", Y:Decimal="", After:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Adds new point to the profile at the end (default) or after the given point.
    Returns an index of new point and a number of all points in the profile. Point
    indices are started from 1.
    API Status: internal
    Args:
        X:Decimal = 0
        Y:Decimal = 0
        After:int = 0
    Returns:
        Index:int
        NumberOfPoints:int
        NumberOfEPoints:int
    Command Timeout: 10000
    Example:AddZProfilePoint 50000 50000
    """
    rsp = MessageServerInterface.sendSciCommand("AddZProfilePoint",X,Y,After)
    global AddZProfilePoint_Response
    if not "AddZProfilePoint_Response" in globals(): AddZProfilePoint_Response = namedtuple("AddZProfilePoint_Response", "Index,NumberOfPoints,NumberOfEPoints")
    return AddZProfilePoint_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]))

def DeleteZProfilePoint(Index:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Deletes the point from the profile. Returns a number of all and enabled points
    in the profile. Point indices are started from 1.
    API Status: internal
    Args:
        Index:int = 0
    Returns:
        NumberOfPoints:int
        NumberOfEPoints:int
    Command Timeout: 10000
    Example:DeleteZProfilePoint 11
    """
    rsp = MessageServerInterface.sendSciCommand("DeleteZProfilePoint",Index)
    global DeleteZProfilePoint_Response
    if not "DeleteZProfilePoint_Response" in globals(): DeleteZProfilePoint_Response = namedtuple("DeleteZProfilePoint_Response", "NumberOfPoints,NumberOfEPoints")
    return DeleteZProfilePoint_Response(int(rsp[0]),int(rsp[1]))

def SetZProfilePointStatus(Index:int="", Status:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Enables or disables the point in the profile. Point indices are started from 1.
    API Status: internal
    Args:
        Index:int = 0
        Status:str = "0"
    Command Timeout: 10000
    Example:SetZProfilePointStatus 11 E
    """
    MessageServerInterface.sendSciCommand("SetZProfilePointStatus",Index,Status)


def GetZProfilePointStatus(Index:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns a status of the point in the profile. Point indices are started from 1.
    API Status: internal
    Args:
        Index:int = 0
    Returns:
        Status:str
    Command Timeout: 10000
    Example:GetZProfilePointStatus 11
    """
    rsp = MessageServerInterface.sendSciCommand("GetZProfilePointStatus",Index)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def PreciseZProfile():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    All points are covered by triangles, each vertex of the triangle is a point of
    the profile. The centers of the triangles are new points of the profile. If all
    three vertexes of the triangle are tested points the new point will be marked as
    tested also and has Z value equal to average Z of all three vertexes. Otherwise
    the new point will be marked as untested. The command returns a number of points
    in the profile after the update.
    API Status: internal
    Returns:
        NumberOfPoints:int
    Command Timeout: 10000
    Example:PreciseZProfile
    """
    rsp = MessageServerInterface.sendSciCommand("PreciseZProfile")
    return int(rsp[0])

def CloseTableView():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Closes the TableView application.
    API Status: internal
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("CloseTableView")


def StepChuckSite(Site:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Steps the wafer chuck stage to the requested Site no. of the chuck table view.
    If no Site no is specified the chuck will step automatically to the next logical
    site location. The first site in the table is site 1.
    API Status: internal
    Args:
        Site:int = -1
    Returns:
        SiteRet:int
    Command Timeout: 60000
    """
    rsp = MessageServerInterface.sendSciCommand("StepChuckSite",Site)
    return int(rsp[0])

def StepChuckSubsite(Site:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Steps the wafer chuck stage to the requested Subsite no. of the chuck subsite
    table view. If no Subsite no. is specified the chuck will step automatically to
    the next logical site location. The first site in the table is site 1.
    API Status: internal
    Args:
        Site:int = -1
    Returns:
        SiteRet:int
    Command Timeout: 60000
    """
    rsp = MessageServerInterface.sendSciCommand("StepChuckSubsite",Site)
    return int(rsp[0])

def StepScopeSite(Site:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Steps the microscope stage to the requested Site no. of the scope table view. If
    no Site no is specified the scope will step automatically to the next logical
    site location. The first site in the table is site 1.
    API Status: internal
    Args:
        Site:int = -1
    Returns:
        SiteRet:int
    Command Timeout: 60000
    """
    rsp = MessageServerInterface.sendSciCommand("StepScopeSite",Site)
    return int(rsp[0])

def StepProbeSite(Probe:int="", Site:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Steps the specified probe to the requested Site no. of the Probe no table view.
    If no Site no. is specified the Probe no. will step automatically to the next
    logical site location. The first site in the table is site 1.
    API Status: internal
    Args:
        Probe:int = -1
        Site:int = -1
    Returns:
        ProbeRet:int
        SiteRet:int
    Command Timeout: 60000
    """
    rsp = MessageServerInterface.sendSciCommand("StepProbeSite",Probe,Site)
    global StepProbeSite_Response
    if not "StepProbeSite_Response" in globals(): StepProbeSite_Response = namedtuple("StepProbeSite_Response", "ProbeRet,SiteRet")
    return StepProbeSite_Response(int(rsp[0]),int(rsp[1]))

def ReadChuckSitePosition():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the actual chuck site position. The first site in the table is site 1.
    API Status: internal
    Returns:
        Site:int
        X:Decimal
        Y:Decimal
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckSitePosition")
    global ReadChuckSitePosition_Response
    if not "ReadChuckSitePosition_Response" in globals(): ReadChuckSitePosition_Response = namedtuple("ReadChuckSitePosition_Response", "Site,X,Y")
    return ReadChuckSitePosition_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def ReadScopeSitePosition():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the site position of the specified probe. The first site in the table is
    site 1.
    API Status: internal
    Returns:
        Site:int
        X:Decimal
        Y:Decimal
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadScopeSitePosition")
    global ReadScopeSitePosition_Response
    if not "ReadScopeSitePosition_Response" in globals(): ReadScopeSitePosition_Response = namedtuple("ReadScopeSitePosition_Response", "Site,X,Y")
    return ReadScopeSitePosition_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def ReadProbeSitePosition(Probe:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the site position of the specified probe. The first site in the table is
    site 1.
    API Status: internal
    Args:
        Probe:int = -1
    Returns:
        ProbeRet:int
        Site:int
        X:Decimal
        Y:Decimal
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadProbeSitePosition",Probe)
    global ReadProbeSitePosition_Response
    if not "ReadProbeSitePosition_Response" in globals(): ReadProbeSitePosition_Response = namedtuple("ReadProbeSitePosition_Response", "ProbeRet,Site,X,Y")
    return ReadProbeSitePosition_Response(int(rsp[0]),int(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]))

def ReadChuckSubsitePosition():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the chuck subsite position. The first site in the table is site 1.
    API Status: internal
    Returns:
        Site:int
        X:Decimal
        Y:Decimal
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadChuckSubsitePosition")
    global ReadChuckSubsitePosition_Response
    if not "ReadChuckSubsitePosition_Response" in globals(): ReadChuckSubsitePosition_Response = namedtuple("ReadChuckSubsitePosition_Response", "Site,X,Y")
    return ReadChuckSubsitePosition_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def StepFirstDie(ClearBins:int="", RecalcRoute:int=""):
    """
    Steps the chuck to the first die of the wafer map. Returns the row and column
    number of the actual die location after the move is completed. If ClearBins is
    1, all binning data will be cleared from dies. If yes the route will be
    recalculated. All dies marked to skip during the last test (marked to skip with
    SetDieStatus) will be eliminated from the route.
    API Status: published
    Args:
        ClearBins:int = 1
        RecalcRoute:int = 1
    Returns:
        DieX:int
        DieY:int
        CurSite:int
        LastSiteIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepFirstDie",ClearBins,RecalcRoute)
    global StepFirstDie_Response
    if not "StepFirstDie_Response" in globals(): StepFirstDie_Response = namedtuple("StepFirstDie_Response", "DieX,DieY,CurSite,LastSiteIndex")
    return StepFirstDie_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def StepNextDie(CDieX:int="", CDieY:int="", Site:int=""):
    """
    Steps the chuck to the specified x,y die location of the wafer map. If no
    command data is passed, the chuck automatically steps to the next logical wafer
    map die location. Returns the row and column number of the actual die location
    after the move is completed. In addition, the SubDie location, and total number
    of SubDies is also returned.  If Site (i.e. SubDie) is -1, the chuck will move
    to SubDie 0, on the next die; in this case, the first 2 parameters are ignored.
    If sent without parameters, it will literally 'step to the next die'. When using
    this command from shared code, use SendWithoutParameter().
    API Status: published
    Args:
        CDieX:int = 0
        CDieY:int = 0
        Site:int = 0
    Returns:
        RDieX:int
        RDieY:int
        CurSite:int
        LastSiteIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepNextDie",CDieX,CDieY,Site)
    global StepNextDie_Response
    if not "StepNextDie_Response" in globals(): StepNextDie_Response = namedtuple("StepNextDie_Response", "RDieX,RDieY,CurSite,LastSiteIndex")
    return StepNextDie_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def BinMapDie(Bin:int="", CDieX:int="", CDieY:int=""):
    """
    Assigns the bin information to the wafer map at the current die, unless a row
    and column is specified. Inks the device if the real time inking option (of the
    wafer map) is enabled.
    API Status: published
    Args:
        Bin:int = 0
        CDieX:int = 0
        CDieY:int = 0
    Returns:
        RDieX:int
        RDieY:int
    Command Timeout: 30000
    Example:BinMapDie 1
    """
    rsp = MessageServerInterface.sendSciCommand("BinMapDie",Bin,CDieX,CDieY)
    global BinMapDie_Response
    if not "BinMapDie_Response" in globals(): BinMapDie_Response = namedtuple("BinMapDie_Response", "RDieX,RDieY")
    return BinMapDie_Response(int(rsp[0]),int(rsp[1]))

def AssignMapBins(Bins:str=""):
    """
    Assigns the pass or fail information to the actual bin value. Redundant to
    SetBinCode.
    API Status: published
    Args:
        Bins:str = ""
    Command Timeout: 10000
    Example:AssignMapBins PFFFFFF
    """
    MessageServerInterface.sendSciCommand("AssignMapBins",Bins)


def StepFailedBack():
    """
    Steps the chuck back the number of consecutive failed dies (goes back to the
    last known good die) and returns the number of consecutive failed dies.
    API Status: published
    Returns:
        DieIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepFailedBack")
    return int(rsp[0])

def StepFailedForward():
    """
    Steps the chuck forward the number of consecutive failed dies (goes to next
    untested die).
    API Status: published
    Returns:
        DieIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepFailedForward")
    return int(rsp[0])

def ReadMapPosition(Pos:int="", FromPos:str=""):
    """
    Returns the actual Wafer Map chuck position. The SubDie collection is 1-based,
    the first value is 1, not 0.     M_pnCurSite returns the currently selected
    Subdie (1-based) or 0 if no Subdie is currently selected. This command (i.e.
    ReadMapPosition) has been included for legacy support.       ReadMapPosition2 is
    the preferred method for reading Wafer Map chuck position.
    API Status: published
    Args:
        Pos:int = 0
        FromPos:str = "R"
    Returns:
        DieX:int
        DieY:int
        XFromHome:Decimal
        YFromHome:Decimal
        CurSite:int
        LastSiteIndex:int
        CurDie:int
        DiesCount:int
        CurCluster:int
        ClustersCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadMapPosition",Pos,FromPos)
    global ReadMapPosition_Response
    if not "ReadMapPosition_Response" in globals(): ReadMapPosition_Response = namedtuple("ReadMapPosition_Response", "DieX,DieY,XFromHome,YFromHome,CurSite,LastSiteIndex,CurDie,DiesCount,CurCluster,ClustersCount")
    return ReadMapPosition_Response(int(rsp[0]),int(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]))

def ReadMapYield():
    """
    Returns the actual wafer map yield data information.
    API Status: published
    Returns:
        TotalDies:int
        TestedDies:int
        Passed:int
        Failed:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadMapYield")
    global ReadMapYield_Response
    if not "ReadMapYield_Response" in globals(): ReadMapYield_Response = namedtuple("ReadMapYield_Response", "TotalDies,TestedDies,Passed,Failed")
    return ReadMapYield_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def BinStepDie(Bin:int="", CDieX:int="", CDieY:int="", Site:int=""):
    """
    Bins the current die and steps the chuck to the next selected die location of
    the wafer map (default) or steps to the specified Column and Row position, if
    these values are passed.  In contrast to StepNextDie, the BinStepDie command
    will only step from die to die while staying on the current subdie. It will not
    step through the subdies so it cannot be used for subdie stepping.
    API Status: published
    Args:
        Bin:int = 0
        CDieX:int = 0
        CDieY:int = 0
        Site:int = 0
    Returns:
        RDieX:int
        RDieY:int
        CurSite:int
        LastSiteIndex:int
    Command Timeout: 6000000
    Example:BinStepDie 1
    """
    rsp = MessageServerInterface.sendSciCommand("BinStepDie",Bin,CDieX,CDieY,Site)
    global BinStepDie_Response
    if not "BinStepDie_Response" in globals(): BinStepDie_Response = namedtuple("BinStepDie_Response", "RDieX,RDieY,CurSite,LastSiteIndex")
    return BinStepDie_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def SetMapHome(DieX:int="", DieY:int=""):
    """
    If the command has no parameters it sets the current position as home position
    both for the wafer map and for the chuck. Otherwise, it changes the wafer map
    home position using the given die coordinates.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetMapHome",DieX,DieY)


def SaveMapFile(FileName:str="", FileType:str=""):
    """
    Saves current map file with specified name.
    API Status: published
    Args:
        FileName:str = ""
        FileType:str = "m"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SaveMapFile",FileName,FileType)


def SetWaferMapMode(Mode:str=""):
    """
    Enables or disables an external mode for the application. In the external mode,
    all controls are disabled. The application handles all its remote commands in
    both modes. Special interactive modes can also be turned on.
    API Status: published
    Args:
        Mode:str = ""
    Returns:
        ModeType:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("SetWaferMapMode",Mode)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def GetWaferMapMode(ModeType:str=""):
    """
    Returns whether the application is in external mode or not.
    API Status: published
    Args:
        ModeType:str = ""
    Returns:
        Mode:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferMapMode",ModeType)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetWaferNum(Number:str=""):
    """
    Specifies the wafer number.
    API Status: published
    Args:
        Number:str = "0"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetWaferNum",Number)


def GetWaferNum():
    """
    Returns the wafer number for the current wafer.
    API Status: published
    Returns:
        Number:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferNum")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetWaferID(ID:str=""):
    """
    Specifies the ID for the current wafer.
    API Status: published
    Args:
        ID:str = "0"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetWaferID",ID)


def GetWaferID():
    """
    Returns the wafer ID for the current wafer.
    API Status: published
    Returns:
        ID:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferID")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetProductID(ID:str=""):
    """
    Specifies the product ID for the current wafer.
    API Status: published
    Args:
        ID:str = "0"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetProductID",ID)


def GetProductID():
    """
    Displays the product ID for the current wafer.
    API Status: published
    Returns:
        ID:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetProductID")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def DoInkerRun():
    """
    Instructs the WaferMap to perform an ink run on the current wafer. Returns the
    number of dies which were inked during the inker run.
    API Status: published
    Returns:
        InkedDies:int
    Command Timeout: 30000
    """
    rsp = MessageServerInterface.sendSciCommand("DoInkerRun")
    return int(rsp[0])

def CloseWaferMap():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Closes the Wafer Map application.
    API Status: internal
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("CloseWaferMap")


def GetNumSelectedDies():
    """
    Gets the number of dies in the map which are selected for probing.
    API Status: published
    Returns:
        SelectedDies:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetNumSelectedDies")
    return int(rsp[0])

def GetSelectedDieCoords(Die:int=""):
    """
    Given the index of a selected die in the range [1..NumSelectedDies], returns the
    column and row indices for the selected die.
    API Status: published
    Args:
        Die:int = 0
    Returns:
        DieX:int
        DieY:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSelectedDieCoords",Die)
    global GetSelectedDieCoords_Response
    if not "GetSelectedDieCoords_Response" in globals(): GetSelectedDieCoords_Response = namedtuple("GetSelectedDieCoords_Response", "DieX,DieY")
    return GetSelectedDieCoords_Response(int(rsp[0]),int(rsp[1]))

def StepNextDieOffset(XOffset:Decimal="", YOffset:Decimal="", CDieX:int="", CDieY:int=""):
    """
    Moves to a user-specified offset within a die. The optional col row params can
    be used to specify the die. If they are omitted, WaferMap moves to the specified
    offset within the next selected die.
    API Status: published
    Args:
        XOffset:Decimal = 0
        YOffset:Decimal = 0
        CDieX:int = 0
        CDieY:int = 0
    Returns:
        RDieX:int
        RDieY:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepNextDieOffset",XOffset,YOffset,CDieX,CDieY)
    global StepNextDieOffset_Response
    if not "StepNextDieOffset_Response" in globals(): StepNextDieOffset_Response = namedtuple("StepNextDieOffset_Response", "RDieX,RDieY")
    return StepNextDieOffset_Response(int(rsp[0]),int(rsp[1]))

def ReadMapPosition2(Pos:int="", FromPos:str=""):
    """
    Returns the actual Wafer Map chuck position. The SubDie collection is 0-based,
    the first value is 0, not 1. M_pnCurSite returns the currently selected Subdie
    (0-based) or -1 if no Subdie is currently selected.  This command is the
    preferred method for reading Wafer Map chuck position.
    API Status: published
    Args:
        Pos:int = 0
        FromPos:str = "R"
    Returns:
        DieX:int
        DieY:int
        XFromHome:Decimal
        YFromHome:Decimal
        CurSite:int
        LastSiteIndex:int
        CurDie:int
        DiesCount:int
        CurCluster:int
        ClustersCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadMapPosition2",Pos,FromPos)
    global ReadMapPosition2_Response
    if not "ReadMapPosition2_Response" in globals(): ReadMapPosition2_Response = namedtuple("ReadMapPosition2_Response", "DieX,DieY,XFromHome,YFromHome,CurSite,LastSiteIndex,CurDie,DiesCount,CurCluster,ClustersCount")
    return ReadMapPosition2_Response(int(rsp[0]),int(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]))

def DeleteSubDie2(Site:int=""):
    """
    Deletes selected subdie. The SubDie collection is 0-based, the first value is 0,
    not 1.       This command is the preferred method for deleting a selected
    subdie.
    API Status: published
    Args:
        Site:int = 0
    Returns:
        SitesCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("DeleteSubDie2",Site)
    return int(rsp[0])

def DeleteAllSubDie():
    """
    Deletes all subdies for all dies.
    API Status: published
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("DeleteAllSubDie")


def GetDieLabel(DieX:int="", DieY:int=""):
    """
    Returns a label from the wafer map at the current die, unless a row and column
    are specified.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
    Returns:
        Label:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieLabel",DieX,DieY)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetDieLabel(Label:str="", DieX:int="", DieY:int=""):
    """
    Assigns a label to the wafer map at the current die, unless a row and column are
    specified.
    API Status: published
    Args:
        Label:str = ""
        DieX:int = 0
        DieY:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieLabel",Label,DieX,DieY)


def StepNextSubDie(Site:int=""):
    """
    Steps the chuck to the specified SubDie number relative to the current die
    origin of the wafer map. Returns the SubDie number of the actual die location
    after the move is completed and the total number of subdies.
    API Status: published
    Args:
        Site:int = 0
    Returns:
        CurSite:int
        LastSiteIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepNextSubDie",Site)
    global StepNextSubDie_Response
    if not "StepNextSubDie_Response" in globals(): StepNextSubDie_Response = namedtuple("StepNextSubDie_Response", "CurSite,LastSiteIndex")
    return StepNextSubDie_Response(int(rsp[0]),int(rsp[1]))

def OpenWaferMap(FileName:str=""):
    """
    Opens a Wafer Map file.
    API Status: published
    Args:
        FileName:str = ""
    Command Timeout: 240000
    """
    MessageServerInterface.sendSciCommand("OpenWaferMap",FileName)


def SetDieResult(Result:str="", DieX:int="", DieY:int=""):
    """
    Assigns a measurement result to the wafer map at the current die, unless a row
    and column are specified.
    API Status: published
    Args:
        Result:str = ""
        DieX:int = 0
        DieY:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieResult",Result,DieX,DieY)


def GetDieResult(DieX:int="", DieY:int=""):
    """
    Returns a measurement result from the wafer map at the current die, unless a row
    and column are specified.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
    Returns:
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieResult",DieX,DieY)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetDieMapResult(Result:str="", DieX:int="", DieY:int="", Site:int=""):
    """
    Assigns a measurement result to the wafer die map at the current die and the
    current subdie, unless a subdie, row, and column are specified. The SubDie
    collection is 0-based, the first value is 0, not 1.
    API Status: published
    Args:
        Result:str = ""
        DieX:int = 0
        DieY:int = 0
        Site:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieMapResult",Result,DieX,DieY,Site)


def GetDieMapResult(DieX:int="", DieY:int="", Site:int=""):
    """
    Returns a measurement result from the wafer map at the current die and current
    subdie, unless a row, column, and subdie are specified. The SubDie collection is
    0-based, the first value is 0, not 1.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
        Site:int = 0
    Returns:
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieMapResult",DieX,DieY,Site)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def BinSubDie(Bin:int="", CDieX:int="", CDieY:int="", Site:int=""):
    """
    Assigns the bin information for the current subdie in the current die, unless a
    subdie, row, and column are specified. The SubDie collection is 0-based, the
    first value is 0, not 1.
    API Status: published
    Args:
        Bin:int = 0
        CDieX:int = 0
        CDieY:int = 0
        Site:int = 0
    Returns:
        RDieX:int
        RDieY:int
        CurSite:int
        LastSiteIndex:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("BinSubDie",Bin,CDieX,CDieY,Site)
    global BinSubDie_Response
    if not "BinSubDie_Response" in globals(): BinSubDie_Response = namedtuple("BinSubDie_Response", "RDieX,RDieY,CurSite,LastSiteIndex")
    return BinSubDie_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def SetSubDieData(Site:int="", X:Decimal="", Y:Decimal="", Label:str=""):
    """
    Sets up SubDie data. The SubDie collection is 0-based, the first value is 0, not
    1.
    API Status: published
    Args:
        Site:int = 0
        X:Decimal = 0
        Y:Decimal = 0
        Label:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetSubDieData",Site,X,Y,Label)


def GetSubDieData(Site:int=""):
    """
    Returns the information of a SubDie. The SubDie collection is 0-based, the first
    value is 0, not 1.
    API Status: published
    Args:
        Site:int = 0
    Returns:
        CurSite:int
        X:Decimal
        Y:Decimal
        Label:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSubDieData",Site)
    global GetSubDieData_Response
    if not "GetSubDieData_Response" in globals(): GetSubDieData_Response = namedtuple("GetSubDieData_Response", "CurSite,X,Y,Label")
    return GetSubDieData_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),str("" if len(rsp) < 4 else ' '.join(rsp[3:])))

def GetMapHome():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command reads the home die location of the WaferMap.
    API Status: internal
    Returns:
        DieX:int
        DieY:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetMapHome")
    global GetMapHome_Response
    if not "GetMapHome_Response" in globals(): GetMapHome_Response = namedtuple("GetMapHome_Response", "DieX,DieY")
    return GetMapHome_Response(int(rsp[0]),int(rsp[1]))

def GetMapDims():
    """
    Returns the parameters for the current wafer.
    API Status: published
    Returns:
        MapType:str
        XIndex:Decimal
        YIndex:Decimal
        Columns:int
        Rows:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetMapDims")
    global GetMapDims_Response
    if not "GetMapDims_Response" in globals(): GetMapDims_Response = namedtuple("GetMapDims_Response", "MapType,XIndex,YIndex,Columns,Rows")
    return GetMapDims_Response(str(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),int(rsp[3]),int(rsp[4]))

def SetWaferMapParams(Diameter:Decimal="", DieWidth:Decimal="", DieHeight:Decimal="", FlatLength:Decimal="", FlatAngle:int="", XOffset:Decimal="", YOffset:Decimal="", EdgeArea:Decimal=""):
    """
    Creates the circle wafer with specified parameters. If parameter is omitted,
    then zero is used. For this version of the command, units for XOffset and
    YOffset are percentages.
    API Status: published
    Args:
        Diameter:Decimal = 200
        DieWidth:Decimal = 10000
        DieHeight:Decimal = 10000
        FlatLength:Decimal = 20
        FlatAngle:int = 0
        XOffset:Decimal = 0
        YOffset:Decimal = 0
        EdgeArea:Decimal = 0
    Command Timeout: 240000
    """
    MessageServerInterface.sendSciCommand("SetWaferMapParams",Diameter,DieWidth,DieHeight,FlatLength,FlatAngle,XOffset,YOffset,EdgeArea)


def SetRectMapParams(DieWidth:Decimal="", DieHeight:Decimal="", Columns:int="", Rows:int=""):
    """
    Creates the rectangle wafer with specified parameters.
    API Status: published
    Args:
        DieWidth:Decimal = 0
        DieHeight:Decimal = 0
        Columns:int = 0
        Rows:int = 0
    Command Timeout: 240000
    """
    MessageServerInterface.sendSciCommand("SetRectMapParams",DieWidth,DieHeight,Columns,Rows)


def StepToDie(DieNumber:int="", Site:int=""):
    """
    Steps the chuck to the die location specified by the die number of the wafer
    map. If no command data is passed, the chuck automatically steps to the next
    logical wafer map die location. Returns the row and column number of the actual
    die location after the move is completed. In addition, the SubDie location, and
    total number of SubDies is also returned.
    API Status: published
    Args:
        DieNumber:int = -1
        Site:int = 0
    Returns:
        RDieX:int
        RDieY:int
        CurSite:int
        LastSiteIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepToDie",DieNumber,Site)
    global StepToDie_Response
    if not "StepToDie_Response" in globals(): StepToDie_Response = namedtuple("StepToDie_Response", "RDieX,RDieY,CurSite,LastSiteIndex")
    return StepToDie_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def GetMapOrientation(UseOrientationCornerForShift:int=""):
    """
    Returns parameters of the map coordinate system.
    API Status: published
    Args:
        UseOrientationCornerForShift:int = 0
    Returns:
        Orientation:int
        OriginShiftX:int
        OriginShiftY:int
        UseAlphas:int
        UseIOs:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetMapOrientation",UseOrientationCornerForShift)
    global GetMapOrientation_Response
    if not "GetMapOrientation_Response" in globals(): GetMapOrientation_Response = namedtuple("GetMapOrientation_Response", "Orientation,OriginShiftX,OriginShiftY,UseAlphas,UseIOs")
    return GetMapOrientation_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]))

def SetMapOrientation(Orientation:int="", OriginShiftX:int="", OriginShiftY:int="", UseAlphas:int="", UseIOs:int="", UseOrientationCornerForShift:int=""):
    """
    Sets up new map origin and new coordinate system after that.
    API Status: published
    Args:
        Orientation:int = 0
        OriginShiftX:int = 0
        OriginShiftY:int = 0
        UseAlphas:int = 0
        UseIOs:int = 1
        UseOrientationCornerForShift:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetMapOrientation",Orientation,OriginShiftX,OriginShiftY,UseAlphas,UseIOs,UseOrientationCornerForShift)


def SetDieStatus(DieX:int="", DieY:int="", Status:str=""):
    """
    Sets the die status.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
        Status:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieStatus",DieX,DieY,Status)


def GetDieStatus(DieX:int="", DieY:int=""):
    """
    Gets the die status.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
    Returns:
        Status:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieStatus",DieX,DieY)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetSubDieStatus(Site:int="", Status:str=""):
    """
    Sets the SubDie status. The SubDie collection is 0-based, the first value is 0,
    not 1.
    API Status: published
    Args:
        Site:int = 0
        Status:str = "0"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetSubDieStatus",Site,Status)


def GetSubDieStatus(Site:int=""):
    """
    Returns the SubDie status. The SubDie collection is 0-based, the first value is
    0, not 1.
    API Status: published
    Args:
        Site:int = 0
    Returns:
        Status:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSubDieStatus",Site)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def GetBinCode(Bin:int=""):
    """
    Returns the Die size from the current map.
    API Status: published
    Args:
        Bin:int = 0
    Returns:
        Chars:str
        Color:int
        Status:str
        Inker1:int
        Inker2:int
        Inker3:int
        Inker4:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetBinCode",Bin)
    global GetBinCode_Response
    if not "GetBinCode_Response" in globals(): GetBinCode_Response = namedtuple("GetBinCode_Response", "Chars,Color,Status,Inker1,Inker2,Inker3,Inker4")
    return GetBinCode_Response(str(rsp[0]),int(rsp[1]),str(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]))

def SetBinCode(Bin:int="", Chars:str="", Color:int="", Status:str="", Inker1:int="", Inker2:int="", Inker3:int="", Inker4:int=""):
    """
    Appends the Bin information to a bin code.
    API Status: published
    Args:
        Bin:int = 0
        Chars:str = ""
        Color:int = 0
        Status:str = ""
        Inker1:int = 0
        Inker2:int = 0
        Inker3:int = 0
        Inker4:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetBinCode",Bin,Chars,Color,Status,Inker1,Inker2,Inker3,Inker4)


def GetDieDataAsNum(CDieIndex:int=""):
    """
    Returns the Die Information in the Row Column format. If the Die Number is
    invalid it returns an error. If the Die Number is absent it uses the current die
    on the wafer.
    API Status: published
    Args:
        CDieIndex:int = 0
    Returns:
        RDieIndex:int
        DieX:int
        DieY:int
        Bin:int
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieDataAsNum",CDieIndex)
    global GetDieDataAsNum_Response
    if not "GetDieDataAsNum_Response" in globals(): GetDieDataAsNum_Response = namedtuple("GetDieDataAsNum_Response", "RDieIndex,DieX,DieY,Bin,Result")
    return GetDieDataAsNum_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),str("" if len(rsp) < 5 else ' '.join(rsp[4:])))

def SetDieDataAsNum(DieIndex:int="", Bin:int="", Result:str=""):
    """
    Sets the Die Information. If the Die Number is invalid it returns an error.
    API Status: published
    Args:
        DieIndex:int = 0
        Bin:int = 0
        Result:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieDataAsNum",DieIndex,Bin,Result)


def GetSubDieDataAsNum(CDieIndex:int="", Site:int=""):
    """
    Returns the information of a SubDie. The SubDie collection is 0-based, the first
    value is 0, not 1.
    API Status: published
    Args:
        CDieIndex:int = 0
        Site:int = 0
    Returns:
        RDieIndex:int
        DieX:int
        DieY:int
        CurSite:int
        Bin:int
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSubDieDataAsNum",CDieIndex,Site)
    global GetSubDieDataAsNum_Response
    if not "GetSubDieDataAsNum_Response" in globals(): GetSubDieDataAsNum_Response = namedtuple("GetSubDieDataAsNum_Response", "RDieIndex,DieX,DieY,CurSite,Bin,Result")
    return GetSubDieDataAsNum_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),str("" if len(rsp) < 6 else ' '.join(rsp[5:])))

def SetSubDieDataAsNum(DieIndex:int="", Site:int="", Bin:int="", Result:str=""):
    """
    Sets up SubDie data. The SubDie collection is 0-based, the first value is 0, not
    1.
    API Status: published
    Args:
        DieIndex:int = 0
        Site:int = 0
        Bin:int = 0
        Result:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetSubDieDataAsNum",DieIndex,Site,Bin,Result)


def GetDieDataAsColRow(CDieX:int="", CDieY:int=""):
    """
    Returns the Die Information in the Row Column format. If the Die Number is
    invalid it returns an error. If the Die Column and Row are absent it uses the
    current die on the wafer.
    API Status: published
    Args:
        CDieX:int = 0
        CDieY:int = 0
    Returns:
        DieIndex:int
        RDieX:int
        RDieY:int
        Bin:int
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieDataAsColRow",CDieX,CDieY)
    global GetDieDataAsColRow_Response
    if not "GetDieDataAsColRow_Response" in globals(): GetDieDataAsColRow_Response = namedtuple("GetDieDataAsColRow_Response", "DieIndex,RDieX,RDieY,Bin,Result")
    return GetDieDataAsColRow_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),str("" if len(rsp) < 5 else ' '.join(rsp[4:])))

def SetDieDataAsColRow(DieX:int="", DieY:int="", Bin:int="", Result:str=""):
    """
    Sets the Data in the Row Column format. If the Die is invalid it returns an
    error.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
        Bin:int = 0
        Result:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieDataAsColRow",DieX,DieY,Bin,Result)


def GetSubDieDataAsColRow(CDieX:int="", CDieY:int="", Site:int=""):
    """
    Returns the information of a SubDie. The SubDie collection is 0-based, the first
    value is 0, not 1.
    API Status: published
    Args:
        CDieX:int = 0
        CDieY:int = 0
        Site:int = 0
    Returns:
        DieIndex:int
        RDieX:int
        RDieY:int
        CurSite:int
        Bin:int
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSubDieDataAsColRow",CDieX,CDieY,Site)
    global GetSubDieDataAsColRow_Response
    if not "GetSubDieDataAsColRow_Response" in globals(): GetSubDieDataAsColRow_Response = namedtuple("GetSubDieDataAsColRow_Response", "DieIndex,RDieX,RDieY,CurSite,Bin,Result")
    return GetSubDieDataAsColRow_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),str("" if len(rsp) < 6 else ' '.join(rsp[5:])))

def SetSubDieDataAsColRow(DieX:int="", DieY:int="", Site:int="", Bin:int="", Result:str=""):
    """
    Sets up SubDie data. The SubDie collection is 0-based, the first value is 0, not
    1.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
        Site:int = 0
        Bin:int = 0
        Result:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetSubDieDataAsColRow",DieX,DieY,Site,Bin,Result)


def SelectAllDiesForProbing(DoSelectAll:int="", DoEdgeDies:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Enables all dies.
    API Status: internal
    Args:
        DoSelectAll:int = 0
        DoEdgeDies:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SelectAllDiesForProbing",DoSelectAll,DoEdgeDies)


def GetMapName():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current WaferMap Filename.
    API Status: internal
    Returns:
        Name:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetMapName")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetLotID(ID:str=""):
    """
    Specifies the ID for the current wafer.
    API Status: published
    Args:
        ID:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetLotID",ID)


def GetLotID():
    """
    Returns the Lot ID for the current wafer.
    API Status: published
    Returns:
        ID:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetLotID")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def StepFirstCluster(ClearBins:int="", RecalcRoute:int=""):
    """
    Steps the chuck to the first die cluster of the cluster map. If clusters are not
    defined, the first Die is used. Returns the row and column information of the
    actual cluster and die location after the move is completed. Switches to remote
    control if the "Disable Velox" flag is set in the external options window.
    API Status: published
    Args:
        ClearBins:int = 1
        RecalcRoute:int = 1
    Returns:
        ClusterX:int
        ClusterY:int
        ClusterIndex:int
        IncompleteCluster:int
        DieX:int
        DieY:int
        DieIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepFirstCluster",ClearBins,RecalcRoute)
    global StepFirstCluster_Response
    if not "StepFirstCluster_Response" in globals(): StepFirstCluster_Response = namedtuple("StepFirstCluster_Response", "ClusterX,ClusterY,ClusterIndex,IncompleteCluster,DieX,DieY,DieIndex")
    return StepFirstCluster_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]))

def StepNextCluster(CClusterX:int="", CClusterY:int=""):
    """
    Steps the chuck to the specified x,y cluster die location of the cluster map. If
    no command data is passed, the chuck automatically steps to the next logical
    cluster map location. If clusters are not defined, the Die information is used.
    Returns the row and column number of the actual die location after the move is
    completed.
    API Status: published
    Args:
        CClusterX:int = 0
        CClusterY:int = 0
    Returns:
        RClusterX:int
        RClusterY:int
        ClusterIndex:int
        IncompleteCluster:int
        DieX:int
        DieY:int
        DieIndex:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepNextCluster",CClusterX,CClusterY)
    global StepNextCluster_Response
    if not "StepNextCluster_Response" in globals(): StepNextCluster_Response = namedtuple("StepNextCluster_Response", "RClusterX,RClusterY,ClusterIndex,IncompleteCluster,DieX,DieY,DieIndex")
    return StepNextCluster_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]))

def SetMapRoute(MoveMode:str="", StartColumn:str="", StartRow:str="", MoveParam:str=""):
    """
    Specifies the Move Path for the probe station inside the Wafer Map. Optimization
    is done for the shortest move way for the station.
    API Status: published
    Args:
        MoveMode:str = "B"
        StartColumn:str = "L"
        StartRow:str = "T"
        MoveParam:str = "H"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetMapRoute",MoveMode,StartColumn,StartRow,MoveParam)


def GetMapRoute():
    """
    Returns the specified move path for the probe station inside the Wafer Map.
    API Status: published
    Returns:
        MoveMode:str
        StartColumn:str
        StartRow:str
        MoveParam:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetMapRoute")
    global GetMapRoute_Response
    if not "GetMapRoute_Response" in globals(): GetMapRoute_Response = namedtuple("GetMapRoute_Response", "MoveMode,StartColumn,StartRow,MoveParam")
    return GetMapRoute_Response(str(rsp[0]),str(rsp[1]),str(rsp[2]),str("" if len(rsp) < 4 else ' '.join(rsp[3:])))

def SetClusterParams(UseClusters:int="", ClusterWidth:int="", ClusterHeight:int="", TestIncomplete:int=""):
    """
    Specifies the clusters parameters.
    API Status: published
    Args:
        UseClusters:int = 0
        ClusterWidth:int = 1
        ClusterHeight:int = 1
        TestIncomplete:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetClusterParams",UseClusters,ClusterWidth,ClusterHeight,TestIncomplete)


def GetClusterParams():
    """
    Returns current clusters parameters.
    API Status: published
    Returns:
        UseClusters:int
        ClusterWidth:int
        ClusterHeight:int
        TestIncomplete:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetClusterParams")
    global GetClusterParams_Response
    if not "GetClusterParams_Response" in globals(): GetClusterParams_Response = namedtuple("GetClusterParams_Response", "UseClusters,ClusterWidth,ClusterHeight,TestIncomplete")
    return GetClusterParams_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def NewWaferMap():
    """
    Deletes current wafer map, sub dies and binning information; then creates new
    wafer map with defaults parameters.
    API Status: published
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("NewWaferMap")


def AddSubDie(X:Decimal="", Y:Decimal="", Label:str=""):
    """
    Adds new subdie at the end of the table.
    API Status: published
    Args:
        X:Decimal = 0
        Y:Decimal = 0
        Label:str = ""
    Returns:
        SitesCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("AddSubDie",X,Y,Label)
    return int(rsp[0])

def DeleteSubDie(Site:int=""):
    """
    Deletes selected subdie. The SubDie collection is 1-based, the first value is 1,
    not 0. If 0 is passed in as the subdie index, WaferMap will delete all subdies
    for all dies.This command (i.e. DeleteSubDie) has been included for legacy
    support.       DeleteSubDie2 is the preferred method for deleting a selected
    subdie. DeleteAllSubDie is the preferred method for deleting all subdies for all
    dies.
    API Status: published
    Args:
        Site:int = 0
    Returns:
        SitesCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("DeleteSubDie",Site)
    return int(rsp[0])

def GetNumSelectedClusters():
    """
    Gets the number of clusters in the map which are selected for probing.
    API Status: published
    Returns:
        SelectedClusters:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetNumSelectedClusters")
    return int(rsp[0])

def GetSelectedClusterCoords(ClusterIndex:int=""):
    """
    Given the index of a selected cluster in the range [1..NumSelectedClusters],
    returns the column and row indices for the selected cluster.
    API Status: published
    Args:
        ClusterIndex:int = 0
    Returns:
        ClusterX:int
        ClusterY:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSelectedClusterCoords",ClusterIndex)
    global GetSelectedClusterCoords_Response
    if not "GetSelectedClusterCoords_Response" in globals(): GetSelectedClusterCoords_Response = namedtuple("GetSelectedClusterCoords_Response", "ClusterX,ClusterY")
    return GetSelectedClusterCoords_Response(int(rsp[0]),int(rsp[1]))

def GetClusterDieStatus(ClusterX:int="", ClusterY:int="", DieX:int="", DieY:int=""):
    """
    Gets the die status in the cluster. Die coordinates are internal for the cluster
    using the wafer map coordinate system. (0,0) die in the cluster is left top
    corner (whether this die exists or not).
    API Status: published
    Args:
        ClusterX:int = 0
        ClusterY:int = 0
        DieX:int = 0
        DieY:int = 0
    Returns:
        Status:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetClusterDieStatus",ClusterX,ClusterY,DieX,DieY)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetClusterDieStatus(ClusterX:int="", ClusterY:int="", DieX:int="", DieY:int="", Status:str=""):
    """
    Sets the die status in the cluster. Die coordinates are internal for the cluster
    using the wafer map coordinate system. (0,0) die in the cluster is left top
    corner (whether this die exists or not).
    API Status: published
    Args:
        ClusterX:int = 0
        ClusterY:int = 0
        DieX:int = 0
        DieY:int = 0
        Status:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetClusterDieStatus",ClusterX,ClusterY,DieX,DieY,Status)


def OpenBinCodeTable(FileName:str=""):
    """
    Opens a Bin Code Table file (.bct) with the specified name.
    API Status: published
    Args:
        FileName:str = ""
    Command Timeout: 240000
    """
    MessageServerInterface.sendSciCommand("OpenBinCodeTable",FileName)


def SaveBinCodeTable(FileName:str=""):
    """
    Saves bin code table to a file with the specified name.
    API Status: published
    Args:
        FileName:str = ""
    Command Timeout: 240000
    """
    MessageServerInterface.sendSciCommand("SaveBinCodeTable",FileName)


def SetBinTableSize(BinsSize:int=""):
    """
    Sets size of the bin code table. This is the size of bins used in statistics and
    binning.
    API Status: published
    Args:
        BinsSize:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetBinTableSize",BinsSize)


def GetBinTableSize():
    """
    Gets size of the bin code table.
    API Status: published
    Returns:
        BinsSize:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetBinTableSize")
    return int(rsp[0])

def StepFailedClusterBack():
    """
    Steps the chuck the consecutive failed clusters back (goes back to the last
    known good cluster) and returns the number of consecutive failed clusters.
    API Status: published
    Returns:
        FailedClusters:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepFailedClusterBack")
    return int(rsp[0])

def StepFailedClusterForward():
    """
    Steps the chuck the consecutive failed clusters forward and returns the number
    of consecutive failed clusters (goes to next untested cluster).
    API Status: published
    Returns:
        FailedClusters:int
    Command Timeout: 6000000
    """
    rsp = MessageServerInterface.sendSciCommand("StepFailedClusterForward")
    return int(rsp[0])

def GoToWaferHome():
    """
    Moves the chuck to the wafer home position.
    API Status: published
    Command Timeout: 6000000
    """
    MessageServerInterface.sendSciCommand("GoToWaferHome")


def GetWaferInfo():
    """
    Returns a number of all units marked to test. Note that TestSites is a number of
    all sites for all dies.
    API Status: published
    Returns:
        ClustersCount:int
        DiesCount:int
        SitesCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferInfo")
    global GetWaferInfo_Response
    if not "GetWaferInfo_Response" in globals(): GetWaferInfo_Response = namedtuple("GetWaferInfo_Response", "ClustersCount,DiesCount,SitesCount")
    return GetWaferInfo_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]))

def GetClusterInfo(Cluster:int=""):
    """
    Returns a number of all dies and sites marked to test in the given cluster.
    API Status: published
    Args:
        Cluster:int = 0
    Returns:
        DiesCount:int
        SitesCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetClusterInfo",Cluster)
    global GetClusterInfo_Response
    if not "GetClusterInfo_Response" in globals(): GetClusterInfo_Response = namedtuple("GetClusterInfo_Response", "DiesCount,SitesCount")
    return GetClusterInfo_Response(int(rsp[0]),int(rsp[1]))

def GetDieInfo(Die:int=""):
    """
    Returns a number of sites marked to test in the given die.
    API Status: published
    Args:
        Die:int = 0
    Returns:
        SitesCount:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieInfo",Die)
    return int(rsp[0])

def ConvertToAlphas(Start:int="", Finish:int=""):
    """
    Returns a string of the alpha column coordinates for the given range divided by
    spaces.
    API Status: published
    Args:
        Start:int = 0
        Finish:int = 0
    Returns:
        Alphas:str
    Command Timeout: 240000
    """
    rsp = MessageServerInterface.sendSciCommand("ConvertToAlphas",Start,Finish)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetActiveLayer(Layer:str=""):
    """
    Sets new active layer.
    API Status: published
    Args:
        Layer:str = ""
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetActiveLayer",Layer)


def GetActiveLayer():
    """
    Returns current active layer.
    API Status: published
    Returns:
        Layer:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetActiveLayer")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetDieRefPoint(RefX:Decimal="", RefY:Decimal=""):
    """
    Sets a new reference point for the die. This point is NOT used for die stepping,
    nor for subdie stepping. When using the "Chuck Position from Reference" WaferMap
    GUI setting, the Die Reference Point can be set to be more representative of the
    actual reference location within the die. A setting of (0.0, 0.0) is defined as
    the upper left corner of the die. All subdie coordinates are relative to upper
    left corner of the die.
    API Status: published
    Args:
        RefX:Decimal = 0
        RefY:Decimal = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieRefPoint",RefX,RefY)


def GetDieRefPoint():
    """
    Returns current reference point for the die. For details see SetDieRefPoint
    command.
    API Status: published
    Returns:
        RefX:Decimal
        RefY:Decimal
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieRefPoint")
    global GetDieRefPoint_Response
    if not "GetDieRefPoint_Response" in globals(): GetDieRefPoint_Response = namedtuple("GetDieRefPoint_Response", "RefX,RefY")
    return GetDieRefPoint_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def ClearAllBins():
    """
    Clears all binning data in the wafer map.
    API Status: published
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("ClearAllBins")


def SetWindowState(State:str="", Window:str=""):
    """
    Has sense in the application only (not for ActiveX controls). It shows or hides
    a window. All parameters are case-insensitive.
    API Status: published
    Args:
        State:str = "s"
        Window:str = "setup"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetWindowState",State,Window)


def SetCurrentBin(Bin:int="", ButtonStatus:int=""):
    """
    Sets the current bin for the application. Second parameter allows to enable or
    disable "Mark with Bin" mode in the application.
    API Status: published
    Args:
        Bin:int = 0
        ButtonStatus:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetCurrentBin",Bin,ButtonStatus)


def GetCurrentBin():
    """
    Returns the current bin in the application.
    API Status: published
    Returns:
        Bin:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetCurrentBin")
    return int(rsp[0])

def ReadClusterPosition(Pos:int="", FromPos:str=""):
    """
    Returns the actual wafer map cluster position. If the cluster probing is
    disabled, the command will assume a cluster of size 1x1.
    API Status: published
    Args:
        Pos:int = 0
        FromPos:str = "R"
    Returns:
        ClusterX:int
        ClusterY:int
        ClusterIndex:int
        DieX:int
        DieY:int
        DieIndex:int
        ClusterWidth:int
        ClusterHeight:int
        EnabledDies:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("ReadClusterPosition",Pos,FromPos)
    global ReadClusterPosition_Response
    if not "ReadClusterPosition_Response" in globals(): ReadClusterPosition_Response = namedtuple("ReadClusterPosition_Response", "ClusterX,ClusterY,ClusterIndex,DieX,DieY,DieIndex,ClusterWidth,ClusterHeight,EnabledDies")
    return ReadClusterPosition_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),str("" if len(rsp) < 9 else ' '.join(rsp[8:])))

def GetWaferMapParams():
    """
    Returns the circle wafer parameters. For this version of the command, units for
    XOffset and YOffset are percentages.
    API Status: published
    Returns:
        Diameter:Decimal
        DieWidth:Decimal
        DieHeight:Decimal
        FlatLength:Decimal
        FlatAngle:int
        XOffset:Decimal
        YOffset:Decimal
        EdgeArea:Decimal
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferMapParams")
    global GetWaferMapParams_Response
    if not "GetWaferMapParams_Response" in globals(): GetWaferMapParams_Response = namedtuple("GetWaferMapParams_Response", "Diameter,DieWidth,DieHeight,FlatLength,FlatAngle,XOffset,YOffset,EdgeArea")
    return GetWaferMapParams_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),int(rsp[4]),Decimal(rsp[5]),Decimal(rsp[6]),Decimal(rsp[7]))

def GetRectMapParams():
    """
    Creates a rectangular wafermap with specified parameters.
    API Status: published
    Returns:
        DieWidth:Decimal
        DieHeight:Decimal
        Columns:int
        Rows:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetRectMapParams")
    global GetRectMapParams_Response
    if not "GetRectMapParams_Response" in globals(): GetRectMapParams_Response = namedtuple("GetRectMapParams_Response", "DieWidth,DieHeight,Columns,Rows")
    return GetRectMapParams_Response(Decimal(rsp[0]),Decimal(rsp[1]),int(rsp[2]),int(rsp[3]))

def SyncMapHome(X:Decimal="", Y:Decimal=""):
    """
    Tries to find an appropriate position in the wafer for the current chuck
    position. X and Y describe the chuck position of the wafer center relatively to
    the chuck zero position. If the wafer position is found the command sets it as
    the wafer map home position and sets the current chuck position as the chuck
    home position. If there is no corresponding wafer position the command returns
    error 701. Command is used by AutoAlign for the BuildMap feature.
    API Status: published
    Args:
        X:Decimal = 0
        Y:Decimal = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SyncMapHome",X,Y)


def SetWaferProfileOptions(ProfileSensor:str="", SearchSpeed:Decimal="", Gap:Decimal="", SuccessRatio:Decimal="", ProfDistX:Decimal="", ProfDistY:Decimal=""):
    """
    Sets some WaferMap profiling options remotely.
    API Status: published
    Args:
        ProfileSensor:str = "e"
        SearchSpeed:Decimal = 50
        Gap:Decimal = 10
        SuccessRatio:Decimal = 75
        ProfDistX:Decimal = 0
        ProfDistY:Decimal = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetWaferProfileOptions",ProfileSensor,SearchSpeed,Gap,SuccessRatio,ProfDistX,ProfDistY)


def GetWaferProfileOptions():
    """
    Returns predefined settings of the WaferMap profiling options.
    API Status: published
    Returns:
        ProfileSensor:str
        SearchSpeed:Decimal
        Gap:Decimal
        SuccessRatio:Decimal
        ProfDistX:Decimal
        ProfDistY:Decimal
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferProfileOptions")
    global GetWaferProfileOptions_Response
    if not "GetWaferProfileOptions_Response" in globals(): GetWaferProfileOptions_Response = namedtuple("GetWaferProfileOptions_Response", "ProfileSensor,SearchSpeed,Gap,SuccessRatio,ProfDistX,ProfDistY")
    return GetWaferProfileOptions_Response(str(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]))

def StartWaferProfiling(DoContinue:int=""):
    """
    Starts the profiling process. To determine the current profiling state, use
    GetWaferProfilingStatus command.
    API Status: published
    Args:
        DoContinue:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("StartWaferProfiling",DoContinue)


def GetWaferProfilingStatus():
    """
    Returns status of the profiling process. If this status is true, the process is
    started.
    API Status: published
    Returns:
        Started:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferProfilingStatus")
    return int(rsp[0])

def StopWaferProfiling():
    """
    Stops the profiling process.
    API Status: published
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("StopWaferProfiling")


def DoWaferProfiling():
    """
    Profiles the wafer and returns a status of the profiling as an error code.
    API Status: published
    Command Timeout: 36000000
    """
    MessageServerInterface.sendSciCommand("DoWaferProfiling")


def DoWaferProfilingOffAxis():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Profiles the wafer and returns a status of the profiling as an error code.
    Executes profiling using the off axis camera
    API Status: internal
    Command Timeout: 36000000
    """
    MessageServerInterface.sendSciCommand("DoWaferProfilingOffAxis")


def GetSubDieLabel(DieX:int="", DieY:int="", Site:int=""):
    """
    Returns a label from the wafer map at the current die and current subdie, unless
    a row, column, and subdie are specified. The SubDie collection is 0-based, the
    first value is 0, not 1.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
        Site:int = 0
    Returns:
        Label:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSubDieLabel",DieX,DieY,Site)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetSubDieLabel(Label:str="", DieX:int="", DieY:int="", Site:int=""):
    """
    Assigns a label to the wafer map at the current die and the current subdie,
    unless a subdie, row, and column are specified. The SubDie collection is
    0-based, the first value is 0, not 1.
    API Status: published
    Args:
        Label:str = ""
        DieX:int = 0
        DieY:int = 0
        Site:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetSubDieLabel",Label,DieX,DieY,Site)


def GetSubDieLabelAsNum(CDieIndex:int="", Site:int=""):
    """
    Returns a label from the wafer map the current die and the current subdie,
    unless a subdie, and die number are specified. The SubDie collection is 0-based,
    the first value is 0, not 1.
    API Status: published
    Args:
        CDieIndex:int = 0
        Site:int = 0
    Returns:
        Label:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSubDieLabelAsNum",CDieIndex,Site)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetSubDieLabelAsNum(Label:str="", CDieIndex:int="", Site:int=""):
    """
    Assigns a label to the wafer map at the current die and the current subdie,
    unless a subdie, and die number are specified. The SubDie collection is 0-based,
    the first value is 0, not 1.
    API Status: published
    Args:
        Label:str = ""
        CDieIndex:int = 0
        Site:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetSubDieLabelAsNum",Label,CDieIndex,Site)


def GetDieLabelAsNum(CDieIndex:int=""):
    """
    Returns a label from the wafer map at the current die, unless a die number is
    specified.
    API Status: published
    Args:
        CDieIndex:int = 0
    Returns:
        Label:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieLabelAsNum",CDieIndex)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetDieLabelAsNum(Label:str="", CDieIndex:int=""):
    """
    Assigns a label to the wafer map at the current die, unless a die number is
    specified.
    API Status: published
    Args:
        Label:str = ""
        CDieIndex:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieLabelAsNum",Label,CDieIndex)


def GetHomeDieOffset():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the XY offset from the reference position of the Home Die to wafer
    center in chuck coordinates.
    API Status: internal
    Returns:
        X:Decimal
        Y:Decimal
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetHomeDieOffset")
    global GetHomeDieOffset_Response
    if not "GetHomeDieOffset_Response" in globals(): GetHomeDieOffset_Response = namedtuple("GetHomeDieOffset_Response", "X,Y")
    return GetHomeDieOffset_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def SetWaferMapParams2(Diameter:Decimal="", DieWidth:Decimal="", DieHeight:Decimal="", FlatLength:Decimal="", FlatAngle:int="", XOffset:Decimal="", YOffset:Decimal="", EdgeArea:Decimal=""):
    """
    Creates the circle wafer with specified parameters. If parameter is omitted,
    then zero is used. For this version of the command, units for XOffset and
    YOffset are microns.
    API Status: published
    Args:
        Diameter:Decimal = 200
        DieWidth:Decimal = 10000
        DieHeight:Decimal = 10000
        FlatLength:Decimal = 20
        FlatAngle:int = 0
        XOffset:Decimal = 0
        YOffset:Decimal = 0
        EdgeArea:Decimal = 0
    Command Timeout: 240000
    """
    MessageServerInterface.sendSciCommand("SetWaferMapParams2",Diameter,DieWidth,DieHeight,FlatLength,FlatAngle,XOffset,YOffset,EdgeArea)


def GetWaferMapParams2():
    """
    Returns the circle wafer parameters. For this version of the command, units for
    XOffset and YOffset are microns.
    API Status: published
    Returns:
        Diameter:Decimal
        DieWidth:Decimal
        DieHeight:Decimal
        FlatLength:Decimal
        FlatAngle:int
        XOffset:Decimal
        YOffset:Decimal
        EdgeArea:Decimal
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferMapParams2")
    global GetWaferMapParams2_Response
    if not "GetWaferMapParams2_Response" in globals(): GetWaferMapParams2_Response = namedtuple("GetWaferMapParams2_Response", "Diameter,DieWidth,DieHeight,FlatLength,FlatAngle,XOffset,YOffset,EdgeArea")
    return GetWaferMapParams2_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),int(rsp[4]),Decimal(rsp[5]),Decimal(rsp[6]),Decimal(rsp[7]))

def SetWaferTestAngle(Angle:int=""):
    """
    This command sets the Wafer Test Angle. This is different from the notch angle
    and allows rotating the WaferMap.
    API Status: published
    Args:
        Angle:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetWaferTestAngle",Angle)


def GetWaferTestAngle():
    """
    This returns the Wafer Test Angle. This is different from the notch angle and
    allows rotating the WaferMap.
    API Status: published
    Returns:
        Angle:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferTestAngle")
    return int(rsp[0])

def LoadPreMappedDiesTable(FileName:str="", ClearMap:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Loads the Pre-Mapped Dies Table file with specified name.
    API Status: internal
    Args:
        FileName:str = ""
        ClearMap:int = 1
    Command Timeout: 240000
    """
    MessageServerInterface.sendSciCommand("LoadPreMappedDiesTable",FileName,ClearMap)


def GetPreMappedDieInfo(DieX:int="", DieY:int=""):
    """
    This command is valid when a PreMapped Dies Table has been loaded. Returns
    values at the current die, unless a column (M_pnDieX) and row (M_pnDieY) are
    specified.  Returns actual (as measured during the Pre-Mapping) x, y, z, and
    theta die positions. Also returns whether or not Z and Theta are being used.
    This command is only valid when a Pre-Mapped Dies Table has been loaded. If a
    PreMapped Dies Table has NOT been loaded, ERR_IllegalParameters (715) is
    returned.
    API Status: published
    Args:
        DieX:int = 0
        DieY:int = 0
    Returns:
        UseZ:int
        UseTheta:int
        ActualX:Decimal
        ActualY:Decimal
        ActualZ:Decimal
        Theta:Decimal
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetPreMappedDieInfo",DieX,DieY)
    global GetPreMappedDieInfo_Response
    if not "GetPreMappedDieInfo_Response" in globals(): GetPreMappedDieInfo_Response = namedtuple("GetPreMappedDieInfo_Response", "UseZ,UseTheta,ActualX,ActualY,ActualZ,Theta")
    return GetPreMappedDieInfo_Response(int(rsp[0]),int(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]))

def GetDieResultAsNum(CDieIndex:int=""):
    """
    Returns a measurement result from the wafer map at the current die, unless a die
    number is specified.
    API Status: published
    Args:
        CDieIndex:int = 0
    Returns:
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieResultAsNum",CDieIndex)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetDieResultAsNum(Result:str="", CDieIndex:int=""):
    """
    Assigns a measurement result to the wafer map at the current die, unless a die
    number is specified.
    API Status: published
    Args:
        Result:str = ""
        CDieIndex:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieResultAsNum",Result,CDieIndex)


def GetDieMapResultAsNum(CDieIndex:int="", Site:int=""):
    """
    Returns a measurement result from the wafer map the current die and the current
    subdie, unless a subdie, and die number are specified. The SubDie collection is
    0-based, the first value is 0, not 1.
    API Status: published
    Args:
        CDieIndex:int = 0
        Site:int = 0
    Returns:
        Result:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetDieMapResultAsNum",CDieIndex,Site)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetDieMapResultAsNum(Result:str="", CDieIndex:int="", Site:int=""):
    """
    Assigns a measurement result to the wafer die map at the current die at the
    current subdie, unless a subdie, and die number are specified. The SubDie
    collection is 0-based, the first value is 0, not 1.
    API Status: published
    Args:
        Result:str = ""
        CDieIndex:int = 0
        Site:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetDieMapResultAsNum",Result,CDieIndex,Site)


def MapEdgeDies(Enable:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Enables or disables edge dies for test
    API Status: internal
    Args:
        Enable:int = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("MapEdgeDies",Enable)


def GetSpectrumData(DataPath:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Allows access to read any data item in Spectrum explorer.     GetSpectrumData
    AlignWafer/ProjectData/Mark1/ChuckPosition/X     GetSpectrumData Chuck
    Camera/Camera Settings/Shutter
    API Status: internal
    Args:
        DataPath:str = ""
    Returns:
        Value:str
    Command Timeout: 6000
    Example:GetSpectrumData Chuck Camera/Camera Settings/Shutter
    """
    rsp = MessageServerInterface.sendSciCommand("GetSpectrumData",DataPath)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetSpectrumData(PathAndValue:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Allows changing any data item in Spectrum explorer. Works independent of access
    level. SetSpectrumData AlignWafer/ProjectData/Mark1/ChuckPosition/X=1000
    SetSpectrumData Chuck Camera/Camera Settings/Shutter=17
    API Status: internal
    Args:
        PathAndValue:str = ""
    Command Timeout: 6000
    Example:SetSpectrumData Scope Camera/Camera Settings/Shutter=17
    """
    MessageServerInterface.sendSciCommand("SetSpectrumData",PathAndValue)


def ReadVMPosition(ToolName:str="", XY:int="", Z:int="", Model:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command reads the current chuck and microscope position and sets them as
    new model or chuck and microscope positions.     The command was originally used
    by ReAlignWizard but may be removed in the future because of direct access to
    tooldata     within Spectrum.
    API Status: internal
    Args:
        ToolName:str = ""
        XY:int = 1
        Z:int = 0
        Model:int = -1
    Command Timeout: 60000
    Example:ReadVMPosition AlignWafer 1 0 0
    """
    MessageServerInterface.sendSciCommand("ReadVMPosition",ToolName,XY,Z,Model)


def MoveToVMPosition(ToolName:str="", XYChuck:int="", ZChuck:int="", XYScope:int="", ZScope:int="", Model:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command moves to trained stages positions of a requested tool. Command is
    used by ReAlignWizard to move to     the trained positions for AutoAlign and
    DetectWaferHeight.
    API Status: internal
    Args:
        ToolName:str = ""
        XYChuck:int = 1
        ZChuck:int = 1
        XYScope:int = 0
        ZScope:int = 0
        Model:int = -1
    Command Timeout: 120000
    Example:MoveToVMPosition AlignWafer 1 0 0 0 0
    """
    MessageServerInterface.sendSciCommand("MoveToVMPosition",ToolName,XYChuck,ZChuck,XYScope,ZScope,Model)


def ShapeTracker(SetHome:int="", AutoEdgeFind:int="", FileName:str=""):
    """
    ShapeTracker automatically tracks the shape of a substrate (e.g. a broken wafer)
    to determine the contour of it. The data will be memorized as xy coordinates of
    contour points referenced to the home position. These Points are written to a
    file after tracking the shape.
    API Status: published
    Args:
        SetHome:int = 1
        AutoEdgeFind:int = 0
        FileName:str = ""
    Command Timeout: 600000
    Example:ShapeTracker 1
    """
    MessageServerInterface.sendSciCommand("ShapeTracker",SetHome,AutoEdgeFind,FileName)


def DetectWaferHeight(SetStartPosition:int="", Synchronize:int="", ChuckX:Decimal="", ChuckY:Decimal=""):
    """
    Synchronizes chuck and top camera in X, Y and Z. Then the wafer surface is
    focused on the trained chuck position or the manual adjusted reference position.
    This tool uses the FindFocus tool with its own Range.
    API Status: published
    Args:
        SetStartPosition:int = 0
        Synchronize:int = 0
        ChuckX:Decimal = -1
        ChuckY:Decimal = -1
    Returns:
        PositionX:Decimal
        PositionY:Decimal
        WaferHeight:Decimal
        SynchGap:Decimal
        ZOffset:Decimal
        Stage:str
    Command Timeout: 300000
    Example:DetectWaferHeight 0 1
    """
    rsp = MessageServerInterface.sendSciCommand("DetectWaferHeight",SetStartPosition,Synchronize,ChuckX,ChuckY)
    global DetectWaferHeight_Response
    if not "DetectWaferHeight_Response" in globals(): DetectWaferHeight_Response = namedtuple("DetectWaferHeight_Response", "PositionX,PositionY,WaferHeight,SynchGap,ZOffset,Stage")
    return DetectWaferHeight_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),str("" if len(rsp) < 6 else ' '.join(rsp[5:])))

def CheckSpectrumPlugin(Plugin:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command checks if a plugin is trained and returns a string of error/warning
    messages including information about what is not trained, setup for the tool to
    run.
    API Status: internal
    Args:
        Plugin:str = ""
    Returns:
        PluginAvailable:int
        Message:str
    Command Timeout: 1000
    Example:CheckSpectrumPlugin AlignWafer
    """
    rsp = MessageServerInterface.sendSciCommand("CheckSpectrumPlugin",Plugin)
    global CheckSpectrumPlugin_Response
    if not "CheckSpectrumPlugin_Response" in globals(): CheckSpectrumPlugin_Response = namedtuple("CheckSpectrumPlugin_Response", "PluginAvailable,Message")
    return CheckSpectrumPlugin_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def AutoAlign(SetValue:int="", SkipSettingHome:int=""):
    """
    Executes the AutoAlign tool to do a theta alignment of the wafer with optional
    index calculation or thermal expansion measurement. The command will update home
    if home was trained. It will only move to its trained chuck/scope position
    before starting the alignment if the option "MoveToTrainedXYPosition" and/or
    "MoveToTrainedZPosition" is true.
    API Status: published
    Args:
        SetValue:int = 0
        SkipSettingHome:int = 0
    Command Timeout: 300000
    Example:AutoAlign 1
    """
    MessageServerInterface.sendSciCommand("AutoAlign",SetValue,SkipSettingHome)


def SetCameraQuiet(Active:int=""):
    """
    Activates/deactivates the camera quiet mode. (Applies only to ATM300A and
    SPS300/SUMMIT200 stations.)     The camera quiet mode deactivates the chuck,
    platen and contact view camera and triggers a digital output     which
    connects/disconnects these cameras firewire connection to the PC.
    API Status: published
    Args:
        Active:int = 0
    Command Timeout: 30000
    Example:SetCameraQuiet 1
    """
    MessageServerInterface.sendSciCommand("SetCameraQuiet",Active)


def SetRefDieOffset(RefDieCol:int="", RefDieRow:int="", RefDieDistToCentreX:Decimal="", RefDieDistToCentreY:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command is based on the SetMapOrientation command. It allows shifting the
    center of the reference die to the center of the wafer.
    API Status: internal
    Args:
        RefDieCol:int = 0
        RefDieRow:int = 0
        RefDieDistToCentreX:Decimal = 0
        RefDieDistToCentreY:Decimal = 0
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetRefDieOffset",RefDieCol,RefDieRow,RefDieDistToCentreX,RefDieDistToCentreY)


def AlignWafer(TrackPosition:int=""):
    """
    Performs a two-point alignment and moves chuck to the trained align position. XY
    correction is made afterwards to calculate the new home position.
    API Status: published
    Args:
        TrackPosition:int = 0
    Returns:
        ThetaOffset:Decimal
    Command Timeout: 120000
    Example:AlignWafer
    """
    rsp = MessageServerInterface.sendSciCommand("AlignWafer",TrackPosition)
    return Decimal(rsp[0])

def AlignChip():
    """
    Performs a single or two point alignment and moves the current chip to the
    trained aligned position in Theta (in degrees) and X, Y (in microns). The
    current chip is assumed to be in the region of interest when the command is
    called.
    API Status: published
    Returns:
        ThetaOffset:Decimal
        XOffset:Decimal
        YOffset:Decimal
    Command Timeout: 180000
    Example:AlignChip
    """
    rsp = MessageServerInterface.sendSciCommand("AlignChip")
    global AlignChip_Response
    if not "AlignChip_Response" in globals(): AlignChip_Response = namedtuple("AlignChip_Response", "ThetaOffset,XOffset,YOffset")
    return AlignChip_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def FindFocus(StepCount:int="", Range:Decimal=""):
    """
    Determines the Z axis position where an object in the region of interest is in
    focus. First output parameter is the Z axis value in microns from zero of the
    new focus height. Second output parameter is the used stage to perform focus
    search.
    API Status: published
    Args:
        StepCount:int = -1
        Range:Decimal = -1
    Returns:
        ZPosition:Decimal
        Stage:str
    Command Timeout: 120000
    Example:FindFocus 50 500
    """
    rsp = MessageServerInterface.sendSciCommand("FindFocus",StepCount,Range)
    global FindFocus_Response
    if not "FindFocus_Response" in globals(): FindFocus_Response = namedtuple("FindFocus_Response", "ZPosition,Stage")
    return FindFocus_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def AlignAux(AuxSiteID:int=""):
    """
    Performs an automated aux site alignment in XYZ. Tool can correct reference
    position and contact height for the given aux site.
    API Status: published
    Args:
        AuxSiteID:int = 0
    Command Timeout: 300000
    Example:AlignAux 1
    """
    MessageServerInterface.sendSciCommand("AlignAux",AuxSiteID)


def FindFeature(Model:int="", ReturnDistanceFromModelOrigin:int="", UseSingleImageAcquisition:int=""):
    """
    Search user-defined models. Up to 40 different models can be trained. After
    training, these models can be searched on screen either by direct user
    interaction or from external applications with a remote command. The remote
    command returns the X/Y-Positions, angle (degree) and score value (0 - 1.0) for
    each instance of the model found in the region of interest.
    API Status: published
    Args:
        Model:int = 1
        ReturnDistanceFromModelOrigin:int = 0
        UseSingleImageAcquisition:int = 1
    Returns:
        Data:str
    Command Timeout: 10000
    Example:FindFeature 1
    """
    rsp = MessageServerInterface.sendSciCommand("FindFeature",Model,ReturnDistanceFromModelOrigin,UseSingleImageAcquisition)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def CloseSpectrum():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    CloseSpectrum closes the Spectrum application. Used internally by CommonCommands
    during Project loading. Does save configuration data but does not save project
    data.
    API Status: internal
    Command Timeout: 6000
    Example:CloseSpectrum
    """
    MessageServerInterface.sendSciCommand("CloseSpectrum")


def SnapImage(MountPos:str="", FullPath:str="", SnapShotMode:int=""):
    """
    Saves the currently displayed image to the specified file. The image is stored
    in the requested file format (bmp, jpg or png). By default. it will save the raw
    camera image and an image with the overlays that are currently visible on the
    camera view. Using a parameter, one can decide to only save either raw image,
    overlay image or both. By Specifying 'ALL' as the mount position, the captured
    screenshot will consist of the currently selected camera layout without
    providing the raw image. If MountPos and FullPath are empty then the current
    camera view with overlays is copied to the clipboard.
    API Status: published
    Args:
        MountPos:str = "Scope"
        FullPath:str = "Image.bmp"
        SnapShotMode:int = 2
    Command Timeout: 60000
    Example:SnapImage Scope C:/Temp/Image.bmp
    """
    MessageServerInterface.sendSciCommand("SnapImage",MountPos,FullPath,SnapShotMode)


def SetCameraView(Name:str="", Zoom:int="", LiveVideo:int="", WindowState:int=""):
    """
    Switches the desired video window of Spectrum as foreground and active view. The
    camera view can be determined over a tool name or the camera mount position. The
    second parameter defines the displays zoom factor to be used. Third parameter is
    used to toogle the live video. Last parameter can be used to maximize a window.
    API Status: published
    Args:
        Name:str = ""
        Zoom:int = 0
        LiveVideo:int = 2
        WindowState:int = 1
    Command Timeout: 6000
    Example:SetCameraView AlignWafer 0 2 2
    """
    MessageServerInterface.sendSciCommand("SetCameraView",Name,Zoom,LiveVideo,WindowState)


def SetCameraLight(Name:str="", State:int="", Shutter:Decimal="", Gain:Decimal="", Brightness:int="", Contrast:int="", Sharpness:int="", Illumination:int=""):
    """
    Switches the light of the choosen camera on or off. Light values of -1 will
    cause that the parameter is not affected.
    API Status: published
    Args:
        Name:str = ""
        State:int = 0
        Shutter:Decimal = -1
        Gain:Decimal = -1
        Brightness:int = -1
        Contrast:int = -1
        Sharpness:int = -1
        Illumination:int = -1
    Command Timeout: 6000
    Example:SetCameraLight AlignWafer 1 20 5
    """
    MessageServerInterface.sendSciCommand("SetCameraLight",Name,State,Shutter,Gain,Brightness,Contrast,Sharpness,Illumination)


def ShowWizard(ToolName:str="", MountPosition:str="", AskExecute:int=""):
    """
    Starts the wizard of a given tool on the display defined in the tool settings.
    Additionally it can start a wizard for training single models with the syntax
    e.g. ShowWizard FindFeature/ProjectData/Features/Feature1/Model For the tools
    MeasureOnScreen, Calibrate and CameraOrigin you can specify a mount position
    e.g. ShowWizard Calibrate Platen
    API Status: published
    Args:
        ToolName:str = ""
        MountPosition:str = ""
        AskExecute:int = 0
    Returns:
        Cancelled:int
    Command Timeout: 10000000
    Example:ShowWizard AlignWafer
    """
    rsp = MessageServerInterface.sendSciCommand("ShowWizard",ToolName,MountPosition,AskExecute)
    return int(rsp[0])

def ProbeToPadAlign(Position:str=""):
    """
    Sets a new Home position. The command is used during ReAlign to search the
    trained home reference model and to calculate the new xy home position.
    API Status: published
    Args:
        Position:str = "H"
    Returns:
        XOffsetWafer:Decimal
        YOffsetWafer:Decimal
    Command Timeout: 120000
    Example:ProbeToPadAlign H
    """
    rsp = MessageServerInterface.sendSciCommand("ProbeToPadAlign",Position)
    global ProbeToPadAlign_Response
    if not "ProbeToPadAlign_Response" in globals(): ProbeToPadAlign_Response = namedtuple("ProbeToPadAlign_Response", "XOffsetWafer,YOffsetWafer")
    return ProbeToPadAlign_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def ReadOcrString():
    """
    Reads the wafer ID string from the wafer's surface. Returns the read ID as
    string. Requires IDTools license.
    API Status: published
    Returns:
        OcrString:str
    Command Timeout: 60000
    Example:ReadOcrString
    """
    rsp = MessageServerInterface.sendSciCommand("ReadOcrString")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ReadBarCode():
    """
    Reads the wafers barcode and decodes it to a string. Requires IDTools license.
    API Status: published
    Returns:
        BarCodeString:str
    Command Timeout: 60000
    Example:ReadBarCode
    """
    rsp = MessageServerInterface.sendSciCommand("ReadBarCode")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def Read2DMatrixCode():
    """
    Reads the wafers matrix code and decodes it to a string. Requires IDTools
    license.
    API Status: published
    Returns:
        MatrixCodeString:str
    Command Timeout: 60000
    Example:Read2DMatrixCode
    """
    rsp = MessageServerInterface.sendSciCommand("Read2DMatrixCode")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetSpectrumRemote(Activate:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Activates the Spectrum remote mode. In this mode all user interface elements are
    hidden and disabled. This is used when Spectrum is hosted inside VeloxPro.
    API Status: internal
    Args:
        Activate:int = 1
    Command Timeout: 10000
    Example:SetSpectrumRemote 1
    """
    MessageServerInterface.sendSciCommand("SetSpectrumRemote",Activate)


def GetCameraLight(Name:str=""):
    """
    Returns light properties of choosen camera.
    API Status: published
    Args:
        Name:str = ""
    Returns:
        MountPosition:str
        State:int
        Shutter:Decimal
        Gain:Decimal
        Brightness:int
        Contrast:int
        Sharpness:int
        Illumination:int
    Command Timeout: 6000
    Example:GetCameraLight Scope
    """
    rsp = MessageServerInterface.sendSciCommand("GetCameraLight",Name)
    global GetCameraLight_Response
    if not "GetCameraLight_Response" in globals(): GetCameraLight_Response = namedtuple("GetCameraLight_Response", "MountPosition,State,Shutter,Gain,Brightness,Contrast,Sharpness,Illumination")
    return GetCameraLight_Response(str(rsp[0]),int(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]))

def GetCameraView(Name:str=""):
    """
    Returns the present camera view state of a desired tool or active view.
    API Status: published
    Args:
        Name:str = ""
    Returns:
        MountPosition:str
        Zoom:int
        LiveVideo:int
        WindowState:int
    Command Timeout: 6000
    Example:GetCameraView AlignWafer
    """
    rsp = MessageServerInterface.sendSciCommand("GetCameraView",Name)
    global GetCameraView_Response
    if not "GetCameraView_Response" in globals(): GetCameraView_Response = namedtuple("GetCameraView_Response", "MountPosition,Zoom,LiveVideo,WindowState")
    return GetCameraView_Response(str(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def GetPattern(ToolName:str="", ModelName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Transforms the specific model of a demanded tool into a bitmap. This bitmap will
    be stored in the same folder as the project file.     The command was originally
    required by ReAlignWizard and is currently no longer in use.
    API Status: internal
    Args:
        ToolName:str = ""
        ModelName:str = ""
    Returns:
        BitmapPath:str
    Command Timeout: 30000
    Example:GetPattern AlignWafer Model1
    """
    rsp = MessageServerInterface.sendSciCommand("GetPattern",ToolName,ModelName)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ShowPosition(MountPosition:str="", DistPositionX:Decimal="", DistPositionY:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the ChuckCenter under a given camera. When no camera mount position is
    given, Spectrum uses active view. If there is an Offset different from zero,
    this position will be moved under the camera.
    API Status: internal
    Args:
        MountPosition:str = ""
        DistPositionX:Decimal = 0
        DistPositionY:Decimal = 0
    Command Timeout: 60000
    Example:ShowPosition Scope
    """
    MessageServerInterface.sendSciCommand("ShowPosition",MountPosition,DistPositionX,DistPositionY)


def GetCameraHomePosition():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the home die coordinates when the home die is under the alignment camera
    (for instance, the top camera).     Command was used during TrainReAlign to get
    the start position for Z-Profiling. Command is no longer used.
    API Status: internal
    Returns:
        XPosition:Decimal
        YPosition:Decimal
        ZPosition:Decimal
    Command Timeout: 6000
    Example:GetCameraHomePosition
    """
    rsp = MessageServerInterface.sendSciCommand("GetCameraHomePosition")
    global GetCameraHomePosition_Response
    if not "GetCameraHomePosition_Response" in globals(): GetCameraHomePosition_Response = namedtuple("GetCameraHomePosition_Response", "XPosition,YPosition,ZPosition")
    return GetCameraHomePosition_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def SynchronizeCamera(MountPos:str="", SynchronizeXY:int="", SynchronizeZ:int=""):
    """
    Synchronizes the Platen camera with the calibration mark. The mark is mounted on
    the chuck camera. The chuck must be moved to get the mark in view of the
    specified camera.
    API Status: published
    Args:
        MountPos:str = "Scope"
        SynchronizeXY:int = 0
        SynchronizeZ:int = 0
    Returns:
        XPosition:Decimal
        YPosition:Decimal
        ZPosition:Decimal
    Command Timeout: 120000
    Example:SynchronizeCamera S 1 1
    """
    rsp = MessageServerInterface.sendSciCommand("SynchronizeCamera",MountPos,SynchronizeXY,SynchronizeZ)
    global SynchronizeCamera_Response
    if not "SynchronizeCamera_Response" in globals(): SynchronizeCamera_Response = namedtuple("SynchronizeCamera_Response", "XPosition,YPosition,ZPosition")
    return SynchronizeCamera_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def ProbeCardOCS(UpdateZ:int="", MeasureBothGroups:int=""):
    """
    Determines the chuck XYZ axis position where the needles of the probe card are
    in focus. The output parameter is the Z axis value in microns from zero of the
    new focus height.
    API Status: published
    Args:
        UpdateZ:int = 1
        MeasureBothGroups:int = 1
    Returns:
        ZPosition:Decimal
    Command Timeout: 360000
    Example:ProbeCardOCS 1
    """
    rsp = MessageServerInterface.sendSciCommand("ProbeCardOCS",UpdateZ,MeasureBothGroups)
    return Decimal(rsp[0])

def MoveChuckAutoXY(XPosition:Decimal="", YPosition:Decimal="", XSubsiteOffset:Decimal="", YSubsiteOffset:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command is sent by WaferMap to trigger AutoXY, AutoZ or VueTrack for each die
    move. Automation must be activated/trained before command can be used. Response
    is X, Y relative distance of adjustment from requested position.
    API Status: internal
    Args:
        XPosition:Decimal = 0
        YPosition:Decimal = 0
        XSubsiteOffset:Decimal = 0
        YSubsiteOffset:Decimal = 0
    Returns:
        XOffset:Decimal
        YOffset:Decimal
    Command Timeout: 6000000
    Example:MoveChuckAutoXY 5000 10000
    """
    rsp = MessageServerInterface.sendSciCommand("MoveChuckAutoXY",XPosition,YPosition,XSubsiteOffset,YSubsiteOffset)
    global MoveChuckAutoXY_Response
    if not "MoveChuckAutoXY_Response" in globals(): MoveChuckAutoXY_Response = namedtuple("MoveChuckAutoXY_Response", "XOffset,YOffset")
    return MoveChuckAutoXY_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def VueTrackAlign(FullVueTrackAlign:int=""):
    """
    Alignment for the next wafer when using VueTrack.
    API Status: published
    Args:
        FullVueTrackAlign:int = 1
    Command Timeout: 6000000
    Example:VueTrackAlign
    """
    MessageServerInterface.sendSciCommand("VueTrackAlign",FullVueTrackAlign)


def AutoFocusEVue(DistBelow:Decimal="", DistAbove:Decimal="", XOffsetCenter:int="", YOffsetCenter:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command is only used internally for software testing and for providing backwards
    compatibility with SCPI legacy commands. It executes a focus search using the
    eVue focus drive.
    API Status: internal
    Args:
        DistBelow:Decimal = 0
        DistAbove:Decimal = 0
        XOffsetCenter:int = 0
        YOffsetCenter:int = 0
    Returns:
        FocusScore:Decimal
        ZPosition:Decimal
    Command Timeout: 30000
    Example:AutoFocusEVue 200 200 0 0
    """
    rsp = MessageServerInterface.sendSciCommand("AutoFocusEVue",DistBelow,DistAbove,XOffsetCenter,YOffsetCenter)
    global AutoFocusEVue_Response
    if not "AutoFocusEVue_Response" in globals(): AutoFocusEVue_Response = namedtuple("AutoFocusEVue_Response", "FocusScore,ZPosition")
    return AutoFocusEVue_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def AutoAlignOffAxis(SetValue:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Executes the ReAlign Wafer Alignment tool to do a theta alignment of the wafer
    with optional index calculation or thermal expansion measurement. AutoAlign is
    performed using the Platen camera. Only supported for systems with off-axis
    camera.
    API Status: internal
    Args:
        SetValue:int = 0
    Command Timeout: 300000
    Example:AutoAlignOffAxis 1
    """
    MessageServerInterface.sendSciCommand("AutoAlignOffAxis",SetValue)


def FindFocusOffAxis(StepCount:int="", Range:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Determines the Z axis position where an object in the region of interest is in
    focus. First output parameter is the Z axis value in microns from zero of the
    new focus height. Second output parameter is the used stage to perform focus
    search. Focus search is performed using the Platen camera. Only supported for
    systems with off-axis camera.
    API Status: internal
    Args:
        StepCount:int = -1
        Range:Decimal = -1
    Returns:
        ZPosition:Decimal
        Stage:str
    Command Timeout: 120000
    Example:FindFocusOffAxis 50 500
    """
    rsp = MessageServerInterface.sendSciCommand("FindFocusOffAxis",StepCount,Range)
    global FindFocusOffAxis_Response
    if not "FindFocusOffAxis_Response" in globals(): FindFocusOffAxis_Response = namedtuple("FindFocusOffAxis_Response", "ZPosition,Stage")
    return FindFocusOffAxis_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def AlignAuxOffAxis(AuxSiteID:int=""):
    """
    Performs an automated aux site alignment in XYZ using the Off Axis camera. Tool
    can correct reference position and contact height for the given aux site.
    API Status: published
    Args:
        AuxSiteID:int = 0
    Command Timeout: 300000
    Example:AlignAuxOffAxis 1
    """
    MessageServerInterface.sendSciCommand("AlignAuxOffAxis",AuxSiteID)


def FindFocusPlaten(StepCount:int="", Range:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Determines the Z axis position where an object in the region of interest is in
    focus. First output parameter is the Z axis value in microns from zero of the
    new focus height. Second output parameter is the used stage to perform focus
    search. Uses the FindFocus tool settings but always the Platen camera -
    independent of the FindFocus mount. This command is used on e.g. BlueRay systems
    that have a platen camera but can't use ReAlign/DetectWaferHeight as they don't
    have an upward looking camera.
    API Status: internal
    Args:
        StepCount:int = -1
        Range:Decimal = -1
    Returns:
        ZPosition:Decimal
        Stage:str
    Command Timeout: 120000
    Example:FindFocusPlaten 50 500
    """
    rsp = MessageServerInterface.sendSciCommand("FindFocusPlaten",StepCount,Range)
    global FindFocusPlaten_Response
    if not "FindFocusPlaten_Response" in globals(): FindFocusPlaten_Response = namedtuple("FindFocusPlaten_Response", "ZPosition,Stage")
    return FindFocusPlaten_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def AlignChipOffAxis():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Performs a single or two point alignment and moves the current chip to the
    trained aligned position in Theta (in degrees) and X, Y (in microns). This
    command is using the off axis platen camera with functionality of ReAlign.
    API Status: internal
    Returns:
        ThetaOffset:Decimal
        XOffset:Decimal
        YOffset:Decimal
    Command Timeout: 180000
    Example:AlignChipOffAxis
    """
    rsp = MessageServerInterface.sendSciCommand("AlignChipOffAxis")
    global AlignChipOffAxis_Response
    if not "AlignChipOffAxis_Response" in globals(): AlignChipOffAxis_Response = namedtuple("AlignChipOffAxis_Response", "ThetaOffset,XOffset,YOffset")
    return AlignChipOffAxis_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def SelectAZoomLens(Lens:int=""):
    """
    Selects 1 of 4 symbolic lenses (4 classified coarse ranges).
    API Status: published
    Args:
        Lens:int = 1
    Command Timeout: 10000
    Example:SelectAZoomLens 1
    """
    MessageServerInterface.sendSciCommand("SelectAZoomLens",Lens)


def GetAZoomLens():
    """
    Returns 1 of 4 symbolic lenses, coarse ranges.
    API Status: published
    Returns:
        Lens:int
    Command Timeout: 5000
    Example:GetAZoomLens
    """
    rsp = MessageServerInterface.sendSciCommand("GetAZoomLens")
    return int(rsp[0])

def AZoomSetupDialog():
    """
    Opens the operator panel. In this window you can change the settings for all
    defined lenses.
    API Status: published
    Command Timeout: 5000
    Example:AZoomSetupDialog
    """
    MessageServerInterface.sendSciCommand("AZoomSetupDialog")


def MoveAZoomFocus(Focus:int="", Ref:str=""):
    """
    Changes the focus magnitude.
    API Status: published
    Args:
        Focus:int = 100
        Ref:str = "R"
    Returns:
        RetFocus:int
    Command Timeout: 10000
    Example:MoveAZoomFocus 100
    """
    rsp = MessageServerInterface.sendSciCommand("MoveAZoomFocus",Focus,Ref)
    return int(rsp[0])

def ReadAZoomFocus():
    """
    Returns the focus magnitude.
    API Status: published
    Returns:
        Focus:int
    Command Timeout: 5000
    Example:ReadAZoomFocus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadAZoomFocus")
    return int(rsp[0])

def MoveAZoomVelocity(Direction:str="", Velocity:int=""):
    """
    Moves the A-Zoom using the set focus speed.
    API Status: published
    Args:
        Direction:str = ""
        Velocity:int = 100
    Returns:
        RetVelocity:Decimal
    Command Timeout: 240000
    Example:MoveAZoomVelocity + 67
    """
    rsp = MessageServerInterface.sendSciCommand("MoveAZoomVelocity",Direction,Velocity)
    return Decimal(rsp[0])

def StopAZoom():
    """
    Stops the A-Zoom movements.
    API Status: published
    Command Timeout: 5000
    Example:StopAZoom
    """
    MessageServerInterface.sendSciCommand("StopAZoom")


def SetAZoomLight(Light:int=""):
    """
    Switches all lights ON or OFF. ON means the values defined by the current lens.
    1 switches the light on, 0 switches the light off. Without parameter toggles
    between on an off.
    API Status: published
    Args:
        Light:int = 0
    Command Timeout: 5000
    Example:SetAZoomLight 1
    """
    MessageServerInterface.sendSciCommand("SetAZoomLight",Light)


def CloseAZoom():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Closes the OpticalControl application. Used during Project File handling.
    API Status: internal
    Command Timeout: 5000
    Example:CloseAZoom
    """
    MessageServerInterface.sendSciCommand("CloseAZoom")


def OCLightVal(Value:int="", Channel:int="", Segment:int=""):
    """
    Set the brightness of given channel and segment to the given value.
    API Status: published
    Args:
        Value:int = 0
        Channel:int = 1
        Segment:int = 1
    Command Timeout: 5000
    Example:OCLightVal 128 1 4
    """
    MessageServerInterface.sendSciCommand("OCLightVal",Value,Channel,Segment)


def OCLightOn(On:int="", Channel:int=""):
    """
    Switch the light (if it has segments then all) in a given channel ON or OFF.
    Switch ON - that means: light to the before adjusted brightness.
    API Status: published
    Args:
        On:int = 0
        Channel:int = 1
    Command Timeout: 5000
    Example:OCLightOn 1 1
    """
    MessageServerInterface.sendSciCommand("OCLightOn",On,Channel)


def OCSetZoomLevel(Zoom:int="", Motor:int=""):
    """
    Set logical zoom factor for given motor (if has more then one, else to the one)
    API Status: published
    Args:
        Zoom:int = 0
        Motor:int = 1
    Command Timeout: 5000
    Example:OCSetZoomLevel 50 1
    """
    MessageServerInterface.sendSciCommand("OCSetZoomLevel",Zoom,Motor)


def OCGetZoomLevel(Motor:int=""):
    """
    Get logical zoom factor for given motor (if has more then one, else to the one)
    API Status: published
    Args:
        Motor:int = 1
    Returns:
        Zoom:int
    Command Timeout: 5000
    Example:OCGetZoomLevel 1
    """
    rsp = MessageServerInterface.sendSciCommand("OCGetZoomLevel",Motor)
    return int(rsp[0])

def StartReAlignTemperature(TargetTemperature:Decimal="", ThetaAlignOnFinish:int="", ContactOnFinish:int=""):
    """
    Starts temperature ramping using ReAlign. ReAlign will re-adjust the probes and
    wafer during ramping to the new target temperature. Command returns immediately.
    API Status: published
    Args:
        TargetTemperature:Decimal = 0
        ThetaAlignOnFinish:int = 0
        ContactOnFinish:int = 0
    Command Timeout: 5000
    Example:StartReAlignTemperature 150
    """
    MessageServerInterface.sendSciCommand("StartReAlignTemperature",TargetTemperature,ThetaAlignOnFinish,ContactOnFinish)


def StopReAlignTemperature():
    """
    Stops temperature ramping using ReAlign.
    API Status: published
    Command Timeout: 10000
    Example:StopReAlignTemperature
    """
    MessageServerInterface.sendSciCommand("StopReAlignTemperature")


def GetReAlignTemperatureStatus():
    """
    Returns the status of the current temperature ramping using ReAlign process.
    API Status: published
    Returns:
        StatusId:int
        StatusStr:str
    Command Timeout: 300000
    Example:GetReAlignTemperatureStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetReAlignTemperatureStatus")
    global GetReAlignTemperatureStatus_Response
    if not "GetReAlignTemperatureStatus_Response" in globals(): GetReAlignTemperatureStatus_Response = namedtuple("GetReAlignTemperatureStatus_Response", "StatusId,StatusStr")
    return GetReAlignTemperatureStatus_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def ReAlign(Repeats:int="", Mode:str="", AlignProbeCard:int="", CorrectZ:int=""):
    """
    Performs an automatic realignment of the wafer. This includes measuring the
    needle drift XYZ, aligning the wafer, measuring chuck expansion, measuring chuck
    drift XYZ and optionally a Z-Profile. Alternatively the tool performs a
    ProbeToDie Alignment to correct the needle position for the current die. Command
    returns once ReAlign is finished or aborted because of an error.
    API Status: published
    Args:
        Repeats:int = 1
        Mode:str = "H"
        AlignProbeCard:int = 2
        CorrectZ:int = 2
    Returns:
        XOffsetWafer:Decimal
        YOffsetWafer:Decimal
        ZOffsetWafer:Decimal
        XOffsetCard:Decimal
        YOffsetCard:Decimal
        ZOffsetCard:Decimal
    Command Timeout: 1000000
    Example:ReAlign 2 H 0 0
    """
    rsp = MessageServerInterface.sendSciCommand("ReAlign",Repeats,Mode,AlignProbeCard,CorrectZ)
    global ReAlign_Response
    if not "ReAlign_Response" in globals(): ReAlign_Response = namedtuple("ReAlign_Response", "XOffsetWafer,YOffsetWafer,ZOffsetWafer,XOffsetCard,YOffsetCard,ZOffsetCard")
    return ReAlign_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]))

def NextWafer():
    """
    Starts the NextWafer routine.
    API Status: published
    Returns:
        Canceled:int
    Command Timeout: 60000000
    Example:NextWafer
    """
    rsp = MessageServerInterface.sendSciCommand("NextWafer")
    return int(rsp[0])

def StartReAlign(Repeats:int="", Mode:str="", AlignProbeCard:int="", CorrectZ:int=""):
    """
    Starts an automatic realignment of the wafer. This includes measuring the needle
    drift XYZ, aligning the wafer, measuring chuck expansion, measuring chuck drift
    XYZ and optionally a Z-Profile. Alternatively the tool performs a ProbeToDie
    Alignment to correct the needle position for the current die. Command returns
    immediately.
    API Status: published
    Args:
        Repeats:int = 1
        Mode:str = "H"
        AlignProbeCard:int = 2
        CorrectZ:int = 2
    Command Timeout: 60000
    Example:StartReAlign 2 H 0 0
    """
    MessageServerInterface.sendSciCommand("StartReAlign",Repeats,Mode,AlignProbeCard,CorrectZ)


def StopReAlign():
    """
    Stops the ReAlign procedure.
    API Status: published
    Command Timeout: 120000
    Example:StopReAlign
    """
    MessageServerInterface.sendSciCommand("StopReAlign")


def GetReAlignStatus():
    """
    Returns a status of the ReAlign procedure. If the return value is true, ReAlign
    is running.
    API Status: published
    Returns:
        Running:int
    Command Timeout: 60000
    Example:GetReAlignStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetReAlignStatus")
    return int(rsp[0])

def EnableOverlay(Overlay:int=""):
    """
    Allows activating the overlay of the needles for the top camera.
    API Status: published
    Args:
        Overlay:int = 0
    Command Timeout: 6000
    Example:EnableOverlay 0
    """
    MessageServerInterface.sendSciCommand("EnableOverlay",Overlay)


def SwitchOffset(Offset:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Switches the offset compensation. Applicable for MicroAlign stations only.
    API Status: internal
    Args:
        Offset:int = 0
    Command Timeout: 60000
    Example:SwitchOffset 1
    """
    MessageServerInterface.sendSciCommand("SwitchOffset",Offset)


def TrainFeature(Model:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command was only implemented for supporting a SCPI legacy command. Does not make
    sense in Velox, as there is no default training rectangle on the screen as in
    Nucleus.
    API Status: internal
    Args:
        Model:int = 1
    Returns:
        Data:str
    Command Timeout: 30000
    Example:TrainFeature 1
    """
    rsp = MessageServerInterface.sendSciCommand("TrainFeature",Model)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def GetEvueExposureLevel():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the exposure value of the eVue. Implemented for supporting SCPI legacy
    command.
    API Status: internal
    Returns:
        Exposure:Decimal
    Command Timeout: 10000
    Example:GetEvueExposureLevel
    """
    rsp = MessageServerInterface.sendSciCommand("GetEvueExposureLevel")
    return Decimal(rsp[0])

def SetEvueExposureLevel(Exposure:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the exposure value of the eVue. Implemented for supporting SCPI legacy
    command.
    API Status: internal
    Args:
        Exposure:Decimal = 0
    Command Timeout: 10000
    Example:SetEvueExposureLevel
    """
    MessageServerInterface.sendSciCommand("SetEvueExposureLevel",Exposure)


def MoveEvueFocusStage(EvueZ:Decimal="", EvueVelocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the eVue focus stage to a specified position. Implemented for supporting
    SCPI legacy command.
    API Status: internal
    Args:
        EvueZ:Decimal = 0
        EvueVelocity:Decimal = 100
    Command Timeout: 30000
    Example:MoveEvueFocusStage 1000
    """
    MessageServerInterface.sendSciCommand("MoveEvueFocusStage",EvueZ,EvueVelocity)


def GetEvueFocusStagePos():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current position of the eVue focus stage. Implemented for supporting
    SCPI legacy command.
    API Status: internal
    Returns:
        EvueZ:Decimal
    Command Timeout: 5000
    Example:GetEvueFocusStagePos
    """
    rsp = MessageServerInterface.sendSciCommand("GetEvueFocusStagePos")
    return Decimal(rsp[0])

def RunEvueAutoExpose(UseCB:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command runs the AutoExpose function for the eVue. Implemented for supporting
    SCPI legacy command.
    API Status: internal
    Args:
        UseCB:int = 1
    Command Timeout: 20000
    Example:RunEvueAutoExpose 1
    """
    MessageServerInterface.sendSciCommand("RunEvueAutoExpose",UseCB)


def GetEvueZoomLevel():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Valid only with the eVue microscope that is connected to Velox.     On eVue
    systems, this command, returns values ranging from 0.5 to 5.0 for a 10x system
    and 0.5 to 20.0 for a 40x system.
    API Status: internal
    Returns:
        Zoom:Decimal
    Command Timeout: 5000
    Example:GetEvueZoomLevel
    """
    rsp = MessageServerInterface.sendSciCommand("GetEvueZoomLevel")
    return Decimal(rsp[0])

def SetEvueZoomLevel(Zoom:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Valid only with the eVue microscope or an A-Zoom microscope that is connected to
    Velox. On eVue systems, this command sets the proper CCD zoom level to the
    appropriate optical path.
    API Status: internal
    Args:
        Zoom:Decimal = 0
    Command Timeout: 5000
    Example:SetEvueZoomLevel 2.0
    """
    MessageServerInterface.sendSciCommand("SetEvueZoomLevel",Zoom)


def StartAutomationTemperature(TargetTemperature:Decimal="", ThetaAlignOnFinish:int="", ContactOnFinish:int="", AlignOnFinish:int=""):
    """
    Starts temperature ramping using Automation. The Automation (mostly VueTrack)
    will re-adjust the probes and wafer during ramping to the new target
    temperature.
    API Status: published
    Args:
        TargetTemperature:Decimal = 0
        ThetaAlignOnFinish:int = 0
        ContactOnFinish:int = 0
        AlignOnFinish:int = 1
    Command Timeout: 5000
    Example:StartAutomationTemperature 150
    """
    MessageServerInterface.sendSciCommand("StartAutomationTemperature",TargetTemperature,ThetaAlignOnFinish,ContactOnFinish,AlignOnFinish)


def StopAutomationTemperature():
    """
    Stops temperature ramping using Automation.
    API Status: published
    Command Timeout: 10000
    Example:StopAutomationTemperature
    """
    MessageServerInterface.sendSciCommand("StopAutomationTemperature")


def GetAutomationTemperatureStatus():
    """
    Returns the status of the current temperature ramping using automation process.
    API Status: published
    Returns:
        StatusId:int
        StatusStr:str
    Command Timeout: 300000
    Example:GetAutomationTemperatureStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetAutomationTemperatureStatus")
    global GetAutomationTemperatureStatus_Response
    if not "GetAutomationTemperatureStatus_Response" in globals(): GetAutomationTemperatureStatus_Response = namedtuple("GetAutomationTemperatureStatus_Response", "StatusId,StatusStr")
    return GetAutomationTemperatureStatus_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def GetAutomationActive():
    """
    Command to read from Spectrum if Automation (AutoXY, AutoZ or VueTrack) is
    active. Command is used     by WaferMap to read if it must send MoveChuckAutoXY
    instead of MoveChuck
    API Status: published
    Returns:
        Active:int
    Command Timeout: 1000
    Example:GetAutomationActive
    """
    rsp = MessageServerInterface.sendSciCommand("GetAutomationActive")
    return int(rsp[0])

def AutomationNeedleSearch(NeedleIndex:int="", MoveScope:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    VueTrack vision search of the given needle index.
    API Status: internal
    Args:
        NeedleIndex:int = 1
        MoveScope:int = 1
    Returns:
        XOffset:Decimal
        YOffset:Decimal
        ZOffset:Decimal
        XYMatchScore:Decimal
        ZMatchScore:Decimal
    Command Timeout: 60000
    Example:AutomationNeedleSearch 1 1
    """
    rsp = MessageServerInterface.sendSciCommand("AutomationNeedleSearch",NeedleIndex,MoveScope)
    global AutomationNeedleSearch_Response
    if not "AutomationNeedleSearch_Response" in globals(): AutomationNeedleSearch_Response = namedtuple("AutomationNeedleSearch_Response", "XOffset,YOffset,ZOffset,XYMatchScore,ZMatchScore")
    return AutomationNeedleSearch_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]))

def AutomationReferenceSearch():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    AutomationReferenceSearch exposes the functionality of searching the Automation
    reference target via remote command
    API Status: internal
    Returns:
        XOffset:Decimal
        YOffset:Decimal
        ZOffset:Decimal
        XYMatchScore:Decimal
    Command Timeout: 60000
    Example:AutomationReferenceSearch
    """
    rsp = MessageServerInterface.sendSciCommand("AutomationReferenceSearch")
    global AutomationReferenceSearch_Response
    if not "AutomationReferenceSearch_Response" in globals(): AutomationReferenceSearch_Response = namedtuple("AutomationReferenceSearch_Response", "XOffset,YOffset,ZOffset,XYMatchScore")
    return AutomationReferenceSearch_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]))

def MovePositionersSafe():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the configured motorized positioners to a safe position
    API Status: internal
    Command Timeout: 60000
    Example:MovePositionersSafe
    """
    MessageServerInterface.sendSciCommand("MovePositionersSafe")


def SetConstantContactMode(IsOn:int="", ForceLastCorrection:int=""):
    """
    Starts Constant Contact mode using Automation. The Automation will re-adjust the
    wafer during ramping to the new target temperature.
    API Status: published
    Args:
        IsOn:int = 0
        ForceLastCorrection:int = 0
    Command Timeout: 5000
    Example:SetConstantContactMode 1
    """
    MessageServerInterface.sendSciCommand("SetConstantContactMode",IsOn,ForceLastCorrection)


def GetConstantContactModeStatus():
    """
    Returns the status of the current ConstantContact automation process.
    API Status: published
    Returns:
        StatusId:int
        StatusStr:str
    Command Timeout: 5000
    Example:GetConstantContactModeStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetConstantContactModeStatus")
    global GetConstantContactModeStatus_Response
    if not "GetConstantContactModeStatus_Response" in globals(): GetConstantContactModeStatus_Response = namedtuple("GetConstantContactModeStatus_Response", "StatusId,StatusStr")
    return GetConstantContactModeStatus_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def SetAutomationActive(Activate:int=""):
    """
    Command to set if Automation (AutoXY, AutoZ or VueTrack) is active. Command can
    be used to e.g. deactivate automation     programmatically in case it is no
    longer used.     When activating automation, the command will return an error in
    case it is not possible (e.g. not trained)
    API Status: published
    Args:
        Activate:int = 0
    Command Timeout: 1000
    Example:SetAutomationActive 1
    """
    MessageServerInterface.sendSciCommand("SetAutomationActive",Activate)


def AutomationSearchCurrentDie():
    """
    Performs an Automation search and position correction using the current chuck
    position. Response is X, Y relative distance of adjustment.
    API Status: published
    Returns:
        XOffset:Decimal
        YOffset:Decimal
    Command Timeout: 6000000
    Example:AutomationSearchCurrentDie
    """
    rsp = MessageServerInterface.sendSciCommand("AutomationSearchCurrentDie")
    global AutomationSearchCurrentDie_Response
    if not "AutomationSearchCurrentDie_Response" in globals(): AutomationSearchCurrentDie_Response = namedtuple("AutomationSearchCurrentDie_Response", "XOffset,YOffset")
    return AutomationSearchCurrentDie_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def PreMapWafer():
    """
    PreMapWafer finds actual singulated die locations and updates positions used by
    WaferMap.
    API Status: published
    Returns:
        NumberOfDies:int
    Command Timeout: 14400000
    Example:PreMapWafer
    """
    rsp = MessageServerInterface.sendSciCommand("PreMapWafer")
    return int(rsp[0])

def ISSProbeAlign():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Performs an probe to pad operation on the ISS with two RF positioners.
    API Status: internal
    Command Timeout: 6000000
    Example:ISSProbeAlign
    """
    MessageServerInterface.sendSciCommand("ISSProbeAlign")


def FindWaferCenter(NoManualRecovery:int=""):
    """
    FindWaferCenter finds the center of the wafer using edge detection.
    API Status: published
    Args:
        NoManualRecovery:int = 0
    Returns:
        ChuckX:Decimal
        ChuckY:Decimal
    Command Timeout: 300000
    Example:FindWaferCenter
    """
    rsp = MessageServerInterface.sendSciCommand("FindWaferCenter",NoManualRecovery)
    global FindWaferCenter_Response
    if not "FindWaferCenter_Response" in globals(): FindWaferCenter_Response = namedtuple("FindWaferCenter_Response", "ChuckX,ChuckY")
    return FindWaferCenter_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def LocateHomeDie(NoManualRecovery:int=""):
    """
    LocateHomeDie finds the center of the wafer using edge detection and sets the
    home position.
    API Status: published
    Args:
        NoManualRecovery:int = 0
    Returns:
        ChuckX:Decimal
        ChuckY:Decimal
    Command Timeout: 300000
    Example:LocateHomeDie
    """
    rsp = MessageServerInterface.sendSciCommand("LocateHomeDie",NoManualRecovery)
    global LocateHomeDie_Response
    if not "LocateHomeDie_Response" in globals(): LocateHomeDie_Response = namedtuple("LocateHomeDie_Response", "ChuckX,ChuckY")
    return LocateHomeDie_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def SetAutomationProbeLayout(LayoutName:str="", ProbeID:int="", XOffset:Decimal="", YOffset:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Stores the provided X or Y offset for the given probe for the specified layout.
    API Status: internal
    Args:
        LayoutName:str = ""
        ProbeID:int = 0
        XOffset:Decimal = 0
        YOffset:Decimal = 0
    Command Timeout: 10000
    Example:SetAutomationProbeLayout "layout1" 1 100.0 0
    """
    MessageServerInterface.sendSciCommand("SetAutomationProbeLayout",LayoutName,ProbeID,XOffset,YOffset)


def DeleteAutomationProbeLayout(LayoutName:str="", ProbeID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Delete the specfied layout. If LayoutName is empty then all layouts are deleted.
    If optional ProbeID parmameter is set, it removes just that probe from the
    layout.
    API Status: internal
    Args:
        LayoutName:str = ""
        ProbeID:int = 0
    Command Timeout: 10000
    Example:DeleteAutomationProbeLayout "layout1"
    """
    MessageServerInterface.sendSciCommand("DeleteAutomationProbeLayout",LayoutName,ProbeID)


def CaptureAutomationProbeLayout(LayoutName:str="", ProbeID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Capture the specfied layout. If optional ProbeID parmameter is set, it captures
    just that probe from the layout.
    API Status: internal
    Args:
        LayoutName:str = ""
        ProbeID:int = 0
    Command Timeout: 30000
    Example:CaptureAutomationProbeLayout "layout1"
    """
    MessageServerInterface.sendSciCommand("CaptureAutomationProbeLayout",LayoutName,ProbeID)


def MoveToAutomationProbeLayout(LayoutName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Move to the probes to specfied layout which are offsets from the trained
    positions.
    API Status: internal
    Args:
        LayoutName:str = ""
    Command Timeout: 300000
    Example:MoveToAutomationProbeLayout "layout1"
    """
    MessageServerInterface.sendSciCommand("MoveToAutomationProbeLayout",LayoutName)


def ResetAutomation():
    """
    Reset automation data back to trained values.
    API Status: published
    Command Timeout: 10000
    Example:ResetAutomation
    """
    MessageServerInterface.sendSciCommand("ResetAutomation")


def GetWaferCenter():
    """
    GetWaferCenter returns the chuck location (zero based) of the wafer center. It
    returns 0 0 if FindWaferCenter has not been executed for the current wafer.
    API Status: published
    Returns:
        ChuckX:Decimal
        ChuckY:Decimal
    Command Timeout: 10000
    Example:GetWaferCenter
    """
    rsp = MessageServerInterface.sendSciCommand("GetWaferCenter")
    global GetWaferCenter_Response
    if not "GetWaferCenter_Response" in globals(): GetWaferCenter_Response = namedtuple("GetWaferCenter_Response", "ChuckX,ChuckY")
    return GetWaferCenter_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def InitEvueFocusStage():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Initializes the eVue focus stage by finding the limit switches
    API Status: internal
    Command Timeout: 30000
    Example:InitEvueFocusStage
    """
    MessageServerInterface.sendSciCommand("InitEvueFocusStage")


def EvueSetNumTraceEntriesPreTrigger(NumTraceEntriesPreTrigger:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the number of trace log items to preserve prior to the trigger event. With
    the continuous event capture log in Bluestone, up to {X} events are captured and
    kept after the trigger event is sensed. Then, events are captured after the
    trigger event until the trace log is full and then trace capture is halted.
    API Status: internal
    Args:
        NumTraceEntriesPreTrigger:int = 0
    Command Timeout: 30000
    Example:EvueSetNumTraceEntriesPreTrigger 14
    """
    MessageServerInterface.sendSciCommand("EvueSetNumTraceEntriesPreTrigger",NumTraceEntriesPreTrigger)


def EvueGetNumTraceEntriesPreTrigger():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the number of trace log items to preserve prior to the trigger event. With
    the continuous event capture log in Bluestone, up to {X} events are captured and
    kept after the trigger event is sensed. Then, events are captured after the
    trigger event until the trace log is full and then trace capture is halted.
    API Status: internal
    Returns:
        NumTraceEntriesPreTrigger:int
    Command Timeout: 30000
    Example:EvueGetNumTraceEntriesPreTrigger
    """
    rsp = MessageServerInterface.sendSciCommand("EvueGetNumTraceEntriesPreTrigger")
    return int(rsp[0])

def EvueStartCaptureServoTrace():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Starts capturing events in the eVue motion capture log. Capture continues until
    the log is full. However, log entries will overwrite the oldest entry until the
    trigger event is encountered. Then, {X} events are preserved prior to the
    trigger event and the oldest events are only overwritten if they are not part of
    that preserved set.
    API Status: internal
    Command Timeout: 30000
    Example:EvueStartCaptureServoTrace
    """
    MessageServerInterface.sendSciCommand("EvueStartCaptureServoTrace")


def EvueGetTraceMachineStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the current status of the trace machine. Bit fields - bit0 is 1 and bit4 is
    16, etc. bit0 - active and in pre-trigger state bit1 - active and in post-
    trigger state bit2 - stopped by servo error, lens crash or lens removal bit3 -
    stopped on requested server state entry bit4 - stopped by immediate command
    bit5..31 - reserved
    API Status: internal
    Returns:
        TraceMachineStatus:int
    Command Timeout: 30000
    Example:EvueGetTraceMachineStatus
    """
    rsp = MessageServerInterface.sendSciCommand("EvueGetTraceMachineStatus")
    return int(rsp[0])

def EvueSetTraceCaptureStopBits(TraceCaptureStopBits:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets condition bits to trigger servo trace capture. Bit fields - bit0 is 1 and
    bit4 is 16, etc. bit0 - immediate stop bit1 - stop on servo error, lens crash or
    lens removal bit2 - stop on requested server state (defined by bits 4..7) bit3 -
    stop on motor move finish bit4..7 - servo state that triggers a trace stop (not
    an index but the 4-bit state that, if seen, is the trigger for trace capture)
    bit8..31 - reserved
    API Status: internal
    Args:
        TraceCaptureStopBits:int = 0
    Command Timeout: 30000
    Example:EvueSetTraceCaptureStopBits
    """
    MessageServerInterface.sendSciCommand("EvueSetTraceCaptureStopBits",TraceCaptureStopBits)


def EvueGetNumTraceEntries():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the current status of the trace machine.
    API Status: internal
    Returns:
        TraceEntries:int
    Command Timeout: 30000
    Example:EvueGetNumTraceEntries
    """
    rsp = MessageServerInterface.sendSciCommand("EvueGetNumTraceEntries")
    return int(rsp[0])

def EvueGetTraceEntry(EntryIdx:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the N'th trace entry in the log.
    API Status: internal
    Args:
        EntryIdx:int = 0
    Returns:
        CommandedPositionMotorCounts:int
        CommandedPositionMicrons:Decimal
        MeasuredPositionMotorCounts:int
        MeasuredPositionMicrons:Decimal
        TimestampMicroseconds:int
        ServoStatus:int
        PwmVal:int
    Command Timeout: 30000
    Example:EvueGetTraceEntry 32
    """
    rsp = MessageServerInterface.sendSciCommand("EvueGetTraceEntry",EntryIdx)
    global EvueGetTraceEntry_Response
    if not "EvueGetTraceEntry_Response" in globals(): EvueGetTraceEntry_Response = namedtuple("EvueGetTraceEntry_Response", "CommandedPositionMotorCounts,CommandedPositionMicrons,MeasuredPositionMotorCounts,MeasuredPositionMicrons,TimestampMicroseconds,ServoStatus,PwmVal")
    return EvueGetTraceEntry_Response(int(rsp[0]),Decimal(rsp[1]),int(rsp[2]),Decimal(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]))

def AutomationRFProbeSearch(ImageFilename:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the distance in X,Y between the center tips of the RF probes.
    API Status: internal
    Args:
        ImageFilename:str = ""
    Returns:
        X:Decimal
        Y:Decimal
    Command Timeout: 5000
    Example:AutomationRFProbeSearch
    """
    rsp = MessageServerInterface.sendSciCommand("AutomationRFProbeSearch",ImageFilename)
    global AutomationRFProbeSearch_Response
    if not "AutomationRFProbeSearch_Response" in globals(): AutomationRFProbeSearch_Response = namedtuple("AutomationRFProbeSearch_Response", "X,Y")
    return AutomationRFProbeSearch_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def StartAutoRFCalibration():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Starts the AutoRF calibration sequence.
    API Status: internal
    Command Timeout: 3000
    Example:StartAutoRFCalibration
    """
    MessageServerInterface.sendSciCommand("StartAutoRFCalibration")


def StopAutoRFCalibration():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Stops the currently running AutoRF calibraiton.
    API Status: internal
    Command Timeout: 10000
    Example:StopAutoRFCalibration
    """
    MessageServerInterface.sendSciCommand("StopAutoRFCalibration")


def GetAutoRFCalibrationStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the status of the AutoRF calibration sequence.
    API Status: internal
    Returns:
        StatusId:int
        StatusStr:str
    Command Timeout: 1000
    Example:GetAutoRFCalibrationStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetAutoRFCalibrationStatus")
    global GetAutoRFCalibrationStatus_Response
    if not "GetAutoRFCalibrationStatus_Response" in globals(): GetAutoRFCalibrationStatus_Response = namedtuple("GetAutoRFCalibrationStatus_Response", "StatusId,StatusStr")
    return GetAutoRFCalibrationStatus_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def GetAutomationLastStepDiagnostics(Index:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the diagnostic state information for the provided index.
    API Status: internal
    Args:
        Index:int = 0
    Returns:
        DiagnosticInfo:str
    Command Timeout: 5000
    Example:GetAutomationLastStepDiagnostics
    """
    rsp = MessageServerInterface.sendSciCommand("GetAutomationLastStepDiagnostics",Index)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetWLEMNanoChamberState(State:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the WLEM Nano Chamber State.
    API Status: internal
    Args:
        State:str = "Free"
    Command Timeout: 5000
    Example:SetWLEMNanoChamberState Free
    """
    MessageServerInterface.sendSciCommand("SetWLEMNanoChamberState",State)


def GetWLEMNanoChamberState():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the WLEM Nano Chamber State.
    API Status: internal
    Returns:
        State:str
    Command Timeout: 5000
    Example:GetWLEMNanoChamberState
    """
    rsp = MessageServerInterface.sendSciCommand("GetWLEMNanoChamberState")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetWLEMState(State:str="", Value:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the state of a WLEM pneumatic control (valve).
    API Status: internal
    Args:
        State:str = "NCSeal"
        Value:int = 0
    Command Timeout: 5000
    Example:SetWLEMState NCSeal 1
    """
    MessageServerInterface.sendSciCommand("SetWLEMState",State,Value)


def GetWLEMState(State:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the state of a WLEM pneumatic control (valve).
    API Status: internal
    Args:
        State:str = "NCSeal"
    Returns:
        Value:int
    Command Timeout: 5000
    Example:GetWLEMState NCSeal
    """
    rsp = MessageServerInterface.sendSciCommand("GetWLEMState",State)
    return int(rsp[0])

def GetWLEMSensorValue(Sensor:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets the value of a WLEM Sensor.
    API Status: internal
    Args:
        Sensor:str = "O2Concentration"
    Returns:
        Value:Decimal
    Command Timeout: 5000
    Example:GetWLEMSensorValue O2Concentration
    """
    rsp = MessageServerInterface.sendSciCommand("GetWLEMSensorValue",Sensor)
    return Decimal(rsp[0])

def SetWLEMOption(Option:str="", Value:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets a WLEM Control program option.
    API Status: internal
    Args:
        Option:str = "MinimizeToTray"
        Value:int = 0
    Command Timeout: 5000
    Example:SetWLEMOption MinimizeToTray 1
    """
    MessageServerInterface.sendSciCommand("SetWLEMOption",Option,Value)


def GetWLEMOption(Option:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets a WLEM Control program option.
    API Status: internal
    Args:
        Option:str = "MinimizeToTray"
    Returns:
        Value:int
    Command Timeout: 5000
    Example:GetWLEMOption MinimizeToTray
    """
    rsp = MessageServerInterface.sendSciCommand("GetWLEMOption",Option)
    return int(rsp[0])

def NewTesterProject(LotID:str="", TileID:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester that a new Lot/Tile is to be tested. The tester
    responds with the correct project name for the test. This is needed because the
    prober needs to verify that the correct project is loaded. In case no valid
    project is available, the command is returned with an error.
    API Status: internal
    Args:
        LotID:str = ""
        TileID:str = ""
    Returns:
        ProjectName:str
    Command Timeout: 30000
    Example:NewTesterProject Lot01 Tile01
    """
    rsp = MessageServerInterface.sendSciCommand("NewTesterProject",LotID,TileID)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def StartMeasurement(DieColumn:int="", DieRow:int="", ActiveDies:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command tells the tester to begin measuring (Needles are in correct
    position and in contact). The command is responded when the measurement has
    finished. The response string holds the binning information separated by comma.
    For deactivated dies, a bin value of '0' should be responded.
    API Status: internal
    Args:
        DieColumn:int = 0
        DieRow:int = 0
        ActiveDies:str = ""
    Returns:
        BinNumbers:str
    Command Timeout: 100000
    Example:StartMeasurement 1 1 1
    """
    rsp = MessageServerInterface.sendSciCommand("StartMeasurement",DieColumn,DieRow,ActiveDies)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def EndOfWafer():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command tells the tester, that the test of the current substrate has
    finished. It enables the tester application to save measurement data and/or
    prepare for the next substrate.
    API Status: internal
    Command Timeout: 30000
    Example:EndOfWafer
    """
    MessageServerInterface.sendSciCommand("EndOfWafer")


def EndOfLot():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command tells the tester, that the test of the current lot has finished. It
    enables the tester application to save measurement data and/or prepare for the
    next lot.
    API Status: internal
    Command Timeout: 30000
    Example:EndOfLot
    """
    MessageServerInterface.sendSciCommand("EndOfLot")


def VerifyProductID(ProductID:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester about the ProductID that is to be tested. The
    tester can respond with an error in case the ProductID is not allowed for
    testing.
    API Status: internal
    Args:
        ProductID:str = ""
    Command Timeout: 30000
    Example:VerifyProductID Product123
    """
    MessageServerInterface.sendSciCommand("VerifyProductID",ProductID)


def VerifyLotID(LotID:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester about the LotID that is to be tested. The tester
    can respond with an error in case the LotID is not allowed for testing.
    API Status: internal
    Args:
        LotID:str = ""
    Command Timeout: 30000
    Example:VerifyLotID Lot123
    """
    MessageServerInterface.sendSciCommand("VerifyLotID",LotID)


def VerifySubstrateID(SubstrateID:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester about the SubstrateID that is to be tested. The
    tester can respond with an error in case the SubstrateID is not allowed for
    testing.
    API Status: internal
    Args:
        SubstrateID:str = ""
    Command Timeout: 30000
    Example:VerifySubstrateID Substrate123
    """
    MessageServerInterface.sendSciCommand("VerifySubstrateID",SubstrateID)


def VerifyProbecard(ProbeCard:str="", Touchdowns:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester about the ProbecardID and touchdowns that is
    used for testing. The tester can respond with an error in case the Probecard is
    not allowed for testing.
    API Status: internal
    Args:
        ProbeCard:str = ""
        Touchdowns:int = 0
    Command Timeout: 30000
    Example:VerifyProbecard Probecard123 10596
    """
    MessageServerInterface.sendSciCommand("VerifyProbecard",ProbeCard,Touchdowns)


def VerifyUserID(User:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester about the User ID. The tester can respond with
    an error in case the User ID is not allowed for testing.
    API Status: internal
    Args:
        User:str = ""
    Command Timeout: 30000
    Example:VerifyUserID User123
    """
    MessageServerInterface.sendSciCommand("VerifyUserID",User)


def TesterAbort():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester that the job was aborted and no more test will
    happen.
    API Status: internal
    Command Timeout: 30000
    Example:TesterAbort
    """
    MessageServerInterface.sendSciCommand("TesterAbort")


def VerifySOTReady():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester that a wafer is ready for testing which will
    immediately start. This command is sent in the recipe sequence "Verify
    SOTReady".
    API Status: internal
    Command Timeout: 30000
    Example:VerifySOTReady
    """
    MessageServerInterface.sendSciCommand("VerifySOTReady")


def VerifyWaferStart(SubstrateID:str="", CassettePlace:str="", LotID:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command is sent in the VeloxPro recipe sequence "Verify Wafer Start" and
    informs the tester about the current wafer on the chuck.
    API Status: internal
    Args:
        SubstrateID:str = ""
        CassettePlace:str = ""
        LotID:str = ""
    Command Timeout: 30000
    Example:VerifyWaferStart Wafer01 1 Lot01
    """
    MessageServerInterface.sendSciCommand("VerifyWaferStart",SubstrateID,CassettePlace,LotID)


def TesterCassetteInfo(CassetteCmd:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command will be sent after the user selected which wafers are to be tested.
    It contains a string which represents the state of each wafer: 0 = empty, 1 =
    full (and selected), 2 = error (e.g. double slotted), 3 = unknown, 4 =
    deselected
    API Status: internal
    Args:
        CassetteCmd:str = ""
    Returns:
        CassetteRsp:str
    Command Timeout: 30000
    Example:TesterCassetteInfo 0000001110000000010010111
    """
    rsp = MessageServerInterface.sendSciCommand("TesterCassetteInfo",CassetteCmd)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def VerifyProject(ProjectName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command is sent after selecting a project file in the VeloxPro product
    setup page. The command sends the name of the project to tester for
    verification.
    API Status: internal
    Args:
        ProjectName:str = ""
    Command Timeout: 30000
    Example:VerifyProject C:/Users/Public/Documents/Velox/Projects/Test.spp
    """
    MessageServerInterface.sendSciCommand("VerifyProject",ProjectName)


def TesterAbortWafer():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command informs the tester that the test for the current wafer was aborted
    and no more tests will happen with the current wafer. The job will continue
    though.
    API Status: internal
    Command Timeout: 30000
    Example:TesterAbortWafer
    """
    MessageServerInterface.sendSciCommand("TesterAbortWafer")


def DoTTLTest():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Starts execution of one test. It returns a bin number or multple bin numbers
    when clusters are enabled in the WaferMap (one number for each die in a
    cluster).  The command starts execution of one test. It returns a bin number or
    multple bin numbers when clusters are enabled in the WaferMap (one number for
    each die in a cluster).
    API Status: internal
    Returns:
        BitNumber:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("DoTTLTest")
    return int(rsp[0])

def StartTTLTest():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Starts the test of a wafer. Depending on the cluster definitions queried from
    the WaferMap, all clusters or all dies will be tested.  The command starts the
    test of a wafer. Depending on the cluster definitions queried from the WaferMap
    all clusters or all dies will be tested.
    API Status: internal
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("StartTTLTest")


def CancelTTLTest():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Stops the wafer test.
    API Status: internal
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("CancelTTLTest")


def SetTTLLine(Line:int="", Value:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the selected line of PA port.
    API Status: internal
    Args:
        Line:int = 0
        Value:int = 0
    Command Timeout: 10000
    Example:SetTTLLine 2 0
    """
    MessageServerInterface.sendSciCommand("SetTTLLine",Line,Value)


def GetTTLLines():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the I/O lines as bit array.
    API Status: internal
    Returns:
        LineA:int
        LineB:int
        LineC:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetTTLLines")
    global GetTTLLines_Response
    if not "GetTTLLines_Response" in globals(): GetTTLLines_Response = namedtuple("GetTTLLines_Response", "LineA,LineB,LineC")
    return GetTTLLines_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]))

def GetTTLStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns returns the error 914 if the test is in progress.
    API Status: internal
    Returns:
        ErrCode:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetTTLStatus")
    return int(rsp[0])

def StartScript(ScriptName:str=""):
    """
    Starts the script and returns the response immediately.
    API Status: published
    Args:
        ScriptName:str = ""
    Command Timeout: 10000
    Example:StartScript myscript
    """
    MessageServerInterface.sendSciCommand("StartScript",ScriptName)


def GetRunStatus(ScriptName:str=""):
    """
    Command returns information about Communicator status.
    API Status: published
    Args:
        ScriptName:str = ""
    Returns:
        Running:int
        LastError:int
        Title:str
    Command Timeout: 5000
    Example:GetRunStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetRunStatus",ScriptName)
    global GetRunStatus_Response
    if not "GetRunStatus_Response" in globals(): GetRunStatus_Response = namedtuple("GetRunStatus_Response", "Running,LastError,Title")
    return GetRunStatus_Response(int(rsp[0]),int(rsp[1]),str("" if len(rsp) < 3 else ' '.join(rsp[2:])))

def CloseCommunicator():
    """
    Command closes the program. Used during ProjectFile handling.
    API Status: published
    Command Timeout: 10000
    Example:CloseCommunicator
    """
    MessageServerInterface.sendSciCommand("CloseCommunicator")


def DoScript(ScriptName:str=""):
    """
    Executes the script and returns the response afterwards.
    API Status: published
    Args:
        ScriptName:str = ""
    Command Timeout: 10000000
    Example:DoScript myscript
    """
    MessageServerInterface.sendSciCommand("DoScript",ScriptName)


def ReadKernelData(SilentMode:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Reads Kernel Data to KernelSetup (Left Program pane).
    API Status: internal
    Args:
        SilentMode:int = 0
    Command Timeout: 300000
    Example:ReadKernelData 0
    """
    MessageServerInterface.sendSciCommand("ReadKernelData",SilentMode)


def SaveKernelDataAs(FileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Saves Kernel Data (Left Program pane) to File. An existing File will be
    overwritten. If the Folder does not exist, it will be created
    API Status: internal
    Args:
        FileName:str = ""
    Command Timeout: 10000
    Example:SaveKernelDataAs C:/Temp/RCConfigSample1.xml
    """
    MessageServerInterface.sendSciCommand("SaveKernelDataAs",FileName)


def LoadConfigFile(FileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Loads File Data to KernelSetup (Right Program pane).
    API Status: internal
    Args:
        FileName:str = ""
    Command Timeout: 10000
    Example:LoadConfigFile C:/Temp/RCConfigSample1.xml
    """
    MessageServerInterface.sendSciCommand("LoadConfigFile",FileName)


def ReplaceKernelDataByFileData(SilentMode:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Replaces Kernel Data (Left pane) by File Data (Right pane).
    API Status: internal
    Args:
        SilentMode:int = 0
    Command Timeout: 300000
    Example:ReplaceKernelDataByFileData 0
    """
    MessageServerInterface.sendSciCommand("ReplaceKernelDataByFileData",SilentMode)


def ReplaceFileTreeByKernelData(SilentMode:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Replaces File Tree (Right pane) by Kernel Data (Left pane).
    API Status: internal
    Args:
        SilentMode:int = 0
    Command Timeout: 300000
    Example:ReplaceFileTreeByKernelData 0
    """
    MessageServerInterface.sendSciCommand("ReplaceFileTreeByKernelData",SilentMode)


def SaveFileTreeAs(FileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Saves File Tree (Right pane) to File. An existing File will be overwritten. If
    the Folder does not exist, it will be created.
    API Status: internal
    Args:
        FileName:str = ""
    Command Timeout: 10000
    Example:SaveFileTreeAs C:/Temp/RCConfigSample2.xml
    """
    MessageServerInterface.sendSciCommand("SaveFileTreeAs",FileName)


def HeatChuck(Temperature:Decimal="", Unit:str="", ReduceContact:int=""):
    """
    Sets a new target temperature and starts the heating or cooling of the chuck. An
    answer to the command will be returned after reaching the given temperature and
    waiting the soak time or an unexpected interrupt of the process. Given back is
    the already reached temperature.
    API Status: published
    Args:
        Temperature:Decimal = 25
        Unit:str = "Celsius"
        ReduceContact:int = 1
    Returns:
        RespTemperature:Decimal
        RespUnit:str
    Command Timeout: 36000000
    Example:HeatChuck 61.3 C
    """
    rsp = MessageServerInterface.sendSciCommand("HeatChuck",Temperature,Unit,ReduceContact)
    global HeatChuck_Response
    if not "HeatChuck_Response" in globals(): HeatChuck_Response = namedtuple("HeatChuck_Response", "RespTemperature,RespUnit")
    return HeatChuck_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def SetHeaterTemp(Temperature:Decimal="", Unit:str="", UseContactSafety:int=""):
    """
    Sets a new target temperature and starts the heating or cooling of the
    temperature chuck. The new target temperature is returned immediately as the
    command does not wait until heating is complete.
    API Status: published
    Args:
        Temperature:Decimal = 25
        Unit:str = "Celsius"
        UseContactSafety:int = 1
    Returns:
        RespTemperature:Decimal
        RespUnit:str
    Command Timeout: 60000
    Example:SetHeaterTemp 55.5 C
    """
    rsp = MessageServerInterface.sendSciCommand("SetHeaterTemp",Temperature,Unit,UseContactSafety)
    global SetHeaterTemp_Response
    if not "SetHeaterTemp_Response" in globals(): SetHeaterTemp_Response = namedtuple("SetHeaterTemp_Response", "RespTemperature,RespUnit")
    return SetHeaterTemp_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def GetHeaterTemp(Unit:str="", ExternalHeaterID:int=""):
    """
    Reads the current temperature of the chuck and determines the status of the
    thermal system.
    API Status: published
    Args:
        Unit:str = "Celsius"
        ExternalHeaterID:int = 0
    Returns:
        RespTemperature:Decimal
        RespUnit:str
        Status:str
    Command Timeout: 60000
    Example:GetHeaterTemp C
    """
    rsp = MessageServerInterface.sendSciCommand("GetHeaterTemp",Unit,ExternalHeaterID)
    global GetHeaterTemp_Response
    if not "GetHeaterTemp_Response" in globals(): GetHeaterTemp_Response = namedtuple("GetHeaterTemp_Response", "RespTemperature,RespUnit,Status")
    return GetHeaterTemp_Response(Decimal(rsp[0]),str(rsp[1]),str("" if len(rsp) < 3 else ' '.join(rsp[2:])))

def EnableHeaterHoldMode(HoldMode:int=""):
    """
    Switches the Temperature Chuck devices hold mode on or off. In hold mode the
    chuck is heated with a constant current to avoid noise from the temperature
    control. The hold mode can be enabled only in HoldReady state.
    API Status: published
    Args:
        HoldMode:int = 1
    Returns:
        RespHoldMode:int
    Command Timeout: 60000
    Example:EnableHeaterHoldMode 1
    """
    rsp = MessageServerInterface.sendSciCommand("EnableHeaterHoldMode",HoldMode)
    return int(rsp[0])

def StopHeatChuck():
    """
    Stops a pending heating or cooling process. If the device is not at temperature,
    the actual temperature is set as target temperature.
    API Status: published
    Command Timeout: 60000
    Example:StopHeatChuck
    """
    MessageServerInterface.sendSciCommand("StopHeatChuck")


def GetDewPointTemp(Unit:str=""):
    """
    Returns the current dew point temperature, if a dew point sensor is connected.
    API Status: published
    Args:
        Unit:str = "Celsius"
    Returns:
        RespTemperature:Decimal
        RespUnit:str
    Command Timeout: 60000
    Example:GetDewPointTemp C
    """
    rsp = MessageServerInterface.sendSciCommand("GetDewPointTemp",Unit)
    global GetDewPointTemp_Response
    if not "GetDewPointTemp_Response" in globals(): GetDewPointTemp_Response = namedtuple("GetDewPointTemp_Response", "RespTemperature,RespUnit")
    return GetDewPointTemp_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def GetTemperatureChuckOptions():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the currently set temperature chuck options.
    API Status: internal
    Returns:
        UseSoakTime:int
        SyncTemp:int
        CurrConnection:int
        MinTemperature:Decimal
        MaxTemperature:Decimal
        UsePurge:int
        UseDynamicSoakTime:int
        UseFixedDieSoakTime:int
        UseDynamicDieSoakTime:int
        UseEcoMode:int
        PurgeOnChamberDoor:int
        ForceBypassPurge:int
        DoorClosedTime:int
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("GetTemperatureChuckOptions")
    global GetTemperatureChuckOptions_Response
    if not "GetTemperatureChuckOptions_Response" in globals(): GetTemperatureChuckOptions_Response = namedtuple("GetTemperatureChuckOptions_Response", "UseSoakTime,SyncTemp,CurrConnection,MinTemperature,MaxTemperature,UsePurge,UseDynamicSoakTime,UseFixedDieSoakTime,UseDynamicDieSoakTime,UseEcoMode,PurgeOnChamberDoor,ForceBypassPurge,DoorClosedTime")
    return GetTemperatureChuckOptions_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]),int(rsp[10]),int(rsp[11]),int(rsp[12]))

def SetTemperatureChuckOptions(UseFixedWaferSoak:int="", SyncTemp:int="", CurrConnection:int="", UsePurge:int="", UseDynamicWaferSoak:int="", UseFixedDieSoakTime:int="", UseDynamicDieSoakTime:int="", UseEcoMode:int="", PurgeOnChamberDoor:int="", ForceBypassPurge:int="", DoorClosedTime:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command is used to change the currently set temperature chuck options.
    API Status: internal
    Args:
        UseFixedWaferSoak:int = -1
        SyncTemp:int = -1
        CurrConnection:int = -1
        UsePurge:int = -1
        UseDynamicWaferSoak:int = -1
        UseFixedDieSoakTime:int = -1
        UseDynamicDieSoakTime:int = -1
        UseEcoMode:int = -1
        PurgeOnChamberDoor:int = -1
        ForceBypassPurge:int = -1
        DoorClosedTime:int = -1
    Returns:
        UseFixedWaferSoakRsp:int
        SyncTempRsp:int
        CurrConnectionRsp:int
        UsePurgeRsp:int
        UseDynamicWaferSoakRsp:int
        UseFixedDieSoakTimeRsp:int
        UseDynamicDieSoakTimeRsp:int
        UseEcoModeRsp:int
        PurgeOnChamberDoorRsp:int
        ForceBypassPurgeRsp:int
        DoorClosedTimeRsp:int
    Command Timeout: 300000
    Example:SetTemperatureChuckOptions 1 0 1 1 1 1 1
    """
    rsp = MessageServerInterface.sendSciCommand("SetTemperatureChuckOptions",UseFixedWaferSoak,SyncTemp,CurrConnection,UsePurge,UseDynamicWaferSoak,UseFixedDieSoakTime,UseDynamicDieSoakTime,UseEcoMode,PurgeOnChamberDoor,ForceBypassPurge,DoorClosedTime)
    global SetTemperatureChuckOptions_Response
    if not "SetTemperatureChuckOptions_Response" in globals(): SetTemperatureChuckOptions_Response = namedtuple("SetTemperatureChuckOptions_Response", "UseFixedWaferSoakRsp,SyncTempRsp,CurrConnectionRsp,UsePurgeRsp,UseDynamicWaferSoakRsp,UseFixedDieSoakTimeRsp,UseDynamicDieSoakTimeRsp,UseEcoModeRsp,PurgeOnChamberDoorRsp,ForceBypassPurgeRsp,DoorClosedTimeRsp")
    return SetTemperatureChuckOptions_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]),int(rsp[10]))

def GetHeaterSoak():
    """
    Returns the current soak time values in seconds and the soaking status.
    API Status: published
    Returns:
        FixedWaferSoakTime:int
        FixedWaferSoakStatus:int
        DynamicWaferSoakTime:Decimal
        DynamicWaferSoakStatus:int
        FixedDieSoakTime:Decimal
        DynamicDieSoakTime:Decimal
        FixedDieSoakStatus:int
        DynamicDieSoakStatus:int
    Command Timeout: 60000
    Example:GetHeaterSoak
    """
    rsp = MessageServerInterface.sendSciCommand("GetHeaterSoak")
    global GetHeaterSoak_Response
    if not "GetHeaterSoak_Response" in globals(): GetHeaterSoak_Response = namedtuple("GetHeaterSoak_Response", "FixedWaferSoakTime,FixedWaferSoakStatus,DynamicWaferSoakTime,DynamicWaferSoakStatus,FixedDieSoakTime,DynamicDieSoakTime,FixedDieSoakStatus,DynamicDieSoakStatus")
    return GetHeaterSoak_Response(int(rsp[0]),int(rsp[1]),Decimal(rsp[2]),int(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]),int(rsp[6]),int(rsp[7]))

def SetHeaterSoak(FixedWaferSoakTime:int="", DynamicWaferSoakTime:Decimal="", FixedDieSoakTime:Decimal="", DynamicDieSoakTime:Decimal=""):
    """
    Sets the new soak time values. The unit of the values is seconds. If soak time
    is actually running, it may be affected by the change.
    API Status: published
    Args:
        FixedWaferSoakTime:int = 60
        DynamicWaferSoakTime:Decimal = -1
        FixedDieSoakTime:Decimal = -1
        DynamicDieSoakTime:Decimal = -1
    Command Timeout: 60000
    Example:SetHeaterSoak 60
    """
    MessageServerInterface.sendSciCommand("SetHeaterSoak",FixedWaferSoakTime,DynamicWaferSoakTime,FixedDieSoakTime,DynamicDieSoakTime)


def EnableHeaterStandby(Standby:int=""):
    """
    Switches the power save (standby) mode of the device on or off. If the device is
    in power save mode, setting and reading temperatures switches off the power save
    mode automatically.
    API Status: published
    Args:
        Standby:int = 1
    Returns:
        RespStandby:int
    Command Timeout: 60000
    Example:EnableHeaterStandby 1
    """
    rsp = MessageServerInterface.sendSciCommand("EnableHeaterStandby",Standby)
    return int(rsp[0])

def ReadTemperatureChuckStatus():
    """
    Returns values of the temperature chuck status. The status byte gives
    information about the current controller's action. The dew point sensor status
    encapsulates information, if such a sensor is connected, and if the actual dew
    point difference temperature is readable (active). It can be used for purge
    control. Soak time left (in seconds) is used when soak time is actually running.
    API Status: published
    Returns:
        Status:str
        DPSensor:int
        SoakTimeLeft:int
        HasEcoMode:int
    Command Timeout: 60000
    Example:ReadTemperatureChuckStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ReadTemperatureChuckStatus")
    global ReadTemperatureChuckStatus_Response
    if not "ReadTemperatureChuckStatus_Response" in globals(): ReadTemperatureChuckStatus_Response = namedtuple("ReadTemperatureChuckStatus_Response", "Status,DPSensor,SoakTimeLeft,HasEcoMode")
    return ReadTemperatureChuckStatus_Response(str(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def GetTargetTemp(Unit:str=""):
    """
    Reads the target temperature of the chuck.
    API Status: published
    Args:
        Unit:str = "Celsius"
    Returns:
        RespTemperature:Decimal
        RespUnit:str
    Command Timeout: 60000
    Example:GetTargetTemp C
    """
    rsp = MessageServerInterface.sendSciCommand("GetTargetTemp",Unit)
    global GetTargetTemp_Response
    if not "GetTargetTemp_Response" in globals(): GetTargetTemp_Response = namedtuple("GetTargetTemp_Response", "RespTemperature,RespUnit")
    return GetTargetTemp_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def SetThermoWindow(Window:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command sets the window for the target temperture which is the window in which a
    station is assumed to be at temp. Only supported on Nucleus stations.
    API Status: internal
    Args:
        Window:Decimal = 1
    Returns:
        RespWindow:Decimal
    Command Timeout: 60000
    Example:SetThermoWindow 2.0
    """
    rsp = MessageServerInterface.sendSciCommand("SetThermoWindow",Window)
    return Decimal(rsp[0])

def GetThermoWindow():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command returns the current thermo window which is the window in which a station
    is assumed to be at temp. Only supported on Nucleus stations.
    API Status: internal
    Returns:
        RespWindow:Decimal
    Command Timeout: 60000
    Example:GetThermoWindow
    """
    rsp = MessageServerInterface.sendSciCommand("GetThermoWindow")
    return Decimal(rsp[0])

def SendThermoCommand(Command:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sends a command string to the thermal chuck using the thermal chuck protocol and
    returns the thermal chucks response as command response. This command can be
    used to access thermal chuck features that are not exposed as standalone SCI
    commands. Command is currently implemented for ERS and ATT chucks.
    API Status: internal
    Args:
        Command:str = ""
    Returns:
        Response:str
    Command Timeout: 5000
    Example:SendThermoCommand RH
    """
    rsp = MessageServerInterface.sendSciCommand("SendThermoCommand",Command)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ReadAuxStatus(AuxID:int=""):
    """
    Returns the status of a single AUX site.
    API Status: published
    Args:
        AuxID:int = -1
    Returns:
        AuxIDEcho:int
        FlagsMode:int
        Comp:str
        PresetHeight:str
        AuxSiteType:str
    Command Timeout: 10000
    Example:ReadAuxStatus 1
    """
    rsp = MessageServerInterface.sendSciCommand("ReadAuxStatus",AuxID)
    global ReadAuxStatus_Response
    if not "ReadAuxStatus_Response" in globals(): ReadAuxStatus_Response = namedtuple("ReadAuxStatus_Response", "AuxIDEcho,FlagsMode,Comp,PresetHeight,AuxSiteType")
    return ReadAuxStatus_Response(int(rsp[0]),int(rsp[1]),str(rsp[2]),str(rsp[3]),str("" if len(rsp) < 5 else ' '.join(rsp[4:])))

def ReadAuxPosition(AuxID:int="", Unit:str="", PosRef:str="", Comp:str=""):
    """
    Returns the actual AUX sites position in X, Y and Z. With AUX ID set to 0, the
    position is read for the chuck stage. If no AUX ID is given, it tries to read
    the position from the active site.
    API Status: published
    Args:
        AuxID:int = -1
        Unit:str = "Microns"
        PosRef:str = "Home"
        Comp:str = "Default"
    Returns:
        AuxIDEcho:int
        X:Decimal
        Y:Decimal
        Z:Decimal
    Command Timeout: 10000
    Example:ReadAuxPosition 1 Y Z
    """
    rsp = MessageServerInterface.sendSciCommand("ReadAuxPosition",AuxID,Unit,PosRef,Comp)
    global ReadAuxPosition_Response
    if not "ReadAuxPosition_Response" in globals(): ReadAuxPosition_Response = namedtuple("ReadAuxPosition_Response", "AuxIDEcho,X,Y,Z")
    return ReadAuxPosition_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]))

def ReadAuxHeights(AuxID:int="", Unit:str=""):
    """
    Returns the actual technology heights from an AUX site. If AUX ID is set to 0,
    all response values are read from chuck stage. If no AUX ID is given, it tries
    to read the heights from the active site.
    API Status: published
    Args:
        AuxID:int = -1
        Unit:str = "Microns"
    Returns:
        AuxIDEcho:int
        Contact:Decimal
        Overtravel:Decimal
        AlignDist:Decimal
        SepDist:Decimal
    Command Timeout: 10000
    Example:ReadAuxHeights 1 Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadAuxHeights",AuxID,Unit)
    global ReadAuxHeights_Response
    if not "ReadAuxHeights_Response" in globals(): ReadAuxHeights_Response = namedtuple("ReadAuxHeights_Response", "AuxIDEcho,Contact,Overtravel,AlignDist,SepDist")
    return ReadAuxHeights_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]))

def SetAuxMode(AuxID:int="", Overtravel:int=""):
    """
    Modes manage the way a stage behaves when it is in contact height. AUX site mode
    holds only a single flag. Flags can be turned on by using the value 1 or turned
    off by using the value 0. If you do not want to change the flag - use the value
    of 2. If AUX ID is set to 0, all flags are set for chuck stage. AUX site will
    move an additional overtravel on every contact move.
    API Status: published
    Args:
        AuxID:int = -1
        Overtravel:int = 2
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetAuxMode 1 2
    """
    rsp = MessageServerInterface.sendSciCommand("SetAuxMode",AuxID,Overtravel)
    return int(rsp[0])

def SetAuxHome(AuxID:int="", Mode:str="", Unit:str="", XValue:Decimal="", YValue:Decimal=""):
    """
    Sets the AUX sites Home position in X and Y. It defines the origin of the AUX
    sites coordinate system for later movements. Usually this position is identical
    to the die home position.
    API Status: published
    Args:
        AuxID:int = -1
        Mode:str = "0"
        Unit:str = "Microns"
        XValue:Decimal = 0
        YValue:Decimal = 0
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetAuxHome 1 0 Y
    """
    rsp = MessageServerInterface.sendSciCommand("SetAuxHome",AuxID,Mode,Unit,XValue,YValue)
    return int(rsp[0])

def SetAuxIndex(AuxID:int="", XValue:Decimal="", YValue:Decimal="", Unit:str=""):
    """
    Sets the AUX sites index size. If AUX ID is set to 0, index size is set for
    chuck stage.
    API Status: published
    Args:
        AuxID:int = -1
        XValue:Decimal = 0
        YValue:Decimal = 0
        Unit:str = "Microns"
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetAuxIndex 1 1000. 1000. Y
    """
    rsp = MessageServerInterface.sendSciCommand("SetAuxIndex",AuxID,XValue,YValue,Unit)
    return int(rsp[0])

def SetAuxHeight(AuxID:int="", PresetHeight:str="", Mode:str="", Unit:str="", Value:Decimal=""):
    """
    Sets the AUX sites contact height and corresponding gaps for overtravel,
    alignment and separation height. A contact height search gap for contact search
    with edge sensor can also be set. This search gap is always identical for all
    AUX sites. Without any optional parameters the command sets contact height to
    the current position.
    API Status: published
    Args:
        AuxID:int = -1
        PresetHeight:str = "Contact"
        Mode:str = "0"
        Unit:str = "Microns"
        Value:Decimal = 0
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetAuxHeight 1 C 0 Y
    """
    rsp = MessageServerInterface.sendSciCommand("SetAuxHeight",AuxID,PresetHeight,Mode,Unit,Value)
    return int(rsp[0])

def ReadAuxIndex(AuxID:int="", Unit:str=""):
    """
    Returns the actual AUX sites index values. If AUX ID is set to 0, the index size
    is read from chuck stage. If no AUX ID is given, it tries to read the index from
    the active site.
    API Status: published
    Args:
        AuxID:int = -1
        Unit:str = "Microns"
    Returns:
        AuxIDEcho:int
        IndexX:Decimal
        IndexY:Decimal
    Command Timeout: 10000
    Example:ReadAuxIndex 1 Y
    """
    rsp = MessageServerInterface.sendSciCommand("ReadAuxIndex",AuxID,Unit)
    global ReadAuxIndex_Response
    if not "ReadAuxIndex_Response" in globals(): ReadAuxIndex_Response = namedtuple("ReadAuxIndex_Response", "AuxIDEcho,IndexX,IndexY")
    return ReadAuxIndex_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def SetAuxThetaHome(AuxID:int="", Mode:str="", Unit:str="", Position:Decimal=""):
    """
    Sets the AUX sites theta home position. It defines the origin of the AUX sites
    theta coordinate system for later movements. If AUX ID is set to 0, theta home
    position is set for chuck stage.
    API Status: published
    Args:
        AuxID:int = -1
        Mode:str = "0"
        Unit:str = "Microns"
        Position:Decimal = 0
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetAuxThetaHome 1 0
    """
    rsp = MessageServerInterface.sendSciCommand("SetAuxThetaHome",AuxID,Mode,Unit,Position)
    return int(rsp[0])

def EnableOffset(Stage:str="", Enable:int="", Move:int=""):
    """
    Enables or disables the Offset XY compensation for the selected stage. If the
    compensation holds an offset different from zero, the chuck is automatically
    moved the distance of the offset. The chuck also moves automatically to a safe
    height. The move can be disabled by the third parameter. This may put the stage
    outside the software fence.
    API Status: published
    Args:
        Stage:str = "Chuck"
        Enable:int = 1
        Move:int = 1
    Command Timeout: 60000
    Example:EnableOffset C 1
    """
    MessageServerInterface.sendSciCommand("EnableOffset",Stage,Enable,Move)


def SetOffset(Stage:str="", OffsetX:Decimal="", OffsetY:Decimal=""):
    """
    Sets the offset values for the Offset XY compensation for the selected stage.
    The changes take effect immediately. Note that the Offset XY compensation must
    be enabled for the values to take effect. The compensation is enabled or
    disabled using EnableOffset command.
    API Status: published
    Args:
        Stage:str = "Chuck"
        OffsetX:Decimal = 0
        OffsetY:Decimal = 0
    Command Timeout: 5000
    Example:SetOffset C 100000.0 0.0
    """
    MessageServerInterface.sendSciCommand("SetOffset",Stage,OffsetX,OffsetY)


def GetOffsetInfo(Stage:str=""):
    """
    Gets information about the Offset XY compensation of the selected stage,
    including the stored offset values and whether the compensation is enabled or
    disabled.
    API Status: published
    Args:
        Stage:str = "Chuck"
    Returns:
        Enable:int
        OffsetX:Decimal
        OffsetY:Decimal
    Command Timeout: 5000
    Example:GetOffsetInfo C
    """
    rsp = MessageServerInterface.sendSciCommand("GetOffsetInfo",Stage)
    global GetOffsetInfo_Response
    if not "GetOffsetInfo_Response" in globals(): GetOffsetInfo_Response = namedtuple("GetOffsetInfo_Response", "Enable,OffsetX,OffsetY")
    return GetOffsetInfo_Response(int(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]))

def SetSwitchPosition(Stage:str="", AuxSite:int="", X:Decimal="", Y:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the switch position of a stage. This is the position to move to if an aux
    site gets active. This is only supported for the chuck and it's aux sites. Aux
    index 0 means wafer site, 1 means aux site 1 and so on.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        AuxSite:int = 0
        X:Decimal = 0
        Y:Decimal = 0
    Command Timeout: 5000
    Example:SetSwitchPosition C 0 5000 5000
    """
    MessageServerInterface.sendSciCommand("SetSwitchPosition",Stage,AuxSite,X,Y)


def MoveAuxSite(AuxID:int=""):
    """
    Moves the chuck to the position of a given AUX site. A safe height is used for
    the move. If AUX ID is set to 0, the target of the move is the wafer site.
    API Status: published
    Args:
        AuxID:int = -1
    Returns:
        AuxIDEcho:int
    Command Timeout: 60000
    Example:MoveAuxSite 1
    """
    rsp = MessageServerInterface.sendSciCommand("MoveAuxSite",AuxID)
    return int(rsp[0])

def SetAuxSiteCount(AuxSiteCount:int=""):
    """
    Sets the number of available AUX sites. For preparing for example two cal
    chucks, the count must be set to 2. For the changes to take effect the system
    needs to be restarted.
    API Status: published
    Args:
        AuxSiteCount:int = 0
    Command Timeout: 10000
    Example:SetAuxSiteCount 2
    """
    MessageServerInterface.sendSciCommand("SetAuxSiteCount",AuxSiteCount)


def GetAuxSiteCount():
    """
    Reads the number of available AUX sites and the ID of the actual active AUX
    site. If this is 0, the chuck stage is currently active.
    API Status: published
    Returns:
        AuxSiteCount:int
        ActualAuxSite:int
    Command Timeout: 10000
    Example:GetAuxSiteCount
    """
    rsp = MessageServerInterface.sendSciCommand("GetAuxSiteCount")
    global GetAuxSiteCount_Response
    if not "GetAuxSiteCount_Response" in globals(): GetAuxSiteCount_Response = namedtuple("GetAuxSiteCount_Response", "AuxSiteCount,ActualAuxSite")
    return GetAuxSiteCount_Response(int(rsp[0]),int(rsp[1]))

def SetAuxSiteName(AuxID:int="", AuxSiteName:str=""):
    """
    Sets the description of an AUX site. With AUX ID zero, the description of the
    wafer site can be set.
    API Status: published
    Args:
        AuxID:int = -1
        AuxSiteName:str = ""
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetAuxSiteName 1 Aux site 1
    """
    rsp = MessageServerInterface.sendSciCommand("SetAuxSiteName",AuxID,AuxSiteName)
    return int(rsp[0])

def GetAuxSiteName(AuxID:int=""):
    """
    This command reads the description of an AUX site. If AUX ID is set to 0, the
    description of the chuck stage is given back. If no AUX ID is given, it tries to
    read from the active site.
    API Status: published
    Args:
        AuxID:int = -1
    Returns:
        AuxIDEcho:int
        AuxSiteName:str
    Command Timeout: 10000
    Example:GetAuxSiteName 1
    """
    rsp = MessageServerInterface.sendSciCommand("GetAuxSiteName",AuxID)
    global GetAuxSiteName_Response
    if not "GetAuxSiteName_Response" in globals(): GetAuxSiteName_Response = namedtuple("GetAuxSiteName_Response", "AuxIDEcho,AuxSiteName")
    return GetAuxSiteName_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def CleanProbeTip(AuxID:str=""):
    """
    Starts a probe tip cleaning on the given AUX site. The cleaning algorithm is
    dependent from the type of the AUX site and from the duration and the cleaning
    count that is set in configuration. The cleaning algorithm includes both a move
    to the pad site and a move back to the source site.
    API Status: published
    Args:
        AuxID:str = "-1"
    Returns:
        AuxIDEcho:int
    Command Timeout: 300000
    Example:CleanProbeTip 1
    """
    rsp = MessageServerInterface.sendSciCommand("CleanProbeTip",AuxID)
    return int(rsp[0])

def SetAuxSiteType(AuxID:int="", AuxSiteType:str=""):
    """
    Sets the type for a given AUX site. It depends on the type of the AUX site, if
    there is a cleaning algorithm available. It is not possible to set the type of
    the wafer site (AUX site 0).
    API Status: published
    Args:
        AuxID:int = -1
        AuxSiteType:str = "AuxUnknown"
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetAuxSiteType 1 G
    """
    rsp = MessageServerInterface.sendSciCommand("SetAuxSiteType",AuxID,AuxSiteType)
    return int(rsp[0])

def SetCleaningParams(AuxID:int="", Count:int="", Time:int=""):
    """
    Sets the cleaning parameters for a given AUX site. It is not possible to set the
    cleaning parameters of the wafer site (AUX site 0). If no AUX ID is given, it
    tries to set the parameters of the active site.     The cleaning count defines,
    how much times the cleaning is performed repeatedly. The cleaning time defines,
    how much     milliseconds the needles wait in cleaning position during each
    cleaning cycle.
    API Status: published
    Args:
        AuxID:int = -1
        Count:int = 1
        Time:int = 0
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:SetCleaningParams 1 5 1000
    """
    rsp = MessageServerInterface.sendSciCommand("SetCleaningParams",AuxID,Count,Time)
    return int(rsp[0])

def GetCleaningParams(AuxID:int=""):
    """
    Reads the cleaning parameters of a given AUX site. It is not possible to read
    cleaning parameters of the wafer site (AUX site 0).
    API Status: published
    Args:
        AuxID:int = -1
    Returns:
        AuxIDEcho:int
        Count:int
        Time:int
        Remaining:int
    Command Timeout: 30000
    Example:GetCleaningParams
    """
    rsp = MessageServerInterface.sendSciCommand("GetCleaningParams",AuxID)
    global GetCleaningParams_Response
    if not "GetCleaningParams_Response" in globals(): GetCleaningParams_Response = namedtuple("GetCleaningParams_Response", "AuxIDEcho,Count,Time,Remaining")
    return GetCleaningParams_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]))

def UpdateAuxSitePositions(AuxID:int="", XOffset:Decimal="", YOffset:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Rotate the switch, home, and fence positions to match the current chuck theta
    angle and adjust Home/Switch by XY offset. Should only be used for Aux sites
    that don't move theta.
    API Status: internal
    Args:
        AuxID:int = -1
        XOffset:Decimal = 0
        YOffset:Decimal = 0
    Returns:
        AuxIDEcho:int
    Command Timeout: 5000
    Example:UpdateAuxSitePositions 1
    """
    rsp = MessageServerInterface.sendSciCommand("UpdateAuxSitePositions",AuxID,XOffset,YOffset)
    return int(rsp[0])

def ResetCleaningPosition(AuxID:str="", OffsetX:Decimal="", OffsetY:Decimal=""):
    """
    Resets the cleaning position to the beginning of the cleaning aux site (home).
    API Status: published
    Args:
        AuxID:str = "-1"
        OffsetX:Decimal = 0
        OffsetY:Decimal = 0
    Returns:
        AuxIDEcho:int
    Command Timeout: 10000
    Example:ResetCleaningPosition 5
    """
    rsp = MessageServerInterface.sendSciCommand("ResetCleaningPosition",AuxID,OffsetX,OffsetY)
    return int(rsp[0])

def BnR_EchoData(ControllerID:int="", TestCmd:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Test Command for the Kernel Communication. It is like a ping command. The given
    text string is returned unchanged.
    API Status: internal
    Args:
        ControllerID:int = 1
        TestCmd:str = "Test"
    Returns:
        TestRsp:str
    Command Timeout: 5000
    Example:BnR_EchoData 1 Hello World
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_EchoData",ControllerID,TestCmd)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def BnR_ReportKernelVersion(ControllerID:int="", Module:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the actual version information of the controller software.
    The 'Version' value contains version number and revision level of the actual
    implementation.                                    The text string contains a
    code description, version number and the revision date.
    The 'Module' byte is optional (default is K).
    API Status: internal
    Args:
        ControllerID:int = 1
        Module:str = "K"
    Returns:
        Version:Decimal
        Description:str
    Command Timeout: 5000
    Example:BnR_ReportKernelVersion 1 K
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_ReportKernelVersion",ControllerID,Module)
    global BnR_ReportKernelVersion_Response
    if not "BnR_ReportKernelVersion_Response" in globals(): BnR_ReportKernelVersion_Response = namedtuple("BnR_ReportKernelVersion_Response", "Version,Description")
    return BnR_ReportKernelVersion_Response(Decimal(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_GetStationType(ControllerID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns information about the connected station.
    API Status: internal
    Args:
        ControllerID:int = 1
    Returns:
        StationType:str
        Type:str
    Command Timeout: 5000
    Example:BnR_GetStationType 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetStationType",ControllerID)
    global BnR_GetStationType_Response
    if not "BnR_GetStationType_Response" in globals(): BnR_GetStationType_Response = namedtuple("BnR_GetStationType_Response", "StationType,Type")
    return BnR_GetStationType_Response(str(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_ResetController(ControllerID:int="", Mode:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Restarts the BnR controller.
    API Status: internal
    Args:
        ControllerID:int = 1
        Mode:str = "X"
    Command Timeout: 10000
    Example:BnR_ResetController 1
    """
    MessageServerInterface.sendSciCommand("BnR_ResetController",ControllerID,Mode)


def BnR_SetOutput(ControllerID:int="", Channel:str="", State:int="", CycleTime:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Controls the Velox output channel signals. It can be used to activate/deactivate
    outputs.
    API Status: internal
    Args:
        ControllerID:int = 1
        Channel:str = "DO_WaferVacuum"
        State:int = 0
        CycleTime:int = 0
    Command Timeout: 5000
    Example:BnR_SetOutput 1 1000 1 2000
    """
    MessageServerInterface.sendSciCommand("BnR_SetOutput",ControllerID,Channel,State,CycleTime)


def BnR_GetOutput(ControllerID:int="", Channel:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the state of an output channel. By using the string identifier DO_ALL, a
    string list of all outputs is returned in addition
    API Status: internal
    Args:
        ControllerID:int = 1
        Channel:str = "DO_WaferVacuum"
    Returns:
        State:int
        AllOutputs:str
    Command Timeout: 5000
    Example:BnR_GetOutput 1 DO_WaferVacuum
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetOutput",ControllerID,Channel)
    global BnR_GetOutput_Response
    if not "BnR_GetOutput_Response" in globals(): BnR_GetOutput_Response = namedtuple("BnR_GetOutput_Response", "State,AllOutputs")
    return BnR_GetOutput_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_GetInput(ControllerID:int="", Channel:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the state of an input channel. By using the string identifier DI_ALL, a
    string list of all outputs is returned in addition
    API Status: internal
    Args:
        ControllerID:int = 1
        Channel:str = "DI_MotorPower"
    Returns:
        State:int
        AllInputs:str
    Command Timeout: 5000
    Example:BnR_GetInput 1 DI_MotorPower
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetInput",ControllerID,Channel)
    global BnR_GetInput_Response
    if not "BnR_GetInput_Response" in globals(): BnR_GetInput_Response = namedtuple("BnR_GetInput_Response", "State,AllInputs")
    return BnR_GetInput_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_SetAnalogOutput(ControllerID:int="", Channel:str="", OutputPercent:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets an analog output channel to a given value.
    API Status: internal
    Args:
        ControllerID:int = 1
        Channel:str = "AO_PurgeDewPoint"
        OutputPercent:Decimal = 50
    Command Timeout: 5000
    Example:BnR_SetAnalogOutput 1 AO_PurgeDewPoint 50
    """
    MessageServerInterface.sendSciCommand("BnR_SetAnalogOutput",ControllerID,Channel,OutputPercent)


def BnR_GetAnalogIO(ControllerID:int="", Channel:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current value of an analog output or input.
    API Status: internal
    Args:
        ControllerID:int = 1
        Channel:str = "AO_PurgeDewPoint"
    Returns:
        Value:Decimal
        UnderOverflow:int
    Command Timeout: 5000
    Example:BnR_GetAnalogIO 1 AO_PurgeDewPoint
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetAnalogIO",ControllerID,Channel)
    global BnR_GetAnalogIO_Response
    if not "BnR_GetAnalogIO_Response" in globals(): BnR_GetAnalogIO_Response = namedtuple("BnR_GetAnalogIO_Response", "Value,UnderOverflow")
    return BnR_GetAnalogIO_Response(Decimal(rsp[0]),int(rsp[1]))

def BnR_GetStartupStatus(ControllerID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the startup status of the BnR controller to determine if the controller
    is properly booted or still starting.
    API Status: internal
    Args:
        ControllerID:int = 1
    Returns:
        StartupStatus:str
        AdditionalStatusInfo:str
    Command Timeout: 5000
    Example:BnR_GetStartupStatus 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetStartupStatus",ControllerID)
    global BnR_GetStartupStatus_Response
    if not "BnR_GetStartupStatus_Response" in globals(): BnR_GetStartupStatus_Response = namedtuple("BnR_GetStartupStatus_Response", "StartupStatus,AdditionalStatusInfo")
    return BnR_GetStartupStatus_Response(str(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_CreateSdmSystemDump(ControllerID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Creates a Sdm System Dump file on the B&R flash
    API Status: internal
    Args:
        ControllerID:int = 1
    Command Timeout: 60000
    Example:BnR_CreateSdmSystemDump
    """
    MessageServerInterface.sendSciCommand("BnR_CreateSdmSystemDump",ControllerID)


def BnR_GetControllerData(ControllerID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Gets controller data from the B&R controller. Currently used for init
    information.
    API Status: internal
    Args:
        ControllerID:int = 1
    Command Timeout: 10000
    Example:BnR_GetControllerData 1
    """
    MessageServerInterface.sendSciCommand("BnR_GetControllerData",ControllerID)


def BnR_WriteMessage(MessageType:str="", Message:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command to write a (native) message to Controller
    API Status: internal
    Args:
        MessageType:str = "mtCryoLoader"
        Message:str = ""
    Command Timeout: 5000
    Example:BnR_WriteMessage 1 mtCryoLoader SampleMessage
    """
    MessageServerInterface.sendSciCommand("BnR_WriteMessage",MessageType,Message)


def BnR_ReadMessage(MessageType:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command to read a (native) message from Controller
    API Status: internal
    Args:
        MessageType:str = "mtCryoLoader"
    Returns:
        Message:str
    Command Timeout: 5000
    Example:BnR_ReadMessage 1 mtCryoLoader
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_ReadMessage",MessageType)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def BnR_GetDataIterator(ControllerID:int="", ShowAll:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns a data stream handle which represents a data stream of setup parameters
    and requires the BnR_GetNextDatum command.
    API Status: internal
    Args:
        ControllerID:int = 1
        ShowAll:int = 0
    Returns:
        IdentityToken:int
        SizeNoAll:int
    Command Timeout: 5000
    Example:BnR_GetDataIterator 1 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetDataIterator",ControllerID,ShowAll)
    global BnR_GetDataIterator_Response
    if not "BnR_GetDataIterator_Response" in globals(): BnR_GetDataIterator_Response = namedtuple("BnR_GetDataIterator_Response", "IdentityToken,SizeNoAll")
    return BnR_GetDataIterator_Response(int(rsp[0]),int(rsp[1]))

def BnR_GetNextDatum(ControllerID:int="", IdentityToken:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the next parameter from the data stream. Fields are separated by a
    colon. Structure of the response parameter Value:
    Path_Path:Name:Description:Value
    API Status: internal
    Args:
        ControllerID:int = 1
        IdentityToken:int = 0
    Returns:
        IsLastDatum:int
        DatumCode:int
        PathNameDescrValue:str
    Command Timeout: 10000
    Example:BnR_GetNextDatum 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetNextDatum",ControllerID,IdentityToken)
    global BnR_GetNextDatum_Response
    if not "BnR_GetNextDatum_Response" in globals(): BnR_GetNextDatum_Response = namedtuple("BnR_GetNextDatum_Response", "IsLastDatum,DatumCode,PathNameDescrValue")
    return BnR_GetNextDatum_Response(int(rsp[0]),int(rsp[1]),str("" if len(rsp) < 3 else ' '.join(rsp[2:])))

def BnR_SetDatum(ControllerID:int="", PathNameAndValue:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the value of a parameter. An empty parameter string saves the whole
    configuration to non-volatile memory. Fields are separated by a colon.
    API Status: internal
    Args:
        ControllerID:int = 1
        PathNameAndValue:str = ""
    Command Timeout: 20000
    Example:BnR_SetDatum 1 Chuck_XAxisData:CurrentMaximal:70
    """
    MessageServerInterface.sendSciCommand("BnR_SetDatum",ControllerID,PathNameAndValue)


def BnR_GetDatum(ControllerID:int="", PathName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns a value string. The Value string consists of the value and the
    description. The Locator only consists of the path and the name. All fields are
    separated by a colon.  Structure of the command parameter Locator:
    Path_Path:Name Structure of the response parameter Value: Value:Description
    API Status: internal
    Args:
        ControllerID:int = 1
        PathName:str = ""
    Returns:
        DatumCode:int
        ValueDesc:str
    Command Timeout: 5000
    Example:BnR_GetDatum 1 Chuck_XAxisData:CurrentMaximal
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetDatum",ControllerID,PathName)
    global BnR_GetDatum_Response
    if not "BnR_GetDatum_Response" in globals(): BnR_GetDatum_Response = namedtuple("BnR_GetDatum_Response", "DatumCode,ValueDesc")
    return BnR_GetDatum_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_DoInternalTask(ControllerID:int="", Task:str="", PCmdInt1:int="", PCmdInt2:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Executes an internal BnR Task
    API Status: internal
    Args:
        ControllerID:int = 1
        Task:str = ""
        PCmdInt1:int = 0
        PCmdInt2:int = 0
    Returns:
        RspInt:int
        RspString:str
    Command Timeout: 10000
    Example:BnR_DoInternalTask 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_DoInternalTask",ControllerID,Task,PCmdInt1,PCmdInt2)
    global BnR_DoInternalTask_Response
    if not "BnR_DoInternalTask_Response" in globals(): BnR_DoInternalTask_Response = namedtuple("BnR_DoInternalTask_Response", "RspInt,RspString")
    return BnR_DoInternalTask_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_GetPosition(Stage:str="", Unit:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current positions for the X,Y,Z (or T) axis for the specified stage
    as well as the commanded positions.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Unit:str = "Microns"
    Returns:
        XorT:Decimal
        Y:Decimal
        Z:Decimal
        CommandedXorT:Decimal
        CommandedY:Decimal
        CommandedZ:Decimal
    Command Timeout: 5000
    Example:BnR_GetPosition 1 C
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetPosition",Stage,Unit)
    global BnR_GetPosition_Response
    if not "BnR_GetPosition_Response" in globals(): BnR_GetPosition_Response = namedtuple("BnR_GetPosition_Response", "XorT,Y,Z,CommandedXorT,CommandedY,CommandedZ")
    return BnR_GetPosition_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]))

def BnR_Move(Stage:str="", XValue:Decimal="", YValue:Decimal="", VelX:Decimal="", VelY:Decimal="", WaitFinished:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command executes a XY movement for a specified stage. This can be either a
    blocking or non blocking move.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        XValue:Decimal = 0
        YValue:Decimal = 0
        VelX:Decimal = 0
        VelY:Decimal = 0
        WaitFinished:int = 1
    Returns:
        X:Decimal
        Y:Decimal
    Command Timeout: 60000
    Example:BnR_Move 1 C 5000 5000 Z 100 100 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_Move",Stage,XValue,YValue,VelX,VelY,WaitFinished)
    global BnR_Move_Response
    if not "BnR_Move_Response" in globals(): BnR_Move_Response = namedtuple("BnR_Move_Response", "X,Y")
    return BnR_Move_Response(Decimal(rsp[0]),Decimal(rsp[1]))

def BnR_MoveZ(Stage:str="", ZValue:Decimal="", Vel:Decimal="", Dec:Decimal="", WaitFinished:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the stage Z axis to a new position.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        ZValue:Decimal = 0
        Vel:Decimal = 0
        Dec:Decimal = 0
        WaitFinished:int = 1
    Returns:
        Z:Decimal
    Command Timeout: 600000
    Example:BnR_MoveZ 1 C 12000 100 100 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_MoveZ",Stage,ZValue,Vel,Dec,WaitFinished)
    return Decimal(rsp[0])

def BnR_ScanMoveZ(ControllerID:int="", Stage:str="", ZDistance:Decimal="", TriggerEveryNthCycle:int="", Vel:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command executes a scan movement of the Z axis that sets a digital output
    every couple microns to trigger e.g. a camera. After the move is finished, the
    command returns a list of Z heights at which the digital output was set.
    API Status: internal
    Args:
        ControllerID:int = 1
        Stage:str = "Chuck"
        ZDistance:Decimal = 1000
        TriggerEveryNthCycle:int = 2
        Vel:Decimal = 10
    Command Timeout: 300000
    Example:BnR_ScanMoveZ 1 C 1000 6 10
    """
    MessageServerInterface.sendSciCommand("BnR_ScanMoveZ",ControllerID,Stage,ZDistance,TriggerEveryNthCycle,Vel)


def BnR_MoveT(TValue:Decimal="", Vel:Decimal="", WaitFinished:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Executes a movement of the theta axis, either blocking or non blocking
    API Status: internal
    Args:
        TValue:Decimal = 0
        Vel:Decimal = 0
        WaitFinished:int = 1
    Returns:
        T:Decimal
    Command Timeout: 60000
    Example:BnR_MoveT 1 1.003 10 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_MoveT",TValue,Vel,WaitFinished)
    return Decimal(rsp[0])

def BnR_StopAxis(Stage:str="", FlagsStop:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Stops 1... all axes of a stage
    API Status: internal
    Args:
        Stage:str = "Chuck"
        FlagsStop:int = 15
    Command Timeout: 5000
    Example:BnR_StopAxis 1 C 7
    """
    MessageServerInterface.sendSciCommand("BnR_StopAxis",Stage,FlagsStop)


def BnR_InitAxis(Stage:str="", FlagsInit:int="", FlagsDirection:int="", FlagsInitInPlace:int="", LowLimitX:Decimal="", LowLimitY:Decimal="", LowLimitZ:Decimal="", LowLimitTh:Decimal="", InitInPlaceMoveRangeX:Decimal="", InitInPlaceMoveRangeY:Decimal="", InitInPlaceMoveRangeZ:Decimal="", InitInPlaceMoveRangeTh:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Machine Coordinate System: X Y Z Theta  - _FlagsInit_: X, Y, Z, Theta -
    _FlagsDirection_: X, Y, Z, Theta (true means plus direction) -
    _FlagsInitInPlace_: X, Y, Z, Theta   All flags can be accessed by indirect
    members. Initializes the stage and resets current coordinate system. Should be
    used only in cases when the reported coordinates do not correspond to real
    position of mechanics. Init in Place performs the initialization without any
    movements.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        FlagsInit:int = 0
        FlagsDirection:int = 0
        FlagsInitInPlace:int = 0
        LowLimitX:Decimal = 0
        LowLimitY:Decimal = 0
        LowLimitZ:Decimal = 0
        LowLimitTh:Decimal = 0
        InitInPlaceMoveRangeX:Decimal = 0
        InitInPlaceMoveRangeY:Decimal = 0
        InitInPlaceMoveRangeZ:Decimal = 0
        InitInPlaceMoveRangeTh:Decimal = 0
    Command Timeout: 300000
    Example:BnR_InitAxis 1 C 7
    """
    MessageServerInterface.sendSciCommand("BnR_InitAxis",Stage,FlagsInit,FlagsDirection,FlagsInitInPlace,LowLimitX,LowLimitY,LowLimitZ,LowLimitTh,InitInPlaceMoveRangeX,InitInPlaceMoveRangeY,InitInPlaceMoveRangeZ,InitInPlaceMoveRangeTh)


def BnR_GetAxisState(Stage:str="", Axis:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command returns the state of an axis (disabled/standstill/errorstop/stoppin
    g/homing/continuousmotion/discretemotion/synchronizedmotion)
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
    Returns:
        State:str
        AdditionalStateInfo:str
    Command Timeout: 5000
    Example:BnR_GetAxisState 1 C X
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetAxisState",Stage,Axis)
    global BnR_GetAxisState_Response
    if not "BnR_GetAxisState_Response" in globals(): BnR_GetAxisState_Response = namedtuple("BnR_GetAxisState_Response", "State,AdditionalStateInfo")
    return BnR_GetAxisState_Response(str(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def BnR_GetAxisStatus(Stage:str="", Axis:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command returns some axis status information
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
    Returns:
        Initialized:int
        PositiveEndlimit:int
        NegativeEndlimit:int
    Command Timeout: 5000
    Example:BnR_GetAxisStatus 1 C X
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetAxisStatus",Stage,Axis)
    global BnR_GetAxisStatus_Response
    if not "BnR_GetAxisStatus_Response" in globals(): BnR_GetAxisStatus_Response = namedtuple("BnR_GetAxisStatus_Response", "Initialized,PositiveEndlimit,NegativeEndlimit")
    return BnR_GetAxisStatus_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]))

def BnR_SetQuietMode(Stage:str="", QuietMode:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command to enable the quiet mode for a stage (quiet turns motors powerless)
    API Status: internal
    Args:
        Stage:str = "Chuck"
        QuietMode:int = 0
    Command Timeout: 5000
    Example:BnR_SetQuietMode 1 C 1
    """
    MessageServerInterface.sendSciCommand("BnR_SetQuietMode",Stage,QuietMode)


def BnR_GetQuietMode(Stage:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command to query the quiet mode for a stage
    API Status: internal
    Args:
        Stage:str = "Chuck"
    Returns:
        QuietMode:int
    Command Timeout: 5000
    Example:BnR_GetQuietMode 1 C
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetQuietMode",Stage)
    return int(rsp[0])

def BnR_GetInternalAxisInfo(Stage:str="", Axis:str="", InfoType:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command returns various axis information, dependent on the InfoType
    parameter
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
        InfoType:str = "StallInfo"
    Returns:
        RspString:str
    Command Timeout: 5000
    Example:BnR_GetInternalAxisInfo 1 C X
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetInternalAxisInfo",Stage,Axis,InfoType)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def BnR_GetWiringTesterData(Stage:str="", Axis:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command to get various information required for the BnR wiring tester tool.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
    Returns:
        STIn_ModuleOK:int
        STIn_LifeCnt:int
        STIn_DrvOK:int
        STIn_OvertemperatureError:int
        STIn_CurrentError:int
        STIn_OvercurrentError:int
        STIn_RefPulsePos:int
        STIn_RefPulseCnt:int
        STIn_ModulePowerSupplyError:int
        STOut_SetTime:int
        STOut_MotorStep0:int
        STOut_DriveEnable:int
        STOut_BoostCurrent:int
        STOut_StandStillCurrent:int
        STOut_ClearError:int
        CMIn_ModuleOK:int
        CMIn_SDCLifeCount:int
        CMIn_Encoder:int
        CMIn_EncoderTimeValid:int
        CMIn_DigitalInput1:int
        CMIn_DigitalInput2:int
        CMIn_BWChannelA:int
        CMIn_BWChannelB:int
        CMIn_PowerSupply2:int
        CMOut_QuitChannelA:int
        CMOut_QuitChannelB:int
        SWAxisErrorID:int
        SWAxisErrorDesc:str
    Command Timeout: 5000
    Example:BnR_GetWiringTesterData 1 C X
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetWiringTesterData",Stage,Axis)
    global BnR_GetWiringTesterData_Response
    if not "BnR_GetWiringTesterData_Response" in globals(): BnR_GetWiringTesterData_Response = namedtuple("BnR_GetWiringTesterData_Response", "STIn_ModuleOK,STIn_LifeCnt,STIn_DrvOK,STIn_OvertemperatureError,STIn_CurrentError,STIn_OvercurrentError,STIn_RefPulsePos,STIn_RefPulseCnt,STIn_ModulePowerSupplyError,STOut_SetTime,STOut_MotorStep0,STOut_DriveEnable,STOut_BoostCurrent,STOut_StandStillCurrent,STOut_ClearError,CMIn_ModuleOK,CMIn_SDCLifeCount,CMIn_Encoder,CMIn_EncoderTimeValid,CMIn_DigitalInput1,CMIn_DigitalInput2,CMIn_BWChannelA,CMIn_BWChannelB,CMIn_PowerSupply2,CMOut_QuitChannelA,CMOut_QuitChannelB,SWAxisErrorID,SWAxisErrorDesc")
    return BnR_GetWiringTesterData_Response(int(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),int(rsp[4]),int(rsp[5]),int(rsp[6]),int(rsp[7]),int(rsp[8]),int(rsp[9]),int(rsp[10]),int(rsp[11]),int(rsp[12]),int(rsp[13]),int(rsp[14]),int(rsp[15]),int(rsp[16]),int(rsp[17]),int(rsp[18]),int(rsp[19]),int(rsp[20]),int(rsp[21]),int(rsp[22]),int(rsp[23]),int(rsp[24]),int(rsp[25]),int(rsp[26]),str("" if len(rsp) < 28 else ' '.join(rsp[27:])))

def BnR_MoveAxis(Stage:str="", Axis:str="", Value:Decimal="", Vel:Decimal="", Dec:Decimal="", WaitFinished:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command allows moving a single axis to and e.g. in case of X does not
    trigger a Y movement
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
        Value:Decimal = 0
        Vel:Decimal = 0
        Dec:Decimal = 0
        WaitFinished:int = 1
    Returns:
        PositionAfterMove:Decimal
    Command Timeout: 60000
    Example:BnR_MoveAxis 1 C X 20000 100 100 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_MoveAxis",Stage,Axis,Value,Vel,Dec,WaitFinished)
    return Decimal(rsp[0])

def BnR_MoveZCombined(ChuckTargetZ:Decimal="", WaitFinished:int="", ForcedAbsVelocity:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Move Chuck-Z and (by fixed factor) Scope X, Y and Z
    API Status: internal
    Args:
        ChuckTargetZ:Decimal = 0
        WaitFinished:int = 1
        ForcedAbsVelocity:int = 0
    Returns:
        ChuckZ:Decimal
        ScopeX:Decimal
        ScopeY:Decimal
        ScopeZ:Decimal
    Command Timeout: 600000
    Example:BnR_MoveZCombined 1 17592.5 1
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_MoveZCombined",ChuckTargetZ,WaitFinished,ForcedAbsVelocity)
    global BnR_MoveZCombined_Response
    if not "BnR_MoveZCombined_Response" in globals(): BnR_MoveZCombined_Response = namedtuple("BnR_MoveZCombined_Response", "ChuckZ,ScopeX,ScopeY,ScopeZ")
    return BnR_MoveZCombined_Response(Decimal(rsp[0]),Decimal(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]))

def BnR_StepMove(Stage:str="", ZDown:Decimal="", XValue:Decimal="", YValue:Decimal="", ZUp:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    This command does a combined Z-XY-Z- move completely on the BnR-controller
    without WinKernel interaction. This is a part of an ongoing optimization.
    API Status: internal
    Args:
        Stage:str = "Chuck"
        ZDown:Decimal = 0
        XValue:Decimal = 0
        YValue:Decimal = 0
        ZUp:Decimal = 0
    Command Timeout: 60000
    Example:BnR_StepMove 1 C 250 1000 1000 250
    """
    MessageServerInterface.sendSciCommand("BnR_StepMove",Stage,ZDown,XValue,YValue,ZUp)


def BnR_SearchEdgeSensor(SearchEndPos:Decimal="", Velocity:Decimal=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Performs a search move until the search end position is reached or the edge
    sensor triggers. If the edge sensor triggers during the move, the trigger
    position is returned.Otherwise, an edge sensor not found error is returned.
    API Status: internal
    Args:
        SearchEndPos:Decimal = 0
        Velocity:Decimal = 0
    Returns:
        EdgeSensorTriggerPos:Decimal
    Command Timeout: 300000
    Example:BnR_SearchEdgeSensor 3000 10
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_SearchEdgeSensor",SearchEndPos,Velocity)
    return Decimal(rsp[0])

def BnR_GetTraceData(ControllerID:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns a collection of trace data
    API Status: internal
    Args:
        ControllerID:int = 1
    Returns:
        Data:str
    Command Timeout: 5000
    Example:BnR_GetTraceData 1 C
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_GetTraceData",ControllerID)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def BnR_SetTraceMode(ControllerID:int="", Mode:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Commands sets the trace mode
    API Status: internal
    Args:
        ControllerID:int = 1
        Mode:int = 0
    Command Timeout: 5000
    Example:BnR_SetTraceMode 1 1
    """
    MessageServerInterface.sendSciCommand("BnR_SetTraceMode",ControllerID,Mode)


def BnR_WriteAxisModuleRegister(Stage:str="", Axis:str="", MotorModule:int="", RegisterName:str="", Value:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Development command to change a module register value without controller restart
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
        MotorModule:int = 0
        RegisterName:str = ""
        Value:int = 0
    Command Timeout: 5000
    Example:BnR_WriteAxisModuleRegister 1 C X 1 ConfigOutput03 70
    """
    MessageServerInterface.sendSciCommand("BnR_WriteAxisModuleRegister",Stage,Axis,MotorModule,RegisterName,Value)


def BnR_ReadAxisModuleRegister(Stage:str="", Axis:str="", MotorModule:int="", RegisterName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Development command to get any desired module register value
    API Status: internal
    Args:
        Stage:str = "Chuck"
        Axis:str = "XAxis"
        MotorModule:int = 0
        RegisterName:str = ""
    Returns:
        Value:int
    Command Timeout: 5000
    Example:BnR_ReadAxisModuleRegister 1 C X 1 ConfigOutput03
    """
    rsp = MessageServerInterface.sendSciCommand("BnR_ReadAxisModuleRegister",Stage,Axis,MotorModule,RegisterName)
    return int(rsp[0])

def ProcessStationGetStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns process station status (UNKNOWN, IDLE, BUSY, ERROR, PAUSED, Not
    Initialized) and error code with error message when error.
    API Status: internal
    Returns:
        Status:str
        SubstratePresent:int
        LastError:int
        UseLoaderModule:int
        WaferSizes:str
        StatusMessage:str
        IsLoaderJobRunning:int
    Command Timeout: 25000
    Example:ProcessStationGetStatus
    """
    rsp = MessageServerInterface.sendSciCommand("ProcessStationGetStatus")
    global ProcessStationGetStatus_Response
    if not "ProcessStationGetStatus_Response" in globals(): ProcessStationGetStatus_Response = namedtuple("ProcessStationGetStatus_Response", "Status,SubstratePresent,LastError,UseLoaderModule,WaferSizes,StatusMessage,IsLoaderJobRunning")
    return ProcessStationGetStatus_Response(str(rsp[0]),int(rsp[1]),int(rsp[2]),int(rsp[3]),str(rsp[4]),str(rsp[5]),int(rsp[6]))

def ProcessStationInit():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Initialize process station machine. This is not the prober init it is a fast
    program initialization. Only applies to fully auto systems.
    API Status: internal
    Command Timeout: 2400000
    Example:ProcessStationInit
    """
    MessageServerInterface.sendSciCommand("ProcessStationInit")


def ProcessStationFinish():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Finishes a process station process. This resets some internal test information
    for the probe station. Some data is only reset in case this command is sent
    after the last wafer in the job was tested. Only applies to fully auto systems.
    API Status: internal
    Command Timeout: 7500000
    Example:ProcessStationFinish
    """
    MessageServerInterface.sendSciCommand("ProcessStationFinish")


def ProcessStationPrepareForLoad():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Command moves the chuck of the probe station to the secondary load position and
    if available also checks the table level sensor. Only applies to fully auto
    systems.
    API Status: internal
    Command Timeout: 120000
    Example:ProcessStationPrepareForLoad
    """
    MessageServerInterface.sendSciCommand("ProcessStationPrepareForLoad")


def ProcessStationLoadComplete():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Moves the chuck out of the load position and checks if a wafer is placed. Only
    applies to fully auto systems.
    API Status: internal
    Command Timeout: 60000
    Example:ProcessStationLoadComplete
    """
    MessageServerInterface.sendSciCommand("ProcessStationLoadComplete")


def ProcessStationPrepareForUnLoad():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The module should do whatever is necessary to prepare the current wafer for
    unload. Typically this includes things such as moving lift pins and opening
    doors.
    API Status: internal
    Command Timeout: 1000000
    Example:ProcessStationPrepareForUnLoad
    """
    MessageServerInterface.sendSciCommand("ProcessStationPrepareForUnLoad")


def ProcessStationUnLoadComplete():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The module should so whatever is necessary after a wafer is unloaded. This may
    for example include closing doors.
    API Status: internal
    Command Timeout: 60000
    Example:ProcessStationUnLoadComplete
    """
    MessageServerInterface.sendSciCommand("ProcessStationUnLoadComplete")


def ProcessStationLoadRecipe(ForceReOpenProject:int="", ProjectFileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    The recipe is a zipped archive that includes all project data. This command
    tells the device to load the recipe.
    API Status: internal
    Args:
        ForceReOpenProject:int = 0
        ProjectFileName:str = ""
    Command Timeout: 60000
    Example:ProcessStationLoadRecipe 1 SampleProject.spp
    """
    MessageServerInterface.sendSciCommand("ProcessStationLoadRecipe",ForceReOpenProject,ProjectFileName)


def ProcessStationVerifyRecipe(ProjectFileName:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Requests that the device verify that the recipe given can be executed on the
    device. It should check that the recipe is correctly formed and conforms to the
    hardware of the device. It should not check for transient things such as whether
    there is sufficient media or facilities available. those kinds of checks should
    be done in PrepareForProcess
    API Status: internal
    Args:
        ProjectFileName:str = ""
    Returns:
        Verified:int
        ErrorDescription:str
    Command Timeout: 60000
    Example:ProcessStationVerifyRecipe SampleProject.spp
    """
    rsp = MessageServerInterface.sendSciCommand("ProcessStationVerifyRecipe",ProjectFileName)
    global ProcessStationVerifyRecipe_Response
    if not "ProcessStationVerifyRecipe_Response" in globals(): ProcessStationVerifyRecipe_Response = namedtuple("ProcessStationVerifyRecipe_Response", "Verified,ErrorDescription")
    return ProcessStationVerifyRecipe_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def ProcessStationStartRecipe(CurrentWaferInJob:int="", TotalWafersInJob:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Tells VeloxPro to start the current recipe. The station will switch to error if
    an error occurs. If VeloxPro recipe execution is currently paused, this command
    tells the system to continue execution.
    API Status: internal
    Args:
        CurrentWaferInJob:int = -1
        TotalWafersInJob:int = -1
    Command Timeout: 25000
    Example:ProcessStationStartRecipe 1
    """
    MessageServerInterface.sendSciCommand("ProcessStationStartRecipe",CurrentWaferInJob,TotalWafersInJob)


def ProcessStationStopRecipe():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Tells the device to stop the current recipe. The station will switch to error if
    an error occurs.
    API Status: internal
    Command Timeout: 25000
    Example:ProcessStationStopRecipe
    """
    MessageServerInterface.sendSciCommand("ProcessStationStopRecipe")


def ProcessStationRecoverError():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Tells the module to do whatever is necessary to recover from an error condition.
    API Status: internal
    Command Timeout: 60000
    Example:ProcessStationRecoverError
    """
    MessageServerInterface.sendSciCommand("ProcessStationRecoverError")


def ProcessStationGetWaferResult():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Get substrate information from process station controller application.
    API Status: internal
    Returns:
        Result:str
        PercentDone:Decimal
        AllowSkipWafer:int
        TestInformation:str
    Command Timeout: 25000
    Example:ProcessStationGetWaferResult
    """
    rsp = MessageServerInterface.sendSciCommand("ProcessStationGetWaferResult")
    global ProcessStationGetWaferResult_Response
    if not "ProcessStationGetWaferResult_Response" in globals(): ProcessStationGetWaferResult_Response = namedtuple("ProcessStationGetWaferResult_Response", "Result,PercentDone,AllowSkipWafer,TestInformation")
    return ProcessStationGetWaferResult_Response(str(rsp[0]),Decimal(rsp[1]),int(rsp[2]),str("" if len(rsp) < 4 else ' '.join(rsp[3:])))

def QueryWaferInfo():
    """
    Returns information about the wafer that is currently on the probe station. It
    will return an error when there is no wafer currently on the chuck.
    API Status: published
    Returns:
        Size:int
        Angle:Decimal
        ID:str
        LotID:str
        ProductID:str
    Command Timeout: 25000
    Example:QueryWaferInfo
    """
    rsp = MessageServerInterface.sendSciCommand("QueryWaferInfo")
    global QueryWaferInfo_Response
    if not "QueryWaferInfo_Response" in globals(): QueryWaferInfo_Response = namedtuple("QueryWaferInfo_Response", "Size,Angle,ID,LotID,ProductID")
    return QueryWaferInfo_Response(int(rsp[0]),Decimal(rsp[1]),str(rsp[2]),str(rsp[3]),str("" if len(rsp) < 5 else ' '.join(rsp[4:])))

def ProcessStationPauseRecipe():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Sets the process station to PAUSE mode
    API Status: internal
    Command Timeout: 25000
    Example:ProcessStationPauseRecipe
    """
    MessageServerInterface.sendSciCommand("ProcessStationPauseRecipe")


def GetProbingStatus():
    """
    Retrieves the current status of the prober. If probing status is AtFirstDie the
    tester can take control.
    API Status: published
    Returns:
        Status:str
    Command Timeout: 25000
    Example:GetProbingStatus
    """
    rsp = MessageServerInterface.sendSciCommand("GetProbingStatus")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ProceedProbing():
    """
    Tells the prober to proceed the recipe when current status is AtFirstDie.
    API Status: published
    Command Timeout: 25000
    Example:ProceedProbing
    """
    MessageServerInterface.sendSciCommand("ProceedProbing")


def GetCassetteStatus(Cassette:int=""):
    """
    Provides all available wafer information. It returns a set of data for each
    wafer in either cassette. The data contains the cassette and the slot number
    where the wafer is located, the status of the wafer, and identification
    information.
    API Status: published
    Args:
        Cassette:int = 0
    Returns:
        CassetteStatus:str
    Command Timeout: 25000
    Example:GetCassetteStatus 0
    """
    rsp = MessageServerInterface.sendSciCommand("GetCassetteStatus",Cassette)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def QueryWaferID(Module:str="", Slot:int=""):
    """
    Queries the wafer ID of a given module and slot.
    API Status: published
    Args:
        Module:str = "Robot"
        Slot:int = 0
    Returns:
        ID:str
    Command Timeout: 25000
    Example:QueryWaferID Cassette1 1
    """
    rsp = MessageServerInterface.sendSciCommand("QueryWaferID",Module,Slot)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def UpdateWaferID(Module:str="", Slot:int="", ID:str=""):
    """
    Overrides the wafer ID of the given module and slot. If the wafer id is empty
    and the module is a Loadport, the id will be read by the idreader if possible.
    This process behaves as follows:  - the current wafer id is reset - if the read-
    wafer-process would be delayed (e.g. there is already a   wafer on the idreader)
    the process will be aborted and an error         will be returned - if the id-
    reading fails, the process behaves like a normal inventory  triggered by the UI:
    skip (returns success), abort (returns error)      or "ask user". It is
    recomended to use either skip or abort for         remote id reading.  If the
    module is a Loadport and the slot is set to -1, a regular inventory will be
    triggered. This behaves similar to an inventory triggered by the UI: The ID
    won't be reset and already scanned wafers won't be reset. Setting an ID
    explicitly with slot -1 is an error:  - Okay, read id of wafer in slot 3 even if
    it is already set: UpdateWaferID Cassette1 3 - Okay, set id of wafer in slot 3
    to XYZ123: UpdateWaferID Cassette1 3 XYZ123 - Okay, start full inventory:
    UpdateWaferID Cassette1 -1  - Error: UpdateWaferID Cassette1 -1 XYZ123
    API Status: published
    Args:
        Module:str = "Robot"
        Slot:int = 0
        ID:str = ""
    Command Timeout: 1500000
    Example:UpdateWaferID Cassette1 1 Wafer01
    """
    MessageServerInterface.sendSciCommand("UpdateWaferID",Module,Slot,ID)


def ConfirmRecipe(ProjectFileName:str=""):
    """
    Queries whether the given project/flow name is a valid project/flow at the probe
    station.  Using file and folder names without white spaces is recommended. For
    folders and files whith white spaces use quotation marks for the path.  Example
    for using white spaces:  ConfirmRecipe
    "C:/Users/Public/Documents/Velox/Projects/White Spaces.spp"
    API Status: published
    Args:
        ProjectFileName:str = ""
    Returns:
        Verified:int
        ErrorDescription:str
    Command Timeout: 25000
    Example:ConfirmRecipe C:/Temp/Test.spp
    """
    rsp = MessageServerInterface.sendSciCommand("ConfirmRecipe",ProjectFileName)
    global ConfirmRecipe_Response
    if not "ConfirmRecipe_Response" in globals(): ConfirmRecipe_Response = namedtuple("ConfirmRecipe_Response", "Verified,ErrorDescription")
    return ConfirmRecipe_Response(int(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def StartWaferJob(RecipeName:str="", WaferIDs:str=""):
    """
    Creates and starts a new job by specifying the flow/spp file and the wafers to
    be included in the job.
    API Status: published
    Args:
        RecipeName:str = ""
        WaferIDs:str = ""
    Returns:
        JobID:str
    Command Timeout: 25000
    Example:StartWaferJob C:/Users/Public/Documents/Velox/Test.flow 1;1 2;1
    """
    rsp = MessageServerInterface.sendSciCommand("StartWaferJob",RecipeName,WaferIDs)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def GetJobParams(JobID:str=""):
    """
    Get job information for a specific job ID including the flow file and the list
    of wafers.
    API Status: published
    Args:
        JobID:str = ""
    Returns:
        RecipeName:str
        WaferIDs:str
    Command Timeout: 25000
    Example:GetJobParams 1
    """
    rsp = MessageServerInterface.sendSciCommand("GetJobParams",JobID)
    global GetJobParams_Response
    if not "GetJobParams_Response" in globals(): GetJobParams_Response = namedtuple("GetJobParams_Response", "RecipeName,WaferIDs")
    return GetJobParams_Response(str(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def JobStatus(JobID:str=""):
    """
    Retrieves the status of a specific job by its ID. If the status is ErrorWaiting,
    an error string is returned.
    API Status: published
    Args:
        JobID:str = ""
    Returns:
        Status:str
        JobStatusInfo:str
    Command Timeout: 25000
    Example:JobStatus 1
    """
    rsp = MessageServerInterface.sendSciCommand("JobStatus",JobID)
    global JobStatus_Response
    if not "JobStatus_Response" in globals(): JobStatus_Response = namedtuple("JobStatus_Response", "Status,JobStatusInfo")
    return JobStatus_Response(str(rsp[0]),str("" if len(rsp) < 2 else ' '.join(rsp[1:])))

def AbortJob(JobID:str="", Unload:int=""):
    """
    Aborts the job given by the job ID. The status of the job will be set to
    "Aborted". The "Unload" parameter defines whether the wafer remains on the chuck
    or not.
    API Status: published
    Args:
        JobID:str = ""
        Unload:int = 0
    Command Timeout: 25000
    Example:AbortJob 2 1
    """
    MessageServerInterface.sendSciCommand("AbortJob",JobID,Unload)


def ProcessStationCloseApplication(NoUserPrompt:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Closes the VeloxPro application.
    API Status: internal
    Args:
        NoUserPrompt:int = 0
    Command Timeout: 25000
    Example:ProcessStationCloseApplication
    """
    MessageServerInterface.sendSciCommand("ProcessStationCloseApplication",NoUserPrompt)


def UnloadWafer():
    """
    Unolads a Wafer from the chuck to its origin. If no origin is known, the first
    free Slot of a loadport will be chosen. A Wafer should be on the chuck.
    API Status: published
    Command Timeout: 600000
    Example:UnloadWafer
    """
    MessageServerInterface.sendSciCommand("UnloadWafer")


def GetJobList(JobType:str=""):
    """
    Returns a string for the relevant JobIDs.
    API Status: published
    Args:
        JobType:str = "Probing"
    Returns:
        GetJobList:str
    Command Timeout: 25000
    Example:GetJobList
    """
    rsp = MessageServerInterface.sendSciCommand("GetJobList",JobType)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def ProceedJob(ProceedJob:str=""):
    """
    Continues a job that is waiting on an error (Job Status ErrorWaiting). The mode
    determines how the job continues.
    API Status: published
    Args:
        ProceedJob:str = "AbortJob"
    Command Timeout: 25000
    Example:ProceedJob AbortJob
    """
    MessageServerInterface.sendSciCommand("ProceedJob",ProceedJob)


def QueryCassetteID(Cassette:int=""):
    """
    Returns the ID of a cassette that is placed on the load port. The loadport and
    the cassette must support RFID reading (additional hardware needed).
    API Status: published
    Args:
        Cassette:int = 1
    Returns:
        ID:str
    Command Timeout: 25000
    Example:QueryCassetteID 1
    """
    rsp = MessageServerInterface.sendSciCommand("QueryCassetteID",Cassette)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def DockCassette(LoadPortId:int="", DockUndock:int=""):
    """
    Docks or undocks a cassette which is placed on a LoadPort (CM300 only). It will
    return an error if no cassette is placed: the LoadPort is not ready/available or
    the docking failed. The command will do the docking/undocking and return when
    this is done.
    API Status: published
    Args:
        LoadPortId:int = 0
        DockUndock:int = 0
    Command Timeout: 60000
    Example:DockCassette 1 1
    """
    MessageServerInterface.sendSciCommand("DockCassette",LoadPortId,DockUndock)


def LoadWafer(LoadportID:int="", SlotID:int="", AlignmentAngle:Decimal=""):
    """
    Load a wafer from a given loadport onto the prober. If no slot id is defined,
    the first available wafer with the lowest slot id will be loaded. If no loadport
    is defined, it will try to use the first loadport. If there is no suitable
    wafer, it will try the second.  Returns an error if the loading process fails or
    no suitable wafer is found.  To define an alignment angle and still use the
    "autoselect" behaviour, use -1 for loadport and slot.
    API Status: published
    Args:
        LoadportID:int = -1
        SlotID:int = -1
        AlignmentAngle:Decimal = 0
    Command Timeout: 600000
    Example:LoadWafer 1 1
    """
    MessageServerInterface.sendSciCommand("LoadWafer",LoadportID,SlotID,AlignmentAngle)


def UpdateCassetteStatus(Cassette:int=""):
    """
    Updates the cassette status with a simple scan.
    API Status: published
    Args:
        Cassette:int = 0
    Returns:
        CassetteStatus:str
    Command Timeout: 1200000
    Example:UpdateCassetteStatus 1
    """
    rsp = MessageServerInterface.sendSciCommand("UpdateCassetteStatus",Cassette)
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def TransportWafer(SourceLocation:str="", SourceSlot:int="", DestinationLocation:str="", DestinationSlot:int=""):
    """
    Transport a wafer from one location to another. This command behaves like the
    wafer-transport inside the LoaderModule. The Slot must always be set.
    API Status: published
    Args:
        SourceLocation:str = "Cassette1"
        SourceSlot:int = 1
        DestinationLocation:str = "Cassette1"
        DestinationSlot:int = 1
    Command Timeout: 600000
    Example:TransportWafer Cassette1 1 PreAligner 1
    """
    MessageServerInterface.sendSciCommand("TransportWafer",SourceLocation,SourceSlot,DestinationLocation,DestinationSlot)


def ProcessWafer(Module:str="", ProcessParam:str=""):
    """
    "Process" a wafer on a given location. What is done depends on the current
    station:  - IDReader: read ID - PreAligner: align wafer (alignment angle
    mandatory) - Prober: Perform current recipe
    API Status: published
    Args:
        Module:str = "Cassette1"
        ProcessParam:str = ""
    Command Timeout: 100000
    Example:ProcessWafer PreAligner 90.0
    """
    MessageServerInterface.sendSciCommand("ProcessWafer",Module,ProcessParam)


def GetIDReaderPos():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Returns the current position of the IDReader
    API Status: internal
    Returns:
        IDReaderPos:str
    Command Timeout: 2000
    """
    rsp = MessageServerInterface.sendSciCommand("GetIDReaderPos")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def SetIDReaderPos(IDReaderPos:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set the current position of the IDReader
    API Status: internal
    Args:
        IDReaderPos:str = "Bottom"
    Command Timeout: 10000
    """
    MessageServerInterface.sendSciCommand("SetIDReaderPos",IDReaderPos)


def CryoCommand(Process:str=""):
    """
    CryoCommand controls automatic cooling and warm up.
    API Status: published
    Args:
        Process:str = "CD"
    Command Timeout: 60000
    Example:CryoCommand CD
    """
    MessageServerInterface.sendSciCommand("CryoCommand",Process)


def CryoReadTemperature(Stage:str=""):
    """
    Reads the current temperature from sensor chuck or shield.
    API Status: published
    Args:
        Stage:str = "C"
    Returns:
        Temp:Decimal
    Command Timeout: 10000
    Example:CryoReadTemperature C
    """
    rsp = MessageServerInterface.sendSciCommand("CryoReadTemperature",Stage)
    return Decimal(rsp[0])

def CryoSetTemperature(Stage:str="", Temp:Decimal=""):
    """
    Sets temperature value for TIC chuck or shield. (Only available in process state
    'Idle' or 'Cold'.)
    API Status: published
    Args:
        Stage:str = "C"
        Temp:Decimal = 320
    Command Timeout: 10000
    Example:CryoSetTemperature C 70.5
    """
    MessageServerInterface.sendSciCommand("CryoSetTemperature",Stage,Temp)


def CryoStartRefill(Stage:str=""):
    """
    Enables refill. (Only available in process state 'Idle'.)
    API Status: published
    Args:
        Stage:str = "C"
    Command Timeout: 10000
    Example:CryoStartRefill C
    """
    MessageServerInterface.sendSciCommand("CryoStartRefill",Stage)


def CryoStopRefill(Stage:str=""):
    """
    Disables refill. (Only available in process state 'Idle'.)
    API Status: published
    Args:
        Stage:str = "C"
    Command Timeout: 10000
    Example:CryoStopRefill C
    """
    MessageServerInterface.sendSciCommand("CryoStopRefill",Stage)


def CryoReadState():
    """
    Reads current state.
    API Status: published
    Returns:
        State:str
    Command Timeout: 10000
    """
    rsp = MessageServerInterface.sendSciCommand("CryoReadState")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def CryoMoveBBPark():
    """
    Moves the black body to parking position.
    API Status: published
    Command Timeout: 60000
    """
    MessageServerInterface.sendSciCommand("CryoMoveBBPark")


def CryoMoveBBWork(NbrPosition:int=""):
    """
    Moves the black body to working position.
    API Status: published
    Args:
        NbrPosition:int = 1
    Command Timeout: 60000
    Example:CryoMoveBBWork 1
    """
    MessageServerInterface.sendSciCommand("CryoMoveBBWork",NbrPosition)


def CryoMoveShutter(Position:str="", Shutter:int=""):
    """
    Moves one of the two shutters.
    API Status: published
    Args:
        Position:str = "C"
        Shutter:int = 1
    Command Timeout: 60000
    Example:CryoMoveShutter F 1
    """
    MessageServerInterface.sendSciCommand("CryoMoveShutter",Position,Shutter)


def CryoMoveScopeWork():
    """
    Moves the microscope to working position.
    API Status: published
    Command Timeout: 60000
    """
    MessageServerInterface.sendSciCommand("CryoMoveScopeWork")


def CryoMoveScopePark():
    """
    Moves the microscope to parking position.
    API Status: published
    Command Timeout: 60000
    """
    MessageServerInterface.sendSciCommand("CryoMoveScopePark")


def CryoReadPressure():
    """
    Reads the current pressure of the vacuum chamber.
    API Status: published
    Returns:
        Pressure:Decimal
    Command Timeout: 60000
    """
    rsp = MessageServerInterface.sendSciCommand("CryoReadPressure")
    return Decimal(rsp[0])

def MoveZCombined(Height:Decimal="", Percent:Decimal="", Async:int=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Move both Chuck and Scope to a new absolute z-Height. The position must be
    within 0 and a predefined maximum height (e.g. 3000um). Moves are performed with
    maximum velocity for now
    API Status: internal
    Args:
        Height:Decimal = 0
        Percent:Decimal = 0
        Async:int = 0
    Command Timeout: 15000
    """
    MessageServerInterface.sendSciCommand("MoveZCombined",Height,Percent,Async)


def GetSoftwareStop():
    """
    Get the state of the software stop.
    API Status: published
    Returns:
        StopState:int
    Command Timeout: 1000
    """
    rsp = MessageServerInterface.sendSciCommand("GetSoftwareStop")
    return int(rsp[0])

def MoveZCombinedSetStatus(Status:str="", Message:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Used to set the system either in off, on, error or locked state.  For lock, a
    key is required. To unlock this key, doe a 'SetStatus' with the same key. So,
    SetStatus without message means enable/ recover from error, with message it
    means unlock. If the system wasn't enabled or in error state before an unlock,
    it will remain in this state after the unlock.
    API Status: internal
    Args:
        Status:str = "Off"
        Message:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("MoveZCombinedSetStatus",Status,Message)


def GetScopeWorkingStage():
    """
    Get the currently active ScopeWorkingStage or -1 if unknown. Normally, this
    should be the same as the currently active ScopeSilo
    API Status: published
    Returns:
        ScopeWorkingStage:int
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetScopeWorkingStage")
    return int(rsp[0])

def SetPerformanceMode(Mode:str=""):
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Set the performance mode in use by remote command. If this feature is not
    supported and the mode is anything but Standard, an error is returned.
    API Status: internal
    Args:
        Mode:str = "Standard"
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("SetPerformanceMode",Mode)


def SetScopeWorkingStage(ScopeWorkingStage:int=""):
    """
    Move to the target working stage
    API Status: published
    Args:
        ScopeWorkingStage:int = -1
    Command Timeout: 30000
    """
    MessageServerInterface.sendSciCommand("SetScopeWorkingStage",ScopeWorkingStage)


def GetPerformanceMode():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Get the currently configured performance mode. If this feature is not supported
    on a station, Standard will be returned
    API Status: internal
    Returns:
        Mode:str
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("GetPerformanceMode")
    return str("" if len(rsp) < 1 else ' '.join(rsp))

def MoveZCombinedGetStatus():
    """
    ***WARNING: internal command. Do not use without explicit instructions from FormFactor***
    Get the current status of the combined-z-move-system
    API Status: internal
    Returns:
        Status:str
        PlatenSafe:int
        Height:Decimal
        HeightMax:Decimal
        HeightRelative:Decimal
        SafeHeight:Decimal
        Message:str
    Command Timeout: 5000
    """
    rsp = MessageServerInterface.sendSciCommand("MoveZCombinedGetStatus")
    global MoveZCombinedGetStatus_Response
    if not "MoveZCombinedGetStatus_Response" in globals(): MoveZCombinedGetStatus_Response = namedtuple("MoveZCombinedGetStatus_Response", "Status,PlatenSafe,Height,HeightMax,HeightRelative,SafeHeight,Message")
    return MoveZCombinedGetStatus_Response(str(rsp[0]),int(rsp[1]),Decimal(rsp[2]),Decimal(rsp[3]),Decimal(rsp[4]),Decimal(rsp[5]),str("" if len(rsp) < 7 else ' '.join(rsp[6:])))

def LoadScopeFenceConfiguration(Enable:int="", Path:str=""):
    """
    Load a previously saved Scope-Fence-configuration or remove the current
    configuration
    API Status: published
    Args:
        Enable:int = 0
        Path:str = ""
    Command Timeout: 5000
    """
    MessageServerInterface.sendSciCommand("LoadScopeFenceConfiguration",Enable,Path)


def SetSoftwareStop(StopState:int=""):
    """
    Set the state of the software stop.
    API Status: published
    Args:
        StopState:int = 0
    Command Timeout: 1000
    """
    MessageServerInterface.sendSciCommand("SetSoftwareStop",StopState)


#End of module
