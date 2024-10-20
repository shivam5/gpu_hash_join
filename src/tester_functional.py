import unittest
import join_pandas as jp
import join_triton as jt

class TestJoin(unittest.TestCase):
    def test_inner_join_simple(self):
        table_a = {
            'id': {0:1, 1:2, 2:3, 3:4},
            'name': {0:'Jiashen', 1:'Shivam', 2:'Sirish', 3:'James'}
        }

        table_b = {
            'id': {0:3, 1:4, 2:5, 3:6},
            'order': {0:'pizza', 1:'taco', 2:'sushi', 3:'sandwitch'}
        }

        result = {
            'id': {0:3, 1:4},
            'name': {0:'Sirish', 1:'James'},
            'order': {0:'pizza', 1:'taco'}
        }

        tablejoin = jp.TableJoin(table_a, table_b)
        table_c = tablejoin.inner_join('id', ['id', 'name', 'order'])

        self.assertEqual(table_c, result)

    def test_inner_join_nonunique(self):
        table_a = {
            'id': {0:1, 1:2, 2:3, 3:4},
            'name': {0:'Jiashen', 1:'Shivam', 2:'Sirish', 3:'James'}
        }

        table_b = {
            'id': {0:3, 1:4, 2:4, 3:6},
            'order': {0:'pizza', 1:'taco', 2:'sushi', 3:'sandwitch'}
        }

        result = {
            'id': {0:3, 1:4, 2:4},
            'name': {0:'Sirish', 1:'James', 2:'James'},
            'order': {0:'pizza', 1:'taco', 2:'sushi'}
        }

        tablejoin = jp.TableJoin(table_a, table_b)
        table_c = tablejoin.inner_join('id', ['id', 'name', 'order'])

        self.assertEqual(table_c, result)

    def test_inner_join_nonunique2(self):
        table_a = {
            'id': {0:1, 1:2, 2:2, 3:3},
            'name': {0:'Jiashen', 1:'Shivam', 2:'Sirish', 3:'James'}
        }

        table_b = {
            'id': {0:2, 1:3, 2:4, 3:5},
            'order': {0:'pizza', 1:'taco', 2:'sushi', 3:'sandwitch'}
        }

        result = {
            'id': {0:2, 1:2, 2:3},
            'name': {0:'Shivam', 1:'Sirish', 2:'James'},
            'order': {0:'pizza', 1:'pizza', 2:'taco'}
        }

        tablejoin = jp.TableJoin(table_a, table_b)
        table_c = tablejoin.inner_join('id', ['id', 'name', 'order'])

        self.assertEqual(table_c, result)

if __name__ == "__main__":
    unittest.main()