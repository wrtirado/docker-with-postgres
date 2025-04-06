import pytest
from example_tests import count_total_list_items, format_data_for_display, is_palendrome
from fixtures import (
    example_people_data_2,
)  # <- Method 2: import the fuxture from a different file


# Method 1: Using a fixture in same file to provide data
# and a method_1 marker. Call with 'pytest -m method_1'
# See pytest.ini for the marker definition
@pytest.fixture
def example_people_data_1():
    return [
        {
            "given_name": "Alfonsa",
            "family_name": "Ruiz",
            "title": "Senior Software Engineer",
        },
        {
            "given_name": "Sayid",
            "family_name": "Khan",
            "title": "Project Manager",
        },
    ]


@pytest.mark.method_1
def test_count_total_list_items_1(example_people_data_1):
    assert count_total_list_items(example_people_data_1) == 2


@pytest.mark.method_1
def test_format_data_for_display_1(example_people_data_1):
    assert format_data_for_display(example_people_data_1) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]


# Method 2: Using a fixture in a different file to provide data
# and a method_2 marker. Call with 'pytest -m method_2'
# See pytest.ini for the marker definition
@pytest.mark.method_2
def test_count_total_list_items_2(example_people_data_2):
    assert count_total_list_items(example_people_data_2) == 2


@pytest.mark.method_2
def test_format_data_for_display_2(example_people_data_2):
    assert format_data_for_display(example_people_data_2) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]


# Tests showing parameterization


@pytest.mark.parametrized
@pytest.mark.parametrize(
    "palindrome",
    [
        "racecar",
        "level",
        "rotor",
        "deified",
        "civic",
        "madam",
        "",
        "a",
        "aa",
        "aba",
        "abba",
        "Bob",
        "Never odd or even",
        "Do geese see God?",
    ],
)
def test_is_palindrome(palindrome):
    assert is_palendrome(palindrome)


@pytest.mark.parametrized
@pytest.mark.parametrize(
    "non_palindrome",
    [
        "hello",
        "world",
        "python",
        "pytest",
        "testing",
        "example",
        "data",
        "structure",
        "algorithm",
        "function",
    ],
)
def test_is_not_palindrome(non_palindrome):
    assert not is_palendrome(non_palindrome)
