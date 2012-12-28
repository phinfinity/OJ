#!/bin/bash 
# Script by Phinfinity <rndanish@gmail.com>

compile() {
	mkdir bin
	g++ fib.cpp -o bin/fib
	g++ hugemem.cpp -o bin/hugemem
	g++ non0.cpp -o bin/non0
	g++ ok.cpp -o bin/ok
	cp pyfail.py bin/pyfail.py
	g++ segfault.cpp -o bin/segfault
	cp sh.sh bin/sh.sh
	g++ sigabrt.cpp -o bin/sigabrt
	g++ tle.cpp -o bin/tle
}

test_programs() {
	echo "Expect OK"
	./processtrack.py 5 32 ./bin/ok
	echo "Expect OK"
	./processtrack.py 5 32 ./bin/fib
	echo "Expect MLE"
	./processtrack.py 5 32 ./bin/hugemem
	echo "Expect OK"
	./processtrack.py 5 45 ./bin/hugemem
	echo "Expect NZEC"
	./processtrack.py 5 32 ./bin/non0
	echo "Expect NZEC from python"
	./processtrack.py 5 32 python bin/pyfail.py
	echo "Expect SEGFAULT"
	./processtrack.py 5 32 ./bin/segfault
	echo "Expect OK"
	./processtrack.py 5 32 bash bin/sh.sh
	echo "Expect SIGABRT"
	./processtrack.py 5 32 ./bin/sigabrt
	echo "Expect TLE"
	./processtrack.py 1 32 ./bin/tle
	echo "Cleaning up binaries"
	rm -rf bin/
}
echo "Compiling..."
compile
test_programs
