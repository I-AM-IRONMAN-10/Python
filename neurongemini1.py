import numpy as np

# Activation function (Sigmoid)
def sigmoid(x):
    """
    Squashes the input value into a range between 0 and 1.
    This function is often used for a neuron's output.
    """
    return 1 / (1 + np.exp(-x))

class Neuron:
    """
    Represents a single neuron in a neural network.
    """
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def feedforward(self, inputs):
        """
        Calculates the neuron's output.
        It sums the weighted inputs, adds the bias, and then
        applies the activation function.
        """
        # Step 1: Multiply inputs by weights and sum them up
        total = np.dot(self.weights, inputs) + self.bias
        
        # Step 2: Apply the activation function
        return sigmoid(total)

# --- Let's model the connection ---

# Define the weights and bias for our neurons
# Imagine Neuron 1 takes 2 input values
weights_n1 = np.array([0.5, -0.5]) 
bias_n1 = 0.1

# Neuron 2 will take the output of Neuron 1 as its single input
weights_n2 = np.array([0.8])
bias_n2 = -0.2

# Create the two neurons
neuron1 = Neuron(weights_n1, bias_n1)
neuron2 = Neuron(weights_n2, bias_n2)

# --- Let the data flow! ---

# Provide some initial inputs to the first neuron
initial_inputs = np.array([10, 5]) # e.g., pixel values from an image

print(f"🔹 Initial Inputs to Neuron 1: {initial_inputs}")

# Calculate the output of the first neuron
output_n1 = neuron1.feedforward(initial_inputs)
print(f" Neuron 1 Output: {output_n1:.4f}")

print("\n--- Connection ---")
print(f"The output of Neuron 1 ({output_n1:.4f}) now becomes the input for Neuron 2.\n")

# The output of Neuron 1 is the input for Neuron 2
output_n2 = neuron2.feedforward(output_n1)

print(f"🔸 Final Output from Neuron 2: {output_n2:.4f}")