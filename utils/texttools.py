import re


def remove_source(input_string: str, replacement=""):
    # Create a regex pattern to match (Source: BLANK)

    input_string = input_string.replace("[Written by MAL Rewrite]", "")

    pattern = re.compile(r"\(Source: (.+?)\)")

    # Replace the pattern with the provided replacement
    result = pattern.sub(replacement, input_string)

    return result
