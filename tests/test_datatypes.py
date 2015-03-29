from minecraft.networking.datatypes import *
import unittest


class Datatypes(unittest.TestCase):
    def test_datatype(self):
        pass

    def test_boolean(self):
        pass
        
    def test_datatypes(self):
        for datatype in all_datatypes:
            print(datatype)
            # Test instanciate
            datatype()

            if datatype.PYTHON_TYPE == bool:
                initial_data = True

            elif datatype.PYTHON_TYPE == int:
                initial_data = 124

            elif datatype.PYTHON_TYPE == float:
                initial_data = 3.14
            else:
                initial_data = None

            data = datatype.serialize(initial_data)
            self.assertEqual(datatype.deserialize(data), initial_data)



