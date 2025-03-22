import random
from typing import Dict, List, Any, Optional, Union
from collections import defaultdict

class SchnassNats:
    """A class to manage events and their probabilities."""
    
    def __init__(self):
        """Initialize an empty probability library with version tracking."""
        self.probs: Dict[Any, float] = defaultdict(float) 
        self.version = "2.0.0"
        self._frozen = False 

    def add(self, event: Any, prob: float) -> None:
        """
        Adds an event and its probability.
        
        Args:
            event: Any hashable object
            prob: Probability (0-100)
            
        Raises:
            ValueError: If probability is invalid or total exceeds 100%
            TypeError: If event is not hashable
            RuntimeError: If library is frozen
        """
        if self._frozen:
            raise RuntimeError("Cannot modify a frozen SchnassNats instance")
        try:
            hash(event)  
            if not isinstance(prob, (int, float)):
                raise TypeError("Probability must be a number")
            if not 0 <= prob <= 100:
                raise ValueError("Probability must be between 0 and 100")
            new_total = self.total() + prob - self.probs[event]  
            if new_total > 100 + 1e-10:
                raise ValueError(f"Total probability ({new_total:.1f}%) cannot exceed 100%")
            self.probs[event] = prob
        except TypeError:
            raise TypeError("Event must be a hashable object")

    def remove(self, event: Any) -> None:
        """Removes an event. Raises KeyError if not found, RuntimeError if frozen."""
        if self._frozen:
            raise RuntimeError("Cannot modify a frozen SchnassNats instance")
        try:
            del self.probs[event]
        except KeyError:
            raise KeyError(f"Event '{event}' not found")

    def get(self, event: Any, default: Optional[float] = None) -> Optional[float]:
        """
        Gets an event's probability with optional default value.
        
        Args:
            event: Event to query
            default: Value to return if event not found (default: None)
            
        Returns:
            Probability or default value
        """
        return self.probs.get(event, default)

    def events(self) -> List[Any]:
        """Lists all events."""
        return list(self.probs.keys())

    def total(self) -> float:
        """Gets total probability."""
        return sum(self.probs.values())

    def pick(self, seed: Optional[int] = None) -> Any:
        """
        Picks a random event with optional seed for reproducibility.
        
        Args:
            seed: Optional random seed
            
        Returns:
            Random event
            
        Raises:
            ValueError: If empty
        """
        if not self.probs:
            raise ValueError("Empty library. Add events first.")
        if seed is not None:
            random.seed(seed)
        rand_num = random.uniform(0, self.total())
        cumulative = 0
        for event, prob in self.probs.items():
            cumulative += prob
            if rand_num <= cumulative:
                return event
        return list(self.probs.keys())[-1]  

    def clear(self) -> None:
        """Clears all events. Raises RuntimeError if frozen."""
        if self._frozen:
            raise RuntimeError("Cannot modify a frozen SchnassNats instance")
        self.probs.clear()

    def update(self, event: Any, new_prob: float) -> None:
        """Updates an event's probability by reusing add logic."""
        self.add(event, new_prob)  

    def left(self) -> float:
        """Gets remaining probability."""
        return 100 - self.total()

    def norm(self) -> None:
        """Normalizes probabilities to 100%. Does nothing if total is 0 or frozen."""
        if self._frozen:
            raise RuntimeError("Cannot modify a frozen SchnassNats instance")
        total = self.total()
        if total == 0:
            return
        scale = 100 / total
        for event in self.probs:
            self.probs[event] *= scale

    def freeze(self) -> None:
        """Freezes the instance to prevent further modifications."""
        self._frozen = True

    def unfreeze(self) -> None:
        """Unfreezes the instance to allow modifications."""
        self._frozen = False

    def is_frozen(self) -> bool:
        """Checks if the instance is frozen."""
        return self._frozen

    def __repr__(self) -> str:
        """String representation of the instance."""
        return f"SchnassNats(version={self.version}, events={dict(self.probs)}, frozen={self._frozen})"
