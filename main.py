import copy

def match_wood_to_elements(wood_database, chair_elements):
    # Sort wood pieces by length in descending order
    wood_database.sort(key=lambda wood: wood['length'], reverse=True)

    # Create a copy of the wood database to track updated lengths after cutting
    remaining_wood = copy.deepcopy(wood_database)

    # Dictionary to store the mapping of chair elements to selected wood pieces
    wood_mapping = {}

    for element in chair_elements:
        best_fit = None

        for wood in remaining_wood:
            if (
                wood['length'] >= element['length'] and
                wood['width'] >= element['width'] and
                wood['height'] >= element['height']
            ):
                if best_fit is None or best_fit['length'] > wood['length']:
                    best_fit = wood

        if best_fit is not None:
            # Reduce the length of the selected wood piece after cutting the element
            best_fit['length'] -= element['length']
            wood_mapping[element['name']] = best_fit

    # Calculate updated lengths of wood pieces after cutting all chair elements
    updated_lengths = {wood['id']: wood['length'] for wood in remaining_wood}

    return wood_mapping, updated_lengths

# Example usage
wood_database = [
    {'id': 1, 'length': 1000, 'width': 233, 'height': 20},
    {'id': 3, 'length': 1500, 'width': 160, 'height': 23},
    {'id': 4, 'length': 2500, 'width': 120, 'height': 23},
    {'id': 5, 'length': 1005, 'width': 96, 'height': 19},
    {'id': 6, 'length': 800, 'width': 106, 'height': 20},
    {'id': 7, 'length': 1115, 'width': 116, 'height': 21},
    {'id': 8, 'length': 915, 'width': 89, 'height': 19},
    {'id': 9, 'length': 1520, 'width': 90, 'height': 25},
    {'id': 10, 'length': 875, 'width': 110, 'height': 30},
    # ... add more wood pieces to the database
]

chair_elements = [
    {'name': 'Backrest', 'length': 320, 'width': 50, 'height': 19},
    {'name': 'Backrest2', 'length': 320, 'width': 40, 'height': 19},
    {'name': 'Backrest3', 'length': 320, 'width': 40, 'height': 19},
    {'name': 'Backrest4', 'length': 320, 'width': 40, 'height': 19},
    {'name': 'Leg', 'length': 420, 'width': 40, 'height': 19},
    {'name': 'Seat', 'length': 420, 'width': 60, 'height': 19},
    # ... add more chair elements
]

wood_mapping, updated_lengths = match_wood_to_elements(wood_database, chair_elements)

# Print the results
for element, wood in wood_mapping.items():
    print(f"{element} is made from wood piece {wood['id']}")

print("\nUpdated lengths of wood pieces:")
for wood_id, length in updated_lengths.items():
    print(f"Wood piece {wood_id}: {length} units remaining")