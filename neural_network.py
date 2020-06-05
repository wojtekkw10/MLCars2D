import numpy as np


def nonlinear(x, derivative=False):
    if derivative:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


def generate_layer(height, width):
    return 2 * np.random.random((height, width)) - 1


def flatten(matrix):
    return np.reshape(matrix, (1, -1))[0]


class CarNeuralNetwork:

    def __init__(self, id, shape_matrix):
        self.id = id
        self.shape_matrix = shape_matrix
        self.value = 0
        self.joint_matrix = []
        self.weight_matrix = []

        for i in range(len(shape_matrix) - 1):
            height = shape_matrix[i]
            width = shape_matrix[i + 1]
            self.joint_matrix.append(generate_layer(height, width))
            self.weight_matrix.append(generate_layer(1, height)[0])

    def randomize(self):
        for i in range(len(self.joint_matrix)):
            shape_ = np.shape(self.joint_matrix[i])
            self.joint_matrix[i] = generate_layer(shape_[0], shape_[1])

        for i in range(len(self.weight_matrix)):
            shape_ = np.shape(self.weight_matrix[i])
            self.weight_matrix[i] = generate_layer(shape_[0], shape_[1])[0]

    def calc(self, input_):

        temp_layer = input_
        for i in range(len(self.joint_matrix)):
            temp_layer += self.weight_matrix[i]
            temp_layer = nonlinear(np.dot(temp_layer, self.joint_matrix[i]))

        self.value = temp_layer
        return self.value

    def set_weight_list(self, weight_arr):
        weight_arr = weight_arr.copy()
        shape = self.shape_matrix
        for i in range(len(shape)-1):
            self.weight_matrix[i] = np.array(weight_arr[0:shape[i]])
            del(weight_arr[0:shape[i]])
            for j in range(shape[i]):
                self.joint_matrix[i][j] = np.array(weight_arr[0:shape[i+1]])
                del (weight_arr[0:shape[i+1]])

    def get_weight_list(self):
        weight_arr = []

        for i in range(len(self.joint_matrix)):
            weight_arr.extend(flatten(self.weight_matrix[i]))
            weight_arr.extend(flatten(self.joint_matrix[i]))

        return weight_arr



