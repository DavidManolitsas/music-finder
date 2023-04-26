# Music Finder

A python application that finds the latest search releases from a range of search artists

https://davidmanolitsas.github.io/music-finder/

## Setup Project

Start virtual environment (venv) with:

```bash
python3 -m virtualenv venv
```

```bash
source venv/bin/activate
```

Install requirements:

```bash
pip3 install -U -r requirements.txt
```

## Run Project

Run the project with:

```bash
make run
```

or

```bash
python3 main.py \
    --days 31 \
    --artists "Above & Beyond" "Kasbo" "Yoste" "Lane 8" "ODESZA" "Emmit Fenn" "Shallou" "ZHU" \
    "Lastlings" "RUFUS DU SOL" "Elderbrook" "Oh Wonder" "Joji" "Alex Lustig" "HONNE" "Jai Wolf" \
    "Andrew Belle" "bülow" "grum" "EMBRZ" "Novo Amor" "Frank Ocean" "Hozier" "CHRVCHES" \
    "Spacey Jane" 
```

## Clean Up

Deactivate `venv` with:

```bash
deactivate
```
