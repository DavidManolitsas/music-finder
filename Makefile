#!/usr/bin/env make

ARTISTS ?= "Above & Beyond" "Kasbo" "Yoste" "Lane 8" "ODESZA" "Emmit Fenn" "Shallou" "ZHU" "Lastlings" "RUFUS DU SOL" "Elderbrook" "Oh Wonder" "Joji" "Alex Lustig" "HONNE" "Jai Wolf" "Andrew Belle" "bülow" "grum" "EMBRZ" "Novo Amor" "Frank Ocean" "Flume" "Harry Styles" "Sam Smith"
DAYS ?= 90

help:
	@echo
	@echo "Complete the following before running the script."
	@echo
	@echo "Install virtualenv:"
	@echo "    pip3 install -U virtualenv"
	@echo
	@echo "Initialise virtual environment (venv) with:"
	@echo "    python3 -m virtualenv venv"
	@echo "    source venv/bin/activate"
	@echo "    pip3 install -U -r requirements.txt"
	@echo
	@echo "Deactivate venv with:"
	@echo "    deactivate"

run: main open

main:
	@echo " __  __           _        _____ _           _           "
	@echo "|  \/  |_   _ ___(_) ___  |  ___(_)_ __   __| | ___ _ __ "
	@echo "| |\/| | | | / __| |/ __| | |_  | |  _ \ / _  |/ _ \  __|"
	@echo "| |  | | |_| \__ \ | (__  |  _| | | | | | (_| |  __/ |   "
	@echo "|_|  |_|\__ _|___/_|\___| |_|   |_|_| |_|\__ _|\___|_|   "
	@echo "Created by David Manolitsas "
	@echo
	python3 music_finder.py \
        --days $(DAYS)  \
        --artists $(ARTISTS)

open:
	open output/index.html

#EOF
