#/bin/bash
python main.py --seed 50 -iter 20000 -a -5000 -cuda 0 --dataset adult --synthetic 0 &
python main.py --seed 51 -iter 20000 -a -5000 -cuda 1 --dataset adult --synthetic 0 &
python main.py --seed 52 -iter 20000 -a -5000 -cuda 2 --dataset adult --synthetic 0 &
python main.py --seed 53 -iter 20000 -a -5000 -cuda 3 --dataset adult --synthetic 0 &

python main.py --seed 50 -iter 20000 -a 0 -cuda 4 --dataset adult --synthetic 0 &
python main.py --seed 51 -iter 20000 -a 0 -cuda 5 --dataset adult --synthetic 0 &
python main.py --seed 52 -iter 20000 -a 0 -cuda 6 --dataset adult --synthetic 0 &
python main.py --seed 53 -iter 20000 -a 0 -cuda 7 --dataset adult --synthetic 0 

python main.py --seed 50 -iter 20000 -a 5000 -cuda 0 --dataset adult --synthetic 0 &
python main.py --seed 51 -iter 20000 -a 5000 -cuda 1 --dataset adult --synthetic 0 &
python main.py --seed 52 -iter 20000 -a 5000 -cuda 2 --dataset adult --synthetic 0 &
python main.py --seed 53 -iter 20000 -a 5000 -cuda 3 --dataset adult --synthetic 0 &

python main.py --seed 50 -iter 20000 -a 10000 -cuda 4 --dataset adult --synthetic 0 &
python main.py --seed 51 -iter 20000 -a 10000 -cuda 5 --dataset adult --synthetic 0 &
python main.py --seed 52 -iter 20000 -a 10000 -cuda 6 --dataset adult --synthetic 0 &
python main.py --seed 53 -iter 20000 -a 10000 -cuda 7 --dataset adult --synthetic 0 

python main.py --seed 50 -iter 20000 -a 15000 -cuda 4 --dataset adult --synthetic 0 &
python main.py --seed 51 -iter 20000 -a 15000 -cuda 5 --dataset adult --synthetic 0 &
python main.py --seed 52 -iter 20000 -a 15000 -cuda 6 --dataset adult --synthetic 0 &
python main.py --seed 53 -iter 20000 -a 15000 -cuda 7 --dataset adult --synthetic 0
