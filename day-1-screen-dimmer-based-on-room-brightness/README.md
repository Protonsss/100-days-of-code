# day 1: screen dimmer based on room brightness

so basically this thing uses your webcam to detect how bright your room is and dims your screen accordingly. idk why but I thought it would be cool. Works surprisingly well, but sometimes the brightness flickers a bit.

## why i made this
my eyes hurt from staring at the screen all day and i'm too lazy to manually adjust the brightness. plus, it's kinda funny to watch my laptop freak out when I turn on the lights.

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
i learned that opencv is kinda jank but also pretty powerful. also, screen_brightness_control is a lifesaver.

## known bugs
sometimes crashes if you look at it wrong. the brightness adjustment isn't perfect, but it's good enough.