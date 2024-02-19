function_string = """
```python
def calculate_rectangle_area(length, width):
    \"\"\"
    Calculates the area of a rectangle.

    Parameters:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Returns:
        float: The area of the rectangle.
    \"\"\"
    if length <= 0 or width <= 0:
        raise ValueError("Length and width must be positive numbers")
    return length * width
```
"""