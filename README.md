TravellingSalesmanPython
========================

Python implementation of genetic algorithms to solve travelling salesman

### Requirements

* Python 3.3

### How to use

#### Run with graphic interface

To run the script with an graphic interface to create cities, execute the **ChavaillazJupille.py** file : 
```
ChavaillazJupille.py
```

To create a city, just click in the window. When you want to search the best path for travelling salesman, use the ENTER key of your keyboard. During the process, you can see the best solution for each generation.

#### Run without graphic interface

To make tests with data set without graphic interface, execute the **ProblemTester.py** file :
```
ProblemTester.py
```

This tester will test the following data set during the indicated time :
* data/pb005.txt (1 second)
* data/pb010.txt (5 seconds)
* data/pb010.txt (10 seconds)
* data/pb050.txt (30 seconds)
* data/pb050.txt (60 seconds)
* data/pb100.txt (20 seconds)
* data/pb100.txt (90 seconds)

### Data set generator

To generate set of data, use **data/CitiesGenerator.py** :
```
CitiesGenerator.py <number> <file>
```
Where
* ```<number>``` is the number of city to create in the set
* ```<file>``` is the file that contains the set of data 

### Feedback

Don't hesitate to fork this project, improve it and make a pull request.

### License

This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
