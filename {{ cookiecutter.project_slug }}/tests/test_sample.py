import pytest
# import {{cookiecutter.project_slug}} to use the code for testing


# Start of your testing code
def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

def test_sum_tuple():
    assert sum((1, 2, 2)) == 6, "Should be 6"
