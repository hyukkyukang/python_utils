import unittest

import hkkang_utils.pattern as pattern_utils


class Test_pattern_utils(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_pattern_utils, self).__init__(*args, **kwargs)

    def test_singleton_design(self):
        class SingletonClass(pattern_utils.Singleton):
            def __init__(self):
                self.a = 1

        a = SingletonClass()
        b = SingletonClass()
        self.assertEqual(a, b)

    def test_singleton_decorator(self):
        @pattern_utils.singleton
        class SingletonClass:
            def __init__(self):
                self.a = 1

        a = SingletonClass()
        b = SingletonClass()
        self.assertEqual(a, b)

    def test_signleton_with_args(self):
        class CustomClass(pattern_utils.SingletonWithArgs):
            def __init__(self, a):
                self.a = a

        a = CustomClass(1)
        b = CustomClass(1)
        self.assertEqual(a, b)

        c = CustomClass(2)
        self.assertNotEqual(a, c)


if __name__ == "__main__":
    unittest.main()
