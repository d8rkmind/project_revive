from prompt_toolkit.completion import NestedCompleter
import os

PLUGIN = str(os.path.join(os.getcwd(), 'plugin'))


completer_values = {
    'options': {
        'set': {
            'target=': None
        },
        'load': set([root.removeprefix(PLUGIN + "/") for (root, _, files)
                     in os.walk(PLUGIN, topdown=True) if '__init__.py' in files]),
    },
    'run': None,
    'tasks': {
        "kill": None,
    }
}

Completer = NestedCompleter.from_nested_dict(completer_values)
