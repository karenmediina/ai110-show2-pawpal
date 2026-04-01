import pytest
from pawpal_system import Task, Pet

def test_task_completion():
    """Initialize a Task with title, duration_minutes, priority, and default not-completed status."""
    """Return True if the task is completed, otherwise False."""
    """Mark the task as completed."""
    # Arrange: Create a task that is initially not completed
    task = Task(title="Afternoon Nap", duration_minutes=30, priority="low")
    assert task.is_completed is False
    
    # Act: Call the completion method
    task.mark_complete()
    
    # Assert: Verify the status has flipped to True
    assert task.is_completed is True

def test_task_addition():
    """Verify adding a Task to a Pet increases the Pet's task count by one and that the added Task is appended.
    Arrange: create a Pet instance and a Task instance.
    Act: record the initial task list length, add the Task to the Pet.
    Assert: the length of pet.tasks equals initial length + 1 and the last task's title matches the added Task's title.
    Requirement: Verify adding a task to a Pet increases the count.
"""
    # Arrange: Create a pet and a new task
    my_pet = Pet(name="Kiki", species="Cat")
    task = Task(title="Lunch Time", duration_minutes=10, priority="high")
    
    # Act: Check the count before and after adding
    initial_count = len(my_pet.tasks)
    my_pet.add_task(task)
    
    # Assert: The count should increase by exactly 1
    assert len(my_pet.tasks) == initial_count + 1
    # Extra check: Ensure the last task in the list is the one we added
    assert my_pet.tasks[-1].title == "Lunch Time"