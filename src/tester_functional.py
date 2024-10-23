import unittest
import join_pandas as jp
import join_numpy as jn
import join_triton as jt


class TestJoin(unittest.TestCase):
    def test_inner_join_simple_numpy(self):
        table_a = {
            'id': {0:1, 1:2, 2:3, 3:4},
            'name': {0:'Jiashen', 1:'Shivam', 2:'Sirish', 3:'James'}
        }

        table_b = {
            'id': {0:3, 1:4, 2:5, 3:6},
            'order': {0:'pizza', 1:'taco', 2:'sushi', 3:'sandwitch'}
        }

        tablejoinmatrix = jt.TableJoinTriton(table_a, table_b)
        table_c = tablejoinmatrix.inner_join('id', ['id', 'name', 'order'])

        tablejoinpandas = jp.TableJoin(table_a, table_b)
        result = tablejoinpandas.inner_join('id', ['id', 'name', 'order'])

        self.assertEqual(table_c, result)

    def test_inner_join_nonunique_numpy(self):
        table_a = {
            'id': {0:1, 1:2, 2:3, 3:4},
            'name': {0:'Jiashen', 1:'Shivam', 2:'Sirish', 3:'James'}
        }

        table_b = {
            'id': {0:3, 1:4, 2:4, 3:6},
            'order': {0:'pizza', 1:'taco', 2:'sushi', 3:'sandwitch'}
        }

        tablejoinmatrix = jt.TableJoinTriton(table_a, table_b)
        table_c = tablejoinmatrix.inner_join('id', ['id', 'name', 'order'])

        tablejoinpandas = jp.TableJoin(table_a, table_b)
        result = tablejoinpandas.inner_join('id', ['id', 'name', 'order'])

        self.assertEqual(table_c, result)

    def test_inner_join_nonunique2_numpy(self):
        table_a = {
            'id': {0:1, 1:2, 2:2, 3:3},
            'name': {0:'Jiashen', 1:'Shivam', 2:'Sirish', 3:'James'}
        }

        table_b = {
            'id': {0:2, 1:3, 2:4, 3:5},
            'order': {0:'pizza', 1:'taco', 2:'sushi', 3:'sandwitch'}
        }

        tablejoinmatrix = jt.TableJoinTriton(table_a, table_b)
        table_c = tablejoinmatrix.inner_join('id', ['id', 'name', 'order'])

        tablejoinpandas = jp.TableJoin(table_a, table_b)
        result = tablejoinpandas.inner_join('id', ['id', 'name', 'order'])

        self.assertEqual(table_c, result)

def suite():
    suite = unittest.TestSuite()
    # Add tests in the specific order you want
    suite.addTest(TestJoin('test_inner_join_simple_numpy'))
    suite.addTest(TestJoin('test_inner_join_nonunique_numpy'))
    suite.addTest(TestJoin('test_inner_join_nonunique2_numpy'))
    return suite

if __name__ == '__main__':
    # Running in parallel
    unittest.main()

    # Running in serial
    runner = unittest.TextTestRunner()
    runner.run(suite())



# if __name__ == "__main__":