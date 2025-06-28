from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import json
import re

class ScenarioAgent:
    SCENARIO_TEMPLATES = {
        "ICE Home Visit": {
            "had_warrant": None,
            "door_opened": None,
            "consent_given": None
        },
        "Border Stop": {
            "port_of_entry": None,
            "visa_type": None,
            "entry_purpose": None
        },
        "ICE Workplace Raid": {
            "employer_present": None,
            "detained_count": None,
            "coerced_signing": None
        }
    }

    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2")
        self.scenario = {
            "type": None,  # Classified scenario type (e.g., "ICE Street Encounter")
            "description": None,  # Original user description

            "metadata": {
                "location": None,
                "time_of_day": None,
                "duration": None
            },

            "user_context": {
                "status": None,
                "user_activity": None,
                "user_emotional_state": None,
                "language_used": None,
                "accompanied": None,
                "user_role": None
            },

            "interaction": {
                "id_requested": None,
                "id_provided": None,
                "documents_present": None,
                "trigger_reason": None,
                "officer_behavior": None,
                "escalation": None
            },

            "legal_concerns": None,  # Freeform issues or flagged rights violations

            "confidence_scores": {
                "status": None,
                "id_provided": None,
                "trigger_reason": None
            },

            "custom_fields": {}  # Dynamically populated based on scenario type
        }
        self.history = []

    def classify_scenario_type(self, user_input: str):
        # Classification prompt
        classification_prompt = ChatPromptTemplate.from_template("""
        You are a classification agent for immigration scenarios.

        Given the user's input, classify the situation into one of the following types:
        - "ICE Home Visit"
        - "ICE Street Encounter"
        - "ICE Workplace Raid"
        - "Border Stop"
        - "Other"

        Only respond with the exact type.

        Input:
        {input}
    """)
        result = (classification_prompt | self.llm).invoke({"input": user_input})

        # Store scenario type
        self.scenario["type"] = result.strip().replace('"', '')
        # Inject custom fields based on scenario type
        self._inject_custom_fields()

        self.scenario["description"] = user_input
        print(f"🧭 Scenario type identified: {self.scenario['type']}")

    def _inject_custom_fields(self):
        scenario_type = self.scenario.get("type")
        if scenario_type in self.SCENARIO_TEMPLATES:
            self.scenario["custom_fields"] = self.SCENARIO_TEMPLATES[scenario_type].copy()


    def ask_followup(self):
        print("🤖 Thanks. I’ll now ask a few follow-up questions to better understand your situation.\n")

        while True:
            # Check if all fields are filled
            missing_fields = self._get_missing_fields()
            if not missing_fields:
                break

            # Generate the next follow-up question
            followup_prompt = ChatPromptTemplate.from_template("""
            You are a legal assistant agent helping to gather missing scenario details.

            This is a summary of the current user scenario (missing fields are marked as null):
            {scenario}

            Here is a history of what’s been asked and how the user responded:
            {history}

            Choose **one** of the missing fields to ask about. Prioritize relevance and clarity.
            Avoid repetition, and respect the user's apparent role (e.g., witness, target).

            Format:
            Question: <your question>
            Target Field: <flattened.key>
            """)

            result = (followup_prompt | self.llm).invoke({
                "scenario": json.dumps(self.scenario, indent=2),
                "history": "\n".join([f"Q: {q}\nA: {a}" for q, a in self.history])
            })


            # Parse result with regex for safety
            question_match = re.search(r"Question:\s*(.*)", result, re.IGNORECASE)
            field_match = re.search(r"Target Field:\s*([\w\.]+)", result, re.IGNORECASE)

            if question_match and field_match:
                question = question_match.group(1).strip()
                target_field = field_match.group(1).strip()
            else:
                print("⚠️ Could not parse question. Ending.")
                break


            if not question or not target_field:
                print("⚠️ Could not parse question. Ending.")
                break

            print(f"🤖 {question}")
            response = input("👤 ").strip()
            self.history.append((question, response))

            self._assign_response_to_field(target_field, response)


    def confirm_summary(self):
        print("\n✅ Thanks. Here's what I understand about your situation:\n")
        print(json.dumps(self.scenario, indent=2))
        print("\nLet me know if anything here is incorrect or needs adjusting.\n")

    def _get_missing_fields(self):
        flat = self._flatten_scenario(self.scenario)
        return [k for k, v in flat.items() if v is None]

    def _assign_response_to_field(self, field, response):
        vague_responses = ["i don't know", "not sure", "maybe", "idk", "n/a", "no idea"]
        if response.lower() in vague_responses:
            return  # Don't fill field with non-answers

        keys = field.split(".")
        ref = self.scenario
        for k in keys[:-1]:
            if k not in ref or not isinstance(ref[k], dict):
                ref[k] = {}
            ref = ref[k]
        ref[keys[-1]] = response


    def _flatten_scenario(self, d, parent_key='', sep='.'):
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                if not v:
                    items[new_key] = {}  # preserve empty dicts
                else:
                    items.update(self._flatten_scenario(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items


    def run(self):
        print("🗣️ Please describe your immigration situation briefly:")
        user_input = input("👤 ")
        self.classify_scenario_type(user_input)
        self.ask_followup()
        self.confirm_summary()
        return self.scenario
