from unittest import TestCase
from unittest.mock import patch, mock_open, Mock

from data import RandomCSVReader


class TestRandomCSVReader(TestCase):
    def setUp(self):
        self.read_data = '1,2,3\n4,5,6\n7,8,9'
        self.mock_open = patch('data.open', mock_open(read_data=self.read_data)).start()

        lines = self.read_data.split('\n')

        def side_effect(*args):
            filename, index = args
            return lines[index - 1]

        self.getline = patch('data.linecache.getline',
                             Mock(side_effect=side_effect)).start()

        self.filename = '/path/to/target.csv'
        self.reader = RandomCSVReader(self.filename)

    def test_init(self):
        self.mock_open.assert_called_once_with(self.filename)
        self.mock_open.return_value.readlines.assert_called_once()
        self.assertEqual(self.reader._total, 2)
        self.assertEqual(self.reader._csvfile, self.filename)

    def test_getitem(self):
        expected = [line.split(',') for line in self.read_data.split('\n')]
        for i in range(len(self.reader)):
            self.assertListEqual(self.reader[i], expected[i])

        self.assertListEqual(self.reader[0:5], expected[0:5])
        self.assertListEqual(self.reader[0:], expected[0:])
        self.assertListEqual(self.reader[:5], expected[:5])
        self.assertListEqual(self.reader[:5:2], expected[:5:2])

    def tearDown(self):
        patch.stopall()
