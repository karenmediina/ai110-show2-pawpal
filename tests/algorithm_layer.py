# In main.py
from pawpal_system import Owner, Pet, Task, Scheduler

def test_sorting_filtering():
    me = Owner("Jordan", 120)
    mochi = Pet("Mochi", "Dog")
    
    # Adding tasks OUT OF ORDER
    mochi.add_task(Task("Evening Walk", 30, "medium", "18:00"))
    mochi.add_task(Task("Breakfast", 10, "high", "08:00"))
    mochi.add_task(Task("Nap", 60, "low", "14:00"))
    
    me.add_pet(mochi)
    engine = Scheduler(me)

    # 1. Test Filtering (Get only Mochi's tasks)
    mochi_tasks = me.filter_tasks(pet_name="Mochi")
    print(f"Filtered Tasks for Mochi: {len(mochi_tasks)}")

    # 2. Test Sorting
    sorted_tasks = engine.sort_tasks_by_time(mochi_tasks)
    
    print("\n--- Chronological Schedule ---")
    for t, p in sorted_tasks:
        print(f"{t.start_time} | {p}: {t.title}")

def test_full_recursion_cycle():
    print("\n--- Testing Task Recursion Cycle ---")
    
    # Create a task for 'Today'
    today = datetime.now()
    task = Task("Brush Teeth", 5, "high", "08:00", due_date=today, frequency="Daily")
    
    # Act: Complete the task
    successor = task.mark_complete()
    
    # Assert
    assert task.is_completed is True
    assert successor.is_completed is False # Successor must be pending
    assert successor.due_date.day == (today + timedelta(days=1)).day
    
    print(f"✅ Old Task ({today.strftime('%x')}) -> Done")
    print(f"✅ New Task ({successor.due_date.strftime('%x')}) -> Created & Pending")

if __name__ == "__main__":
    test_sorting_filtering()
    test_full_recursion_cycle()