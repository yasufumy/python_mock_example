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
        self.num_lines = len(lines)

    def test_init(self):
        self.mock_open.assert_called_once_with(self.filename)
        self.mock_open.return_value.readlines.assert_called_once()
        self.assertEqual(self.reader._total, self.num_lines)
        self.assertEqual(self.reader._csvfile, self.filename)

    def test_getitem(self):
        expected = [line.split(',') for line in self.read_data.split('\n')]
        for i in range(len(self.reader)):
            self.assertListEqual(self.reader[i], expected[i])

        slices = [slice(0, 5), slice(0), slice(None, 5), slice(None, 5, 2)]

        for slice_ in slices:
            print(self.reader[slice_], expected[slice_])
            self.assertListEqual(self.reader[slice_], expected[slice_])

    def tearDown(self):
        patch.stopall()
