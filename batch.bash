#/bin/bash

python main.py --seed 50 -iter 12000 -a 0 -cuda 0 &
python main.py --seed 51 -iter 12000 -a 0 -cuda 1 &
python main.py --seed 52 -iter 12000 -a 0 -cuda 2 &
python main.py --seed 53 -iter 12000 -a 0 -cuda 3 &

python main.py --seed 50 -iter 12000 -a 10000 -cuda 4 &
python main.py --seed 51 -iter 12000 -a 10000 -cuda 5 &
python main.py --seed 52 -iter 12000 -a 10000 -cuda 6 &
python main.py --seed 53 -iter 12000 -a 10000 -cuda 7 

python main.py --seed 50 -iter 12000 -a 100000 -cuda 0 &
python main.py --seed 51 -iter 12000 -a 100000 -cuda 1 &
python main.py --seed 52 -iter 12000 -a 100000 -cuda 2 &
python main.py --seed 53 -iter 12000 -a 100000 -cuda 3 &

python main.py --seed 50 -iter 12000 -a 1000000 -cuda 4 &
python main.py --seed 51 -iter 12000 -a 1000000 -cuda 5 &
python main.py --seed 52 -iter 12000 -a 1000000 -cuda 6 &
python main.py --seed 53 -iter 12000 -a 1000000 -cuda 7 

python main.py --seed 50 -iter 70000 -a 0 -cuda 0 &
python main.py --seed 51 -iter 70000 -a 0 -cuda 1 &
python main.py --seed 52 -iter 70000 -a 0 -cuda 2 &
python main.py --seed 53 -iter 70000 -a 0 -cuda 3 &

python main.py --seed 50 -iter 70000 -a 10000 -cuda 4 &
python main.py --seed 51 -iter 70000 -a 10000 -cuda 5 &
python main.py --seed 52 -iter 70000 -a 10000 -cuda 6 &
python main.py --seed 53 -iter 70000 -a 10000 -cuda 7 

python main.py --seed 50 -iter 70000 -a 100000 -cuda 0 &
python main.py --seed 51 -iter 70000 -a 100000 -cuda 1 &
python main.py --seed 52 -iter 70000 -a 100000 -cuda 2 &
python main.py --seed 53 -iter 70000 -a 100000 -cuda 3 &

python main.py --seed 50 -iter 70000 -a 1000000 -cuda 4 &
python main.py --seed 51 -iter 70000 -a 1000000 -cuda 5 &
python main.py --seed 52 -iter 70000 -a 1000000 -cuda 6 &
python main.py --seed 53 -iter 70000 -a 1000000 -cuda 7 