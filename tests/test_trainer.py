from unittest import TestCase
from unittest.mock import Mock

import numpy as np
import math

from trainer import Trainer


class TestTrainer(TestCase):
    def test_run(self):
        data_length = 20
        feature_dim = 10
        num_categories = 7

        x = np.random.randn(data_length, feature_dim)
        y = np.random.randint(low=0, high=num_categories, size=(data_length,))

        epoch = 5
        batch_size = 3

        model = Mock()
        trainer = Trainer(model, x, y, batch_size, epoch)
        trainer.run()

        steps = math.ceil(data_length / batch_size)

        for _ in range(epoch):
            prev_xs = []
            prev_ys = []
            for i in range(steps):
                method, args, kwargs = model.method_calls.pop(0)
                self.assertEqual(method, 'partial_fit')
                x, y = args
                size = 2 if i == steps - 1 or i == steps * epoch - 1 else 3
                self.assertTupleEqual(x.shape, (size, feature_dim))
                self.assertTupleEqual(y.shape, (size,))
                for prev_x, prev_y in zip(prev_xs, prev_ys):
                    self.assertRaises(
                        AssertionError, np.testing.assert_array_equal, x, prev_x)
                    self.assertRaises(
                        AssertionError, np.testing.assert_array_equal, y, prev_y)
                prev_xs.append(x)
                prev_ys.append(y)
