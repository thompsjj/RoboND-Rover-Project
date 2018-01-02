import numpy as np
from sklearn import linear_model

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function

def telemetry(Rover):
    if Rover.nav_angles is not None:
        return True
    return False


def stop(Rover):
    # Set mode to "stop" and hit the brakes!
    Rover.throttle = 0
    # Set brake to stored brake value
    Rover.brake = Rover.brake_set
    Rover.steer = 0
    Rover.mode = 'stop'
    return True


def brake(Rover):
    Rover.throttle = 0
    Rover.brake = Rover.brake_set
    Rover.steer = 0


def throttle_forward(Rover):
    Rover.throttle = Rover.throttle_set
    Rover.brake = 0
    Rover.mode = 'forward'
    return True


def coast(Rover):
    Rover.throttle = 0
    if Rover.vel > 0:
        Rover.mode = 'forward'
    elif Rover.vel < 0:
        Rover.mode = 'reverse'
    else:
        Rover.mode = 'stop'


def throttle_reverse(Rover):
    Rover.throttle = -Rover.throttle_set
    Rover.brake = 0
    Rover.mode = 'reverse'
    return True


def is_moving(Rover):
    if (Rover.mode == 'forward') or (Rover.mode == 'reverse'):
        return True
    return False


def is_stopping(Rover):
    if (Rover.mode == 'stop'):
        return True
    return False


def is_stopped(Rover):
    if Rover.vel <= 0.2:
        return True
    return False

def hard_turn_right(Rover):
    Rover.throttle = 0
    # Release the brake to allow turning
    Rover.brake = 0
    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
    Rover.steer = -15

def hard_turn_left(Rover):
    Rover.throttle = 0
    # Release the brake to allow turning
    Rover.brake = 0
    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
    Rover.steer = 15

def steer_left(Rover):
    throttle_forward(Rover)
    Rover.steer = 5

def steer_right(Rover):
    throttle_forward(Rover)
    Rover.steer = -5

def steer_to_center_of_view(Rover):
    # Release the brake
    Rover.brake = 0
    # Set steer to mean angle
    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180 / np.pi), -15, 15)
    Rover.mode = 'forward'

def pathway_clear(Rover, threshold):
    if len(Rover.nav_angles) >= threshold:
        return True
    return False

def escape_obstacle_strategy(Rover):
    # Now we're stopped and we have vision data to see if there's a path forward

    if pathway_clear(Rover, Rover.go_forward):
        throttle_forward(Rover)
        steer_to_center_of_view(Rover)

    else:
        hard_turn_right(Rover)


def at_max_velocity(Rover):
    if Rover.vel < Rover.max_vel:
        return False
    return True

def get_directionality(Rover):

    if Rover.yaw > 315.:
        Rover.facing = 'N'
    elif Rover.yaw > 45.:
        if Rover.yaw < 135:
            Rover.facing = 'E'
        elif Rover.yaw < 225:
            Rover.facing = 'S'
        else:
            Rover.facing = 'W'
    else:
        Rover.facing = 'N'


def peer_left(Rover, obj_type=0, world_size=200):

    rover_x = np.clip(np.int_(Rover.pos[0]), 0, world_size - 1)
    rover_y = np.clip(np.int_(Rover.pos[1]), 0, world_size - 1)
    get_directionality(Rover)

    if Rover.facing == 'N':
        return Rover.worldmap[rover_y:rover_x-1:obj_type]

    elif Rover.facing == 'S':
        return Rover.worldmap[rover_y:rover_x+1:obj_type]

    elif Rover.facing == 'E':
        return Rover.worldmap[rover_y+1:rover_x:obj_type]

    elif Rover.facing == 'W':
        return Rover.worldmap[rover_y-1:rover_x:obj_type]

    else:
        print('catastrophic failure decision.py:peer_left() line 156')
        sys.exit(0)


def peer_right(Rover, obj_type=0, world_size=200):

    rover_x = np.clip(np.int_(Rover.pos[0]), 0, world_size - 1)
    rover_y = np.clip(np.int_(Rover.pos[1]), 0, world_size - 1)
    get_directionality(Rover)

    if Rover.facing == 'N':
        return Rover.worldmap[rover_y:rover_x + 1:obj_type]

    elif Rover.facing == 'S':
        return Rover.worldmap[rover_y:rover_x - 1:obj_type]

    elif Rover.facing == 'E':
        return Rover.worldmap[rover_y - 1:rover_x:obj_type]

    elif Rover.facing == 'W':
        return Rover.worldmap[rover_y + 1:rover_x:obj_type]

    else:
        print('catastrophic failure decision.py:peer_left() line 156')
        sys.exit(0)

def peer_front(Rover, threshold=10, world_size = 200, obj_type=0):

    rover_x = np.clip(np.int_(Rover.pos[0]), 0, world_size - 1)
    rover_y = np.clip(np.int_(Rover.pos[1]), 0, world_size - 1)
    get_directionality(Rover)

    if Rover.facing == 'N':
        return Rover.worldmap[rover_y+1:rover_x:obj_type]

    elif Rover.facing == 'S':
        return Rover.worldmap[rover_y-1:rover_x:obj_type]

    elif Rover.facing == 'E':
        return Rover.worldmap[rover_y:rover_x+1:obj_type]

    elif Rover.facing == 'W':
        return Rover.worldmap[rover_y:rover_x-1:obj_type]

    else:
        print('catastrophic failure decision.py:peer_left() line 156')
        sys.exit(0)

def wall_in_front(Rover, threshold=10):
    # use the rover's yaw as a direction-finding mechanism
    if peer_front(Rover, 0) > threshold:
        return True
    return False

def wall_to_left(Rover, threshold=10):

    # use the rover's yaw as a direction-finding mechanism
    if peer_left(Rover, 0) > threshold:
        return True
    return False

def wall_to_right(Rover, threshold=10):

    # use the rover's yaw as a direction-finding mechanism
    if peer_right(Rover, 0) > threshold:
        return True
    return False

def move_forward(Rover):

    if at_max_velocity(Rover):
        # coast
        coast(Rover)
    else:
        throttle_forward(Rover)



def wander_strategy(Rover):
    # Check for Rover.mode status
    if is_moving(Rover):
        # Check the extent of navigable terrain
        if pathway_clear(Rover, Rover.stop_forward):
            # If mode is forward, navigable terrain looks good
            # and velocity is below max, then throttle
            move_forward(Rover)
            steer_to_center_of_view(Rover)
        # If there's a lack of navigable terrain pixels then go to 'stop' mode
        else:
            stop(Rover)

    # If we're already in "stop" mode then make different decisions
    elif is_stopping(Rover):

        # If we're not moving (vel < 0.2) then do something else
        if is_stopped(Rover):
            # Now we're stopped and we have vision data to see if there's a path forward
            escape_obstacle_strategy(Rover)
        else:
            # If we're in stop mode but still moving keep braking
            brake(Rover)


def angle_between_line_and_xaxis(line_coeff):
    line_coeff = np.array(line_coeff)
    xax_coeff = np.array([1., 0.])
    G = xax_coeff.dot(line_coeff)/np.sqrt(line_coeff.dot(line_coeff))
    return np.arcsin(G) * 180. / 3.1415


def map_visual_input_to_left_grid(image, default_grid_size=40, default_input_dimension=[320,160]):

    # this selects out the left side of the grid via the arguments in the marked line
    X = []
    y = []

    xstart = default_grid_size
    ystart = default_grid_size
    xlim = default_input_dimension[0]/2 # here we're selecting xgrid [0,160] which is left of the camera
    ylim = default_input_dimension[1]
    for i, r in enumerate(image[xstart:xlim-1, ystart:ylim-1]):
        for j, c in enumerate(r):
            X.append([default_grid_size - i, default_grid_size - j])
            if c != 0.:
                y.append(1)
            else:
                y.append(0)
    X = np.array(X)
    y = np.array(y)
    return X, y


def choose_direction(Rover):
    X, y = map_visual_input_to_left_grid(Rover.img)
    lin = linear_model.LinearRegression()
    lin.fit(X, y)
    return angle_between_line_and_xaxis(lin.coef_)


def track_wall(Rover, track='left'):

    # track wall uses visual input and the presumption of correctly analyzed obstacle input to enable the rover
    # to track the wall
    # if not, sets the rover to 'seeking_wall' mode and allows it to drive straight.
    if track == 'left':
        angle = choose_direction(Rover)
        if angle > 15:
            Rover.steer = 14.9
            Rover.state = 'seeking_wall'
        else:
            Rover.steer = angle



def follow_left_strategy(Rover):

    if is_moving(Rover):

        if Rover.state != 'following_wall_left':
            if pathway_clear(Rover, Rover.stop_forward):
                coast(Rover)
            else:
                stop(Rover)
                Rover.state = 'following_wall_left'

        elif Rover.state == 'following_wall_left':
            if pathway_clear(Rover, Rover.stop_forward):
                if wall_to_left(Rover):
                    track_wall(Rover)
                else:
                    stop(Rover)

    elif is_stopping(Rover):

        if Rover.state != 'following_wall_left':

            # If we're not moving (vel < 0.2) then do something else
            if is_stopped(Rover):

                if wall_in_front(Rover):

                    # there's a wall so we want to turn right
                    hard_turn_right(Rover)
                    Rover.state = 'following_wall_left'

                elif wall_to_left(Rover) and pathway_clear(Rover, Rover.stop_forward):

                    track_wall(Rover)

                    Rover.state = 'following_wall_left'
                else:

                    # rover is stopped and there's no wall in front and no wall to left - strategy failed. Keep wandering.
                    escape_obstacle_strategy(Rover)
                    Rover.state = 'wandering'
            else:
                # If we're in stop mode but still moving keep braking
                brake(Rover)

        elif Rover.state == 'following_wall_left':
            # If we're not moving (vel < 0.2) then do something else
            if is_stopped(Rover):
                # Now we're stopped and we have vision data to see if there's a path forward
                if wall_in_front(Rover) or not pathway_clear(Rover, Rover.stop_forward):
                    hard_turn_right(Rover)
                    Rover.state = 'following_wall_left'

                elif wall_to_left(Rover) and not wall_in_front(Rover) and pathway_clear(Rover, Rover.stop_forward):
                    track_wall(Rover)
                    move_forward(Rover)
                    Rover.state = 'following_wall_left'

                elif not wall_to_left(Rover) and not wall_in_front(Rover):

                    # we lost the wall, and we're stuck on an obstacle
                    escape_obstacle_strategy(Rover)
                    Rover.state = 'wandering'
            else:
                # If we're in stop mode but still moving keep braking
                brake(Rover)


def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if telemetry(Rover):

        # if nothing else is happening, allow the rover to wander
        #wander_strategy(Rover)

        follow_left_strategy(Rover)

        # else find a wall



    # Just to make the rover do something 
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

