# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 08:13:09 2023

@author: Jon
"""
##!/usr/local/bin/python3
#
# B551 Fall 2023
# Professor Saúl Blanco
# Do not share these assignments or their solutions outside of this class.
#
# route : city route finder 
#
#
# Submitted by : [Jonathan Hansen]


import sys
import heapq
import math
import collections

# Heuristic function to estimate the cost from the current city to the end city.
# Combines Manhattan distance as the heuristic.
def heuristic(current_city, end_city, city_coordinates):
    if current_city not in city_coordinates or end_city not in city_coordinates:
        # Warning message for missing coordinates
        #print(f"Warning: Missing coordinates for {current_city} or {end_city}. Using a large heuristic value.")
        return float('inf')  # Return a very large heuristic value for missing data
    
    # Calculate Manhattan distance as the heuristic
    x1, y1 = city_coordinates[current_city]
    x2, y2 = city_coordinates[end_city]
    manhattan_distance = abs(x2 - x1) + abs(y2 - y1)
    
    return manhattan_distance

# Function to find the route from start_city to end_city using the specified cost function.
def get_route(start_city, end_city, cost_function):
    city_coordinates = parse_city_coordinates()
    road_network = parse_road_segments()
    
    open_set = []  # Priority queue for nodes to be expanded
    closed_set = set()  # Set to track visited nodes
    g_costs = {start_city: 0}  # Store known shortest distances to cities
    
    # Initialization of heuristic
    h_initial = heuristic(start_city, end_city, city_coordinates)
    initial_state = (h_initial, h_initial, start_city, 0, [])  # Update the initial state
    heapq.heappush(open_set, initial_state)

    while open_set:
        _, h_cost, current_city, g_cost, route_taken = heapq.heappop(open_set)

        # Debugging: Print Nodes Being Expanded
        #print(f"Expanding node {current_city}")

        # If the city is in closed_set and the known g_cost is lower, skip this path
        if current_city in closed_set and g_costs.get(current_city, float('inf')) <= g_cost:
            continue
                
        if current_city == end_city:
            if cost_function == "segments":
                cost = len(route_taken)
            elif cost_function == "distance":
                cost = calculate_total_distance(route_taken, road_network)
            elif cost_function == "time":
                cost = calculate_total_time(route_taken, road_network)
            elif cost_function == "delivery":
                cost = calculate_delivery_hours(route_taken, road_network)
            else:
                raise ValueError("Invalid cost function")

            return {
                "total-segments": len(route_taken),
                "total-miles": calculate_total_distance(route_taken, road_network),
                "total-hours": calculate_total_time(route_taken, road_network),
                "total-delivery-hours": calculate_delivery_hours(route_taken, road_network),
                "route-taken": route_taken
            }

        for neighbor, length, speed_limit, highway_name in road_network[current_city]:
            if cost_function == "segments":
                cost = g_cost + 1
            elif cost_function == "distance":
                cost = g_cost + length
            elif cost_function == "time":
                cost = g_cost + length / speed_limit
            elif cost_function == "delivery":
                cost = g_cost + calculate_delivery_cost(length, speed_limit, g_cost)
            else:
                raise ValueError("Invalid cost function")

            # Debugging statement to check cost computation
            #print(f"Cost from {current_city} to {neighbor} with function {cost_function}: {cost}")

            h_cost = heuristic(neighbor, end_city, city_coordinates)
            total_cost = cost + h_cost  # this is f_cost in A*

            # Debugging: Print g-values during A* Execution
            #print(f"Updated g-value for node {neighbor} is {cost}")

            # Debugging: Print f-values during A* Execution
            #print(f"f-value for node {neighbor} is {total_cost}")

            # Change in the order for pushing into the priority queue
            # Here's the backtracking part: if we find a shorter path to a city, we consider it again
            if neighbor not in g_costs or g_costs[neighbor] > cost:
                g_costs[neighbor] = cost
                heapq.heappush(open_set, (total_cost, h_cost, neighbor, cost, route_taken + [(neighbor, highway_name)]))
            
        # Only add to closed set here, so we have the opportunity to check all paths before closing a city    
        closed_set.add(current_city)
            
        
    raise Exception("No path found from %s to %s" % (start_city, end_city))

# Cost functions for various route evaluation criteria

# Function to calculate delivery cost based on length and speed limit
def calculate_delivery_cost(length, speed_limit, g_cost):
    t_road = length / speed_limit
    p = math.tanh(length/1000) if speed_limit >= 50 else 0
    penalty = p * 2 * (t_road + g_cost)
    cost = t_road + penalty
    return cost

# Function to calculate total delivery hours based on the route taken
def calculate_delivery_hours(route_taken, road_network):
    total_hours = 0
    g_cost = 0
    for i in range(len(route_taken) - 1):
        current_city, _ = route_taken[i]
        next_city, _ = route_taken[i+1]
        for neighbor, length, speed_limit, _ in road_network[current_city]:
            if neighbor == next_city:
                segment_time = length / speed_limit
                total_hours += calculate_delivery_cost(length, speed_limit, g_cost)
                g_cost += segment_time  # incrementing the g_cost by the segment_time for the next iteration
                break
    return total_hours

# Function to calculate distance cost based on length
def calculate_distance_cost(length, speed_limit):
    return length

# Function to calculate total distance based on the route taken
def calculate_total_distance(route_taken, road_network):
    total_distance = 0
    for i in range(len(route_taken) - 1):
        current_city, _ = route_taken[i]
        next_city, _ = route_taken[i + 1]
        
        road_segments_for_current_city = road_network.get(current_city, [])
        road_segment = next((segment for segment in road_segments_for_current_city if segment[0] == next_city), None)
        
        if road_segment is None:
            #print(f"Error: No road segment found between {current_city} and {next_city}")
            return None

        total_distance += road_segment[1]
        #print("total distance debug", total_distance)
        
    #for city, _ in route_taken:
        #if city not in road_network:
            #print(f"{city} not found in the road network!")        
    return total_distance

# Function to calculate total time based on the route taken
def calculate_total_time(route_taken, road_network):
    total_time = 0
    for i in range(len(route_taken) - 1):
        current_city, _ = route_taken[i]
        next_city, _ = route_taken[i + 1]
        
        road_segments_for_current_city = road_network.get(current_city, [])
        road_segment = next((segment for segment in road_segments_for_current_city if segment[0] == next_city), None)
        
        if road_segment is None:
            #print(f"Error: No road segment found between {current_city} and {next_city}")
            return None

        length, speed_limit = road_segment[1], road_segment[2]
        total_time += length / speed_limit
        
    return total_time

# Function to identify junction cities based on road network and coordinates
def find_junction_cities(road_network, city_coordinates):
    junction_cities = []
    
    for city, neighbors in road_network.items():
        if len(neighbors) == 2:
            neighbor1, neighbor2 = neighbors
            if city in city_coordinates and neighbor1[0] in city_coordinates and neighbor2[0] in city_coordinates:
                lat1, lon1 = city_coordinates[neighbor1[0]]
                lat2, lon2 = city_coordinates[neighbor2[0]]
                midpoint_lat = (lat1 + lat2) / 2
                midpoint_lon = (lon1 + lon2) / 2
                junction_cities.append((city, midpoint_lat, midpoint_lon))
                #print(f"Identified {city} as a junction city with midpoint: ({midpoint_lat}, {midpoint_lon})")
            #else:
                #print(f"Warning: Missing coordinates for {city} or its neighbors. Skipping...")                
    return junction_cities

# Function to update city coordinates with junction cities
def update_city_coordinates(city_coordinates, junction_cities):
    for city, lat, lon in junction_cities:
        city_coordinates[city] = (lat, lon)

# Function to compute the average coordinates of neighbors with coordinates
def compute_avg_coordinates(neighbors_with_coords):
    total_lat, total_lon = 0, 0
    for coord in neighbors_with_coords:
        lat, lon = coord
        total_lat += lat
        total_lon += lon
    avg_lat = total_lat / len(neighbors_with_coords)
    avg_lon = total_lon / len(neighbors_with_coords)
    return avg_lat, avg_lon

# Function to update junction coordinates based on road network and city coordinates
def update_junction_coordinates(road_network, city_coordinates):
    for city, neighbors in road_network.items():
        if city not in city_coordinates:
            neighbors_with_coords = [city_coordinates[neighbor[0]] for neighbor in neighbors if neighbor[0] in city_coordinates]
            if len(neighbors_with_coords) >= 2:
                avg_lat, avg_lon = compute_avg_coordinates(neighbors_with_coords)
                city_coordinates[city] = (avg_lat, avg_lon)

# Function to parse city coordinates from a file
def parse_city_coordinates():
    city_coordinates = {}
    with open('city-gps.txt', 'r') as file:
        for line in file:
            parts = line.strip().split()
            city_name = parts[0]
            latitude = float(parts[1])
            longitude = float(parts[2])
            city_coordinates[city_name] = (latitude, longitude)
    
    road_network = parse_road_segments()
    update_junction_coordinates(road_network, city_coordinates)  # This line was added to set coordinates for junctions
    
    return city_coordinates
    
# Function to parse road segments from a file
def parse_road_segments():
    road_network = collections.defaultdict(list)
    with open('road-segments.txt', 'r') as file:
        for line in file:
            parts = line.strip().split()
            city1 = parts[0]
            city2 = parts[1]
            length = float(parts[2])
            speed_limit = float(parts[3])
            highway_name = parts[4]

            road_network[city1].append((city2, length, speed_limit, highway_name))
            road_network[city2].append((city1, length, speed_limit, highway_name))
    return road_network


# Main program execution
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise Exception("Error: expected 3 arguments")

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise Exception("Error: invalid cost function")

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])





# =============================================================================
# 
# References for code:
# [1] https://chat.openai.com/
# [2] https://www.geeksforgeeks.org/a-search-algorithm/
# [3] https://stackoverflow.com/questions/46974075/a-star-algorithm-distance-heuristics
# [4] https://www.simplilearn.com/tutorials/artificial-intelligence-tutorial/a-star-algorithm
# [5] https://en.wikipedia.org/wiki/A*_search_algorithm
# [6] https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# 
# 
# =============================================================================


