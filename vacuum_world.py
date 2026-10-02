from itertools import product
class VacuumEnvironment:
    """
    Modular vacuum-cleaner environment.

    locations: List of locations in the environment.

    initial_dirt: Dictionary indicating whether each location is dirty.

    start_location: Initial location of the vacuum agent.
    """

    def __init__(self, locations, initial_dirt, start_location):
        self.locations = locations
        self.dirt = initial_dirt.copy()
        self.agent_location = start_location

        self.performance = 0
        self.time = 0
# -------------------------
# SENSOR
# -------------------------
    def perceive(self):

#Returns (current location, current location status

        status = "Dirty" if self.dirt[self.agent_location] else "Clean"

        return self.agent_location, status

# -------------------------
# ACTUATORS
# -------------------------
    def execute_action(self, action):
 
#Changes the environment according to the agent's action
        if action == "Suck":
            self.dirt[self.agent_location] = False

        elif action == "Left":
            index = self.locations.index(self.agent_location)

            if index > 0:
                self.agent_location = self.locations[index - 1]

        elif action == "Right":
            index = self.locations.index(self.agent_location)

            if index < len(self.locations) - 1:
                self.agent_location = self.locations[index + 1]

        elif action == "NoOp":
            pass

        else:
            raise ValueError(f"Unknown action: {action}")
# -------------------------
# PERFORMANCE MEASURE
# -------------------------
    def update_performance(self):
        
    #One point is awarded for each clean square at each time step
       
        clean_locations = sum(
            1 for location in self.locations
            if not self.dirt[location]
        )

        self.performance += clean_locations

    def step(self, agent):
    #Performs one complete simulation step
        

        percept = self.perceive()

        action = agent.program(percept)

        self.execute_action(action)

        self.update_performance()

        self.time += 1

        return percept, action

    def run(self, agent, steps=1000):

    #Runs the environment for a given number of time steps


        for _ in range(steps):
            self.step(agent)

        return self.performance


class SimpleReflexVacuumAgent:
   
    #Simple reflex agent for the  two-location vacuum-cleaner world.
    """
    Dirty -> Suck

    Clean at A -> Right
    Clean at B -> Left
    """

    def program(self, percept):

        location, status = percept

        if status == "Dirty":
            return "Suck"

        elif location == "A":
            return "Right"

        elif location == "B":
            return "Left"

        return "NoOp"


def test_all_configurations():

    locations = ["A", "B"]

    agent_locations = ["A", "B"]

    # False = Clean
    # True  = Dirty
    dirt_configurations = list(
        product([False, True], repeat=2)
    )

    results = []

    print(
        f"{'Start':<8}"
        f"{'A':<8}"
        f"{'B':<8}"
        f"{'Score':<8}"
    )

    print("-" * 32)

    for start_location in agent_locations:

        for dirt_A, dirt_B in dirt_configurations:

            initial_dirt = {
                "A": dirt_A,
                "B": dirt_B
            }

            environment = VacuumEnvironment(
                locations=locations,
                initial_dirt=initial_dirt,
                start_location=start_location
            )

            agent = SimpleReflexVacuumAgent()

            score = environment.run(
                agent,
                steps=1000
            )

            results.append(score)

            print(
                f"{start_location:<8}"
                f"{'Dirty' if dirt_A else 'Clean':<8}"
                f"{'Dirty' if dirt_B else 'Clean':<8}"
                f"{score:<8}"
            )

    average = sum(results) / len(results)

    print("-" * 32)

    print(f"Average performance: {average:.2f}")


if __name__ == "__main__":
    test_all_configurations()
