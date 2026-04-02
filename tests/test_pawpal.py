import pytest
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

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


def test_sorting_chronological_order():
    """Verify sort_tasks_by_time returns tasks in increasing start_time order.
    Steps:
    - Arrange: create three Task instances with shuffled start_time strings.
    - Act: call Scheduler.sort_tasks_by_time on the list of (task, pet_name) tuples.
    - Assert: resulting order matches chronological times.
    """
    # Arrange
    t1 = Task(title="T1", duration_minutes=10, priority="low", start_time="13:00")
    t2 = Task(title="T2", duration_minutes=20, priority="low", start_time="09:00")
    t3 = Task(title="T3", duration_minutes=15, priority="low", start_time="12:30")
    owner = Owner(name="O", available_time=120)
    sched = Scheduler(owner)
    unsorted = [(t1, "P"), (t2, "P"), (t3, "P")]

    # Act
    sorted_entries = sched.sort_tasks_by_time(unsorted)

    # Assert
    times = [entry[0].start_time for entry in sorted_entries]
    assert times == ["09:00", "12:30", "13:00"], f"Expected chronological order, got {times}"


def test_detect_conflict_flags_overlap():
    """Detects overlapping tasks and returns a conflict message.
    Steps:
    - Arrange: create two tasks where the second starts before the first ends.
    - Act: call Scheduler.detect_conflicts.
    - Assert: one warning is returned and contains both task titles.
    """
    # Arrange
    t1 = Task(title="Walk", duration_minutes=60, priority="high", start_time="09:00")
    t2 = Task(title="Feed", duration_minutes=30, priority="medium", start_time="09:30")
    pet1 = Pet(name="A", species="Dog", tasks=[t1])
    pet2 = Pet(name="B", species="Cat", tasks=[t2])
    owner = Owner(name="Owner", available_time=120, pets=[pet1, pet2])
    sched = Scheduler(owner)

    # Act
    warnings = sched.detect_conflicts()

    # Assert
    assert len(warnings) == 1, f"Expected 1 conflict warning, got {len(warnings)}: {warnings}"
    assert "Walk" in warnings[0] and "Feed" in warnings[0], "Warning must mention both task titles"


def test_generate_schedule_without_conflict():
    """Ensure generate_plan schedules available non-overlapping tasks within budget.
    Steps:
    - Arrange: two non-overlapping tasks and enough available_time.
    - Act: call Scheduler.generate_plan (provide a get_value_density on tasks).
    - Assert: both tasks scheduled and total scheduled duration <= available_time.
    """
    # Arrange
    t1 = Task(title="Groom", duration_minutes=30, priority="medium", start_time="08:00")
    t2 = Task(title="Vet", duration_minutes=30, priority="high", start_time="10:00")
    # Provide deterministic density values used by generate_plan
    t1.get_value_density = lambda weights: 5
    t2.get_value_density = lambda weights: 10
    pet = Pet(name="Z", species="Dog", tasks=[t1, t2])
    owner = Owner(name="O", available_time=120, pets=[pet])
    sched = Scheduler(owner)

    # Act
    plan = sched.generate_plan()

    # Assert: both included and fit the budget
    assert len(plan) == 2, f"Expected 2 scheduled tasks, got {len(plan)}"
    total = sum(st.task.duration_minutes for st in plan)
    assert total <= owner.available_time, f"Scheduled {total} minutes which exceeds available {owner.available_time}"


def test_multiple_pets_multiple_tasks_selection():
    """Schedule selection across multiple pets respects available_time and density ordering.
    Steps:
    - Arrange: create several tasks across two pets with controlled densities.
    - Act: call Scheduler.generate_plan.
    - Assert: highest-density task scheduled first and total duration <= available_time.
    """
    # Arrange
    a1 = Task(title="A1", duration_minutes=30, priority="low", start_time="08:00")
    a2 = Task(title="A2", duration_minutes=30, priority="low", start_time="09:00")
    b1 = Task(title="B1", duration_minutes=40, priority="high", start_time="07:00")
    # Densities: make b1 dominant so it's selected first
    a1.get_value_density = lambda w: 1
    a2.get_value_density = lambda w: 1
    b1.get_value_density = lambda w: 100

    petA = Pet(name="A", species="Dog", tasks=[a1, a2])
    petB = Pet(name="B", species="Cat", tasks=[b1])
    owner = Owner(name="Owner", available_time=90, pets=[petA, petB])
    sched = Scheduler(owner)

    # Act
    plan = sched.generate_plan()

    # Assert
    assert len(plan) >= 1, "Expected at least one task scheduled"
    assert plan[0].pet_name == "B", f"Expected highest-density task from pet B first, got {plan[0].pet_name}"
    total = sum(st.task.duration_minutes for st in plan)
    assert total <= owner.available_time, "Total scheduled time exceeds owner's available time"


def test_recurring_task_completion_creates_next_day():
    """Marking a daily task complete produces a new task dated +1 day.
    Steps:
    - Arrange: pet with a Daily Task with a known due_date.
    - Act: call Pet.complete_task_by_id.
    - Assert: pet still has a task with due_date advanced by one day and is not completed.
    """
    # Arrange
    base_date = datetime(2026, 4, 1)
    t = Task(title="DailyWalk", duration_minutes=20, priority="high", start_time="07:00", due_date=base_date, frequency="Daily")
    pet = Pet(name="Solo", species="Dog", tasks=[t])

    # Act
    ok = pet.complete_task_by_id(t.task_id)

    # Assert
    assert ok is True, "complete_task_by_id should return True when it finds and completes the task"
    assert len(pet.tasks) == 1, "Recurring task should be replaced by its next occurrence"
    next_task = pet.tasks[0]
    assert next_task.is_completed is False, "New recurrence must not be marked completed"
    assert next_task.due_date.date() == (base_date + timedelta(days=1)).date(), "Next occurrence date incorrect"


def test_one_pet_multiple_tasks_order_and_no_conflict():
    """Single pet with multiple tasks: chronological ordering and no conflicts when spaced.
    Steps:
    - Arrange: create one pet with tasks spaced to avoid overlap.
    - Act: sort and detect conflicts.
    - Assert: sorted order is chronological and detect_conflicts returns empty list.
    """
    t1 = Task(title="M1", duration_minutes=30, priority="low", start_time="08:00")
    t2 = Task(title="M2", duration_minutes=30, priority="low", start_time="09:00")
    pet = Pet(name="Only", species="Bird", tasks=[t2, t1])
    owner = Owner(name="Owner", available_time=120, pets=[pet])
    sched = Scheduler(owner)

    # Act
    sorted_entries = sched.sort_tasks_by_time(owner.get_all_pet_tasks())
    warnings = sched.detect_conflicts()

    # Assert
    times = [e[0].start_time for e in sorted_entries]
    assert times == ["08:00", "09:00"], f"Tasks not ordered chronologically: {times}"
    assert warnings == [], f"Expected no conflicts, but got: {warnings}"