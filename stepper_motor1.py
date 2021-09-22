import RPi.GPIO as GPIO
from time import sleep
import threading


class stepper_motor:
    RESOLUTION = {'full':(0,0,0),
		'half':(1,0,0),
		'1/4':(0,1,0),
		'1/8':(1,1,0),
		'1/16':(1,1,1)}

    #constants for both the motor
    #to set the direction of stepper movement
    CLK_WISE = 1
    COUNTER_CLK_WISE = 0
    #steps per reveolution
    SPR = 200 

    def __init__(self,Name:str,Dir:int,Step:int,Mode:tuple,Resolution:str) -> None:
        
        self.DIR = Dir
        self.STEP = Step
        self.MODE = Mode
        self.NAME = Name
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.GPIOPINS = [self.DIR,self.MODE,self.STEP]
        
        for pins in self.GPIOPINS:
            GPIO.setup(pins,GPIO.OUT)
        
        GPIO.output(self.MODE,self.RESOLUTION[Resolution])
        pass
    
    #controlling no. of steps for forward rotation
    #in full resolution 100 steps == 1mm
    def forward(self,steps):
        GPIO.output(self.DIR,self.CLK_WISE)
        for i in range(int(steps*(self.SPR//2))):
            GPIO.output(self.STEP,GPIO.HIGH)
            sleep(.001)
            GPIO.output(self.STEP,GPIO.LOW)
            sleep(.001)
            print("forward %s"%self.NAME)
            print(i,'of %d'%steps)

    def backward(self,steps):
        GPIO.output(self.DIR,self.COUNTER_CLK_WISE)
        for i in range(int(steps*(self.SPR//2))):
            GPIO.output(self.STEP,GPIO.HIGH)
            sleep(.001)
            GPIO.output(self.STEP,GPIO.LOW)
            sleep(.001)
            print("forward %s"%self.NAME)
            print(i,'of %d'%steps)

    def move(self,current,previous):
        print("current:",current,"previous:",previous)
        try:
            self.mov = current-previous
            if self.mov == 0:
                return
            elif self.mov>0:
                self.forward(self.mov)
            else:
                self.backward(self.mov) 
        except:
            if type(current and previous) != float:
                print("float object required")
            else:       
                print("error")


    @staticmethod
    def reset(motor1 ,motor2,x,y):
        print("resetting to 0,0")
        t1 = threading.Thread(name=motor1.NAME,target=motor1.backward,args=(x,))
        t2 = threading.Thread(name=motor2.NAME,target=motor2.backward,args=(y,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        
       # motor1.backward(x)
       # motor2.backward(y)
        pass

    @staticmethod
    def run_motors(motor1,motor2,curr_x,curr_y,prev_x=0,prev_y=0):
        print("Starting....")
        t3 = threading.Thread(name=motor1.NAME,target=motor1.move,args=(curr_x,prev_x))
        t4 = threading.Thread(name=motor2.NAME,target=motor2.move,args=(curr_y,prev_y))

        t3.start()
        t4.start()

        t3.join()
        t4.join()
      
       # motor1.move(curr_x,prev_x)
       # motor2.move(curr_y,prev_y)
        pass
    
    def __repr__(self) -> str:
        return "motor Name: {}".format(self.NAME)


if __name__ == "__main__":
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

    stepper_motor.reset(motor_x,motor_y,5,5)
    stepper_motor.run_motors(motor_x,motor_y,5,5)
