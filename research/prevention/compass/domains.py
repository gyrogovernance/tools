"""
Domain State Representation

State classes for Economy, Employment, and Education domains.
Each domain maintains potentials (4D), edge vector (6D), aperture, and SI.

Reference: CGM Paper Section 4
"""

import numpy as np
from typing import Optional


class DomainStateBase:
    """
    Base class for domain states.

    Provides basic edge vector storage.
    """

    def __init__(self):
        self.y: Optional[np.ndarray] = None  # Edge vector (6D)


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
                 A: Optional[float] = None):
        super().__init__()
        self.Gov = self._clip(Gov)
        self.Info = self._clip(Info)
        self.Infer = self._clip(Infer)
        self.Int = self._clip(Int)
        if y is not None:
            self.y = y
        self.A = A
    
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
                 A: Optional[float] = None):
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
    
    def update_from_potential_vector(self, x_new: np.ndarray):
        """Updates from length-4 vector."""
        if len(x_new) != 4:
            raise ValueError("x_new must have length 4")
        self.GM = self._clip(x_new[0])
        self.ICu = self._clip(x_new[1])
        self.IInter = self._clip(x_new[2])
        self.ICo = self._clip(x_new[3])
        self._normalize()


class EducationState(DomainStateBase):
    """
    Education domain state (THM).
    
    Potentials: GT, IV, IA, IInteg in [0, 1].
    - GT: Governance Traceability
    - IV: Information Variety
    - IA: Inference Accountability
    - IInteg: Intelligence Integrity
    """
    
    def __init__(self, GT: float, IV: float, IA: float, IInteg: float,
                 y: Optional[np.ndarray] = None,
                 A: Optional[float] = None):
        super().__init__()
        self.GT = self._clip(GT)
        self.IV = self._clip(IV)
        self.IA = self._clip(IA)
        self.IInteg = self._clip(IInteg)
        if y is not None:
            self.y = y
        self.A = A
    
    def _clip(self, value: float) -> float:
        return float(np.clip(value, 0.0, 1.0))
    
    def to_potential_vector(self) -> np.ndarray:
        """Returns [GT, IV, IA, IInteg]."""
        return np.array([self.GT, self.IV, self.IA, self.IInteg])
    
    def update_from_potential_vector(self, x_new: np.ndarray):
        """Updates from length-4 vector."""
        if len(x_new) != 4:
            raise ValueError("x_new must have length 4")
        self.GT = self._clip(x_new[0])
        self.IV = self._clip(x_new[1])
        self.IA = self._clip(x_new[2])
        self.IInteg = self._clip(x_new[3])


