# MPGAA-implementation

A quick (and messy) example implementation of MPGAA* in python, for a 3-d discrete space using the manhattan distance metric.

MPGAA\*  is from **Reusing Previously Found A Paths for Fast Goal-Directed Navigation in Dynamic Terrain** (2015), by
*Carlos Hernandez, Roberto Asin, Jorge A Baier.*

[AAAI publication page, including full pdf.](https://www.aaai.org/ocs/index.php/AAAI/AAAI15/paper/view/10053)

An example visualization of the algorithm's solution for an initially unknown 2-d maze is shown below (generated by `maze_test.py`), along with another visualization of the algorithm's knowledge as it solves the maze: 

![Example maze solution](https://raw.githubusercontent.com/arl-o/MPGAA-implementation/master/maze_sol.gif)

![Example maze solution w/ knowledge](https://raw.githubusercontent.com/arl-o/MPGAA-implementation/master/maze_knowl_sol.gif)
