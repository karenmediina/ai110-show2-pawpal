from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    frequency: str = "Daily"  # ADDED: per requirements
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_completed: bool = False

    def mark_complete(self):
        """Standard method to update task status."""
        self.is_completed = True

    def get_value_density(self, weights: Dict[str, int]) -> float:
        """Calculates score per minute to optimize the schedule."""
        weight = weights.get(self.priority.lower(), 1)
        return weight / max(self.duration_minutes, 1)

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

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    # ADDED: This is the "proper" way for the Scheduler to talk to the Owner
    def get_all_pet_tasks(self) -> List[tuple[Task, str]]:
        """Retrieves all tasks across all pets for the scheduler."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((task, pet.name))
        return all_tasks

@dataclass
class ScheduledTask:
    task: Task
    pet_name: str
    start_minute: int
    reason: str

class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self) -> List[ScheduledTask]:
        # Refined communication: Asking the owner for the data
        all_entries = self.owner.get_all_pet_tasks()

        all_entries.sort(
            key=lambda entry: entry[0].get_value_density(self.owner.priority_weights), 
            reverse=True
        )

        plan = []
        current_time = 0
        remaining_budget = self.owner.available_time

        for task, pet_name in all_entries:
            if task.duration_minutes <= remaining_budget:
                reason = f"High value-density: {task.priority} priority fits in {task.duration_minutes}m."
                plan.append(ScheduledTask(task, pet_name, current_time, reason))
                current_time += task.duration_minutes
                remaining_budget -= task.duration_minutes
        
        return plan