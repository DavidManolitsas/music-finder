# Music Finder

A python application that finds the latest music releases from a range of music artists

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
python3 music_finder.py \
    --days 90 \
    --artists "Above & Beyond" "Kasbo" "Yoste" "Lane 8" "ODESZA" "Emmit Fenn" "Shallou" "ZHU" "Lastlings" "RUFUS DU SOL" "Elderbrook" "Oh Wonder" "Joji" "Alex Lustig" "HONNE" "Jai Wolf" "Andrew Belle" "bülow" "grum" "EMBRZ" "Novo Amor" "Frank Ocean"
```

## Clean Up

Deactivate `venv` with:

```bash
deactivate
```
