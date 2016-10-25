from __future__ import (absolute_import, print_function)

import json


class CallbackModule(object):

    def __init__(self, display=None):
        self.results = []

    def _new_play(self, name):
        return {
            'play': {
                'name': name,
            },
            'tasks': []
        }

    def _new_task(self, name):
        return {
            'task': {
                'name': name,
            },
            'hosts': {}
        }

    def playbook_on_play_start(self, name):
        self.results.append(self._new_play(name))

    def playbook_on_task_start(self, name, is_conditional):
        self.results[-1]['tasks'].append(self._new_task(name))

    def runner_on_ok(self, host, res):
        if len(self.results) > 0:
            if len(self.results[-1]['tasks']) > 0:
                self.results[-1]['tasks'][-1]['hosts'][host] = res

    def playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        output = {
            'plays': self.results,
            'stats': summary
        }

        print(json.dumps(output, indent=4, sort_keys=True))
