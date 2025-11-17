# day 1: posture roast distance detector

So basically, this thing uses your webcam to measure how far away you are from your screen. If you're too close, it roasts your posture with a random, slightly mean, message on the screen. Works surprisingly well, kinda buggy but hey, it's day 1.

## why i made this
I was slouching way too much while coding and needed something to guilt-trip me into sitting up straight. Plus, I thought it'd be funny to get roasted by my own code.

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
I learned that calibrating a webcam is harder than it looks and haarcascades are still useful in 2024!

## known bugs
Sometimes the distance calculation is way off, especially in low light conditions. Sometimes crashes if you look at it wrong.