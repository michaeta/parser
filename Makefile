clean:
	rm -rf *.pyc *.out
	ls

test:
	python m3test.py > test_results.out
	cat test_results.out

stutest.out:
	cat passing_test_cases.txt
	python m3parser.py < passing_test_cases.txt > stutest.out
	cat stutest.out

proftest.out:
	cat passing_test_cases.txt
	python m3parser.py < passing_test_cases.txt > proftest.out
	cat proftest.out
