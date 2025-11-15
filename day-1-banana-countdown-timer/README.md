# day 1: banana countdown timer

so basically, this detects when you have 3 or more bananas in view of the camera. if it sees 3 bananas, it starts a 10-second countdown timer on the screen. idk why but when the timer hits zero, it's supposed to do *something* (you'd have to add that part yourself).

## why i made this
i was eating a banana and thought it would be funny to make my computer count them. works surprisingly well, but like... what else am i gonna do with it?

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
i learned that cascade classifiers are kinda buggy but also kinda cool.

## known bugs
sometimes crashes if you look at it wrong ¯\_(ツ)_/¯