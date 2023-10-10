import re

def transform_to_json(s, level=1):
    pattern = r'([\s\S]+?)\(([\s\S]+)\)'
    matches = re.findall(pattern, s)
    final_dict = {}
    if not matches:
        return None
    for match in matches:
        key = match[0]
        value_str = match[1]
        final_dict[key] = {}
        nested_match = re.findall(r'(\s\S+)\(([\s\S]+?\"\s+)\)', value_str)
        if nested_match:
            for nested in nested_match:
                nested_key = nested[0]
                nested_value = nested[1]
                final_dict[key][nested_key] = {'level': level, 'attributes': [], 'children': []}
                quoted_strings = re.findall(r'"([^"]+)"', nested_value)
                string_without_quotes = re.sub(r'"[^"]+"', '*QS*', nested_value)
                elements = re.split(r'\s{2,}',string_without_quotes)
                results = [element.replace('*QS*', quoted_strings.pop(0)) if element == '*QS*' else element for element in elements]
                for result in results:
                    attribute_pattern = r'(\w+\(.*\))'
                    nested_attribute = re.findall(attribute_pattern, result)
                    if nested_attribute:
                        final_dict[key][nested_key]['children'].append(transform_to_json(f"{nested_attribute}", level+1))
                    else:
                        final_dict[key][nested_key]['attributes'].append(result)
        else:
            attributes = {attribute for attribute in value_str.split()}
            final_dict[key] = attributes
    
    return final_dict

f = open("Santana.tech", "r")

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
