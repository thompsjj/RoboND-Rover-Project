import numpy as np


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

def hard_turn(Rover):
    Rover.throttle = 0
    # Release the brake to allow turning
    Rover.brake = 0
    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
    Rover.steer = -15  # Could be more clever here about which way to turn
# If we're stopped but see sufficient navigable terrain in front then go!

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
        Rover.state = 'escaping'

    else:
        hard_turn(Rover)


def at_max_velocity(Rover):
    if Rover.vel < Rover.max_vel:
        return False
    return True

def explore_area(Rover):


    pass

def return_to_previous_location(Rover):

    pass


def wander_strategy(Rover):
    # Check for Rover.mode status
    if is_moving(Rover):
        # Check the extent of navigable terrain
        if pathway_clear(Rover, Rover.stop_forward):
            # If mode is forward, navigable terrain looks good
            # and velocity is below max, then throttle
            if at_max_velocity(Rover):
                # coast
                coast(Rover)
            else:
                # Set throttle value to throttle setting

                throttle_forward(Rover)

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


def follow_wall_strategy(Rover):

    # if there is a wall to the left or the right and unexplored space in front of the rover, drive straight ahead

    # define what point is straight ahead
        # take yaw and determine which cell is in front of the rover relative to this cell = target_cell

    # define what grid points are to left and right of the rover
        ## if there is a wall to the right, use the parallel to that wall

        ## else if there is a wall to the left use the parallel to that wall


    # if the space in front of the rover has not been visited and there is no object known to be in the next grid point
        # steer towards that point by finding a parallel to the wall





    #if Rover.memorymap[target_y, target_x, 0] == 0 and Rover.worldmap[target_y, target_x, 0] >




    # if there is no unexplored space in front of the rover or there is an obstacle in front, return to wander strategy



    pass



def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if telemetry(Rover):

        # if nothing else is happening, allow the rover to wander
        wander_strategy(Rover)

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

