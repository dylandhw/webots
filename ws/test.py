from controller import Robot

TIMESTEP = 32
MAX_SPEED = 6.28

OBSTACLE_THRESHOLD = 100
CLEAR_THRESHOLD = 70     # below this, we assume the path is clear
TURN_DURATION = 1.0      # seconds for one full turn if uninterrupted
TURN_SPEED = 0.8 * MAX_SPEED

def run_robot(robot):
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    sensors = [robot.getDevice(f'ps{i}') for i in range(8)]
    for s in sensors:
        s.enable(TIMESTEP)

    state = "FORWARD"
    turn_start_time = 0

    while robot.step(TIMESTEP) != -1:
        ps_vals = [s.getValue() for s in sensors]
        front_left = max(ps_vals[0], ps_vals[1], ps_vals[2])
        front_right = max(ps_vals[5], ps_vals[6], ps_vals[7])
        front_center = max(ps_vals[3], ps_vals[4])

        # ======= STATE MACHINE =======
        if state == "FORWARD":
            if max(front_left, front_right, front_center) > OBSTACLE_THRESHOLD:
                # Decide which way to turn
                if front_left > front_right:
                    state = "TURN_RIGHT"
                else:
                    state = "TURN_LEFT"
                turn_start_time = robot.getTime()
            else:
                left_motor.setVelocity(MAX_SPEED)
                right_motor.setVelocity(MAX_SPEED)

        elif state in ["TURN_LEFT", "TURN_RIGHT"]:
            elapsed = robot.getTime() - turn_start_time

            # If we’ve turned long enough or path is clear, stop turning
            if (max(front_left, front_right, front_center) < CLEAR_THRESHOLD) or elapsed > TURN_DURATION:
                state = "FORWARD"
                continue

            if state == "TURN_LEFT":
                left_motor.setVelocity(-TURN_SPEED)
                right_motor.setVelocity(TURN_SPEED)
            else:  # TURN_RIGHT
                left_motor.setVelocity(TURN_SPEED)
                right_motor.setVelocity(-TURN_SPEED)
