run:
	chmod +x taskjob.sh
	chmod +x setup.sh
	./taskjob.sh
	
fr:
	pip freeze > requirements.txt

