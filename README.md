# Piary
Piary allows for continuous, convenient contribution to a daily diary. Piary is foremost intended to offer a minimal experience such that it can be fired up, appended to, and closed down without much fanfare.

When the script is started, the entry for the current date is opened and ready for new text. With each `enter`, the fresh line is appended to a text file, located in the `entries` directory, named according to the current date. The directory and the file are created as they are needed.

At all times, entries for some days in the past and some days in the future are summarized in a small ascii-art bar chart, where each day's text is represented (logarithmically) by the height of a bar.

```lisp
                                 |                    :         
                                 |                    :         
                                 |      #             :         
                                 |      #             :         
                                 |      #             :         
                                 |      #   # #       :         
      #   #                      |  # # #   # # # # # :         
# # # #   # # #                 #|  # # # # # # # # # :         
# # # # # # # # #     # # # # # #|# # # # # # # # # # #         
# # # # # # # # #     # # # # # #|# # # # # # # # # # #         
# # # # # # # # #     # # # # # #|# # # # # # # # # # #         
M_T_W_T_F_S_S_M_T_W_T_F_S_S_M_T_W_T_F_S_S_M_T_W_T_F_S_S_M_T_W_T_
15  17  19  21  23  25  27  29  31  02  04  06  08  10: 12  14  
  16  18  20  22  24  26  28  30  01  03  05  07  09  11  13  15
                                  Feb                 :         
```

Using `commands`, the user can move the _currently selected_ day backwards and forwards in time. How the user organizes their thoughts is entirely up to them. My suggestion is to strictly (more or less) write notes on the days they _occurred_ even if that is not the day that the user is writing the entry.

For best results, contribute entries frequently and write of events that occurred recently, to preserve the details.

## Getting Started
To get your own Piary going, follow these steps
1. Install Python 3 by getting it from [python.org](https://www.python.org/) if you don't have it yet.
1. Use pip to install the needed dependencies with `pip install -r requirements.txt`.
1. Clone this git repository to your local machine. Locate the root of the repo (with files such as `piary.py`)
1. Open `config.py` in some text editor. Change the value of `ENTRIES_PATH` to where you'd like your entries stored. Piary will build the filesystem there. It's recommended that you make this an absolute path (eg: `C:\piary\entries`). Piary will attempt to create the folder if it doesn't exist yet.
1. (_optional_) Set up a git repo of your own inside the folder specified in _#4_, and set the remote source appropriately.
1. Run `piary.py` using python.

## Using Entry Files

Through use of Piary, the user will (presumably) build a large stockpile of daily entry files, built in a hierarchy. These raw text files can copied out and viewed at leisure.

```
└── 2018
    ├── 2018_1
    │   ├── 2018_01_01.txt
    │   ├── 2018_01_02.txt
	   ...
    │   ├── 2018_01_30.txt
    │   └── 2018_01_31.txt
    ├── 2018_2
    │   ├── 2018_02_01.txt
    │   ├── 2018_02_02.txt
		...
```

To faciliate more robustness of the piary, is is suggested to initialize a git repository inside the `entries` folder, and couple it with some remote repo. The `sync` command inside piary will then handle pushing and pulling to this remote repo.


## Commands
Commands allow the user some degree of meta-control over entries. They are entered as regular text, but escaped with a leading `/`. For example: `/prev`. Some commands that are used more often also have 'shortcut' versions for brevity. They are invoked the same way as normal commands, ie `/p`.


command | shortcut | effect
--- | --- | --- 
prev | p | Moves the selected day to the _previous_ chronological date. Allows an optional numeric argument to specify _how many_ days to move backward.
next | n | Moves the selected day to the _previous_ chronological date. Allows an optional numeric argument to specify _how many_ days to move forward.
today | t | The selected date is set to the current date, according to the operating system.
rmln | r | Removes the last line in the selected date's entry. This line is also copied into the clipboard.
sync |  | Attempts to synchronize a git repository located WITHIN the `entries` directory. It will add all, pull and push in that order.
exit |  | Exits the program. An interrupt signal is also a suitable means of exiting.
path |  | Prints the path to the piary entries directory. 

