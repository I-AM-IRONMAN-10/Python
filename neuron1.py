import numpy as np

class Neuron:
    def __init__(self, num_inputs):
        self.weights = None # Or np.zeros(num_inputs) or np.random.rand(num_inputs)
        self.bias = None    # Or 0
        self.num_inputs = num_inputs

    def set_parameters(self, weights, bias):
        # Set weights and bias after initialization if they were None
        if len(weights) != self.num_inputs:
            raise ValueError("Number of weights must match number of inputs")
        self.weights = np.array(weights)
        self.bias = np.array(bias)

    def activate(self, inputs):
        if self.weights is None or self.bias is None:
            raise RuntimeError("Neuron parameters (weights and bias) are not set")
        if len(inputs) != self.num_inputs:
            raise ValueError("Number of inputs must match number of weights")

        # Example: Weighted sum + bias
        weighted_sum = np.dot(inputs, self.weights) + self.bias

        return weighted_sum # For simplicity, returning weighted sum here

# To create a "neuron" with no parameters set yet:
my_neuron = Neuron(num_inputs=3)

# Later, you would set its weights and bias (e.g., after training)
# my_neuron.set_parameters(weights=[0.5, -0.2, 0.1], bias=0.0)

# And then use it with inputs
# result = my_neuron.activate([1.0, 2.0, 0.5])