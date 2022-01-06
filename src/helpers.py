import json

# fetch phantom results file from system
def fetch_json_input_file(path):
    # fetch file from system
    with open(path, encoding="utf8") as f:
        return json.load(f)

# write json results to filesystem
def write_json_output_file(path, payload):
    with open(path, "w") as outfile:
        json.dump(payload, outfile, indent=4)

# does field exist & value greater than null
def does_field_exist_value_non_null(field, obj):
    return True if field in obj and len(obj[field]) > 0 else False