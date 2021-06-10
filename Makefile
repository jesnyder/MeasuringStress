DEFAULT_GOAL:  web

.PHONY: pythonanalysis
pythonanalysis:
	python3  code/python/c0000_main.py

.PHONY: pdf
pdf: pythonanalysis
	cp code/latex/report.txt code/latex/report.tex
	aspell check code/latex/*.tex
	pdflatex -output-directory=latex code/latex/reportTEX.tex
	cp code/latex/report.pdf report.pdf

.PHONY: web
web: pythonanalysis
	python3 -m http.server
	python3 -mwebbrowser http://127.0.0.1:8000/report.pdf
