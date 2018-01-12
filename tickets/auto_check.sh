#!/bin/sh

auto_check()
{
    python tickets.py -z bjx nc 2018-02-02;
    sleep 2;
    python tickets.py -z bjx nc 2018-02-03;
    sleep 2;
    python tickets.py -z bjx nc 2018-02-04;
    sleep 2;
    python tickets.py -z bjx nc 2018-02-05;
    sleep 2;
    python tickets.py -z bjx nc 2018-02-06;
    sleep 2;
    python tickets.py -z bjx nc 2018-02-07;
    sleep 2;
    python tickets.py -z bjx nc 2018-02-08;
    sleep 2;
    return;
}

for i in `seq 1 1000`;do
auto_check
done
