from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_completed: bool = False

    def get_value_density(self, weights: Dict[str, int]) -> float:
        """Calculates score per minute to optimize the schedule."""
        weight = weights.get(self.priority.lower(), 1)
        # Avoid division by zero, though duration should be > 0
        return weight / max(self.duration_minutes, 1)

@dataclass
class ScheduledTask:
    """The result of the scheduling logic."""
    task: Task
    pet_name: str
    start_minute: int
    reason: str

@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

@dataclass
class Owner:
    name: str
    available_time: int
    pets: List[Pet] = field(default_factory=list)
    priority_weights: Dict[str, int] = field(
        default_factory=lambda: {"high": 10, "medium": 5, "low": 2}
    )

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> List[ScheduledTask]:
        """
        Implements a Greedy Value-Density algorithm (Heuristic for Knapsack).
        """
        # 1. Flatten all tasks with pet context
        all_entries = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                all_entries.append((task, pet.name))

        # 2. Sort by Value Density (Score/Duration)
        all_entries.sort(
            key=lambda entry: entry[0].get_value_density(self.owner.priority_weights), 
            reverse=True
        )

        plan = []
        current_time = 0
        remaining_budget = self.owner.available_time

        for task, pet_name in all_entries:
            if task.duration_minutes <= remaining_budget:
                reason = f"High value-density: {task.priority} priority in only {task.duration_minutes}m."
                
                plan.append(ScheduledTask(
                    task=task,
                    pet_name=pet_name,
                    start_minute=current_time,
                    reason=reason
                ))
                
                current_time += task.duration_minutes
                remaining_budget -= task.duration_minutes
        
        return plan