import unittest
import numpy as np

from moniker import sample


class TestSampling(unittest.TestCase):
    def test_against_analytic(self):
        num_samples = 10_000_000
        weights = np.array([4, 1, 5, 2])  # unnormalized probabilities

        sampler = sample.Sampler(weights)
        samples = sampler.sample(num_samples=num_samples)

        _, my_counts = np.unique(samples, return_counts=True)

        np.testing.assert_allclose(
            my_counts / num_samples, weights / sum(weights), rtol=1e-2, atol=0
        )


if __name__ == "__main__":
    unittest.main()
