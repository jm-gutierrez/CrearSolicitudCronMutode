#!/bin/bash
mkdir $1
cd $1
git clone $2
cd $3
mutode -c 1 ./