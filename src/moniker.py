import numpy as np


class Sampler:
    def __init__(self, weights):
        if type(weights).__module__ != np.__name__:
            weights = np.array(weights, dtype=np.float64)
        assert (
            len(weights.shape) == 1
        ), "Please ensure that the input is one-dimensional."
        assert weights.shape[0] > 2, "Using this is pointless!"

        self.normalization = np.sum(weights, dtype=np.float64)
        self.weights = weights
        self.N = len(self.weights)
        self.factor = self.normalization / self.N
        self.make_table()

    def __repr__(self):
        return f"AliasTable(probabilities={self.weights})"

    def make_table(self):
        """Make the Alias table required for sampling."""
        over = []
        under = []

        scaled_weights = self.weights / self.factor

        for i, weight in enumerate(scaled_weights):
            if weight >= 1.0:
                over.append(i)
            else:
                under.append(i)

        alias = np.zeros(self.N, dtype=np.int64)
        cutoffs = np.zeros(self.N)

        while under and over:
            under_idx = under.pop()
            over_idx = over.pop()

            cutoffs[under_idx] = scaled_weights[under_idx]
            alias[under_idx] = over_idx

            scaled_weights[over_idx] = (
                scaled_weights[over_idx] + scaled_weights[under_idx] - 1.0
            )

            if scaled_weights[over_idx] >= 1.0:
                over.append(over_idx)
            else:
                under.append(over_idx)

        while over:
            cutoffs[over.pop()] = 1.0

        while under:
            cutoffs[under.pop()] = 1.0

        self.cutoffs = cutoffs
        self.alias = alias

    def sample(self, num_samples):
        """Draw samples from the Alias table."""
        samples = np.zeros(num_samples, dtype=np.int64)

        for s in range(num_samples):
            u = np.random.rand()
            i = np.random.randint(self.N)

            if u <= self.cutoffs[i]:
                samples[s] = i
            else:
                samples[s] = self.alias[i]

        return samples
