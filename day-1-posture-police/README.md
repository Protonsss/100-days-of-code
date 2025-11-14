# day 1: posture-police

so basically this thing uses your webcam to detect if you're slouching. it looks at your face and if it's too wide, it tells you to straighten up. kinda buggy but works surprisingly well.

## why i made this
i keep getting neck pain from coding all day. thought this would be a funny way to force myself to sit up straight. it's annoying enough that it might actually work 🤷‍♂️

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
i learned that aspect ratio calculations are kinda finicky with webcams.

## known bugs
sometimes crashes if you look at it wrong. the aspect ratio threshold needs tweaking depending on your camera angle.