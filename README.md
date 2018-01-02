### Writeup / README

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

I essentially used the notebook on a few snapshots in order to play with calibrations of the filter cutoff. Although there are technically 3 settings, there are really only two that we have to find: Navigable terrain and the rocks. Obstacles are the complement of the navigable terrain map. Using the google color picker, I decided that navigable terrain was acceptable as greyer versions of pure white which is (255,255,255) in standard rgb values. With trial and error, I found that values between (160,160,160) and (175,175,175) function well as the threshold.

However, it is important to note that the terrain has different levels of lighting. If the cutoff is threshold, i.e. (120,120,120) to include different shades of grey, the rover drives much better and is more capable of detecting navigable terrain, but the mapping fidelity is lowered. Thus there is a tradeoff between mapping fidelity and % of map explored, modulated by the cutoff levels. I renamed color_thresh to find_ground(). In the same vein, I added an additional function find_walls() that provides the complement of the terrain. 

To detect rocks, it's observable from the simulation that rocks are colored dull yellow-brown, almost an ochre color. This color is found to be about (110,110,50) and can include those colors with b below 50 with the color mixer [here](https://www.w3schools.com/colors/colors_converter.asp), to account for shadows. This is a different task than the normal color thresholding, so I wrote another function, find_rocks() to do the thresholding. 


#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

The process_image() function was edited to include a new function, update_worldmap() that cycles through the thresholds and terrain_finding functions. These then update to the appropriate slice of the Rover.worldmap. The explored terrain is automatically rendered as pink area on the video.

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.

I took the boilerplate code provided in the walkthrough and refactored it so that the meanings of the functions and decision trees were clearer. I also included different constants for mapping so that visualized terrain and obstacles were marked differently (this is outlined in the walkthrough). I partially did this in preparation for fully completing the project.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

Due to technical troubles getting the project setup, and running weeks behind, I submitted the project without any special AI. Using the default search method, wander_strategy(), and a threshold for navigable terrain (175,175,175), the rover wanders toward the center of its detected navigable terrain unless executing the escape_obstacle_strategy(). This enables the rover to map 70.1% of the terrain at 60.7% fidelity after about 3 minutes. It finds only a few of the rocks in this simulation. The rover does not pick up rocks, although it faithfully maps several of them. Lowering the terrain threshold to (160,160,160) or even lower to (120,120,120) allows the rover to accurately and quickly traverse up to 98% of the map and find every rock, although the fidelity drops below 50% pretty quickly. 

![wander_strategy](./misc/wander_strategy.png)

The follow_wall_left() strategy was also implemented, enabling the rover to track the wall left by first seeking contact with a wall, then finding a parallel to the wall as its steering heading. This makes higher fidelity exploration possible, with 46.4% of the map explored and 68.2% fidelity after about a minute and 15 seconds. 

![wall_left_strategy](./misc/follow_left_strategy.png)


This result meets the minimum for the project and can still be improved. I will be implementing improvements in the coming weeks:

1) Upgrades to the wall-following strategy. The wall-following strategy could benefit from some additional tuning.

2) An exploring strategy - this would following something like a flood search strategy that would enable the rover to exhaustively explore the area near it using the already implied world grid. 

3) Rock-retrieval strategy - this would plot a direction towards a rock, drive to it, and pick it up. A simple method would include just taking the steering direction in a direct line to the rock. This may require a different obstacle escape strategy as well.

4) A finite state machine - I believe the rover would complete the challenge faster if it was able to switch between different strategies based on context. 

I wish that other sensor data was available other than a camera.





