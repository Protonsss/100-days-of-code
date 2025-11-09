# day 1: posture-parrot

so basically this thing watches you through your webcam and yells at you if your posture is bad. it uses some janky face detection to guess where your shoulders are, and then figures out if you're leaning too far to one side.

## why i made this
honestly i slouch a LOT when im coding, so i figured i could make something to roast me for it. its kinda buggy but works surprisingly well when it feels like it.

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
i learned that estimating shoulder position from face detection is harder than it looks. also, opencv is kinda weird sometimes.

## known bugs
sometimes crashes if you look at it wrong. also, accuracy is questionable. if you dont have a face it just gives up lol.