import re

def parse_attributes(attribute_str):
    return list(set(attribute_str.split()))

def process_nested_value(nested_value, level):
    final_dict = {'level': level, 'attributes': [], 'children': []}
    quoted_strings = re.findall(r'"([^"]+)"', nested_value)
    string_without_quotes = re.sub(r'"[^"]+"', '*QS*', nested_value)
    elements = re.split(r'\s{2,}', string_without_quotes)
    for element in elements:
        if element == '*QS*':
            final_dict['attributes'].append(quoted_strings.pop(0))
        else:
            attribute_pattern = r'(\w+\(.*\))'
            nested_attribute = re.findall(attribute_pattern, element)
            if nested_attribute:
                final_dict['children'].append(transform_to_json(f"{nested_attribute}", level + 1))
            else:
                final_dict['attributes'].append(element)
    return final_dict

def transform_to_json(s, level=1):
    pattern = r'([\s\S]+?)\(([\s\S]+)\)'
    matches = re.findall(pattern, s)
    final_dict = {}

    for match in matches:
        key, value_str = match
        nested_match = re.findall(
            r'(\s\S+)\(([\s\S]+?\"\s+)\)', value_str
        )
        if nested_match:
            final_dict[key] = {
                nested_key: process_nested_value(nested_value, level)
                for nested_key, nested_value in nested_match
            }
        else:
            final_dict[key] = parse_attributes(value_str)

    return final_dict

with open("Santana.tech", "r") as f:
    rules = re.findall(r"(orderedSpacingRules[\s\S]*);orderedSpacingRules", f.read())

final_rules = []
for rule in rules[0].split("\n"):
    if rule == "":
        continue
    if rule.lstrip().startswith(";"):
        continue
    final_rules.append(rule)

ordered_spacing_rules = '\n'.join(final_rules)
#print(ordered_spacing_rules)

# Transform the input string to JSON
json_result = transform_to_json(ordered_spacing_rules)
print(json_result)
