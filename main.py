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
        print("⚠️ No tasks could be scheduled within the time limit.")
    else:
        for entry in plan:
            # Format: [Time] Pet: Task (Duration)
            header = f"[{entry.start_minute:2} min] {entry.pet_name}: {entry.task.title}"
            print(f"{header:<35} ({entry.task.duration_minutes} min)")
            print(f"   ↳ {entry.reason}\n")

    print("="*50)

if __name__ == "__main__":
    run_demo()