"""
Filter Module: Bayesian Updates and Monte Carlo Sampling

Implements uncertainty quantification for displacement components using
Beta distributions and Monte Carlo sampling for route stability.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy.stats import beta
import hashlib


class DisplacementFilter:
    """
    Maintains Bayesian posteriors over displacement components.
    """
    
    def __init__(
        self,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
        mc_samples: int = 1000
    ):
        """
        Initialize filter with Beta priors.
        
        Args:
            prior_alpha: Prior alpha parameter for Beta distribution.
            prior_beta: Prior beta parameter for Beta distribution.
            mc_samples: Number of Monte Carlo samples for stability computation.
        """
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self.mc_samples = mc_samples
        
        # Posterior parameters for each component
        # Initialize with priors
        self.alpha_post = {
            "GTD": prior_alpha,
            "IVD": prior_alpha,
            "IAD": prior_alpha,
            "IID": prior_alpha
        }
        self.beta_post = {
            "GTD": prior_beta,
            "IVD": prior_beta,
            "IAD": prior_beta,
            "IID": prior_beta
        }
    
    def update(
        self,
        displacement: Dict[str, float],
        measurement_noise: float = 0.05
    ) -> None:
        """
        Update posteriors with observed displacement.

        Args:
            displacement: Dict with keys GTD, IVD, IAD, IID.
            measurement_noise: Noise level σ (0 < σ ≤ 1).
        """
        if not (0 < measurement_noise <= 1):
            raise ValueError("measurement_noise must be in (0, 1]")

        sigma_c = float(np.clip(measurement_noise, 0.01, 1.0))

        for component in ["GTD", "IVD", "IAD", "IID"]:
            if component not in displacement:
                continue

            d = float(displacement[component])
            d_c = float(np.clip(d, 0.001, 0.999))

            # n_eff = d(1-d)/sigma^2
            n_eff = (d_c * (1.0 - d_c)) / (sigma_c ** 2)

            # Bayesian update
            self.alpha_post[component] += n_eff * d_c
            self.beta_post[component] += n_eff * (1.0 - d_c)

    def update_with_observations(
        self,
        observations: list,
        default_noise: float = 0.05
    ) -> None:
        """
        Update posteriors with ordered observations, each with optional noise override.

        Args:
            observations: List of observation dicts with keys:
                - 'maps_to': One of GTD, IVD, IAD, IID
                - 'value': Observed value in [0, 1]
                - 'noise': Optional noise override (0 < noise ≤ 1)
            default_noise: Default noise level if not specified per observation.
        """
        for obs in observations:
            component = obs["maps_to"]
            value = obs["value"]
            noise = obs.get("noise", default_noise)

            if not (0 < noise <= 1):
                raise ValueError(f"observation noise must be in (0, 1], got {noise}")
            if not (0 <= value <= 1):
                raise ValueError(f"observation value must be in [0, 1], got {value}")
            if component not in ["GTD", "IVD", "IAD", "IID"]:
                raise ValueError(f"observation maps_to must be one of GTD, IVD, IAD, IID, got {component}")

            # Clamp to avoid boundary issues
            sigma_c = float(np.clip(noise, 0.01, 1.0))
            value_c = float(np.clip(value, 0.001, 0.999))

            # n_eff = d(1-d)/sigma^2
            n_eff = (value_c * (1.0 - value_c)) / (sigma_c ** 2)

            # Bayesian update for this specific observation
            self.alpha_post[component] += n_eff * value_c
            self.beta_post[component] += n_eff * (1.0 - value_c)
    
    def get_posterior_mean(self, component: str) -> float:
        """
        Get posterior mean for a component.
        
        Args:
            component: One of GTD, IVD, IAD, IID.
        
        Returns:
            Posterior mean.
        """
        alpha = self.alpha_post[component]
        beta_val = self.beta_post[component]
        return alpha / (alpha + beta_val)
    
    def get_posterior_means(self) -> Dict[str, float]:
        """
        Get all posterior means.
        
        Returns:
            Dict with keys GTD, IVD, IAD, IID.
        """
        return {
            comp: self.get_posterior_mean(comp)
            for comp in ["GTD", "IVD", "IAD", "IID"]
        }
    
    def get_credible_interval(
        self,
        component: str,
        quantiles: Tuple[float, float] = (0.05, 0.95)
    ) -> Tuple[float, float]:
        """
        Get credible interval for a component.
        
        Args:
            component: One of GTD, IVD, IAD, IID.
            quantiles: Lower and upper quantiles (default 90% interval).
        
        Returns:
            (lower, upper) bounds.
        """
        alpha = self.alpha_post[component]
        beta_val = self.beta_post[component]
        
        lower = beta.ppf(quantiles[0], alpha, beta_val)
        upper = beta.ppf(quantiles[1], alpha, beta_val)
        
        return (float(lower), float(upper))
    
    def get_credible_intervals(
        self,
        quantiles: Tuple[float, float] = (0.05, 0.95)
    ) -> Dict[str, Tuple[float, float]]:
        """
        Get credible intervals for all components.
        
        Args:
            quantiles: Lower and upper quantiles.
        
        Returns:
            Dict mapping component to (lower, upper) bounds.
        """
        return {
            comp: self.get_credible_interval(comp, quantiles)
            for comp in ["GTD", "IVD", "IAD", "IID"]
        }
    
    def sample_posterior(
        self,
        component: str,
        n_samples: int,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        """
        Sample from posterior distribution.

        Args:
            component: One of GTD, IVD, IAD, IID.
            n_samples: Number of samples.
            rng: Random number generator (use default_rng(seed) for reproducible sampling).

        Returns:
            Array of samples.
        """
        alpha = self.alpha_post[component]
        beta_val = self.beta_post[component]

        if rng is None:
            rng = np.random.default_rng()

        # Use numpy's beta distribution for local state control
        return rng.beta(alpha, beta_val, size=n_samples)
    
    def compute_route_stability(
        self,
        tie_break_order: List[str] = None,
        seed: Optional[int] = None
    ) -> Tuple[float, str]:
        """
        Compute route stability via Monte Carlo sampling.

        Args:
            tie_break_order: Order for tie-breaking (default: GTD > IAD > IVD > IID).
            seed: Random seed for reproducibility.

        Returns:
            (stability, dominant_route) where stability is in [0, 1]
            and dominant_route is the most frequent route.
        """
        if tie_break_order is None:
            tie_break_order = ["GTD", "IAD", "IVD", "IID"]

        # Use local generator (PCG64) to ensure deterministic behavior
        rng = np.random.Generator(np.random.PCG64(seed))

        # Sample from all posteriors using local generator
        samples = {}
        for comp in ["GTD", "IVD", "IAD", "IID"]:
            samples[comp] = self.sample_posterior(comp, self.mc_samples, rng=rng)
        
        # Determine dominant component for each sample
        routes = []
        for i in range(self.mc_samples):
            # Deterministic tie-breaking using tie_break_order priority
            dominant = max(
                tie_break_order,
                key=lambda c: samples[c][i]
            )
            routes.append(dominant)
        
        # Count route frequencies
        route_counts = {}
        for route in routes:
            route_counts[route] = route_counts.get(route, 0) + 1
        
        # Most frequent route
        dominant_route = max(route_counts, key=route_counts.get)
        stability = route_counts[dominant_route] / self.mc_samples
        
        return (float(stability), dominant_route)
    
    def get_dominant_component(
        self,
        tie_break_order: List[str] = None
    ) -> str:
        """
        Get dominant component from posterior means.
        
        Args:
            tie_break_order: Order for tie-breaking.
        
        Returns:
            Component name (GTD, IVD, IAD, or IID).
        """
        if tie_break_order is None:
            tie_break_order = ["GTD", "IAD", "IVD", "IID"]
        
        means = self.get_posterior_means()
        max_val = max(means.values())
        candidates = [
            comp for comp, val in means.items()
            if val == max_val
        ]
        
        # Tie-break
        for comp in tie_break_order:
            if comp in candidates:
                return comp
        
        return candidates[0]  # Fallback


def generate_deterministic_seed(
    session_id: Optional[str],
    egress_id: str
) -> int:
    """
    Generate deterministic seed from session and egress IDs.
    
    Args:
        session_id: Session identifier (or None).
        egress_id: Egress packet ID.
    
    Returns:
        Integer seed.
    """
    session_key = session_id if (session_id is not None and session_id != "") else "none"
    combined = f"{session_key}|{egress_id}"
    
    # SHA256 hash, take first 8 bytes, convert to uint64 (little-endian).
    # This matches the spec determinism scenario expected route_stability value.
    hash_bytes = hashlib.sha256(combined.encode("utf-8")).digest()[:8]
    seed = int.from_bytes(hash_bytes, byteorder='little', signed=False)
    
    return seed

