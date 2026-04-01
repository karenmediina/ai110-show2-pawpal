from dataclasses import dataclass, field
from typing import List, Dict, Optional
import uuid

from datetime import datetime, timedelta
from dataclasses import dataclass, field
import uuid

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    start_time: str = "09:00"
    due_date: datetime = field(default_factory=datetime.now)
    frequency: str = "Once"  # "Once", "Daily", "Weekly"
    is_completed: bool = False
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def mark_complete(self):
        """
        Marks current task as done and, if recurring, returns 
         a fresh instance for the next occurrence.
        """
        self.is_completed = True
        
        if self.frequency == "Once":
            return None
        
        # Calculate the next interval using timedelta
        # Daily = +1 day, Weekly = +7 days
        days_to_add = 1 if self.frequency == "Daily" else 7
        next_occurrence_date = self.due_date + timedelta(days=days_to_add)
        
        # Return a 'clone' of the task but with the new date and reset status
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            start_time=self.start_time,
            due_date=next_occurrence_date,
            frequency=self.frequency,
            is_completed=False
        )

@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task_id: str):
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def complete_task_by_id(self, task_id: str):
        """Finds a task, completes it, and handles recursion."""
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                # 1. Mark complete and get the 'successor'
                next_task = task.mark_complete()
                
                # 2. If it's recurring, swap the old one for the new one
                if next_task:
                    self.tasks[i] = next_task
                return True
        return False

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

    # SORTING LOGIC: Using lambda for time strings
    def sort_tasks_by_time(self, task_list: List[tuple]):
        """
        Sorts a list of (Task, pet_name) tuples by the Task.start_time string.
        Uses a lambda to ensure '09:00' comes before '10:00'.
        """
        return sorted(task_list, key=lambda entry: entry[0].start_time)

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
    def _time_to_minutes(self, time_str: str) -> int:
        """Helper to convert 'HH:MM' to total minutes from midnight."""
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes

    def detect_conflicts(self) -> List[str]:
        Detect overlapping pet care tasks and return human-readable warnings.
        This method inspects all scheduled pet tasks owned by this scheduler, orders
        them by start time, and identifies adjacent tasks whose time windows overlap.
        For each detected overlap it produces a warning string indicating the first
        task, its computed end time, and the second task with its scheduled start time.
        Returns:
            List[str]: A list of warning messages. Each message follows the pattern:
                "⚠️ CONFLICT: '<first_task_title>' (<first_pet>) ends at HH:MM, but
                 '<second_task_title>' (<second_pet>) starts at <second_task_start>."
                 (HH:MM is computed from the first task's start time plus its duration;
                 <second_task_start> is presented as stored on the task.)
        Notes:
            - Tasks are presumed to be provided as pairs of (task_object, pet_identifier)
              where task_object has attributes `start_time` (string "HH:MM") and
              `duration_minutes` (int).
            - Overlap detection is performed by converting start times to minutes and
              checking if the next task's start is strictly less than the current task's
              end time.
            - The tasks are sorted before checking; overall complexity is dominated by
              sorting (O(n log n)) with a linear scan for overlap detection.
            - No state is mutated; the method only reads tasks and returns warnings.
        """
        Identifies overlapping tasks. 
        Returns a list of warning strings.

        """
        all_entries = self.owner.get_all_pet_tasks()
        # Sort by time first so we can check neighbors
        sorted_entries = self.sort_tasks_by_time(all_entries)
        
        warnings = []
        
        for i in range(len(sorted_entries) - 1):
            current_task, current_pet = sorted_entries[i]
            next_task, next_pet = sorted_entries[i+1]
            
            # Calculate end time of current task
            start_min = self._time_to_minutes(current_task.start_time)
            end_min = start_min + current_task.duration_minutes
            
            # Get start time of next task
            next_start_min = self._time_to_minutes(next_task.start_time)
            
            # Check for overlap
            if next_start_min < end_min:
                warnings.append(
                    f"⚠️ CONFLICT: '{current_task.title}' ({current_pet}) ends at "
                    f"{end_min//60:02d}:{end_min%60:02d}, but '{next_task.title}' "
                    f"({next_pet}) starts at {next_task.start_time}."
                )
        
        return warnings