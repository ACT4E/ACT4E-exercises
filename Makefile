
all:
	@echo "You can try:"
	@echo
	@echo "  make build run"
	@echo "  make docs "
	@echo "  make test coverage-combine coverage-report"
	@echo "  "
	@echo "  make -C notebooks clean all"

bump:
	bumpversion patch
	git push --tags
	git push

upload:
	aido-check-not-dirty
	aido-check-tagged
	aido-check-need-upload --package ACT4E-exercises make upload-do

upload-do:
	rm -f dist/*
	rm -rf src/*.egg-info
	python3 setup.py sdist
	devpi use $(TWINE_REPOSITORY_URL)
	devpi login $(TWINE_USERNAME) --password $(TWINE_PASSWORD)
	devpi upload --verbose dist/*

black:
	black -l 110 --target-version py37 src

install-deps:
	pip3 install --user shyaml
	shyaml get-values install_requires < project.pp1.yaml > .requirements.txt
	pip3 install --user --upgrade -r .requirements.txt
	rm .requirements.txt

install-testing-deps:
	pip3 install --user shyaml
	shyaml get-values tests_require < project.pp1.yaml > .requirements_tests.txt
	pip3 install --user --upgrade -r .requirements_tests.txt
	rm .requirements_tests.txt

	pip install 		pipdeptree==0.13.2		bumpversion		nose==1.3.7		nose2==0.9.2		nose2-html-report==0.6.0		nose-parallel==0.3.1		nose_xunitmp==0.4.1		pre-commit==2.1.1		rednose==1.3.0		coverage==5.0.3		codecov==2.0.16		sphinx		sphinx-rtd-theme

cover_packages=act4e_interfaces

# PROJECT_ROOT ?= /project
# REGISTRY ?= docker.io
# PIP_INDEX_URL ?= https://pypi.org/simple
# BASE_IMAGE ?= python:3.7

CIRCLE_NODE_INDEX ?= 0
CIRCLE_NODE_TOTAL ?= 1

out=out
coverage_dir=$(out)/coverage
tr=$(out)/test-results
xunit_output=$(tr)/nose-$(CIRCLE_NODE_INDEX)-xunit.xml

parallel=--processes=8 --process-timeout=1000 --process-restartworker
coverage=--cover-html --cover-html-dir=$(coverage_dir) --cover-tests \
            --with-coverage --cover-package=$(cover_packages)

xunitmp=--with-xunitmp --xunitmp-file=$(xunit_output)
extra=--rednose --immediate

clean:
	coverage erase
	rm -rf $(out) $(coverage_dir) $(tr)

test: clean
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 nosetests $(extra) $(coverage)  src  -v --nologcapture $(xunitmp)


test-parallel: clean
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 nosetests $(extra) $(coverage) src  -v --nologcapture $(parallel)


test-parallel-circle:
	DISABLE_CONTRACTS=1 	NODE_TOTAL=$(CIRCLE_NODE_TOTAL) 	NODE_INDEX=$(CIRCLE_NODE_INDEX) 	nosetests $(coverage) $(xunitmp) TEST_PACKAGES  -v  $(parallel)


coverage-combine:
	coverage combine

docs:
	sphinx-build src $(out)/docs
        
# sigil 9ae10bcbb4764a2f765d285dd8e4a4d6
