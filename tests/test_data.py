from unittest import TestCase
from unittest.mock import patch, Mock

from data import RandomCSVReader


class TestRandomCSVReader(TestCase):
    def setUp(self):
        read_data = '1,2,3\n4,5,6\n7,8,9'
        self.lines = read_data.split('\n')
        self.filename = '/path/to/target.csv'

        def side_effect(*args):
            filename, index = args
            return self.lines[index - 1]

        self.getline = patch('data.linecache.getline',
                             Mock(side_effect=side_effect)).start()

        self.reader = RandomCSVReader(self.filename)

    def test_getitem(self):
        expected = [line.split(',') for line in self.lines]
        for i in range(len(self.reader)):
            self.assertListEqual(self.reader[i], expected[i])
            self.getline.assert_called_with(self.filename, i + 1)

    def tearDown(self):
        patch.stopall()
