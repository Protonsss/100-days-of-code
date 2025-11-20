# day 1: is-my-fridge-closed

so basically, this script uses your webcam to check if your fridge is open or closed. it compares the current view to a baseline image taken when the script starts and if it sees a significant difference, it assumes the fridge is open.

## why i made this
honestly i kept forgetting to close the fridge and my roommate was yelling at me. seemed easier to code something than develop basic habits.

## how to run
```bash
pip install -r requirements.txt
python main.py
```

## what i learned
i learned that opencv is kinda weird and also that i should probably just close the fridge.

## known bugs
sometimes crashes if you look at it wrong. also doesn't work well in the dark.