The following scripts are for test:

1. run_mf.py: Matrix Factorization Model

Command: python run_mf.py NUM_OF_FEATURES MAX_ITER
Example: python run_mf.py 2 100
In this example, the number latent features is 2 and will run 100 iterations

PARAM:
NUM_OF_FEATURES: Integer The K in matrix factorization model
MAX_ITER: Number Integer of iterations for calculation

This file will use the following training and test data:
Training data: dataset/reviews.txt
Test data: dataset/test1000.txt


2. run_cf.py: Collaboration Filtering Model
Command: python run_cf.py TOP_N
Example: python run_cf.py 20
In this example, the model will find the top 20 similar users and calculate their
average scores as rating

PARAM:
TOP_N: Integer top n similar users

Training data: dataset/reviews.txt
Test data: dataset/test1000.txt


3. run_query.py
Command: python run_query.py TOP_N
Example: python run_query.py 20
In this example, the model will rank all users based on the review text and
find the top 20 ranked users and calculate their average scores as rating

PARAM:
TOP_N: Integer top n ranked users

Training data: index.txt. This is a invert index file created on training.txt
Test data: test1000.txt. This file is in same directory as run_query.py, it has
different format comparing with the previous one.


