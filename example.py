# Import the JsonEditor class from the module
from json_editor import json_editor

# Create an instance of JsonEditor with the JSON file path
editor = json_editor("data.json")

# Set a value in a specific path
editor.set("key", "new_value")

# Get the value from a specific path
value = editor.get("key")
print(value)  # Output: new_value

# Unset a path
editor.unset("key")

# Append a value/object to a specific path
editor.append("list", "value1")
editor.append("list", "value2")

# Pop an array from a specific path
editor.pop("list")

# Save the changes to the JSON file
editor.save()
