import copy
import json
import requests


def _match_wood_to_elements(wood_database, design_elements):

    wood_database.sort(key=lambda wood: wood["length"], reverse=True)
    remaining_wood = copy.deepcopy(wood_database)

    wood_mapping = {}

    changed = []

    for element in design_elements:
        best_fit = None
        for wood in remaining_wood:

            if (
                wood["length"] >= element["length"]
                and wood["width"] >= element["width"]
                # and wood["height"] >= element["height"]
            ):
                if best_fit is None or best_fit["length"] > wood["length"]:
                    best_fit = wood

        if best_fit is not None:
            best_fit["length"] -= element["length"]
            changed.append(best_fit["id"])
            wood_mapping[element["name"]] = best_fit["id"]

    updated_lengths = {
        wood["id"]: wood["length"] for wood in remaining_wood if wood["id"] in changed
    }

    return wood_mapping, updated_lengths, changed


def match_design(db, design_lengths, design_widths, part_index):
    
    db_data = json.loads(db)

    lengths = [design_lengths[i] for i in range(len(design_lengths))]
    widths = [design_widths[i] for i in range(len(design_widths))]
    indecies = [part_index[i] for i in range(len(part_index))]

    parts = ["part_{0}".format(i) for i in indecies]

    design_elements = [
        {"length": length, "width": width, "name": index}
        for length, width, index in zip(lengths, widths, indecies)
    ]

    try:
        print("design matched successfully")
        result = _match_wood_to_elements(db_data, design_elements)

        design_requirements = [
            generate_design_requirements(
                [lengths[i], widths[i]],
                parts[i],
                project_id="test_01",
                part_index=indecies[i],
                wood_ids=result[2][i],
            )
            for i in range(len(parts))
        ]

        return *result, design_requirements

    except json.JSONDecodeError as err:
        print("Error decoding JSON: {0}".format(err))
    except (TypeError, ValueError, KeyError) as err:
        print("Something went wrong: {0}".format(err))


def generate_design_requirements(features, parts, project_id, wood_ids, part_index):
    return json.dumps(
        {
            "wood_id": wood_ids,
            "features": [*features],
            "part": parts,
            "project_id": project_id,
            "part_index": part_index,
        }
    )


if __name__ == "__main__":
    
    db = requests.get("https://robotlab-residualwood.onrender.com/wood")
    
    # example data
    design_lengths = [300, 360, 200]
    design_widths = [80, 60, 90]
    part_index = [1, 2, 3]

    mapped_values, updated_lengths_values, used, design = match_design(db.content, design_lengths, design_widths, part_index)

    # mapped values
    print(mapped_values)

    # updated lengths of wood
    print(updated_lengths_values)

    # used IDs
    print(used)

    # design requirements
    print(design)