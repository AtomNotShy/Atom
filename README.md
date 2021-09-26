# CS561-Project1 3D cave search
author: Tong Zhou
This is a programming assignment in which you will apply AI search techniques to lead an
exploration team to explore an underground cave system such as the one shown in Figure 1.
Conceptually speaking, each cave system is like a sophisticated 3D maze, as shown in Figure 2,
which consists of a grid of points (not cells) with (x, y, z) locations in which your agent may use
one of the 18 elementary actions (see their definitions below), named X+, X-, Y+, Y-, Z+, Z-;
X+Y+, X-Y+, X+Y-, X-Y-, X+Z+, X+Z-, X-Z+, X-Z-, Y+Z+, Y+Z-, Y-Z+, Y-Z-; to move to one of the 18
neighboring grid point locations. At each grid point, your agent is given a list of actions that are
available for the current point your agent is at. Your agent can select and execute one of these
available actions to move inside the 3D maze. For example, in Figure 2, there is a “path” from
(0,0,0) to (10,0,0) and to travel this path starting from (0,0,0), your agent would make ten
actions: X+, X+, X+, X+, X+, X+, X+, X+, X+, X+, and visit the following list of grid points: (0,0,0),
(1,0,0), (2,0,0), (3,0,0), (4,0,0), (5,0,0), (6,0,0), (7,0,0), (8,0,0), (9,0,0), (10,0,0). At each grid
point, your agent is given a list of available actions to select and execute. For example, in Figure
2, at the grid point (60,45,30) there are two actions for your agent: Z+ for going up, and Y- for
going backwards. At the grid point (60,103,97), the available actions are X+ and Y-. At
(60,45,97), the three available actions are Y+, Z-, and X-Y+. If a grid point has no actions
available, then that means such a point has nowhere to go. For example, the point (24,86,31)
(not shown in Figure 2) has nowhere to go and is not accessible.
To find the solution you will use the following algorithms:
- Breadth-first search (BFS)
- Uniform-cost search (UCS)
- A* search (A*).

Breadth-first search (BFS)
In BFS, each move from one location to any of its neighbors counts for a unit path cost of 1. You
do not need to worry about the fact that moving diagonally actually is a bit longer than moving
along the North/South, East/West, and Up/Down directions. So, any allowed move from one
location to an adjacent location costs 1.
Uniform-cost search (UCS)
When running UCS, you should compute unit path costs in any of the 2D plane XY, XZ, YZ, on
which you are moving. Let us assume that a grid location’s center coordinates projected to a 2D
plane are spaced by a 2D distance of 10 units on X and Z plane respectively. That is, on the XZ
plane, move from a grid location to one of its 4-connected straight neighbors incurs a unit path
cost of 10, while a diagonal move to a neighbor incurs a unit path cost of 14 as an
approximation to 10√𝟐 when running UCS.
A* search (A*).
When running A*, you should compute an approximate integer unit path cost of each move as
in the UCS case (unit cost of 10 when moving straight on a plane, and unit cost of 14 when
moving diagonally). Notice for A*, you need to design an admissible heuristic for A* for this
problem.

