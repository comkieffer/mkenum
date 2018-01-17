
run: test
	chmod 775 test
	./test

test : test.cpp generated/ships.cpp
	g++ -std=c++14 -o test generated/ships.cpp test.cpp 

generated/ships.cpp: enum_cfg.yaml
	../mkenum/mkenum.py enum_cfg.yaml

clean:
	rm -rf generated/ test

.PHONY: clean
