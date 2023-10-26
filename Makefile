all:
	@echo


template:
	zuper-cli template

bump:
	zuper-cli bump

upload:
	zuper-cli upload

black:
	black -l 110 --target-version py310 src

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

	pip install \
		pipdeptree\
		bumpversion\
		nose\
		nose2\
		nose2-html-report\
		nose-parallel\
		nose_xunitmp\
		pre-commit\
		rednose\
		coverage\
		codecov\
		sphinx\
		sphinx-rtd-theme
cover_packages=act4e_checks,act4e_checks.good,act4e_checks.thedata,act4e_interfaces,act4e_interfaces_tests,act4e_interfaces_tests.test1

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

xunit=--with-xunit --xunit-file=$(xunit_output)
xunitmp=--with-xunitmp --xunitmp-file=$(xunit_output)
extra=--rednose --immediate

clean:
	coverage erase
	rm -rf $(out) $(coverage_dir) $(tr)

test:
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 nosetests $(extra) $(coverage)  act4e_interfaces_tests  -v --nologcapture $(xunit)


test-parallel:
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 nosetests $(extra) $(coverage) act4e_interfaces_tests -v --nologcapture $(parallel) $(xunitmp)


test-parallel-circle:
	mkdir -p  $(tr)
	DISABLE_CONTRACTS=1 \
	NODE_TOTAL=$(CIRCLE_NODE_TOTAL) \
	NODE_INDEX=$(CIRCLE_NODE_INDEX) \
	nosetests $(coverage) $(xunitmp) act4e_interfaces_tests  -v  $(parallel)


coverage-combine:
	coverage combine

docs:
	sphinx-build src $(out)/docs

-include extra.mk

# sigil 8a1ceef67895c7b66f82e008d5ca11df
