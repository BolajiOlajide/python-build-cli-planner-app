from abc import ABCMeta, abstractmethod, ABC
from collections.abc import Iterable
from datetime import datetime

from dateutil.parser import parse


class DeadlinedMetaReminder(Iterable, metaclass=ABCMeta):
    @abstractmethod
    def is_due(self):
        pass


class DeadlinedReminder(Iterable, ABC):
    @abstractmethod
    def is_due(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is not DeadlinedReminder:
            return NotImplemented

        def attr_in_hierarchy(attr):
            return any (attr in SuperClass.__dict__ for SuperClass in subclass.__mro__)

        if not all(attr_in_hierarchy(attr) for attr in ('__iter__', 'is_due')):
            return NotImplemented

        return True


class DateReminder(DeadlinedReminder):
    def __init__(self, text, date):
        self.date = parse(date, dayfirst=True)
        self.text = text

        # NOTE: As your base class' __init__() is empty, there is no need to call it here.
        # no need to `super()` it.

    def is_due(self):
        return self.date <= datetime.now()

    def __iter__(self):
        formatted_date = self.date.isoformat()
        return iter([self.text, formatted_date])
