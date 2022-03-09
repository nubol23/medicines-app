import json


class ValidateMultiple:
    @classmethod
    def validate(cls, testcase, validation_func, objs, data):
        testcase.assertEqual(len(objs), data.pop("count"))
        dicts = data.pop("results")
        testcase.assertIsInstance(dicts, list)

        for o, d in zip(objs, dicts):
            validation_func(testcase, o, d)


def jsonify(content):
    return json.dumps(content, indent=4)


def print_json(content):
    print(json.dumps(content, indent=4))
