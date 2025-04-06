import pytest
from example_tests import count_total_list_items, format_data_for_display
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
