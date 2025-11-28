# BajsBoard

Analiza podataka o uporabi Bajs bicikala u Zagrebu.  
Provedena analiza i interaktivna karta s postajama mogu se pregledati na [**ovoj poveznici**](https://mkranj.github.io/BajsBoard/pregled_bajs_uporabe.html).

## Opis projekta  

Cilj projekta je pronaći uzorke u korištenju Bajs bicikala u Zagrebu. Moguće je vidjeti u koje vrijeme u danu je na određenim postajama veća razina aktivnosti, kao i koje dane u tjednu prati povećana uporaba bicikala. Opisane su i sumarne statistike za cijeli Zagreb, kao i popis postaja koje su najviše, odnosno najmanje korištene.   

Korisniku Bajsa ove informacije mogu biti korisne za planiranje vremena polazaka kako bi izbjegao vremena u kojoj je na postaji obično prisutan manjak bicikala.  
Na razini cijelog Bajs sustava u Zagrebu moguće je vidjeti popularnost određenih postaja. Informacije o prenapučenim ili slabo korištenim postajama mogu biti polaznišna točka za planiranje proširenja sustava - na primjer, izgradnju novih postaja između slabo korištenih postaja koje su fizički jako udaljene od ostalih postaja ili proširenje broja dostupnih bicikala na često korištenim postajama s manjim brojem bicikala.

Podaci se preuzimaju pomoću [**bajScraper**-a](https://github.com/Mkranj/bajScraper).  
U folderu `data/test_JSON_data` nalazi se manji broj datoteka koje predstavljaju mjerenje u određenim vremenskim točkama kroz nekoliko dana. Na temelju ovih podataka moguće je pokrenuti i isprobati programski kod. Krajnja analiza provodi se na većem uzorku.  

## Setup
U projektu se analiza provodi pomoću jezika **Python** i koristi se **uv** Python package manager. Za daljnje korake potrebno je instalirati Python >=3.13, a zatim uv pomoću naredbe `pip install uv`.  
Konačno, za izradu dokumenta u kojem se provodi analiza podataka potrebno je instalirati **Quarto** - https://quarto.org/docs/get-started/.  

Kako biste postavili radno okruženje i napravili izvještaj iz Quarto dokumenta, pratite sljedeće korake:  
* preuzmite kod ovog repozitorija (`git clone https://github.com/Mkranj/BajsBoard.git`)
* unutar foldera BajsBoard napravite virtualno okruženje (`uv venv`)
* preuzmite potrebne pakete u venv (`uv sync`)
* renderajte .qmd datoteku u .html dokument (`uv run quarto render ./notebooks/pregled_bajs_uporabe.qmd --to html`)

Nakon praćenja koraka u folderu `notebooks/` napravit će se dokument *pregled_bajs_uporabe.html* u kojem je sadržana provedena analiza.  

