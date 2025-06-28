from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class ScenarioAgent:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2")
        self.scenario = {
            "type": None,
            "language": None,
            "location": None,
            "user_role": None,
            "details": None
        }

    def classify_scenario_type(self, user_input: str):
        classification_prompt = ChatPromptTemplate.from_template("""
        You are a classification agent for immigration scenarios.

        Given the user's input, classify the situation into one of the following types:
        - "ICE Home Visit"
        - "ICE Street Encounter"
        - "ICE Workplace Raid"
        - "Border Stop"
        - "Other"

        Only respond with the exact type.

        User Input:
        {input}
        """)
        result = (classification_prompt | self.llm).invoke({"input": user_input})
        self.scenario["type"] = result.strip().replace('"', '')
        self.scenario["details"] = user_input
        print(f"🧭 Scenario type identified: {self.scenario['type']}")

    def ask_followup(self):
        followup_prompt = ChatPromptTemplate.from_template("""
        You are helping clarify an immigration-related scenario for a legal AI assistant.

        Current scenario type: {type}
        Details provided so far: {details}

        Ask the user any follow-up questions necessary to understand the context more clearly.
        Return your question as a single clear line.
        """)
        while not all([self.scenario.get("location"), self.scenario.get("user_role")]):
            question = (followup_prompt | self.llm).invoke({
                "type": self.scenario["type"],
                "details": self.scenario["details"]
            }).strip()
            print(f"🤖 {question}")
            user_response = input("👤 ")
            # Basic keyword detection for simplicity
            if "home" in user_response.lower():
                self.scenario["location"] = "home"
            elif "work" in user_response.lower():
                self.scenario["location"] = "work"
            elif "street" in user_response.lower():
                self.scenario["location"] = "street"
            if any(role in user_response.lower() for role in ["employee", "witness", "bystander", "resident"]):
                self.scenario["user_role"] = user_response

    def run(self):
        print("🗣️ Please describe your immigration situation briefly:")
        user_input = input("👤 ")
        self.classify_scenario_type(user_input)
        self.ask_followup()
        return self.scenario
