# Poject_Revive

> **This project is still in development, and the framework will undergo significant changes.**


# How to write a plugin:

create a folder with the plugin name inside the 'plugin/' directory and inside that there should be a `__init__.py` file that contains two things 


* Dictionary variable named `__option__` which holds the name of all options required for the plugin to run other than target 
* Function named run which could take an dictionary as a paramater  (`def run(option:dict):`)

 
### Example (also refer the 'plugin/' directory):
```
__option__ = {
    "port": True,
    "address": False
}


def run(options: dict):
    print(options)

```
> Note : to print table, data should be stored in the following format
```python3
    # ri is refering row number 
    # ci is refering column number 

    table1 = {
        'header': ['Option1', 'Option2'],
        'value': [
            [r1_c1, r1_c2],
            [r2_c1, r2_c2],
        ]
    }
```

## Utilities for developing a plugin 

### 1. **Resquest** ( from core.utils.request import request ) :
  * This function can be used to send 'GET' request to any given list of urls 
  * Will return a list of data (json/text) 
  * Uses `aiohttp` to send requests 
  * Takes two arguments
    *  `urls: list` -> list of all url to send the reques
    *  `is_text: bool = False` -> specified the type of returned list (json/text)

### 2. **Store.write** ( from core.utils.store import Store )
*  This function is used to store the data to persistant storage (sqlite3)
*  Uses `sqlitedict` to store data 
*  takes two argument :
   *  options dict from which is passed as the paramater. Example : `def run(options: dict): <-- this`
   *  data a list which contains the data to be stored (table_dict/string)
  
