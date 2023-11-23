```
 ____                                  ______                             
|  _ \                                |  ____|                            
| |_) | __ _ _ __   __ _ _ __   __ _  | |__ __ _ _ __ _ __ ___   ___ _ __ 
|  _ < / _` | '_ \ / _` | '_ \ / _` | |  __/ _` | '__| '_ ` _ \ / _ \ '__|
| |_) | (_| | | | | (_| | | | | (_| | | | | (_| | |  | | | | | |  __/ |   
|____/ \__,_|_| |_|\__,_|_| |_|\__,_| |_|  \__,_|_|  |_| |_| |_|\___|_|   
```
# banana_farmer
A simple macro program for Bloons TD6, because [btd6farmer](https://github.com/linus-jansson/btd6farmer) just wasn't enough.  
Just, don't look at the source code. **Please.**

## Table of contents
- Requirements
- Installation Guide
- Usage
  - Arguments
- Making a macro
  - Prerequisites
  - setup.json
  - instructions.json
- Instruction Reference

## Requirements
- Windows, sadly
- Python 3.10 or greater
- [Tesseract v5.0+](https://github.com/UB-Mannheim/tesseract/wiki)

## Installation guide
It's as simple as 1, , !
```console
$ python -m pip install -r requirements.txt
```

## Usage
1. Open BTD6
2. Navigate to the home screen
3. Run the bot.  
   `python main.py --path <path_to_macro>` or `example.bat`

### Arguments
```console
usage: main.py [-h] [--debug] [--restart] --path PATH

A bot to run macros for Bloons TD6

options:
  -h, --help   show this help message and exit
  --debug      Enable debug log mode
  --restart    Restart the macro after every game
  --path PATH  Folder to load the macro from
```

## Making a macro
Here be dragons! The program is currently *very* unfinished, and this process is likely to change. A lot. Adventure at your own risk!

### Prerequisites
```console
$ mkdir <macro_name>
$ touch setup.json
$ touch instructions.json
```
- a basic understanding of SCREAMING_SNAKE_CASE, which is what this program uses.

### setup.json
```py
  VERSION: int = 2     # currently unused, however will in the future allow for the usage of btd6farmer scripts, and other cool things
  # HERO: str | None   # not actually implemented yet, however allows for specific (or inspecific) hero selection. SCREAMING_SNAKE_CASE
  MAP: str             # the desired map, in SCREAMING_SNAKE_CASE
  MODE: str            # map mode (STANDARD, MAGIC_ONLY, CHIMPS, etc)
```
#### example:
```json
{
  "VERSION": 2,
  "HERO": null,
  "MAP": "MONKEY_MEADOW",
  "DIFFICULTY": "EASY",
  "MODE": "PRIMARY_ONLY"
}
```

### instructions.json
```jsonc
{
  "<ROUND_NUMBER>": [
    {
      "INSTRUCTION": "<INSTRUCTION>",
      ... // args, if any
    }
  ]
}
```

## Instruction Reference
### instructions
- `START` - begins game (or round)
  - `FAST_FORWARD` - fast forward (default: True)
- `PLACE_TOWER`
  - `MONKEY` - one of the available monkeys
  - `LOCATION` - [x, y] position of where to place tower
  - `UPGRADE_PATH` - [top, middle, bottom] array of upgrades, e.g. [2, 0, 4]
  - `TARGET` - one of `FIRST` | `LAST` | `CLOSE` | `STRONG`
- `UPGRADE_TOWER`
  - `LOCATION` - [x, y] position of tower to upgrade
  - `UPGRADE_PATH` - [top, middle, bottom] array of upgrades, e.g. [2, 0, 4]
- `SELL_TOWER`
  - `LOCATION` - [x, y] position of tower to sell
- `CHANGE_TARGET`
  - `LOCATION` - [x, y] position of tower to modify
  - `TARGET` - one of `FIRST` | `LAST` | `CLOSE` | `STRONG`

### monkeys
- `DART`
- `BOOMERANG`
- `TACK`
- `ICE`
- `GLUE`
- `SNIPER`
- `SUB`
- `BUCCANEER`
- `ACE`
- `HELI`
- `MORTAR`
- `DARTLING`
- `WIZARD`
- `SUPER`
- `NINJA`
- `ALCHEMIST`
- `DRUID`
- `FARM`
- `ENGINEER`
- `SPIKE`
- `VILLAGE`
- `BEAST`
- `HERO`

