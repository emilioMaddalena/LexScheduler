import pytest

from src.dispatcher import Dispatcher


@pytest.fixture(scope="module")
def base_dispatcher():  # noqa: D103
    base_roster = {
        "marco polo": ["cooking carbonara", "discovering america"],
        "jane doe": ["watching netflix", "saying hi"],
    }
    return Dispatcher(roster=base_roster)


@pytest.mark.parametrize("new_person", ["mikey mouse", "tiririca"])
def test_validate_person_valid(base_dispatcher, new_person):
    """Test _validate_person with valid new persons."""
    try:
        base_dispatcher._validate_person(new_person)
    except ValueError:
        pytest.fail(f"_validate_person raised ValueError unexpectedly for {new_person}!")


@pytest.mark.parametrize("existing_person", ["marco polo", "jane doe"])
def test_validate_person_invalid(base_dispatcher, existing_person):
    """Test _validate_person with already registered people."""
    with pytest.raises(ValueError, match=f"{existing_person} has already been registered!"):
        base_dispatcher._validate_person(existing_person)


@pytest.mark.parametrize(
    "new_responsibilities", [["teaching", "coding"], ["gardening", "painting"]]
)
def test_validate_responsibilities_valid(base_dispatcher, new_responsibilities):
    """Test _valdiate_responsibilities with valid new responsibilities."""
    try:
        base_dispatcher._valdiate_responsibilities(new_responsibilities)
    except ValueError:
        pytest.fail(
            f"_valdiate_responsibilities raised ValueError unexpectedly for {new_responsibilities}!"
        )


@pytest.mark.parametrize("existing_responsibility", [["cooking carbonara"], ["watching netflix"]])
def test_validate_responsibilities_invalid(base_dispatcher, existing_responsibility):
    """Test _valdiate_responsibilities with already registered responsibilities."""
    with pytest.raises(
        ValueError,
        match=f"{existing_responsibility[0]} was already registered as a responsibility.",
    ):
        base_dispatcher._valdiate_responsibilities(existing_responsibility)


@pytest.mark.parametrize(
    "llm_reply, expected_responsibility",
    [
        ("The task is related to cooking carbonara.", "cooking carbonara"),
        ("This is about discovering america.", "discovering america"),
    ]
)
def test_identify_responsibility_valid(base_dispatcher, llm_reply, expected_responsibility):
    """Test _identify_responsibility with valid replies."""
    responsibility = base_dispatcher._identify_responsibility(llm_reply)
    assert responsibility == expected_responsibility

@pytest.mark.parametrize(
    "llm_reply",
    [
        ("This task is related to cooking and discovering."),
        ("No matching responsibility found."),
    ]
)
def test_identify_responsibility_invalid(base_dispatcher, llm_reply):
    """Test _identify_responsibility with invalid replies."""
    with pytest.raises(ValueError, match="Could not identify exactly one responsibility in the reply:"):
        base_dispatcher._identify_responsibility(llm_reply)


@pytest.mark.parametrize(
    "responsibility, expected_person",
    [
        ("cooking carbonara", "marco polo"),
        ("watching netflix", "jane doe"),
    ]
)
def test_identify_person_valid(base_dispatcher, responsibility, expected_person):
    """Test _identify_person with valid responsibilities."""
    person = base_dispatcher._identify_person(responsibility)
    assert person == expected_person

@pytest.mark.parametrize(
    "responsibility",
    [
        ("nonexistent responsibility"),
        ("another fake responsibility"),
    ]
)
def test_identify_person_invalid(base_dispatcher, responsibility):
    """Test _identify_person with invalid responsibilities."""
    with pytest.raises(ValueError, match=f"No person found for responsibility: {responsibility}"):
        base_dispatcher._identify_person(responsibility)


def test_all_responsibilities():
    """Test if the property returns the correct list of responsibilities."""
    dispatcher = Dispatcher(
        roster={
            "person a": ["doing the dishes"],
            "person b": ["saying hi", "waving goodbye"],
        }
    )
    assert dispatcher.all_responsibilities == ["doing the dishes", "saying hi", "waving goodbye"]

