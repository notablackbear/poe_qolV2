from pathlib import Path
import os

SECTION_HEADER_FORMAT = "#==== AUTO GENERATED {} START ====\n"
SECTION_FOOTER_FORMAT = "#==== AUTO GENERATED {} STOP ====\n"
RULE_NAME_FORMAT = "# RULE {}\n"
RULE_NAME_START = "# RULE"

# A Section format is :
"""
#==== AUTO GENERATED <SECTION NAME> START ====
# RULE <RULE1_NAME>
rule
contents
blah
...

# RULE <RULE2_NAME>
...
#==== AUTO GENERATED <SECTION NAME> STOP ====
"""


def get_filter_directory():
    """
    Created by: 0xdavidel

    Get the old default filter path.
    I was wrong to assume that the filter directory was persistant
    """
    user_path = Path.home()
    return os.path.join(user_path, "Documents", "My Games", "Path of Exile")


def get_filter_path(path):
    """
    Created by: 0xdavidel

    Get the absolute filter path, if the path inputted is absolute then it will return it back - meaning you can pass custom full paths 
    """

    filter_directory = get_filter_directory()
    # If path is absolute return the path as is
    if os.path.isabs(path):
        return path
    else:
        # The path is reletive, append it to the POE filter path
        return os.path.join(filter_directory, path)


def read_file(file_path):
    """
    Created by: 0xdavidel

    Read text from file
    """
    try:
        with open(file_path, "r") as f:
            data = f.read()
    except:
        raise Exception("Error reading file @ {}".format(file_path))
    return data


def write_file(file_path, data):
    """
    Created by: 0xdavidel

    Write text to file
    """
    try:
        with open(file_path, "w") as f:
            f.write(data)
    except:
        raise Exception("Error writing to file @ {}".format(file_path))


def extract_section(data, section_name):
    """
    Created by: 0xdavidel

    Basicly a glorified substring by custom format
    Extracts a section (based on what is defined in the start of the file) from filter data
    It will return a tuple of (section_start,section_end,section_raw_data)
    """
    section_header = SECTION_HEADER_FORMAT.format(section_name)
    section_footer = SECTION_FOOTER_FORMAT.format(section_name)

    is_header_present = section_header in data
    is_footer_present = section_footer in data

    # bool that is set to true will equal to the value of 1
    # Bad format, header and footer should either exist together or not at all
    if is_header_present + is_footer_present == 1:
        raise Exception(
            "Bad filter format, either the header or the footer is missing")

    # No section present, return and empty filter representation
    if not is_header_present and not is_footer_present:
        return 0, 0, None

    # This point is reached only if the section is inside the filter
    header_position = data.index(section_header)
    footer_position = data.index(section_footer)

    # Split the data to extract the section
    try:
        section = data[header_position:footer_position + len(section_footer)]
    except:
        raise Exception("Error extracting the target section [{} : {}]".format(
            header_position, footer_position))

    # Trim the section header and footer (Yes I know it could have been done at the prevous step, this is written explisitly for ease of maintanace)
    section = section[len(section_header): - len(section_footer)]
    return header_position, footer_position, section


def parse_section(section_data):
    """
    Created by: 0xdavidel

    Splits a section into rule dictionary, the key is the rule name, the content is the raw content of the rule
    Handles collisions

    Basicly a glorified .split for a custom format
    """
    section_rules_raw = section_data.split(RULE_NAME_START)
    section_rules_dict = {}
    for rule in section_rules_raw:
        # Filter out the empty entries
        if not rule:
            continue

        # Rule name is at the first line
        rule_name = rule.split("\n")[0]
        # Content is in the rest
        rule_content = rule[len(rule_name)+1:]

        # Remove excess whitespace
        rule_name = rule_name.strip()
        rule_content = rule_content.strip()

        # Collision check and solution
        while rule_name in section_rules_dict:
            # current solution is to modify the name
            rule_name += "_collision"

        section_rules_dict[rule_name] = rule_content

    return section_rules_dict


def load_section_from_filter(filter_path, section_name):
    """
    Created by: 0xdavidel
    Given a filter_path and a section_name it will read and return the section parsed into a dictionary
    This will throw custom exceptions when things go wrong with file premissions and section formats. DO NOT FORGET TO CATCH THEM!
    """
    filter_path = read_file(filter_path)
    # Extract our section from the filter
    section_start, section_end, section_data = extract_section(
        filter_path, section_name)

    # Time to parse the rules into a dictionary
    section_rules = parse_section(section_data)

    return section_rules


def load_rules_from_base_filter(filter_path):
    """
    Created by: 0xdavidel
    Read a "base_filter", meaning a source for the different rules to add
    the base filter should not have the section headers as its a waste of work for people to add them manually

    for example look at chaos_item_filter.filter
    """
    section_data = read_file(filter_path)
    section_rules = parse_section(section_data)

    return section_rules


def stringify_section_rules(section_rules):
    """
    Created by: 0xdavidel
    Format a section dictionary into a string that POE can read
    """
    result = ""
    for rule in section_rules:
        result += RULE_NAME_FORMAT.format(rule)
        result += section_rules[rule]
        result += "\n\n"
    return result


def write_section_to_filter(filter_path, section_name, section_rules):
    """
    Created by: 0xdavidel
    Replace / Create a section with the name <section_name> inside the filter at <filter_path>
    the new section content are the rules inside <section_rules>
    """
    filter_data = read_file(filter_path)

    section_start, section_end, section_data = extract_section(
        filter_data, section_name)

    section_rules_string = stringify_section_rules(section_rules)

    section_header = SECTION_HEADER_FORMAT.format(section_name)
    section_footer = SECTION_FOOTER_FORMAT.format(section_name)

    section_string = section_header + section_rules_string + section_footer

    new_filter_data = filter_data[:section_start] + \
        section_string + filter_data[section_end + len(section_footer):]

    write_file(filter_path, new_filter_data)
