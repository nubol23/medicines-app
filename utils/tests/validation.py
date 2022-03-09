import json
from abc import ABC, abstractmethod


class ValidateMultiple:
    @classmethod
    def validate(cls, testcase, validation_func, objs, data):
        testcase.assertEqual(len(objs), data.pop("count"))
        dicts = data.pop("results")
        testcase.assertIsInstance(dicts, list)

        for o, d in zip(objs, dicts):
            validation_func(testcase, o, d)


class BaseValidator(ABC):
    @staticmethod
    @abstractmethod
    def _perform_validation(testcase, obj, dict_entry):
        pass

    @classmethod
    def validate(cls, testcase, obj, dict_entry):
        testcase.assertIsInstance(dict_entry, dict)

        cls._perform_validation(testcase, obj, dict_entry)

        testcase.assertFalse(dict_entry)


def jsonify(content):
    return json.dumps(content, indent=4)


def print_json(content):
    print(json.dumps(content, indent=4))
