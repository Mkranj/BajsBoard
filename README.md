# BajsBoard

## Setup
U repozitoriju koristi se `uv` Python package manager. Za daljnje korake potrebno je instalirati Python >=3.13, a zatim uv pomoću naredbe `pip install uv`.  
Konačno, za izradu dokumenta u kojem se provodi analiza podataka potrebno je instalirati *Quarto* - https://quarto.org/docs/get-started/.  

Kako biste postavili radno okruženje i napravili izvještaj iz Quarto dokumenta, pratite sljedeće korake:  
* preuzmite kod ovog repozitorija (`git clone https://github.com/Mkranj/BajsBoard.git`)
* unutar foldera BajsBoard napravite virtualno okruženje (`uv venv`)
* preuzmite potrebne pakete u venv (`uv sync`)
* renderajte .qmd datoteku u .html dokument (`uv run quarto render <apsolutna putanja do foldera>/BajsBoard/notebooks/pregled_bajs_uporabe.qmd --to html`)

Nakon praćenja koraka u folderu `notebooks/` napravit će se dokument *pregled_bajs_uporabe.html* u kojem je sadržana provedena analiza.  

