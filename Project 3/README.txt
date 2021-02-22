This is the implementation of ARA* which is a different implementation of Astar that is a bit more thorough with its search. 
It begins a search with an inflated heurestic and then runs through the program multiple times, lowering the amount of inflation with each run of the astar algorithm

This program has the implementation of a random environment and finds the path snaking in between the "walls". I used an implementation provided by https://youtu.be/3UxnelT9aCo 
to convert the program into a tile based structure.

Note: Sometimes the program is unable to find a path and this is due to the fact that it is impossible to find a path, due to the random nature of the environment. 
However, if there is a path available it WILL find the path, you just might have to re-run the program once again.

Note 2: The video that is included in the file is considered outdated. I let the ARA* weight go down to 1 which essentially made it A*. I have since fixed that and is 
now accurate within the program file as well as the excel sheet. My bad.

Instructions to run:

1). Make sure all the .py files are in the same file

2). Run the main.py file


-Rural Jay Young III N01132160