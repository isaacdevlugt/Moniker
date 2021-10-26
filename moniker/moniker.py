import numpy as np

class Sampler():
    def __init__(self, vec):
        assert len(vec) > 2, "Using this is pointless!"

        if type(vec).__module__ != np.__name__:
            vec = np.array(vec)
        assert len(vec.shape) == 1, "Please ensure that the input is one-dimensional."

        normalization = np.sum(vec, dtype=np.float64)
        if normalization != 1.0:
            self.probabilities = vec / normalization
        else:
            self.probabilities = vec

        self.K = len(self.probabilities)
        self.weights = self.probabilities * self.K
        self.make_table()

    def __repr__(self):
        return (
            f"AliasTable(probabilities={self.probabilities})"
        )

    def make_table(self):
        """Make the Alias table required for sampling."""
        self.reassignments = np.zeros(self.K, dtype=np.int64)
        
        over = []
        under = []
        for k in range(self.K):
            if self.weights[k] < 1.0:
                under.append(k)
            else:
                over.append(k)
        
        while over and under:
            under_idx = under.pop()
            over_idx = over.pop()

            self.reassignments[under_idx] = over_idx
            self.weights[over_idx] += self.weights[under_idx] - 1.0

            if self.weights[k] < 1.0:
                under.append(over_idx)
            else:
                over.append(over_idx)

    def sample(self, num_samples):
        """Draw samples from the Alias table."""
        samples = np.zeros(num_samples, dtype=np.int64)
        ks = np.random.randint(self.K, size=num_samples)
        rs = np.random.uniform(size=num_samples)

        results = rs < self.weights[ks]
        for i in range(num_samples):
            samples[i] = ks[i] if results[i] else self.reassignments[ks[i]]

        return samples