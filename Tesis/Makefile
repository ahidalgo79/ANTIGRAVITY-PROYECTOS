# Makefile para Tesis Doctoral (Formato ITO)
MAIN=main

all: compile

compile:
	xelatex $(MAIN)
	biber $(MAIN)
	xelatex $(MAIN)
	xelatex $(MAIN)

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.blg *.bbl *.bcf *.run.xml *.pdf
	find contenido -name "*.aux" -delete

view:
	xdg-open $(MAIN).pdf &
