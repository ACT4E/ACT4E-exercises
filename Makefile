
upload:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	twine upload dist/*
#	devpi use $(TWINE_REPOSITORY_URL)
#	devpi login $(TWINE_USERNAME) --password $(TWINE_PASSWORD)
#	devpi upload --verbose dist/*
