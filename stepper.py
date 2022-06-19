#!/usr/bin/python
#
# This is a specialized version of Matt Hawkins code.
#
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#    Stepper Motor Test
#
# A simple script to control
# a stepper motor.
#
# Author : Matt Hawkins
# Date   : 28/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------





# Import required libraries
import sys
import time
import RPi.GPIO as GPIO



class FishFeeder():

  # Define GPIO signals to use
  # Physical pins 16, 19, 20, 21
  # GPIO16, GPIO19, GPIO20, GPIO21
  StepPins = [16, 19, 20, 21]

  # Define advanced sequence
  # as shown in manufacturers datasheet
  Seq = [[1,0,0,1],
         [1,0,0,0],
         [1,1,0,0],
         [0,1,0,0],
         [0,1,1,0],
         [0,0,1,0],
         [0,0,1,1],
         [0,0,0,1]]

  StepCount = len(Seq)
  StepDir = 1 # Set to 1 or 2 for clockwise
              # Set to -1 or -2 for anti-clockwise
  WaitTime = 0  #Initially set this to zero.  Updated in "init".

  def __init__(self):
    print("__init__")

  def init(self):
    print("init")

    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    # Set all pins as output
    for pin in self.StepPins:
      print("Setup pins")
      GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)

    # Read wait time from command line
    if len(sys.argv)>1:
      self.WaitTime = int(sys.argv[1])/float(1000)
    else:
      self.WaitTime = 10/float(1000)  #1000
      self.WaitTime *= 1 * 0.1
      print(f'Wait Time: {self.WaitTime}')


  def feedOnePortion(self):
    print("feedOnePortion")

    # Initialise variables
    StepCounter = 0

    StepsPerCycle = len(self.Seq) * 512  #64
    print(f'Steps per cycle: {StepsPerCycle}')

    CycleStepCounter = 0

    # Start loop
    while CycleStepCounter <= StepsPerCycle:
        #print(StepCounter, CycleStepCounter
        #print(Seq[StepCounter]

        for pin in range( len(self.StepPins) ):
          #print("Pin: ", pin
          xpin = self.StepPins[pin]
          if self.Seq[StepCounter][pin]!=0:
            #print(" Enable GPIO %i" %(xpin)
            GPIO.output(xpin, True)
          else:
            #print(" Disable GPIO %i" %(xpin)
            GPIO.output(xpin, False)

        StepCounter += self.StepDir
        CycleStepCounter += 1

        # If we reach the end of the sequence
        # start again
        if (StepCounter >= self.StepCount):
          StepCounter = 0
        if (StepCounter < 0):
          StepCounter = self.StepCount + self.StepDir

        # Wait before moving on
        time.sleep(self.WaitTime)



  def feedOneServing(self):
    #print("feedOneServing")
    print("Feeding one serving...")
    self.feedOnePortion()
    time.sleep(5)
    self.feedOnePortion()


def shutdown():
  GPIO.cleanup()
  print
  print("Bye!")



try:
  fishFeeder = FishFeeder()

  fishFeeder.init()
  fishFeeder.feedOneServing()
except KeyboardInterrupt:
  # This statement is meaningless other than it allows the program to
  # drop down to the next line.
  print("Keyboard Interrupt")




shutdown()
