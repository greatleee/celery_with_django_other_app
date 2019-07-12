from abc import ABCMeta, abstractmethod
from decimal import Decimal

from celery.result import AsyncResult


PROGRESS_STATE = 'PROGRESS'


class AbtractProgressRecorder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_progress(self, current, total):
        pass


class ConsoleProgressRecorder(AbtractProgressRecorder):

    def set_progress(self, current, total):
        print('processed {} items of {}'.format(current, total))


class ProgressRecorder(AbtractProgressRecorder):

    def __init__(self, task):
        self.task = task

    def set_progress(self, current, total):
        percent = 0
        if total > 0:
            percent = (Decimal(current) / Decimal(total)) * Decimal(100)
            percent = float(round(percent, 2))
        self.task.update_state(
            state=PROGRESS_STATE,
            meta={
                'current': current,
                'total': total,
                'percent': percent,
            }
        )
