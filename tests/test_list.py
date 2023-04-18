import unittest

import src.hkkang_utils.list as list_utils


class Test_list_utils(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_list_utils, self).__init__(*args, **kwargs)
    
    def test_do_flatten_list(self):
        input_list = [[1,2,3], [4,5,6], [7,8,9]]
        gold = [1,2,3,4,5,6,7,8,9]
        result = list_utils.do_flatten_list(input_list)
        self.assertEqual(result, gold, f"result: {result}, gold_after: {gold}")
        
    
    def test_map_many(self):
        input_list = [1,2,3,4,5]
        functions = [lambda x: x+1, lambda x: x*2]
        gold = [4,6,8,10,12]
        result = list_utils.map_many(functions, input_list)
        self.assertEqual(result, gold, f"result: {result}, gold: {gold}")


if __name__ == "__main__":
    unittest.main()
    
    