# Robot localisation

## Goals:
* Create a code that estimates robot's position on the map and allows him to localise itself in as few moves as possible.

## Assumptions
* Robot's sensors are not perfect - they occasionally (0.1 chance by default) return false information about environment
* Robot's movement isn't perfect - it has a small chance (0.05 by default) not to move nor rotate.
* Robot doesn't know it's orientation nor it's position in the world.
* The only information that the robot gets comes from the sensors and it is informed when it collides with a wall.

## How does it work?
Robot's all possible states are kept in a 4\*locations matrix and are presented in a form of probabilities.

### Sensor data
Every move all robot's possible states are updated using the sensor data. Every possible state's probability gets respectively 
multiplied the more it matches the scan.
For example let's take the possible state of the robot where walls exist on the left and right side and the sensor only returned data about the right wall.

* The wall on the right side exists as the sensor says, so the probability gets the multiplier of 0.9 (1 - 0.1 chance of sensor failure)
* The wall on the left side exists but the sensor didn't detect it, so the probability gets the multiplier of 0.1
* The walls in the front and on the back don't exist and the sensor didn't detect them so the probability gets multiplied twice by 0.9

In the end, the probability of this state gets multiplied by 0.9*0.1*0.9*0.9=0.0729

### Transition and rotation data
States' probabilities are also affected by robot's movement. If the robot decides to move forward, the probabilities of robot's states are also moved 'forward' in the matrix. The robot's next planned position gets multiplied by 0.95 (1 - 0.05 chance not to move) and robot's position which it moves from gets multiplied by the remaining 0.05.
The same operation occurs for robots rotation. If the robot bumps into a wall, all states with walls in front of them get multiplied by 1 and the remaining ones by 0.

## Heuristics
Robot's movement is affected by all it's possible states. Robot tries to move into the direction which has the lowest chance of having a wall, prioritizing the forward movement.
