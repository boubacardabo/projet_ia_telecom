import uuid
from llm.llm_model import LlmModel


class ApiService:
    use_case_sessions: dict
    llm_model: LlmModel

    def __init__(self, model: LlmModel):
        self.use_case_sessions = {}
        self.llm_model = model

    def create_session(self, use_case, **kwargs) -> str:
        lang_wrapper = None
        if use_case == "general_chatbot":
            pass
        elif use_case == "use_case_2":
            pass
        else:
            raise ValueError(f"Invalid use_case: {use_case}")

        session_id = str(uuid.uuid4())  # Generate a random UUID
        self.use_case_sessions[session_id] = lang_wrapper
        return session_id

    def get_session_(self, session_id: str):
        return self.use_case_sessions.get(session_id)
