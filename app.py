import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- STEP 2: MANAGE APPLICATION "MEMORY" (SESSION STATE) ---
# This ensures our Owner and Pet objects persist across reruns
if "owner" not in st.session_state:
    # Create the initial owner and a default pet
    initial_owner = Owner(name="Jordan", available_time=60)
    initial_owner.add_pet(Pet(name="Mochi", species="dog"))
    
    # Store the object in the session state "vault"
    st.session_state.owner = initial_owner

# Local reference to the persistent owner object
owner = st.session_state.owner

st.title("PawPal")

# --- SIDEBAR: OWNER & PET MANAGEMENT ---
with st.sidebar:
    st.header("👤 Profile & Settings")
    owner.name = st.text_input("Owner Name", value=owner.name)
    owner.available_time = st.number_input("Time Budget (mins)", min_value=0, value=owner.available_time)
    
    st.divider()
    st.subheader("🐾 Manage Pets")
    
    # NEW: Form to add a new Pet object
    with st.form("add_pet_form", clear_on_submit=True):
        new_pet_name = st.text_input("Pet Name")
        new_pet_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        if st.form_submit_button("Add Pet"):
            if new_pet_name:
                # 1. Create the Pet object
                new_pet = Pet(name=new_pet_name, species=new_pet_species)
                # 2. Call the Owner method you wrote in Phase 2
                owner.add_pet(new_pet)
                st.success(f"Added {new_pet_name}!")
            else:
                st.error("Please enter a name.")

    # Display the current list of live Pet objects
    st.write("---")
    for pet in owner.pets:
        st.write(f"• **{pet.name}** ({pet.species})")

# --- TASK INPUT SECTION ---
st.subheader("📋 Add Care Tasks")

# Create a list of pet names for the dropdown
pet_options = [p.name for p in owner.pets]
selected_pet_name = st.selectbox("Assign to Pet:", pet_options)

col1, col2 = st.columns([2, 1])
with col1:
    t_title = st.text_input("Task title", value="Feeding")
with col2:
    t_duration = st.number_input("Mins", min_value=1, value=15)

t_priority = st.select_slider("Priority", options=["low", "medium", "high"])

if st.button("Add Task"):
    # Find the actual Pet object by name
    target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
    
    # Create and add the Task
    new_task = Task(title=t_title, duration_minutes=int(t_duration), priority=t_priority)
    target_pet.add_task(new_task)
    st.toast(f"✅ Assigned to {target_pet.name}!")

# --- DISPLAY CURRENT TASKS (Generalized for all pets) ---
all_tasks_exist = any(len(p.tasks) > 0 for p in owner.pets)

if all_tasks_exist:
    st.markdown("### All Pending Tasks")
    all_table_data = []
    for pet in owner.pets:
        for t in pet.tasks:
            all_table_data.append({
                "Pet": pet.name,
                "Task": t.title, 
                "Duration": f"{t.duration_minutes}m", 
                "Priority": t.priority
            })
    st.table(all_table_data)
else:
    st.info("No tasks added yet. Use the form above to start.")

# --- STEP 3: THE SCHEDULER BRIDGE ---
st.subheader("Optimized Schedule")
if st.button("Generate Schedule"):
    # Pass the owner object (and all their pets/tasks) into the Scheduler
    engine = Scheduler(owner)
    plan = engine.generate_plan()
    
    if not plan:
        st.warning("No tasks fit in your current time budget. Try adding more time in the sidebar!")
    else:
        st.success(f"Schedule generated for {owner.name}!")
        for entry in plan:
            # Display each scheduled task in a clean expander
            with st.expander(f"{entry.start_minute}m - {entry.task.title} ({entry.pet_name})"):
                st.write(f"**Duration:** {entry.task.duration_minutes} minutes")
                st.info(f"**Optimization Reason:** {entry.reason}")