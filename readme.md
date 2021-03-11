# Approach

My approach is to use depth-first search with backtracking and constraint propagation.

## Depth-first Search

My strategy was to implement depth-first search due to my familiarity with it.  

Implementing it instead of searching for alternatives meant I would have a better understanding of what is going on and I knew that bugs were specific to my algorithm not to a search that I was not familiar with.

### Recursive or Iterative

I initially decided to use recursion but having the different states on different paths of the execution graph made debugging very confusing and in general the behaviour of my algorithm was very confusing. Additionally, recursion meant I was either making numerous copies of the variable for accuracy or I was passing a lot of variables in the method call; both of which meant a slower implementation and a more confusing debugging experience.

Instead I tried the depth first search approach, that we were exposed to in the earlier weeks of the unit and I found it much simpler to work with. Not to mention, understanding the behaviour of my code meant faster debugging and eventually faster run times.



## Backtracking

Initially when using recursion, I used a state class to store the parent state of a state, in hope of backtracking using the parent state. This is the point that I learned about pythons pass by reference nature and that I needed to copy arrays/lists when passing and changing them. As I moved from a recursive search to an iterative one there was no need for a parent node as the backtracking was incorporated in the nature of the iterative approach given that I used a frontier.



## Constraint Propagation

To use propagation I introduced a new board/grid that is essentially a 3D array/list. The first dimension would be the row,the second would be the column and the third would be the options for that cell. I.e. `array[0][0]` would return a list such as `[1,2,5,8]` if the cell at position (0, 0) would be unassigned. This board/grid would mean we would know what values we can assign for a given cell. For our example we could assign cell with position (0, 0) 1, 2 ,5 or 8. 

### Possible Actions Board Initialisation

In order to use such a board we need to initialise it at the beginning. The algorithm loops through all points on the board and checks if they are assigned or unassigned. If the cell is unassigned we say that  actions available for that cell would be `[1, 2, 3, 4, 5, 6, 7, 8, 9]` and for an assigned cell the actions array/list would be empty. 

### How to propagate?

For any propagation it would be as simple as removing a value from a positions list. For example, lets say we want to propagate the effect of assigning 1 to position (0, 0), box-wise - this would mean all positions in the box containing (0, 0), would not contain 1 as a possible action. Note that propagation is not only done box-wise but also in the vertical and horizontal direction. 

### Why propagation is important?

Propagation allows the algorithm to be more efficient. Dynamically storing actions available for a unassigned cell allows the algorithm to perform less checks and computation in comparison to a naive approach. If we had to loop through all 9 possible options for each cell and checking if that cell is, our algorithm would be substantially slower. Propagating allows the algorithm to know that because of that action store, each action available to us is valid and it doesn't have to be checked. 

### What optimisations are enabled by propagation?

By storing actions an interesting optimisation is enabled. When we have a single option for an unassigned cell we can assign the value available for that cell. This means that we do not have to check those cells using our search, making the algorithm more efficient.





# Python

## Pass by reference

Since we are using multi dimensional arrays and given Python's pass by reference it meant that if we had copy an array and changed the copied array, the original array is also changed.

### `copy.copy` (Shallow copy)

Shallow copy means constructing a new collection object and then populating it with references to the objects found in the original. A shallow copy is only *one level deep*. The copying process does not recurse and won't create copies of the original. This means that copy would be suitable for a 2D array but not 3D array. 

### `copy.deepcopy` (Deep copy)

The deep copying process is recursive. Therefore, when copying an object this way, the whole object tree is explored to create an independent copy of the original  object. For a 3D array, a deep copy is necessary for it to work.

### Deep copy vs shallow copy

Deep copy is more thorough but is very slow compared to the shallow copy. As a result, I limited the deep copy use to where it was absolutely necessary and use copy where it wasn't. 



## Data structures

### Dictionaries over Arrays

Typically, when getting a new state because of cell assignment we need to check if that state is in the explored  or frontier array. The lookup has a complexity of O(n) for an array. A way to check the new state is to use a dictionary. Dictionaries have O(1) lookup given the key. By setting the key to something unique to a state it ensures quick and accurate lookup. A way to do this is to hash the board/grid array and store it in the dictionary; the hash being the key and the value being None (the least space needing value).  In the loops for the depth-first search, the `in explored or in frontier` checks are frequent so reducing the complexity from O(n) to O(1) greatly increases the algorithms efficiency.

### When to use arrays

There are instances when arrays can be appropriate, For the simple storage of the states in frontier that we pop and append to, arrays are ideal. Not only are arrays simpler to use and understand than dictionaries but have constant run time for functions such as append.



# Optimisations

## Initial (Before depth-first search)

### Checking if the initial board is valid

By initially checking if every assigned value in the board is valid, it means that if the board is invalid we do not need to preform any search and know that there isn't a solution.  This means that we can reduce the average number of performed computations significantly. Additionally, assuming propagation is performed correctly, if the board is valid we can ensure that the board is in a valid state at all times - we do not have to check constantly, just at the beginning.

### Propagating the already assigned values

By looping through assigned cells in the initial board, we can reduce the number of actions per unassigned cell. This means when the depth-first search is performed we have less options to check and less computation to do. 



## Board State

### Current position

For each board state, the current position of the search is inputted, the current search helps optimise the algorithm. When finding the next unassigned cell we use the current position and only check cells after the current position as it is safe to assume that there will be no unassigned cells before the current position. Additionally, when checking if the board is in a goal state, checking past the current position also means less computations than checking the entire board.