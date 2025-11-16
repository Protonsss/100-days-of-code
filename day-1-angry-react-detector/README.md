# day 1: angry react detector

so basically this thing tries to detect if you look angry in an image or from your webcam. if you look too angry (according to my super scientific anger metric which is literally just average pixel brightness), it'll tell you to calm down and maybe even show a calming image. idk why but it was fun to make.

## why i made this
honestly, i was procrastinating on studying for my linear algebra exam and thought it would be hilarious if my computer could tell me when i looked stressed. this is as close as i got in a few hours. works surprisingly well sometimes.

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
i learned that OpenCV is kinda cool, but also kinda confusing sometimes. also, image processing is harder than it looks.

## known bugs
sometimes crashes if you look at it wrong. also the "anger level" is completely arbitrary.