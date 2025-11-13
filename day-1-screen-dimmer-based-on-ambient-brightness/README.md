# day 1: screen dimmer based on ambient brightness

so basically this thing uses your webcam to detect how bright your room is and then dims your screen accordingly. idk why but I thought it would be cool to have my screen automatically adjust. works surprisingly well, sometimes crashes if you look at it wrong.

## why i made this
honestly, i was bored and wanted to see if i could automate something kinda pointless. plus, i'm procrastinating on a real assignment.

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
I learned that pyautogui is weird and I still need to figure out platform-specific brightness control. Also, opencv is cool.

## known bugs
Sometimes the brightness goes crazy and flickers. Also, the brightness adjustment is just faking it by saving the screen every time, so it's not truly the actual screen brightness.