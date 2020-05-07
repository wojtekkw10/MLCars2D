import numpy as np


def nonlinear(x, derivative=False):
    if derivative:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


def generate_layer(height, width):
    return 2 * np.random.random((height, width)) - 1


class brain:

    def __init__(self, id, shape_matrix):
        self.id = id
        self.value = 0
        self.joint_matrix = []
        self.weight_matrix = []

        for i in range(len(shape_matrix) - 1):
            height = shape_matrix[i]
            width = shape_matrix[i + 1]
            self.joint_matrix.append(generate_layer(height, width))
            self.weight_matrix.append(generate_layer(1, height))

    def randomize(self):
        for i in range(len(self.joint_matrix)):
            shape_ = np.shape(self.joint_matrix[i])
            self.joint_matrix[i] = generate_layer(shape_[0], shape_[1])

        for i in range(len(self.weight_matrix)):
            shape_ = np.shape(self.weight_matrix[i])
            self.weight_matrix[i] = generate_layer(shape_[0], shape_[1])

    def calc(self, input_):

        temp_layer = input_
        for i in range(len(self.joint_matrix)):
            temp_layer += self.weight_matrix[i][0]
            temp_layer = nonlinear(np.dot(temp_layer, self.joint_matrix[i]))

        self.value = temp_layer
        return self.value


car_brain = brain(1, [3, 7, 3])

distances = [3, 5, 4]

print(car_brain.calc(distances))

distances = [1, 2, 8]

print(car_brain.calc(distances))
