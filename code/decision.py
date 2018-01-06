import numpy as np
from sklearn import linear_model
import sys
import scipy.stats as st
import time

def telemetry(Rover):
    if Rover.nav_angles is not None:
        return True
    return False


def current_state(Rover):
    return Rover.state[-1]


def return_to_previous_state(Rover):
    Rover.state.pop()


def rock_visible(Rover, angle_threshold=-.2, dist_threshold = 50):
    if Rover.sample_angles is not None and (np.mean(Rover.sample_angles) > angle_threshold) and (np.mean(Rover.sample_dists) < dist_threshold):
        return True
    return False


def attempt_collection(Rover):

    Rover.collection_time = Rover.total_time
    Rover.state.append('collecting_sample')


def attempt_escape(Rover):
    brake(Rover)
    reset_steering(Rover)
    Rover.state.append('escape_obstacle')
    Rover.obstructed_time = Rover.total_time


def pathway_clear(Rover):
    if len(Rover.nav_angles) >= Rover.stop_forward:
        return True
    return False


def pathway_not_clear(Rover):
    if len(Rover.nav_angles) < Rover.stop_forward or Rover.vel < 0.1:
        return True
    return False

def obstructed(Rover, threshold=5):
    if Rover.vel <= 0.1 and Rover.total_time - Rover.obstructed_time > threshold:
        return True
    return False


def release_brake(Rover):
    Rover.brake = 0


def reset_steering(Rover):
    Rover.steer = 0


def brake(Rover):
    Rover.throttle = 0
    Rover.brake = Rover.brake_set


def coast(Rover):
    Rover.throttle = 0
    Rover.brake = 0


def stop(Rover):
    Rover.throttle = 0
    brake(Rover)
    Rover.state.append('stop')


def move_forward(Rover):
    if Rover.vel < Rover.max_vel:
        # Set throttle value to throttle setting
        Rover.throttle = Rover.throttle_set

    else:  # Else coast
        Rover.throttle = 0


def crush_angles_left(Rover):
    return np.sort(Rover.nav_angles)[-int(len(Rover.nav_angles)/2):]


def crush_angles_right(Rover):
    return np.sort(Rover.nav_angles)[int(len(Rover.nav_angles)/2):]


def steer_for_wall(Rover, track_left=True):

    if track_left:
        Rover.steer = np.clip(np.mean(crush_angles_left(Rover) * (180 / np.pi)), -15, 15)
    else:
        Rover.steer = np.clip(np.mean(crush_angles_right(Rover) * (180 / np.pi)), -15, 15)

    smooth_steering(Rover)


def steer_for_sample(Rover):

    turn_to = np.clip(np.mean(Rover.sample_angles * (180 / np.pi)), -15, 15)

    if not np.isnan(turn_to):
        Rover.steer = turn_to
        smooth_steering(Rover)
    else:
        return_to_previous_state(Rover)


def smooth_steering(Rover, n=5):
    # recalls previous steering states and averages over the last n
    if len(Rover.steer_history) > n:
        Rover.steer_history = Rover.steer_history[n:]

    Rover.steer_history.append(Rover.steer)
    Rover.steer = np.mean(Rover.steer_history)


def escape_attempted(Rover, threshold=1):
    if Rover.total_time - Rover.obstructed_time > threshold:
        return True
    return False


def collection_attempted(Rover, threshold=15):
    if Rover.total_time - Rover.collection_time > threshold:
        return True
    return False


def spin_right(Rover):
    coast(Rover)
    Rover.steer = -15


def spin_left(Rover):
    coast(Rover)
    Rover.steer = 15


def is_moving(Rover):
    if Rover.vel > 0.2:
        return True
    return False


def approach_slowly(Rover):

    if Rover.vel < Rover.max_vel / 2:
        Rover.throttle = 0.2
        Rover.brake = 0
    else:
        brake(Rover)


def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with

    print("ROVER STATE: {}".format(current_state(Rover)))

    if telemetry(Rover):

        if rock_visible(Rover):
            attempt_collection(Rover)

        # if the rover is near a rock, stop immediately
        if current_state(Rover) == 'wandering':

            if pathway_clear(Rover):

                release_brake(Rover)

                if obstructed(Rover):
                    # switch to escape_obstacle state
                    attempt_escape(Rover)

                else:
                    move_forward(Rover)

                steer_for_wall(Rover, track_left=True)

            elif pathway_not_clear(Rover):
                stop(Rover)

        elif current_state(Rover) == 'escape_obstacle':

            if escape_attempted(Rover):

                steer_for_wall(Rover, track_left=True)
                move_forward(Rover)
                return_to_previous_state(Rover)

            else:

                spin_right(Rover)

        elif current_state(Rover) == 'collecting_sample':

            steer_for_sample(Rover)

            if collection_attempted(Rover):

                return_to_previous_state(Rover)

            elif Rover.near_sample:

                brake(Rover) # brake doesn't go into stop mode

            elif obstructed(Rover):

                brake(Rover)
                reset_steering(Rover)
                attempt_escape(Rover)

            else:

                approach_slowly(Rover)

        elif current_state(Rover) == 'stop':

            if is_moving(Rover):

                brake(Rover)
                reset_steering(Rover)

            elif not is_moving(Rover):

                if not pathway_clear(Rover):
                    spin_right(Rover)

                else:
                    steer_for_wall(Rover)
                    move_forward(Rover)
                    return_to_previous_state(Rover)





    # Just to make the rover do something 
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

