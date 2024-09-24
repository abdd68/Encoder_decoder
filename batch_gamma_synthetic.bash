#/bin/bash
python main.py --seed 500 -iter 200000 -a -5000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a -5000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a -5000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a -5000 -cuda 3 --dataset law --synthetic 1 &

python main.py --seed 500 -iter 200000 -a 0 -cuda 4 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 0 -cuda 5 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 0 -cuda 6 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 0 -cuda 7 --dataset law --synthetic 1 

python main.py --seed 500 -iter 200000 -a 5000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 5000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 5000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 5000 -cuda 3 --dataset law --synthetic 1 &

python main.py --seed 500 -iter 200000 -a 10000 -cuda 4 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 10000 -cuda 5 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 10000 -cuda 6 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 10000 -cuda 7 --dataset law --synthetic 1 

python main.py --seed 500 -iter 200000 -a 15000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 15000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 15000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 15000 -cuda 3 --dataset law --synthetic 1 &

python main.py --seed 500 -iter 200000 -a -5000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a -5000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a -5000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a -5000 -cuda 7 --dataset adult --synthetic 1 

python main.py --seed 500 -iter 200000 -a 0 -cuda 0 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 0 -cuda 1 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 0 -cuda 2 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 0 -cuda 3 --dataset adult --synthetic 1 &

python main.py --seed 500 -iter 200000 -a 5000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 5000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 5000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 5000 -cuda 7 --dataset adult --synthetic 1 

python main.py --seed 500 -iter 200000 -a 10000 -cuda 0 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 10000 -cuda 1 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 10000 -cuda 2 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 10000 -cuda 3 --dataset adult --synthetic 1 &

python main.py --seed 500 -iter 200000 -a 15000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 15000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 15000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 15000 -cuda 7 --dataset adult --synthetic 1

python main.py --seed 500 -iter 200000 -a 20000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 20000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 20000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 20000 -cuda 3 --dataset law --synthetic 1 &
python main.py --seed 500 -iter 200000 -a 20000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 20000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 20000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 20000 -cuda 7 --dataset adult --synthetic 1

python main.py --seed 500 -iter 200000 -a 25000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 25000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 25000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 25000 -cuda 3 --dataset law --synthetic 1 &
python main.py --seed 500 -iter 200000 -a 25000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 25000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 25000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 25000 -cuda 7 --dataset adult --synthetic 1

python main.py --seed 500 -iter 200000 -a 100000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 100000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 100000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 100000 -cuda 3 --dataset law --synthetic 1 &
python main.py --seed 500 -iter 200000 -a 100000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 100000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 100000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 100000 -cuda 7 --dataset adult --synthetic 1

python main.py --seed 500 -iter 200000 -a 1000000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 1000000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 1000000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 1000000 -cuda 3 --dataset law --synthetic 1 &
python main.py --seed 500 -iter 200000 -a 1000000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 1000000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 1000000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 1000000 -cuda 7 --dataset adult --synthetic 1

python main.py --seed 500 -iter 200000 -a 10000000 -cuda 0 --dataset law --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 10000000 -cuda 1 --dataset law --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 10000000 -cuda 2 --dataset law --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 10000000 -cuda 3 --dataset law --synthetic 1 &
python main.py --seed 500 -iter 200000 -a 10000000 -cuda 4 --dataset adult --synthetic 1 &
python main.py --seed 510 -iter 200000 -a 10000000 -cuda 5 --dataset adult --synthetic 1 &
python main.py --seed 520 -iter 200000 -a 10000000 -cuda 6 --dataset adult --synthetic 1 &
python main.py --seed 530 -iter 200000 -a 10000000 -cuda 7 --dataset adult --synthetic 1