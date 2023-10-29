"""
CS121: Schelling Model of Housing Segregation

Program for simulating a variant of Schelling's model of
housing segregation.  This program takes six parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: a home at Location (k, l) is in
        the neighborhood of the home at Location (i,j) if 0 <= k < N,
        0 <= l < N, and 0 <= |i-k| + |j-l| <= R.

    similarity_satisfaction_range (lower bound and upper bound) -
        acceptable range for ratio of the number of
        homes of a similar color to the number
        of occupied homes in a neighborhood.

   patience - number of satisfactory homes that must be visited before choosing
        the last one visited.

   max_steps - the maximum number of passes to make over the city
        during a simulation.

Sample: python3 schelling.py --grid_file=tests/a20-sample-writeup.txt --r=1
    --sim_lb=0.40 --sim_ub=0.7 --patience=3 --max_steps=1

The sample command is shown on two lines, but should be entered on
a single line in the linux command-line
"""

import click
import utility

def is_satisfied(grid, R, location, sim_sat_range):
    """
    Determine whether or not the homeowner at a specific location is
    satisfied using an R-neighborhood centered around the location.
    That is, is does their similarity score fall with the specified
    range (inclusive on both sides).

    Args:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied
            with his similarity score

    Returns (boolean): True if homeowner is satisfied, False otherwise.
    """

    # Since it does not make sense to call this function on a home
    # that is for sale, we recommend adding an assertion to verify
    # that the home is not for sale.
    assert grid[location[0]][location[1]] != "F"
    assert location[0] < len(grid)
    assert location[1] < len(grid)
    assert location[0] >= 0
    assert location[1] >= 0 # Check it is a valid location

    n_similar = 0
    n_neighboors = 0
    for k in range(max(0, location[0]-R), min(len(grid), location[0]+R+1)):
        for i in range(max(0, location[1]-R), min(len(grid), location[1]+R+1)):
            distance = abs(location[0] - k) + abs(location[1] - i)
            if (distance >= 0 and distance <= R) and (grid[k][i] != "F"):
               n_neighboors += 1
               if grid[k][i] == grid[location[0]][location[1]]:
                n_similar += 1
    s_score = n_similar/n_neighboors
    if s_score <= sim_sat_range[1] and s_score >= sim_sat_range[0]:
        return True
    return False

def swap_locations(grid, location, new_location):
    """
    Swap current location with specific new one. The current location is now
    at sale and the new location goes from "F" to the color of
    the current location
    
    Args:
        grid (list of lists of strings): the grid
        location: current location
        new_location: new location of the homeowner
    
    Returns: Nothing, it changes the grid in place
    """
    # Check location is not for sale
    if grid[location[0]][location[1]] != "F":
        if grid[location[0]][location[1]] == "M":
            grid[location[0]][location[1]] = "F"
            grid[new_location[0]][new_location[1]] = "M"
        else:
            grid[location[0]][location[1]] = "F"
            grid[new_location[0]][new_location[1]] = "B"


def find_new_location(grid, R, location, sim_sat_range,
                      patience, homes_for_sale):
    """
    Finds new locations where a homeowner is satisfied
    
    Args:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        location: current location
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied
            with his similarity score
        patience (int): how many houses they need to see before moving
        homes_for_sale (list): list with locations equal to "F"
        
    Returns (int): relocation equal to 1 if it happened, 0 otherwise
    """
    relocation = 0
    if (not is_satisfied(grid, R, location, sim_sat_range)
        and grid[location[0]][location[1]] != "F"):
        for home in homes_for_sale:
            swap_locations(grid, location, home)
            if is_satisfied(grid, R, home, sim_sat_range):
                patience -= 1
                if patience != 0:
                 swap_locations(grid, home, location)
            else:
                swap_locations(grid, home, location)
            if patience == 0:
                relocation = 1
                homes_for_sale.insert(0, location)
                homes_for_sale.remove(home)
                break
    return relocation


def do_wave(grid, R, sim_sat_range, patience, homes_for_sale, color):
    """
    Simulates one wave of the indicated color
    
    Args:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied
            with his similarity score
        patience (int): how many houses they need to see before moving
        homes_for_sale (list): list with locations equal to "F"
        color (str): wave color. "M" or "B"
    
    
    Returns (int): number of maroon or blue relocations during the wave
    """
    if color == "M":
        m_relocations = 0
        for i in range(len(grid)):
            for k in range(len(grid)):
                if grid[i][k] == "M":
                    relocation = find_new_location(grid, R, (i, k),
                                                sim_sat_range, patience,
                                                homes_for_sale)
                    if relocation == 1:
                        m_relocations += 1  
        return m_relocations
    if color == "B":
        b_relocations = 0
        for i in range(len(grid)):
            for k in range(len(grid)):
                if grid[i][k] == "B":
                    relocation = find_new_location(grid, R, (i, k),
                                                sim_sat_range, patience,
                                                homes_for_sale)
                    if relocation == 1:
                        b_relocations += 1  
        return b_relocations


def sim_steps(grid, R, sim_sat_range, patience, homes_for_sale):
    """
    Simulates one step. One maroon wave and one blue wave
    
    Args:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied
            with his similarity score
        patience (int): how many houses they need to see before moving
        homes_for_sale (list of tuples): a list of locations with homes for sale
    
    Returns: number of relocations during the step
    """
    n_relocations = 0
    m_relocations = do_wave(grid, R, sim_sat_range,
                                patience, homes_for_sale, "M")
    b_relocations = do_wave(grid, R, sim_sat_range,
                              patience, homes_for_sale, "B")
    n_relocations = b_relocations + m_relocations
    return n_relocations


def do_simulation(grid, R, sim_sat_range, patience, max_steps, homes_for_sale):
    """
    Do the full simulation.

    Args:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
            the range (inclusive) for when the homeowner is satisfied
            with his similarity score
        max_steps (int): maximum number of steps to do
        homes_for_sale (list of tuples): a list of locations with homes for sale

    Returns (int): The number of relocations completed.
    """

    total_relocations = 0
    for _ in range(max_steps):
        n_relocations = sim_steps(grid, R, sim_sat_range,
                                  patience, homes_for_sale)
        total_relocations += n_relocations
        if n_relocations == 0:
            break
    return total_relocations

