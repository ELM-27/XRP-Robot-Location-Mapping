from XRPLib.defaults import *
from XRPLib.board import Board
from XRPLib.reflectance import Reflectance
from XRPLib.differential_drive import DifferentialDrive
import time
import random
import math

def stdFileWrite(recordFile, movements) :
    f.write(movements + "\n")
    
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
    stdFileWrite(recordFile, "Pause: " + str(time.tick_ms()))
    drivetrain.stop()
