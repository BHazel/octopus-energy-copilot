"""
CLI module.
"""

from typing import Any
import jmespath
import jsonpickle

def create_json_output(value: Any, query: str = None) -> str:
    """
    Creates a JSON string from an object, optionally filtered and structured with a JMESPath query.

    Args:
        value (Any): The object to serialize.
        query (str, optional): The JMESPath query to filter and structure the output.
            Defaults to None.
    
    Returns:
        str: The filtered and structured JSON string.
    """
    if query is not None:
        if isinstance(value, list):
            sanitised_value = [item.__dict__ for item in value]
        else:
            sanitised_value = value.__dict__

        value_to_encode = jmespath.search(query, sanitised_value)
    else:
        value_to_encode = value

    return jsonpickle.encode(value_to_encode, indent=True)
