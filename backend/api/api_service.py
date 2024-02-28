import uuid
from llm.llm_model import LlmModel
from use_cases.general_chatbot import setup_chat, invoke_chat
from langchain_wrapper.lang_wrapper import LangWrapper


class ApiService:
    use_case_sessions: dict
    llm_model: LlmModel

    def __init__(self, model: LlmModel):
        self.use_case_sessions = {}
        self.llm_model = model

    def create_use_case_session(self, **kwargs) -> str:
        print(kwargs)
        lang_wrapper = None
        use_case = kwargs.get("use_case")
        kwargs.pop("use_case", None)
        if use_case == "general_chatbot":
            lang_wrapper = setup_chat(model=self.llm_model, **kwargs)
        elif use_case == "use_case_2":
            pass
        else:
            raise ValueError(f"Invalid use_case: {use_case}")

        self.use_case_sessions[use_case] = lang_wrapper
        return use_case

    def invoke_use_case(self, kwargs):
        use_case = kwargs.get("use_case")
        lang_wrapper = self.use_case_sessions.get(use_case)
        if use_case == "general_chatbot":
            return invoke_chat(lang_wrapper=lang_wrapper, **kwargs)  # type: ignore
        elif use_case == "use_case_2":
            pass
        else:
            raise ValueError(f"Invalid use_case: {use_case}")
