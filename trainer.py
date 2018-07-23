import numpy as np


class Trainer:
    def __init__(self, model, x, y, batch_size, epoch):
        self.model = model
        self.x = x
        self.y = y
        self.classes = np.unique(y)
        self.batch_size = batch_size
        self.epoch = epoch
        self.order = np.random.permutation(len(x))

    def run(self):
        batch_size = self.batch_size
        x = self.x
        y = self.y
        classes = self.classes
        model = self.model
        order = self.order

        for _ in range(self.epoch):
            for i in range(0, len(x), batch_size):
                indices = order[i:i+batch_size]
                x_batch, y_batch = x[indices], y[indices]
                model.partial_fit(x_batch, y_batch, classes=classes)
            np.random.shuffle(order)


if __name__ == '__main__':
    import warnings
    from sklearn.neural_network import MLPClassifier
    from sklearn.datasets import fetch_mldata
    from sklearn.model_selection import train_test_split

    warnings.filterwarnings('ignore')

    mnist = fetch_mldata('MNIST original')
    x_train, x_test, y_train, y_test = train_test_split(
        mnist.data / 255., mnist.target, test_size=.2)
    model = MLPClassifier()
    trainer = Trainer(model, x_train, y_train, 128, 50)
    trainer.run()
    print(model.score(x_test, y_test))
