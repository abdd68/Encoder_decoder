#/bin/bash

python main.py --seed 50 -iter 20000 -a 400000000 -cuda 0 --dataset law --synthetic 0 &
python main.py --seed 50 -iter 20000 -a 300000000 -cuda 1 --dataset law --synthetic 0 &
python main.py --seed 50 -iter 20000 -a 200000000 -cuda 2 --dataset law --synthetic 0