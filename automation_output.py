#reading input file
import boto3
from boto3.session import Session
import aws_s3
from datetime import datetime
from picamera import PiCamera
from Cam_capture import Camera
from stepper_motor1 import stepper_motor
import pandas as pd
import RPi.GPIO as GPIO
from time import sleep
import threading


def main(motor_x,motor_y,camera_object):
	
	#resetting the position to origin
	reset_data = pd.read_csv("reset.csv")
	reset_x,reset_y = float(reset_data['X']),float(reset_data['Y'])
	print(float(reset_x),float(reset_y))
	stepper_motor.reset(motor_x,motor_y,reset_x,reset_y)
	
	ScaleDF=pd.read_csv('input.csv')
	ScaleDF.columns = ['x_axis','y_axis']
	
	x_max,y_max = ScaleDF['x_axis'].nlargest(1),ScaleDF['y_axis'].nlargest(1)
	if float(y_max) >= 50 or float(x_max) >= 50:
		print("value out of reach")
    #raise ValueError
	else:
		pass
	
	prev_x = 0.0
	prev_y = 0.0
	
	for index,row in ScaleDF.iterrows():
		try:
			print('x','y')
			print(row['x_axis'],row['y_axis'])
			present_x,present_y = float(row['x_axis']),float(row['y_axis'])			
			stepper_motor.run_motors(motor_x,motor_y,present_x,present_y,prev_x,prev_y)

			cam_obj = Camera()
			cam_obj.Capture(camera_object,present_x,present_y)
			prev_x =present_x
			prev_y =present_y
			print(prev_x,prev_y)
			#del cam_obj
		except(KeyboardInterrupt,SystemExit):
			print("interrupted")
					
if __name__== '__main__':
	s3_obj = aws_s3.Aws_S3()
	s3_obj.download_file()
	# aws_s3_download.download_file()#downloads the input file from s3 as input.csv in same directory
	#pin initialization
    #motor 1
	DIR1= 16
	STEP1= 12

    #motor 2
	DIR2 = 36
	STEP2 = 32
    
    #MS1,MS2,MS3 for each motor driver ...to set resolution mode of a motor
	MODE1 = (11,13,15)
	MODE2 = (31,33,35)
    
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

    #for indication of each motor movement 
	LED_x = 37
	LED_y = 38

	motor_x = stepper_motor("motor_x",DIR1,STEP1,MODE1,"full")
	motor_y = stepper_motor("motor_y",DIR2,STEP2,MODE2,"full")

	camera_object = PiCamera()

	# stepper_motor.reset(motor_x,motor_y,10,10)
	# stepper_motor.run_motors(motor_x,motor_y,10,10)

	main(motor_x,motor_y,camera_object)

		
