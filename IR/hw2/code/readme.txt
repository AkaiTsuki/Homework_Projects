Instruction for Running Code:

1) File List:
pg11.txt: the original text for Alice in Wonderland.
parse.pl: the perl script for extracting words that given in problem set.
output: the result comes from parse.pl.
q2.py: Code for question 2.
test.m: Matlab script for zipf's law validation. 
q3.py: Code for question 3.

2)Instruction for code running
q2.py: use command "python q2.py".

test.m: Running this script in matlab, it will read the "output" file and statistic the words. And save the result function graph to save folder that this script in.

q3.py: use command "python q3.py". 

The q3.py is using "numpy" and "scipy" library.
Since the least squre method in scipy has problems which may cause incorrect result, 
I'm choosing scipy.optimize.curve_fit method. This method is a wrapper of original 
least square method and fix the problem.

The following command is for setting up the scientific computing environment:	
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
