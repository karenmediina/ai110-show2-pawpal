from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    # 1. Create the Owner (60 min available)
    me = Owner(name="Jordan", available_time=60)

    # 2. Create at least two Pets
    mochi = Pet(name="Mochi", species="Dog")
    kiki = Pet(name="Kiki", species="Cat")

    # 3. Add tasks with DIFFERENT times to the pets
    # Mochi's tasks (3 tasks)
    mochi.add_task(Task(title="Park Walk", duration_minutes=30, priority="high"))
    mochi.add_task(Task(title="Quick Brush", duration_minutes=10, priority="low"))
    mochi.add_task(Task(title="Potty Break", duration_minutes=5, priority="high"))

    # Kiki's tasks (2 tasks)
    kiki.add_task(Task(title="Feed Meds", duration_minutes=2, priority="high"))
    kiki.add_task(Task(title="Laser Play", duration_minutes=15, priority="medium"))


    # Register pets to the owner
    me.add_pet(mochi)
    me.add_pet(kiki)

    # 4. Generate the Plan
    engine = Scheduler(me)
    plan = engine.generate_plan()

    # 5. Format the output for readability (avoiding the 'messy list' look)
    print("\n" + "="*50)
    print(f" 🐾 {me.name.upper()}'S PAWPAL+ DAILY CARE PLAN 🐾 ")
    print("="*50)
    print(f"Available Time: {me.available_time} minutes\n")

    if not plan:
        print("No tasks could be scheduled within the time limit.")
    else:
        for entry in plan:
            # Format: [Time] Pet: Task (Duration)
            header = f"[{entry.start_minute:2} min] {entry.pet_name}: {entry.task.title}"
            print(f"{header:<35} ({entry.task.duration_minutes} min)")
            print(f"   ↳ {entry.reason}\n")

    print("="*50)

from pawpal_system import Owner, Pet, Task, Scheduler

def run_algo_test():
    # 1. Setup
    me = Owner("Jordan", 120)
    mochi = Pet("Mochi", "Dog")
    me.add_pet(mochi)
    
    # 2. Add tasks OUT OF ORDER
    # We add 6:00 PM first, then 8:00 AM
    mochi.add_task(Task("Evening Walk", 30, "medium", "18:00"))
    mochi.add_task(Task("Breakfast", 15, "high", "08:00"))
    mochi.add_task(Task("Nap Time", 60, "low", "13:00"))
    
    engine = Scheduler(me)

    # 3. Test Filtering (Get only incomplete tasks)
    print("--- Filtering Test ---")
    incomplete = me.filter_tasks(is_completed=False)
    print(f"Total incomplete tasks: {len(incomplete)}")

    # 4. Test Sorting (The 'Lambda' Magic)
    print("\n--- Sorting Test (Chronological) ---")
    chronological_plan = engine.sort_tasks_by_time(incomplete)
    
    for task, pet_name in chronological_plan:
        print(f"[{task.start_time}] {pet_name}: {task.title}")

def test_conflict_detection():
    """
    Test for conflict detection in the scheduling engine.
    Purpose:
    - Verify that Scheduler.detect_conflicts() identifies overlapping tasks across different pets.
    Setup:
    - Create an Owner instance (e.g., "Jordan") and two Pet instances ("Mochi" the Dog and "Kiki" the Cat).
    - Add a 60-minute high-priority task "Long Walk" for Mochi starting at "09:00" (ends at 10:00).
    - Add a 15-minute medium-priority task "Breakfast" for Kiki starting at "09:30" (overlaps with Mochi's walk).
    - Register both pets with the owner and instantiate a Scheduler for that owner.
    Action:
    - Invoke engine.detect_conflicts(), which should parse "HH:MM" start times, apply durations in minutes to compute end times, and detect temporal overlaps between tasks across pets.
    Expected outcome:
    - detect_conflicts() returns a non-empty list of conflict warning messages describing the overlapping tasks.
    - The test prints any detected conflict messages (or "No conflicts detected." if none).
    - The final assertion asserts that at least one conflict was found, confirming the conflict warning system functions as intended.
    Assumptions:
    - Task start times use "HH:MM" format and durations are in minutes.
    - Conflict detection is based on overlapping time intervals (inclusive/exclusive behavior determined by the Scheduler implementation).
    """
    print("\n--- Conflict Detection Test ---")
    me = Owner("Jordan", 120)
    mochi = Pet("Mochi", "Dog")
    kiki = Pet("Kiki", "Cat")
    
    # Mochi's walk is 60 mins starting at 09:00 (ends at 10:00)
    mochi.add_task(Task("Long Walk", 60, "high", "09:00"))
    
    # Kiki's breakfast starts at 09:30 (OOPS! Conflict!)
    kiki.add_task(Task("Breakfast", 15, "medium", "09:30"))
    
    me.add_pet(mochi)
    me.add_pet(kiki)
    
    engine = Scheduler(me)
    conflicts = engine.detect_conflicts()
    
    if conflicts:
        for msg in conflicts:
            print(msg)
    else:
        print("No conflicts detected.")

    assert len(conflicts) > 0
    print("Conflict warning system verified!")


if __name__ == "__main__":
    run_demo()
    run_algo_test()
    test_conflict_detection()