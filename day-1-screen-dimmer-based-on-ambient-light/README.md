# day 1: screen dimmer based on ambient light

so basically this thing uses your webcam to measure how bright your room is and then automatically dims your screen. idk why but my eyes hurt less now. works surprisingly well...kinda.

## why i made this
honestly? i was bored and my apartment is either pitch black or blindingly bright, no in-between. thought it would be a funny way to automate my screen brightness. plus, gotta pad the resume somehow lol.

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
i learned that opencv is a pain to install and that i should probably learn more about color spaces.

## known bugs
sometimes crashes if you look at it wrong. also, if your room is REALLY dark, it'll just turn your screen off. use at your own risk ⚠️