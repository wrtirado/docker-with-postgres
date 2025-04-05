# Fixtures: Managing State and Dependencies

`pytest` fixtures are a way of providing data, test doubles, or state setup to your tests. Fixtures are functions that can return a wide range of values. Each test that depends on a fixture must explicitly accept that fixture as an argument.

## When to Create Fixtures

If you find yourself writing several tests that all make use of the same underlying test data, then a fixture may be in your future. For example:

### If you have the following functions:

```
# format_data.py
def format_data_for_display(people):
    ...  # Logic logic logic...

def format_data_for_excel(people):
    ...  # Logic logic logic...

```

### And the following tests

```
# test_format_data.py
def test_format_data_for_display():
    people = [
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

    assert format_data_for_display(people) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]


def test_format_data_for_excel():
    people = [
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

    assert format_data_for_excel(example_people_data) == """given,family,title
Alfonsa,Ruiz,Senior Software Engineer
Sayid,Khan,Project Manager
```

### Enter Fixtures

Fixtures will help you extract and centralize the test data into a single function decorated with `@pytest.fixture` to indicate that the function is a pytest fixture.

```
# test_format_data.py
import pytest

@pytest.fixture
defexample_people_data():
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
# ...
```

You can use the fuxture by adding the function reference as an argument to your tests.

> Note that you don't call the fixture function. `pytest` takes care of that. You'll be able to use the return value of the fixture function as the name of the fixture function:

```
# test_format_data.py continued

# ...

def test_format_data_for_display(example_people_data):
    assert format_data_for_display(example_people_data) == [
        "Alfonsa Ruiz: Senior Software Engineer",
        "Sayid Khan: Project Manager",
    ]

def test_format_data_for_excel(example_people_data):
    assert format_data_for_excel(example_people_data) == """given,family,title
Alfonsa,Ruiz,Senior Software Engineer
Sayid,Khan,Project Manager
"""
```

Each test is now notably shorter but still has a clear path back to the data it depends on. Be sure to name your fixture something specific. That way, you can quickly determine if you want to use it when writing new tests in the future!

## When to Avoid Fixtures

Fixtures are great for extracting data or objects that you use across multiple tests. However, they aren’t always as good for tests that require slight variations in the data. Littering your test suite with fixtures is no better than littering it with plain data or objects. It might even be worse because of the added layer of indirection.

## Using Fixtures at Scale

#### Fixture Specific Modules

Rather than potentially placing similar/identical fixtures inside of multiple modules/files, you can create modules that hold only fixtures, and then export/import the fixtues as needed into other modules.

#### Making Fixtures Global (getting around importing/exporting)

If you want to make a fixture available for your whole project without having to import it, a special configuration module called `conftest.py` will allow you to do that.

pytest looks for a `conftest.py` module in each directory. If you add your general-purpose fixtures to the `conftest.py` module, then you’ll be able to use that fixture throughout the module’s parent directory and in any subdirectories without having to import it. This is a great place to put your most widely used fixtures.
