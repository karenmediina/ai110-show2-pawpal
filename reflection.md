# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

From the instructions on the portal, 3 core actions I identified my scheduler shoudl perform are for the owner to add or remove a pet, to give the owner ability to change their priorities/preferences and to generate a daily schedule based on this potentially udpated information. I created 4 classes for this project: owner, pet, task and scheduler. The class owner has attributes like name, daily_available_time and priority weights with which is a dictionary that maps tasks to ints. Their responsabilities include adding a pet, removing a pet and updating their preferences. I also added a class 'pet' which has a name, species and tasks list as attributes. This class can either add or delete a task. The task class has attributes: title, duration (in minutes), a priority assigned to it and a boolean indicated if it was completed or not. Additionally, there is a get_score function that will allow the owner to reprioritize if necessary, based on other constraints like their energy levels and time avaiable. My UML diagram mapped with mermaid is here: ![UML pawpal diagram](image.png)


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---
As I began to implement, Copilot and I noticed that it would be better for tasks to have unique ID's that way a walk for one pet would not be confused for a walk for another pet. Additionally, in order to include both the optimal task and the reason we chose it, I created a result object that includes both the start time and reason. In the first revsion, I included a scoring ration where the value of the score is the given weight over the num of minutes the the task takes. 

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---
a. My scheduler manages tasks by balancing a hard time budget against weighted priority levels (high, medium, and low) for each pet. I prioritized these specific constraints because, for a busy owner, the most valuable schedule is one that fits the most important chores into a strictly limited window of free time.

b. One of the trade offs my implementation has is that it just warns you but doesn't automatically solve a problem when there is task conflict. I think it's reasonable because the owner should still have agency about what happens with their pets, based on their own priorities and preferences, instead of the model deciding for them, in case of conflicts.

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
