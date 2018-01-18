#!/usr/bin/python3

import os, sys, argparse, yaml, datetime

from textwrap import wrap
from jinja2 import Environment, FileSystemLoader
from cerberus import Validator

from config_model import ConfigSchema

# TODO: Increase indentation level for each namespace def
# TODO: Correctly set namespace in t_string function

Jinja = Environment(
    loader=FileSystemLoader( os.path.dirname(__file__) + '/templates/' ), 
    trim_blocks=True, 
    lstrip_blocks=True, 
    keep_trailing_newline=True
)


def generate_declarations(enums):
    template = Jinja.get_template('header.tpl.hpp')
    return template.render(config=enums, date=datetime.datetime.now())


def generate_definitions(enums):
    template = Jinja.get_template('source.tpl.cpp')
    return template.render(config=enums, date=datetime.datetime.now())

def prettyprint_validation_errors(all_errors, indent=''):
    for namespace, errors in all_errors.items():
        print("\n{} +--[ {} ]".format(indent, namespace), end='')

        for single_error in errors:
            if (isinstance(single_error, dict)):
                prettyprint_validation_errors(single_error, indent + '  ')

            else:
                print(" > {}".format(single_error), end='')

    print('')

if __name__ == '__main__':

    argparser = argparse.ArgumentParser(
        prog='mkenum',
        description='Generate C++ enums & associated conversion methods'
    )

    argparser.add_argument('config_file', type=str, help='The configuration file containing the enums to be generated')
    args = argparser.parse_args()

    with open(args.config_file, encoding='utf-8') as config_file:
        config = yaml.load(config_file)

    # Validate the config
    config_validator = Validator(ConfigSchema)
    if not config_validator.validate(config):
        prettyprint_validation_errors(config_validator.errors)

        sys.exit(1)

    # Generate the fully qualified enum-namespace
    # If, in the config file we specify:
    #   namespace = [ "foo", "bar", "baz" ]
    #
    # Then we generate the full namespace: "foo::bar::baz::"
    for enum in config['enumerations']:
        if 'namespace' in enum:
            enum['full_namespace'] = '::'.join(enum["namespace"])

    # Make sure to wrap doc comments
    for enum in config['enumerations']:
        if 'doc_comment' in enum: 
            enum['doc_comment'] = wrap(enum['doc_comment'], width=72)

    # Normalize enums. Put them all in the detailed format
    # Note: since strings are immutable we need to loop over the enum values by index
    for enum in config['enumerations']:
        if enum["values"]:
            for idx in range(len(enum["values"])):
                if isinstance(enum["values"][idx], str):
                    enum["values"][idx] = { 'identifier': enum["values"][idx] }

    # Normalize mappings.
    # The 'name' field on mappings is optional. Here we fill it in
    for enum in config["enumerations"]:
        for mapping in enum.get("mappings", []):
            if not mapping.get("name"):
                mapping["name"] = "get_" + mapping["to"]

    hpp_file = config["outputs"]["header"]["filename"]
    if not os.path.isabs(hpp_file):
        hpp_file = os.path.join(os.getcwd(), hpp_file)

    print("Generating header file '{}'".format(hpp_file))
    os.makedirs(os.path.dirname(hpp_file), exist_ok=True)
    with open(hpp_file, 'w', encoding='utf-8') as f:
        f.write(generate_declarations(config))

    cpp_file = config["outputs"]["source"]["filename"]
    if not os.path.isabs(cpp_file):
        cpp_file = os.path.join(os.getcwd(), cpp_file)

    print("Generating source file '{}'".format(cpp_file))
    os.makedirs(os.path.dirname(cpp_file), exist_ok=True)
    with open(cpp_file, 'w', encoding='utf-8') as f:
        f.write(generate_definitions(config))

