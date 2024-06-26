from llm.llm_model import LlmModel
from use_cases.general_chatbot import setup_chat, invoke_chat
from use_cases.codewriter_system_test import setup_agent, invoke_agent


class ApiService:
    use_case_sessions: dict
    llm_model: LlmModel

    def __init__(self, model: LlmModel):
        self.use_case_sessions = {}
        self.llm_model = model

    def create_use_case_session(self, **kwargs):
        try:
            use_case_object = None
            use_case = kwargs.get("use_case")
            kwargs.pop("use_case", None)
            if use_case == "general_chatbot":
                use_case_object = setup_chat(model=self.llm_model, **kwargs)
            elif use_case == "codewriter_system_test":
                use_case_object = setup_agent(model=self.llm_model, **kwargs)

            else:
                raise ValueError(f"Invalid use_case: {use_case}")

            self.use_case_sessions[use_case] = use_case_object
            return use_case
        except Exception as e:
            return e

    def invoke_use_case(self, **kwargs):
        try:
            use_case = kwargs.get("use_case")
            use_case_object = self.use_case_sessions.get(use_case)
            kwargs.pop("use_case", None)

            if use_case == "general_chatbot":
                return invoke_chat(lang_wrapper=use_case_object, **kwargs)  # type: ignore

            elif use_case == "codewriter_system_test":
                return invoke_agent(agent_executor=use_case_object, **kwargs)  # type: ignore

            else:
                raise ValueError(f"Invalid use_case: {use_case}")
        except Exception as e:
            return e
