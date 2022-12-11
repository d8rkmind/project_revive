# Revive

> **This project is still in its development state and major reworks will be done to the framework**


## How to write a plugin:

create a folder with the plugin name inside the 'plugin/' directory and inside that there should be a `__init__.py` file that contains two things 


* Dictionary variable named `__option__` which holds the name of all options required for the plugin to run other than target 
* Function named run which could take an dictionary as a paramater  (`def run(option:dict):`)

 
### Example (avaliable at 'plugin/recon/brew/__init__.py'):
```
__option__ = {
    "port": True,
    "address": False
}


def run(options: dict):
    print(options)

```
