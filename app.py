import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- SESSION STATE (The App's Memory) ---
if "owner" not in st.session_state:
    # Initial setup for Sofia's demo
    initial_owner = Owner(name="Jordan", available_time=60)
    st.session_state.owner = initial_owner

owner = st.session_state.owner
engine = Scheduler(owner)

st.title("🐾 PawPal+")

# --- SIDEBAR: PROFILE & PETS ---
with st.sidebar:
    st.header("👤 Profile")
    owner.name = st.text_input("Owner Name", value=owner.name)
    owner.available_time = st.number_input("Time Budget (mins)", min_value=0, value=owner.available_time)
    
    st.divider()
    st.subheader("🐱 Manage Pets")
    with st.form("add_pet_form", clear_on_submit=True):
        new_name = st.text_input("Pet Name")
        new_species = st.selectbox("Species", ["Dog", "Cat", "Bird", "Other"])
        if st.form_submit_button("Add Pet"):
            if new_name:
                owner.add_pet(Pet(name=new_name, species=new_species))
                st.rerun()

# --- CONFLICT DETECTION (New "Smart" Feature) ---
# We run this at the top so the user sees warnings immediately
conflicts = engine.detect_conflicts()
if conflicts:
    for warning in conflicts:
        st.warning(warning)

# --- TASK INPUT SECTION ---
st.subheader("📋 Add a Care Task")
if not owner.pets:
    st.info("Add a pet in the sidebar to start scheduling!")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet = st.selectbox("Assign to:", pet_names)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        t_title = st.text_input("Task Title", value="Feeding")
    with col2:
        t_time = st.text_input("Start Time (HH:MM)", value="09:00")
    with col3:
        t_dur = st.number_input("Mins", min_value=1, value=15)
    
    t_freq = st.radio("Frequency", ["Once", "Daily", "Weekly"], horizontal=True)
    t_prio = st.select_slider("Priority", options=["low", "medium", "high"])

    if st.button("➕ Add Task"):
        target_pet = next(p for p in owner.pets if p.name == selected_pet)
        new_task = Task(
            title=t_title, 
            duration_minutes=int(t_dur), 
            priority=t_prio, 
            start_time=t_time,
            frequency=t_freq
        )
        target_pet.add_task(new_task)
        st.toast(f"✅ Added {t_title} for {selected_pet}!")
        st.rerun()

st.divider()

# --- THE SMART SCHEDULE (Reflecting the Algorithmic Layer) ---
st.subheader("🗓️ Master Timeline")
all_entries = owner.get_all_pet_tasks()

if all_entries:
    # Use your Scheduler's sorting logic!
    sorted_entries = engine.sort_tasks_by_time(all_entries)
    
    for task, pet_name in sorted_entries:
        col_check, col_text = st.columns([1, 9])
        
        # Checkbox to trigger the "Recursive Spawning" logic
        if col_check.checkbox("Done", key=task.task_id):
            target_pet = next(p for p in owner.pets if p.name == pet_name)
            target_pet.complete_task_by_id(task.task_id)
            st.success(f"Great job! {task.title} is complete.")
            st.rerun()
            
        with col_text.expander(f"**{task.start_time}** — {task.title} ({pet_name})"):
            st.write(f"**Priority:** {task.priority.upper()} | **Duration:** {task.duration_minutes}m")
            if task.frequency != "Once":
                st.caption(f"🔁 Recurring: {task.frequency}")
else:
    st.info("Your schedule is empty. Add a task above!")