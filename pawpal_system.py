from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Task:
    """Represents a single pet care task."""
    title: str
    duration_minutes: int
    priority: str  # e.g., "high", "medium", "low"
    is_completed: bool = False

    def get_score(self, weights: Dict[str, int]) -> int:
        """Calculates numerical priority score based on owner weights."""
        pass

@dataclass
class Pet:
    """Represents a pet and their specific needs."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Adds a new task to the pet's list."""
        pass

    def delete_task(self, task_title: str):
        """Removes a task by its title."""
        pass

@dataclass
class Owner:
    """Represents the user and their global preferences."""
    name: str
    available_time: int
    pets: List[Pet] = field(default_factory=list)
    priority_weights: Dict[str, int] = field(default_factory=lambda: {"high": 10, "medium": 5, "low": 1})

    def update_preferences(self, new_weights: Dict[str, int]):
        """Updates the importance weights for task priorities."""
        pass

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self, pets: List[Pet]) -> List[Task]:
        """Chooses which tasks to perform."""
        pass

    def explain_logic(self, planned_tasks: List[Task]) -> str:
        """Returns the 'why' behind the chosen tasks."""
        pass