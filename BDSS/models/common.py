import inspect

from sqlalchemy import event
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def validates(attribute_name):
    def validates_decorator(fn):
        fn.__validates_attribute__ = attribute_name
        return fn

    return validates_decorator

@event.listens_for(mapper, 'mapper_configured')
def mapper_configured(mapper, cls):
    if hasattr(cls, '_init_validation') and callable(getattr(cls, '_init_validation')):
        cls._init_validation()

class ValidationMixin:

    _validation_methods = None

    @classmethod
    def _init_validation(cls):
        for method_name, method in inspect.getmembers(cls, predicate=inspect.ismethod):
            if hasattr(method, '__validates_attribute__'):
                if cls._validation_methods is None:
                    cls._validation_methods = {}
                cls._validation_methods[method.__validates_attribute__] = method_name

    def validate(self):
        self.validation_errors = {}

        if self.__class__._validation_methods is None:
            return True

        for attribute_name, method_name in self.__class__._validation_methods.iteritems():
            method = getattr(self, method_name)
            try:
                method(attribute_name, getattr(self, attribute_name))
            except ValueError as e:
                self.validation_errors[attribute_name] = [e.message]

        if self.validation_errors:
            return False

        return True
