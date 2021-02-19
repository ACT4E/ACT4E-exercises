

all: main.pdf

%.pdf: %.tex
	mkdir -p snippets/
	pdflatex -shell-escape $*
	pysnip-make -c make
	latexmk -pdflatex -shell-escape  $*

pysnippets:
	pysnip-make -c make
remake:
	pysnip-make -c "clean; make"
