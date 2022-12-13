import importlib

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

from core.prompt.const import Completer
from core.prompt.validator import InputValidaton
from core.settings import Threading_params
from core.threads import Thread
from core.utils.store import Store
from core.utils.table import table_print

style = Style.from_dict({
    'bottom-toolbar': '#ffffff bg:#333333',
    'bottom-toolbar2': '#606060 bg:#ffffff',
})


class Terminal:
    def __init__(self):
        self.session = PromptSession("_$ ", validator=InputValidaton(), validate_while_typing=False,
                                     completer=Completer, auto_suggest=AutoSuggestFromHistory(),
                                     bottom_toolbar=self.bottom_toolbar, style=style)
        self.controlstatements = {
            "options": self.options,
            "run": self.run,
            "tasks": self.tasks,
            "result": self.result
        }
        self.user_input = ""
        self.temp = None
        self.threadManager: list[Thread] = []
        self.toolbar = "Project Revive"
        self.err_toolbar = ""
        self.requirements = None
        self.load = None
        self.option = {
            'plugin': None,
            'target': None,
        }
        self.prompt()

    def countRunning(self):
        return sum(i.is_alive() for i in self.threadManager)

    def bottom_toolbar(self):
        return [('class:bottom-toolbar', f" [ Child Tasks -> Total: {len(self.threadManager)} \
 Active:{self.countRunning()} ] "),
                ('class:bottom-toolbar', f" Plugin : {self.option['plugin']}"),
                ('class:bottom-toolbar2', self.err_toolbar),]

    def default(self):
        return

    def func(self):
        Threading_params.thread_limiter.acquire()
        if self.load:
            self.load.run(self.option)

        Threading_params.thread_limiter.release()

    def result(self):
        if len(self.temp) == 2:
            Store.result_value(int(self.temp[1]))
        else:
            Store.result()

    def run(self):
        if self.option['plugin'] and self.option['target']:
            thread = Thread(target=self.func,
                            name=f"{self.option['plugin']}-{self.option['target']}",
                            daemon=True)
            thread.start()
            self.threadManager.append(thread)
        else:
            self.err_toolbar = " Please set values for Plugin and TARGET options to continue "

    def options(self):
        if len(self.temp) > 1:
            if self.temp[1] == "set":
                for i in self.temp[2].split(','):
                    j = i.split("=")
                    self.option[j[0]] = j[1]

            elif self.temp[1] == "load":
                self.requirements = None
                self.option['plugin'] = self.temp[2].strip()
                self.load = importlib.import_module(
                    f'plugin.{self.option["plugin"].replace("/", ".")}')
                self.requirements = {'target': True} | self.load.__option__
        else:
            if self.requirements:
                print("[+] Values required to run the module")
                table_print({
                    "header": ["Options", "Requirements"],
                    "value": [[key, "required" if value else "optional"]
                              for key, value in self.requirements.items()]
                })
            print("[+] Currently set Values")
            table_print({
                "header": ["Options", "Values"],
                "value": [[key, value if value else "Not set"]
                          for key, value in self.option.items()]
            })

    def tasks(self):
        if len(self.temp) == 3:
            self.threadManager[int(self.temp[2]) - 1].kill()
        else:
            table_print({
                "header": ["T.No", "Plugin", "Target", "Status"],
                "value": [[index + 1, *str(i.name).strip().split("-"), "Alive" if i.is_alive() else
                           "Dead"]
                          for index, i in enumerate(self.threadManager)]
            })

    def prompt(self):
        while True:
            self.temp = None
            self.err_toolbar = ""
            self.user_input = str(self.session.prompt())
            if self.user_input:
                self.temp = self.user_input.strip().split()
                self.controlstatements.get(
                    self.temp[0], self.default)()
