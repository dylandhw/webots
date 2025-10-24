from controller import Robot

TIMESTEP = 32
MAX_SPEED = 6.28

OBSTACLE_THRESHOLD = 100
TURN_GAIN = 0.001
SPEED_SCALE_FACTOR = 400.0

def run_robot(robot):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    list_ps = [robot.getDevice(f'ps{i}') for i in [0, 1, 2, 5, 6, 7]]
    for ps in list_ps:
        ps.enable(TIMESTEP)

    while robot.step(TIMESTEP) != -1:
        ps_values = [ps.getValue() for ps in list_ps]

        # Split left/right groups
        left_vals = ps_values[0:3]
        right_vals = ps_values[3:6]
        left_intensity = sum(left_vals)
        right_intensity = sum(right_vals)

        # Avoidance logic
        turn = (right_intensity - left_intensity) * TURN_GAIN
        front_val = max(ps_values[2], ps_values[3])
        speed_scale = max(0.2, 1 - (front_val / SPEED_SCALE_FACTOR))

        left_speed = (MAX_SPEED - turn) * speed_scale
        right_speed = (MAX_SPEED + turn) * speed_scale

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
