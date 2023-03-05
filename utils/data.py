def process_data() -> dict[str, str | int]:
    ...


def normalise_string(string: str) -> str:
    """
    Function to normalise a string of character casing, stopwords, etc.

    Parameters
    ----------
    string: str
        String to normalise

    Returns
    -------
    str
        Normalised string.

    """