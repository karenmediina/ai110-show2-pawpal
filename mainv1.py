from pawpal_system import Owner, Pet, Task, Scheduler

def run_demo():
    # 1. Setup Owner & Pets
    me = Owner(name="Jordan", available_time=60)
    mochi = Pet(name="Mochi", species="Dog")
    kiki = Pet(name="Kiki", species="Cat")

    # 2. Add Tasks across different pets
    # Mochi's tasks
    mochi.add_task(Task(title="Park Run", duration_minutes=30, priority="high"))
    mochi.add_task(Task(title="Brush Fur", duration_minutes=20, priority="low"))
    
    # Kiki's tasks
    kiki.add_task(Task(title="Feed Meds", duration_minutes=5, priority="high"))
    kiki.add_task(Task(title="Laser Play", duration_minutes=15, priority="medium"))

    me.pets.extend([mochi, kiki])

    # 3. Generate the Plan
    engine = Scheduler(me)
    plan = engine.generate_plan()

    # 4. Formatted Output (Avoiding the 'messy list' problem)
    print(f"PAWPAL+ DAILY PLAN FOR {me.name.upper()} 🐾")
    print(f"Time Budget: {me.available_time} mins\n")

    if not plan:
        print("No tasks fit in your schedule today!")
    else:
        for entry in plan:
            # Using f-string padding to keep columns aligned
            time_label = f"[{entry.start_minute} min]"
            task_info = f"{entry.pet_name}: {entry.task.title}"
            print(f"{time_label:<10} {task_info:<25} ({entry.task.duration_minutes}m)")
            print(f"Reason: {entry.reason}\n")
    
    print(f"{'='*40}")

if __name__ == "__main__":
    run_demo()