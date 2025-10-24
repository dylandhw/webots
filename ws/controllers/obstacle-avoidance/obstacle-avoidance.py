from controller import Robot 

TIMESTEP = 32
MAX_SPEED = 6.28

def run_robot(robot):
    
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')    
 
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
   
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    
    while robot.step(TIMESTEP) != -1:

        left_motor.setVelocity(MAX_SPEED/4)
        right_motor.setVelocity(MAX_SPEED/2)         

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)
    
    
from controller import Robot 

TIMESTAMP = 32 
MAX_SPEED = 6

def run_robot(robot):
    
    l_motor = robot.getDevice('left wheel motor')
    r_motor = robot.getDevice('right wheel motor')
    
    l_motor.setPosition(float('inf'))
    r_motor.setPosition(float('inf'))    
       
    