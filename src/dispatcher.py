class Dispatcher:
    """
    A legal proceeding dispatcher.

    The dispatcher is based on people and responsibilities.
    Each person can have many responsibilities assigned to him/her.

    The dispatcher reads legal proceedings and assigns them to
    one or more registered people depending on their responsibilities.

    Internally, the dispatcher is powered by a large language model
    (LLM) that links proceedings to people.
    """

    def __init__(self, llm_settings: dict):
        """
        Ingest LLM settings based on which the dispatcher will operate.

        llm_settings = {"llm_model": "llama2-uncensored",
                        "temp": 0.1,
                        "seed": 1}
        """
        self._check_llm_settigns(llm_settings)
        self.llm_settings = llm_settings

        self.people = {}

    def register_person(self, name: str, responsibilities: list[str]):
        self._check_person(name)
        self._check_responsibilities(responsibilities)
        self._register_person(name, responsibilities)

    def _check_person(self, name: str):
        """Check if person has already been registered"""
        if name in self.people:
            ValueError(f"{name} has already been registered!")

    def _check_responsibilities(self, responsibilities: list[str]):
        """Placeholder for future check"""
        pass

    def _register_person(self, name: str, responsibilities: list[str]):
        self.people[name] = responsibilities

    def _check_llm_settigns(self, llm_settings: dict):
        """Check if all LLM settings are present"""
        mandatory_keys = ["llm_model", "temp", "seed"]
        if not all([key in llm_settings.keys() for key in mandatory_keys]):
            raise KeyError(
                f"llm_settings does not contain the minimum set of keys: {mandatory_keys}"
            )
