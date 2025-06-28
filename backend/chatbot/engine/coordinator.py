from chatbot.engine.agents.scenario_agent import ScenarioAgent

def main():
    scenario_agent = ScenarioAgent()
    scenario_context = scenario_agent.run()
    print(scenario_context)

if __name__ == "__main__":
    main()