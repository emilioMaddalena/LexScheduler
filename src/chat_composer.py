from constants import TEXT, LABEL

def compose_chat_from_data(data: list[dict]) -> list[dict]:
    """
    Data must be of the form
    [datum1, datum2, ...], where each dataum is of the form
    {TEXT: "some text", LABEL: "assigned label"}
    """
    return [
        msg for datapoint in data
        for msg in create_msg_pair_from_datapoint(datapoint)
    ]

def create_msg_pair_from_datapoint(datapoint: dict) -> list[dict]:
    """
    The datapoint must be of the form
    {TEXT: "some text", LABEL: "assigned label"}
    """
    return [
        {"role": "user", "content": datapoint[TEXT]},
        {"role": "assistant", "content": datapoint[LABEL]},
    ]
