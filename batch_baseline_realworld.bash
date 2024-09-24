#/bin/bash

python main.py --seed 60 -iter 20000 -a 5000 -cuda 0 --dataset law --synthetic 0 &
python main.py --seed 61 -iter 20000 -a 5000 -cuda 1 --dataset law --synthetic 0 &
python main.py --seed 62 -iter 20000 -a 5000 -cuda 2 --dataset law --synthetic 0 &
python main.py --seed 63 -iter 20000 -a 5000 -cuda 3 --dataset law --synthetic 0 &