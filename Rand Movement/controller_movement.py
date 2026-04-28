from XRPLib.defaults import *

# available variables from defaults: left_motor, right_motor, drivetrain,
#      imu, rangefinder, reflectance, servo_one, board, webserver
# Write your code Here
import sys
import select
from XRPLib.differential_drive import DifferentialDrive

drivetrain = DifferentialDrive.get_default_differential_drive()

MIN_SPEED  = 10
MAX_SPEED  = 80
SPEED_STEP = 10
speed      = 50
TURN_SPEED = 40
ARC_INNER  = 0.4

current_cmd = None
stopDrive = False

fName = "movement_log.txt"
f = open(fName, "w")
f.close()

f = open(fName, "a")

imu.calibrate()

def stdFileWrite(recordFile, movements) :
    recordFile.write(movements + "\n")

def fmt1(v):
    return str(round(v, 1))
    
def fmt3(v):
    return str(round(v, 3))

def rDriveStraight(startEffort, recordFile) :
    drivetrain.set_effort(startEffort, startEffort)
    currentYaw = imu.get_yaw()
    stdFileWrite(recordFile, "Drive: " + fmt1(currentYaw) + " " + fmt3(startEffort) + " " + fmt3(startEffort) + " " + str(time.ticks_ms()))
    
def rDrive(leftEffort, rightEffort, recordFile) :
    drivetrain.set_effort(leftEffort, rightEffort)
    currentYaw = imu.get_yaw()
    stdFileWrite(recordFile, "Drive: " + fmt1(currentYaw) + " " + fmt3(leftEffort) + " " + fmt3(rightEffort) + " " + str(time.ticks_ms()))

def rTurn(degrees, startEffort, recordFile) :
    stdFileWrite(recordFile, "Pause: " + str(time.tick_ms()))
    drivetrain.turn(degrees, startEffort)

def rReverse(startEffort, recordFile) :
    drivetrain.set_effort(-startEffort, -startEffort)
    currentYaw = imu.get_yaw()
    stdFileWrite(recordFile, "Reverse: " + fmt1(currentYaw) + " " + fmt3(-startEffort) + " " + fmt3(-startEffort) + " " + str(time.ticks_ms()))
    
def rStop(recordFile) :
    stdFileWrite(recordFile, "Pause: " + str(time.ticks_ms()))
    drivetrain.stop()

def stop():
    rStop(f)

def drive_forward():
    rDrive(speed / 100, speed / 100, f)

def drive_backward():
    rReverse(speed / 100, f)

def turn_left():
    rDrive(-TURN_SPEED / 100, TURN_SPEED / 100, f)

def turn_right():
    rDrive(TURN_SPEED / 100, -TURN_SPEED / 100, f)

def arc_left():
    rDrive(speed * ARC_INNER / 100, speed / 100, f)

def arc_right():
    rDrive(speed / 100, speed * ARC_INNER / 100, f)

def speed_up():
    global speed
    speed = min(speed + SPEED_STEP, MAX_SPEED)
    print("Speed: " + str(speed) + "%")

def speed_down():
    global speed
    speed = max(speed - SPEED_STEP, MIN_SPEED)
    print("Speed: " + str(speed) + "%")

def apply_command(cmd):
    global current_cmd
    if cmd in ('w', 'W'):
        drive_forward()
    elif cmd in ('s', 'S'):
        drive_backward()
    elif cmd in ('a', 'A'):
        turn_left()
    elif cmd in ('d', 'D'):
        turn_right()
    elif cmd in ('q', 'Q'):
        arc_left()
    elif cmd in ('e', 'E'):
        arc_right()
    elif cmd in (' ', 'x', 'X'):
        stop()
        return None
    elif cmd in ('+', '='):
        speed_up()
        return current_cmd
    elif cmd in ('-', '_'):
        speed_down()
        return current_cmd
    elif cmd in ('0', ')'):
        stop()
        f.close()
        raise 
    else:
        return current_cmd
    return cmd

print("XRP ready. w/s/a/d=drive  q/e=arc  SPACE=stop  +/-=speed")

while True:
    r, _, _ = select.select([sys.stdin], [], [], 0)
    if r:
        ch = sys.stdin.read(1)
        current_cmd = apply_command(ch)
        if current_cmd is None:
            stop()
