from unittest import TestCase
from unittest.mock import Mock

from trainer import Trainer


class TestTrainer(TestCase):
    def test_run(self):
        import numpy as np
        import math

        model = Mock()
        x = np.random.randn(20, 10)
        y = np.random.randint(low=0, high=5, size=(20,))
        classes = np.unique(y)
        epoch = 2
        batch_size = 3

        trainer = Trainer(model, x, y, batch_size, epoch)
        trainer.run()

        steps = math.ceil(20 / batch_size)

        self.assertEqual(len(model.mock_calls), steps * epoch)

        for _ in range(epoch):
            prev_xs = []
            prev_ys = []
            for i in range(steps):
                method, args, kwargs = model.method_calls.pop(0)
                self.assertEqual(method, 'partial_fit')
                self.assertEqual(len(args), 2)
                size = 2 if i == steps - 1 or i == steps * epoch - 1 else 3
                x, y = args
                self.assertTupleEqual(x.shape, (size, 10))
                self.assertTupleEqual(y.shape, (size,))
                self.assertEqual(len(kwargs), 1)
                for prev_x, prev_y in zip(prev_xs, prev_ys):
                    self.assertRaises(
                        AssertionError, np.testing.assert_array_equal, x, prev_x)
                    self.assertRaises(
                        AssertionError, np.testing.assert_array_equal, y, prev_y)
                np.testing.assert_array_equal(kwargs['classes'], classes)
                prev_xs.append(x)
                prev_ys.append(y)
