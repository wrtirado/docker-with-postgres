import re


def count_total_list_items(list):
    """
    This function takes a list as an argument and returns the total number of items in the list.
    """
    return len(list)


def format_data_for_display(data):
    """
    This function takes a list of dictionaries as an argument and returns a formatted string for each dictionary.
    """
    return [
        f"{item['given_name']} {item['family_name']}: {item['title']}" for item in data
    ]


def is_palendrome(string):
    cleaned_string = re.sub(r"[^a-zA-Z0-9]", "", string).lower()
    return cleaned_string == cleaned_string[::-1]
