
# jonjhans-a2
Class: Report For Elements of AI – B551 

Project: Assignment 2 

Name: Jonathan Hansen 

Date: 10/15/2023


## PART 3

1. Description of formulated the search problem:

**Initial State:** the initial state is the beginning city (i.e., start city)

**State space:** the state space is all the cities listed in the gps-city.txt file.

**Successor function:** the successor function lists all the potential cities that you could get to from the current city. It would use the

**Edge weights/ costs:** the edge weights or costs was the cost of the segments between two cities. The cost was either the segment, length, or time.

**Goal State:** the goal state was the end city (i.e., the destination city).

**Heuristic:** I used the Manhattan distance for the heuristic. This seemed to work well for finding the best route on the map. The Manhattan distance calculates a straight line between city and goal and therefore will never overestimate the true cost to reach the goal.

2. Description search algorithm works:
- I used the A* search algorithm. This starts at the initial state and uses cost and heuristic to determine the best path to the goal state. The combined cost and the heuristic cost are used to figure out the best path to the goal. We pop the lowest cost path from the fringe. Backtracking is implemented in this search algorithm in case a better route opens. Open and closed lists were used to keep track of cities that were yet to be checked and cities that had already been evaluated, respectively.

3. Problems faced, any assumptions, simplifications, and design decisions:
- I tried Euclidean distance and Manhattan distance in this problem and found Manhattan distance to work well and efficiently in finding the best route.
- Through debugging I noticed my path was taking me around Indianapolis. I am not super familiar with the roadways near Indianapolis so I checked on google maps to see why I was going around and what “cities” I should have been taking. This is when I noticed the junctions were not listed in the city-gps file and therefore did not have coordinates. This made the junction coordinates read as 'inf', which was my designation for missing information, in my file causing the successor function to choose other routes. I believe it was said on the office hrs. that you can find the coordinates of at least 2 surrounding cities and just place the junction at the midpoint.
- I also dealt with cities that were missing coordinates in the same fashion finding the surrounding cities and placing the missing city at the midpoint between them.
