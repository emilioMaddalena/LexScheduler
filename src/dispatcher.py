from typing import Dict, List, Optional


class Dispatcher:
    """A legal proceeding dispatcher.

    The dispatcher is based on people and responsibilities.
    Each person can have many responsibilities assigned to him/her.
    All this info is stored in a roster.

    The dispatcher reads legal proceedings and assigns them to
    one or more registered people depending on their responsibilities.

    Internally, the dispatcher is powered by a large language model
    (LLM) that links proceedings to people.
    """

    def __init__(self, roster: Optional[Dict[str, List[str]]] = None):
        """Initialize the dispatcher."""
        self._llm_configured = False
        self.roster = {}
        # If already given, register all people
        if roster:
            for person, responsibilities in roster.items():
                self.register_person(person, responsibilities)

    def initialize_llm(self, llm_settings):
        """Set up the LLM based on the settings."""
        self._check_llm_settigns(llm_settings)
        #! TODO Initialize the LLM
        self._llm_configured = True
        pass

    def dispatch_proceeding(self, proceeding: str):
        """Dispatch a proceeding to the right person based on the LLM."""
        if not self._llm_configured:
            raise ValueError("LLM has not been configured yet!")
        pass

    def register_person(self, name: str, responsibilities: list[str]): 
        """_summary_."""
        self._check_person(name)
        self._check_responsibilities(responsibilities)
        self._register_person(name, responsibilities)

    def _check_person(self, name: str):
        """Check if person has already been registered."""
        if name in self.roster:
            ValueError(f"{name} has already been registered!")

    def _check_responsibilities(self, responsibilities: list[str]):
        """Check if the responsibilities are valid."""
        pass

    def _register_person(self, name: str, responsibilities: list[str]):
        self.roster[name] = responsibilities

    def _check_llm_settigns(self, llm_settings: dict):
        """Check if all LLM settings are present."""
        accepted_keys = ["llm_model", "temp", "seed"]
        if not (set(llm_settings.keys()) == set(accepted_keys)):
            raise KeyError(
                f"llm_settings does not contain the keys needed: {accepted_keys}"
            )
        
    @property
    def num_of_people(self):
        """Return the number of people in the roster."""
        return len(self.roster)
    
    @property
    def has_empty_roster(self):
        """Check if the roster is empty."""
        return False if self.num_of_people > 0 else True