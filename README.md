GROUP IMPLEMENTATION PROJECT: READ ME FILE

Group members and corresponding implementation:
  - Hayden Hunskor: Prim's algorithm using a min heap priority queue
  - Tom Gause: Kruskal's algorithm using path compression and union by rank
  - Wright Frost: Prim's algorithm using arrays

Notes about our programs:
Each program implements the graphics package, graphics.py, to animate its
corresponding algorithm. Note that our programs only effectively animate the
test file 'Int-40-80.txt' and a test file that Wright created called
'Int-6-10.txt'. Our programs can run the animations for all other files, 
but it's not pretty or informative.

Each time you run a program, it will output three things:
  - Name of the input .txt file
  - Total weight of the MST
  - Total time it took for the program to run (this includes animation if you
    set the animation argument to True)

Additionally, the program will output these three things to a .csv file called
'tests.csv' which we created to help keep track of all of our test runs.

Instructions:
All three of our .py files are designed to be run in Python 3 from the command
line. They are also set up to run only when all the test files are stored in a
folder called 'MST-Test-Files' which we have included in our submission.

Here are example commands to run the test file 'Int-40-80.txt' for each program:
  - $python3 prims_mhpq.py -i Int-40-80.txt -a True
  - $python3 primlist.py -i Int-40-80.txt -a True
  - $python3 kruskal.py -i Int-40-80.txt -a True

Note that these commands will run the programs WITH an animation. If you want
to run them without animating them, change the animation argument to '-a False'.

We have also created a .txt file called 'tests.txt' that is set up to run using
the command $bash tests.txt. This command will run all of the test files on
all three programs in succession, without animating them. This command will also
output a complete list of all the programs' run times to 'tests.csv'.

Run time analysis:
Below are the theoretical run times of each algorithm, using E to represent the
number of edges and V to represent the number of vertices:
  - Prim's w/ min heap priority queue: O(ElogV)
  - Prim's w/ arrays: O(V^2)
  - Kruskal's w/ union by rank and path compression: O(ElogV)

The problem with comparing actual run times is that each of our programs has
different associated overhead and space complexity. That said, we created a csv
file that has all of the run times for all test files, for each algorithm. The
file is called runtimes.txt and is attached in the zip file.

The most important run time difference to highlight is that Prim's with arrays
will run (comparatively) faster on denser graphs than sparse ones, and Prim's
with min heap and Kruskal's will run (comparatively) faster on sparser graphs
than denser ones. For example, Wright's program has a significantly shorter run
time for 'Int-500-dense' than 'Int-1000-2000'. This makes sense given that the
theoretical run time of 500-dense would be O((500^2)) and
the theoretical run time of 1000-2000 would be O(1000^2).
The same trend appeared for the run times of 'Real-500-dense' vs.
'Real-1000-2000' - that is, Prim's with arrays was faster on 500-dense than
1000-2000.

On the other hand, both Prim's with min heap and Kruskal's had significantly
shorter run times on 'Int-1000-2000' than 'Int-500-dense', which makes sense
given the theoretical run times are O(2000log1000) and O((500^2) * log500),
respectively. Similarly, both programs also had faster run times on
'Real-1000-2000' than 'Real-500-dense'.

Otherwise, in all honesty, there isn't a whole lot of consistency in how the
run times increased for each program, but some of the general trends are
reflected in the differences between sparse and dense files. For sanity sake,
we ran a linear regression analysis on runtimes on all of our test data using
data_analysis.ipynb with the following results:
  - Prim Arrays R value, time/V against V:  0.936064420341668
  - Prim Minheap R value, time/log(V) against E:  0.9978707970457209
  - Kruskal R value, time/log(V) against E:  0.9999296646430175

It's clear that the algorithms with more efficient data structures perform much
closer to their theoretical runtimes. If this was a data structures or 
programming languages course, we could dive into a deeper explanation of 
efficiency, but it's not so we'll end our analysis here.

