class ValidateMultiple:
    @classmethod
    def validate(cls, testcase, validation_func, objs, dicts):
        testcase.assertEqual(len(objs), len(dicts))

        for o, d in zip(objs, dicts):
            validation_func(testcase, o, d)
