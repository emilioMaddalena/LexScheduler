from typing import Dict, List, Optional

from .llm import Llm


class Dispatcher:
    """A legal proceeding dispatcher.

    The dispatcher is based on people and responsibilities.
    Each person can have many responsibilities assigned to him/her.
    All this info is stored in a roster.

    An example of a roster might be:
    self.roster = {
        "jane doe": ["cooking carbonara", "being cool"],
        "mickey mouse": ["writing code"],
        "your cousin": ["skating", "making money"],
    }
    No two people can share the same responsibility.

    The dispatcher reads legal proceedings and assigns them to
    one or more registered people depending on their responsibilities.

    Internally, the dispatcher is powered by a large language model
    (LLM) that links proceedings to people.
    """

    def __init__(self, roster: Optional[Dict[str, List[str]]] = None):
        """Initialize the dispatcher."""
        self.llm = None
        self.roster = {}
        # If already given, register all people
        if roster:
            for person, responsibilities in roster.items():
                self.register_person(person, responsibilities)

    def initialize_llm(self, model_name: str):
        """Instantiate an LLM.

        Args:
            model_name (str): The name of the LLM model to use.

        Raises:
            ValueError: If the LLM initialization fails.
        """
        system_message = (
            "You must answer as a machine."
            "Classify the task below in exactly one of the following categories: "
            f"{', '.join(self.all_responsibilities)}"
        )
        try:
            self.llm = Llm(model_name=model_name, system_message=system_message)
        except Exception as e:
            raise ValueError(f"Failed to initialize LLM: {e}")

    def dispatch_proceeding(self, proceeding: str):
        """Return the person responsible for a proceeding task."""
        if not self.llm:
            raise ValueError("LLM has not been initialized yet!")
        llm_reply = self.llm.chat_http(f"Task: {proceeding}")
        responsibility = self._identify_responsibility(llm_reply)
        person = self._identify_person(responsibility)
        return person

    def _identify_responsibility(self, llm_reply: str) -> str:
        """Identify if exactly one and no other of the responsibilities are present."""
        found_responsibilities = [res for res in self.all_responsibilities if res in llm_reply]
        if len(found_responsibilities) != 1:
            raise ValueError(
                f"Could not identify exactly one responsibility in the reply: {llm_reply}"
            )
        return found_responsibilities[0]

    def _identify_person(self, responsibility: str) -> str:
        """Find which one person from the roster has the responsibility."""
        person = next((p for p, r in self.roster.items() if responsibility in r), None)
        if not person:
            raise ValueError(f"No person found for responsibility: {responsibility}")
        return person

    def register_person(self, name: str, responsibilities: list[str]):
        """Register a new person and a new set of responsibilities."""
        self._validate_person(name)
        self._valdiate_responsibilities(responsibilities)
        self._register_person(name, responsibilities)

    def _validate_person(self, name: str):
        """Check if person has already been registered."""
        if name in self.roster:
            raise ValueError(f"{name} has already been registered!")

    def _valdiate_responsibilities(self, responsibilities: list[str]):
        """Check if the responsibilities have already been registered."""
        already_registered = [res for sublist in self.roster.values() for res in sublist]
        for res in responsibilities:
            if res in already_registered:
                raise ValueError(f"{res} was already registered as a responsibility.")

    def _register_person(self, name: str, responsibilities: list[str]):
        self.roster[name] = responsibilities

    @property
    def num_of_people(self) -> int:
        """Return the number of people in the roster."""
        return len(self.roster)

    @property
    def has_empty_roster(self) -> bool:
        """Check if the roster is empty."""
        return False if self.num_of_people > 0 else True

    @property
    def all_responsibilities(self) -> List:
        """Return all responsibilities all people have."""
        return [res for sublist in self.roster.values() for res in sublist]
