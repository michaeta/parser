clean:
	rm -rf *.pyc *.out
	ls

stutest.out:
	cat passing_test_cases.txt
	python parser.py < passing_test_cases.txt > stutest.out
	cat stutest.out

proftest.out:
	cat passing_test_cases.txt
	python parser.py < passing_test_cases.txt > proftest.out
	cat proftest.out
