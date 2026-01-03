"""
Domain State Representation

State classes for Economy, Employment, Education, and Ecology domains.
Each domain maintains potentials (4D), edge vector (6D), aperture, and SI.

Reference: CGM Paper Section 4
"""

import numpy as np
from typing import Optional, Tuple


class DomainStateBase:
    """
    Base class for domain states.
    
    Provides THM decomposition tracking: y = y_authentic + y_derivative.
    
    THM terminology:
        - Original: self-governance contribution (local feedback)
        - Derivative: cross-domain contribution (AI-mediated flow)
    """
    
    def __init__(self):
        self.y: Optional[np.ndarray] = None            # Edge vector (6D)
        self.y_H: Optional[np.ndarray] = None          # Alias for y_authentic
        self.y_AI: Optional[np.ndarray] = None         # Alias for y_derivative
        self.y_authentic: Optional[np.ndarray] = None  # Original contribution
        self.y_derivative: Optional[np.ndarray] = None # Derivative contribution
    
    def set_decomposition(
        self, 
        y_authentic: np.ndarray, 
        y_derivative: np.ndarray
    ):
        """
        Sets Original and derivative components.
        
        Args:
            y_authentic: Self-governance contribution (6D).
            y_derivative: Cross-domain contribution (6D).
        """
        self.y_authentic = y_authentic
        self.y_derivative = y_derivative
        # Maintain compatibility aliases
        self.y_H = y_authentic
        self.y_AI = y_derivative
    
    def get_human_gradient_fraction(
        self, 
        P_grad: np.ndarray, 
        W: np.ndarray
    ) -> float:
        """
        Computes ||P_grad @ y_authentic||^2_W / ||P_grad @ y||^2_W.
        
        Args:
            P_grad: Gradient projection (6x6).
            W: Weight matrix (6x6).
        
        Returns:
            Fraction in [0, 1], or -1 if not set.
        """
        if self.y_H is None or self.y is None:
            return -1.0
        
        y_grad_H = P_grad @ self.y_H
        y_grad_tot = P_grad @ self.y
        
        G_H = np.dot(y_grad_H, W @ y_grad_H)
        G_tot = np.dot(y_grad_tot, W @ y_grad_tot)
        
        if G_tot < 1e-10:
            return 1.0 if G_H < 1e-10 else 0.0
        
        return float(G_H / G_tot)
    
    def get_ai_cycle_energy(
        self, 
        P_cycle: np.ndarray, 
        W: np.ndarray
    ) -> float:
        """
        Computes ||P_cycle @ y_derivative||^2_W.
        
        Args:
            P_cycle: Cycle projection (6x6).
            W: Weight matrix (6x6).
        
        Returns:
            Cycle energy, or -1 if not set.
        """
        if self.y_AI is None:
            return -1.0
        
        y_cycle_AI = P_cycle @ self.y_AI
        C_AI = np.dot(y_cycle_AI, W @ y_cycle_AI)
        
        return float(C_AI)


class EconomyState(DomainStateBase):
    """
    Economy domain state (CGM).
    
    Potentials: Gov, Info, Infer, Int in [0, 1].
    - Gov: Governance
    - Info: Information
    - Infer: Inference
    - Int: Intelligence
    """
    
    def __init__(self, Gov: float, Info: float, Infer: float, Int: float,
                 y: Optional[np.ndarray] = None,
                 A: Optional[float] = None,
                 S: Optional[float] = None):
        super().__init__()
        self.Gov = self._clip(Gov)
        self.Info = self._clip(Info)
        self.Infer = self._clip(Infer)
        self.Int = self._clip(Int)
        if y is not None:
            self.y = y
        self.A = A
        self.S = S
    
    def _clip(self, value: float) -> float:
        return float(np.clip(value, 0.0, 1.0))
    
    def to_potential_vector(self) -> np.ndarray:
        """Returns [Gov, Info, Infer, Int]."""
        return np.array([self.Gov, self.Info, self.Infer, self.Int])
    
    def update_from_potential_vector(self, x_new: np.ndarray):
        """Updates from length-4 vector."""
        if len(x_new) != 4:
            raise ValueError("x_new must have length 4")
        self.Gov = self._clip(x_new[0])
        self.Info = self._clip(x_new[1])
        self.Infer = self._clip(x_new[2])
        self.Int = self._clip(x_new[3])


class EmploymentState(DomainStateBase):
    """
    Employment domain state (Gyroscope).
    
    Potentials: GM, ICu, IInter, ICo in [0, 1], normalized to sum = 1.
    - GM: Governance Management
    - ICu: Information Curation
    - IInter: Inference Interaction
    - ICo: Intelligence Cooperation
    """
    
    def __init__(self, GM: float, ICu: float, IInter: float, ICo: float,
                 y: Optional[np.ndarray] = None,
                 A: Optional[float] = None,
                 S: Optional[float] = None,
                 scale: float = 1.0):
        super().__init__()
        total = GM + ICu + IInter + ICo
        if total > 0:
            self.GM = GM / total
            self.ICu = ICu / total
            self.IInter = IInter / total
            self.ICo = ICo / total
        else:
            self.GM = self.ICu = self.IInter = self.ICo = 0.25
        
        self.GM = self._clip(self.GM)
        self.ICu = self._clip(self.ICu)
        self.IInter = self._clip(self.IInter)
        self.ICo = self._clip(self.ICo)
        self._normalize()
        
        if y is not None:
            self.y = y
        self.A = A
        self.S = S
        self.scale = scale
    
    def _clip(self, value: float) -> float:
        return float(np.clip(value, 0.0, 1.0))
    
    def _normalize(self):
        total = self.GM + self.ICu + self.IInter + self.ICo
        if total > 0:
            self.GM /= total
            self.ICu /= total
            self.IInter /= total
            self.ICo /= total
        else:
            self.GM = self.ICu = self.IInter = self.ICo = 0.25
    
    def to_potential_vector(self) -> np.ndarray:
        """Returns [GM, ICu, IInter, ICo]."""
        return np.array([self.GM, self.ICu, self.IInter, self.ICo])
    
    def update_from_potential_vector(self, x_new: np.ndarray, scale: Optional[float] = None):
        """Updates from length-4 vector."""
        if len(x_new) != 4:
            raise ValueError("x_new must have length 4")
        self.GM = self._clip(x_new[0])
        self.ICu = self._clip(x_new[1])
        self.IInter = self._clip(x_new[2])
        self.ICo = self._clip(x_new[3])
        if scale is not None:
            self.scale = scale
        self._normalize()


class EducationState(DomainStateBase):
    """
    Education domain state (THM).
    
    Potentials: GMT, ICV, IIA, ICI in [0, 1].
    - GMT: Governance Management Traceability
    - ICV: Information Curation Variety
    - IIA: Inference Interaction Accountability
    - ICI: Intelligence Cooperation Integrity
    """
    
    def __init__(self, GMT: float, ICV: float, IIA: float, ICI: float,
                 y: Optional[np.ndarray] = None,
                 A: Optional[float] = None,
                 S: Optional[float] = None):
        super().__init__()
        self.GMT = self._clip(GMT)
        self.ICV = self._clip(ICV)
        self.IIA = self._clip(IIA)
        self.ICI = self._clip(ICI)
        if y is not None:
            self.y = y
        self.A = A
        self.S = S
    
    def _clip(self, value: float) -> float:
        return float(np.clip(value, 0.0, 1.0))
    
    def to_potential_vector(self) -> np.ndarray:
        """Returns [GMT, ICV, IIA, ICI]."""
        return np.array([self.GMT, self.ICV, self.IIA, self.ICI])
    
    def update_from_potential_vector(self, x_new: np.ndarray):
        """Updates from length-4 vector."""
        if len(x_new) != 4:
            raise ValueError("x_new must have length 4")
        self.GMT = self._clip(x_new[0])
        self.ICV = self._clip(x_new[1])
        self.IIA = self._clip(x_new[2])
        self.ICI = self._clip(x_new[3])


class EcologyState(DomainStateBase):
    """
    Ecology domain state (CGM–Gyroscope–THM BU dual combination).
    
    Ecology is the BU-vertex domain computed via CGM dual combination:
        x_Ecol = (δ_BU/m_a) · x_balanced + A* · x_deriv
    
    Where:
        - δ_BU/m_a ≈ 0.9793 is the Ingress weight (canonical balanced memory)
        - A* ≈ 0.0207 is the Egress weight (derivative domains actuality)
        - x_balanced = [w_CS, w_UNA, w_ONA, w_BU] (CGM stage weights)
        - x_deriv = (x_Econ + x_Emp + x_Edu) / 3 (aggregate derivative domains)
    
    Potentials (BU-vertex stage coordinates):
        - E_gov: Ecological Governance (aggregates Gov + GM + GMT)
        - E_info: Ecological Information (aggregates Info + ICu + ICV)
        - E_inf: Ecological Inference (aggregates Infer + IInter + IIA)
        - E_intel: Ecological Intelligence (aggregates Int + ICo + ICI)
    
    Displacement vector D = |x_deriv - x_balanced|:
        - GTD: Governance Traceability Displacement (preserved)
        - IVD: Information Variety Displacement (preserved)
        - IAD: Inference Accountability Displacement (preserved)
        - IID: Intelligence Integrity Displacement (preserved)
    """
    
    def __init__(self, E_gov: float, E_info: float, E_inf: float, E_intel: float,
                 y: Optional[np.ndarray] = None,
                 A: Optional[float] = None,
                 S: Optional[float] = None,
                 GTD: Optional[float] = None,
                 IVD: Optional[float] = None,
                 IAD: Optional[float] = None,
                 IID: Optional[float] = None):
        super().__init__()
        # State potentials (BU-vertex stage coordinates)
        self.E_gov = self._clip(E_gov)      # Ecological Governance
        self.E_info = self._clip(E_info)    # Ecological Information
        self.E_inf = self._clip(E_inf)      # Ecological Inference
        self.E_intel = self._clip(E_intel)  # Ecological Intelligence
        if y is not None:
            self.y = y
        self.A = A
        self.S = S
        # Displacement vector: D = |x_deriv - x_balanced|
        self.GTD = GTD if GTD is not None else 0.0
        self.IVD = IVD if IVD is not None else 0.0
        self.IAD = IAD if IAD is not None else 0.0
        self.IID = IID if IID is not None else 0.0
    
    def _clip(self, value: float) -> float:
        return float(np.clip(value, 0.0, 1.0))
    
    def to_potential_vector(self) -> np.ndarray:
        """Returns BU-vertex stage potentials [E_gov, E_info, E_inf, E_intel]."""
        return np.array([self.E_gov, self.E_info, self.E_inf, self.E_intel])
    
    def update_from_potential_vector(self, x_new: np.ndarray):
        """Updates from length-4 vector."""
        if len(x_new) != 4:
            raise ValueError("x_new must have length 4")
        self.E_gov = self._clip(x_new[0])
        self.E_info = self._clip(x_new[1])
        self.E_inf = self._clip(x_new[2])
        self.E_intel = self._clip(x_new[3])
    
    def total_displacement(self) -> float:
        """Returns sum of all displacement magnitudes."""
        return float(self.GTD + self.IVD + self.IAD + self.IID)
    
    def displacement_vector(self) -> np.ndarray:
        """Returns displacement vector [GTD, IVD, IAD, IID]."""
        return np.array([self.GTD, self.IVD, self.IAD, self.IID])

