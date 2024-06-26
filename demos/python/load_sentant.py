# ----------------------------------------------------------------------------------------------------
# A Python script for loading and interacting with a single Sentant.
# Usage:
#
# python3 load_sentant.py <filename> <host>
#
# The filename is the name of the file containing the Sentant definition (JSON, TOML, or YAML format).
# The host is the IP address or domain name of the Reality2 node (default is localhost).
# ----------------------------------------------------------------------------------------------------

from reality2 import Reality2 as R2
import sys
import time
import json
import toml
from os.path import exists
from getkey import getkey
import copy
import ruamel.yaml

yaml = ruamel.yaml.YAML(typ='safe')
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Print out the help
# ----------------------------------------------------------------------------------------------------
def printhelp(events):
    print("---------- Send Events ----------")
    for counter, event in enumerate(events):
        print(" Press [", counter, "] for {", event["event"], event["parameters"], "}")

    print(" Press [ h ] for help.")
    print(" Press [ q ] to quit.")
    print("---------------------------------")    
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Print out the result from an awaitSignal
# ----------------------------------------------------------------------------------------------------
def printout(data):
    event = R2.JSONPath(data, "awaitSignal.event")
    
    if (event == "debug"):
        print("DEBUG\n", R2.JSONPath(data, "awaitSignal.parameters")) 
    else: 
        print(R2.JSONPath(data, "awaitSignal.event"), " : ", R2.JSONPath(data, "awaitSignal.parameters"), " :: ", R2.JSONPath(data, "awaitSignal.passthrough"))
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------------------------------------
def main(filename, host):

    # ------------------------------------------------------------------------------------------------
    # Connect to the Reality2 node
    # ------------------------------------------------------------------------------------------------
    r2_node = R2(host, 4001)

    # ------------------------------------------------------------------------------------------------
    # Read the definition file
    # ------------------------------------------------------------------------------------------------
    if (exists(filename)):
        with open(filename, 'r') as file:
            definition = file.read()
    else:
        print("The file", filename, "does not exist.")
        return
    
    # ------------------------------------------------------------------------------------------------
    # Read the variables file (if it exists)
    # ------------------------------------------------------------------------------------------------
    if exists('../../../variables.json'):
        with open('../../../variables.json', 'r') as file:
            variables_txt = file.read()
        
        # Convert the variables to a dictionary
        variables = json.loads(variables_txt)

        # Replace the variables in the definition file
        for key in variables:
            definition = definition.replace(key, variables[key])

    # ------------------------------------------------------------------------------------------------
    # Unload the existing Sentant named in the file if it exists
    # ------------------------------------------------------------------------------------------------
    if filename.endswith('.yaml'):
        definition_json = yaml.load(definition)
    elif filename.endswith('.toml'):
        definition_json = toml.loads(definition)
    elif filename.endswith('.json'):
        definition_json = json.loads(definition)
    else:
        print("The file", filename, "is not a valid format.")
        return
        
    sentant_name = R2.JSONPath(definition_json, "sentant.name")
    print("Unloading existing Sentant named \"", sentant_name, "\"")
    r2_node.sentantUnloadByName(sentant_name)

    # ------------------------------------------------------------------------------------------------
    # Load the Sentant
    # ------------------------------------------------------------------------------------------------
    result = r2_node.sentantLoad(definition, {}, "id name signals events { event parameters }")

    # ------------------------------------------------------------------------------------------------
    # Get the ID of the loaded Sentant
    # ------------------------------------------------------------------------------------------------
    id = R2.JSONPath(result, "sentantLoad.id")

    # ------------------------------------------------------------------------------------------------
    # Get the signals and events
    # ------------------------------------------------------------------------------------------------
    signals = R2.JSONPath(result, "sentantLoad.signals")
    events = R2.JSONPath(result, "sentantLoad.events")

    # ------------------------------------------------------------------------------------------------
    # Start the subscriptions to the Sentant
    # ------------------------------------------------------------------------------------------------
    r2_node.awaitSignal(id, "debug", printout)
    for signal in signals:
        r2_node.awaitSignal(id, signal, printout)

    # ------------------------------------------------------------------------------------------------
    # Wait a second to allow the subscriptions to catch up
    # ------------------------------------------------------------------------------------------------
    time.sleep(1)

    # ------------------------------------------------------------------------------------------------
    # Print out the help
    # ------------------------------------------------------------------------------------------------
    printhelp(events)

    # ------------------------------------------------------------------------------------------------
    # Wait for user input and send the events
    # ------------------------------------------------------------------------------------------------
    while (True):
        key = getkey()
        if (key =="q"):
            break
        elif (key == "h"):
            printhelp(events)
        else:
            if key.isdigit():
                index = int(key)
                if (index >= 0 and index < len(events)):
                    parameters = copy.deepcopy(events[index]["parameters"])

                    for parameter in parameters:
                        print("Type in a", parameters[parameter], "for", parameter, end=" : ")
                        parameters[parameter] = input()

                    print("Sending event [", events[index]["event"], "]")
                    r2_node.sentantSend(id, events[index]["event"], parameters)
                else:
                    print("Please enter a number between 0 and", len(events) - 1, "inclusive.")
            else:
                print("Please enter a number, h for help, or q to quit.")

    # ------------------------------------------------------------------------------------------------
    # Close the subscriptions
    # ------------------------------------------------------------------------------------------------
    print("Closing the subscriptions and quitting.")
    r2_node.close()
# ----------------------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------------------------
# If this script is run from the command line then call the main function.
# ----------------------------------------------------------------------------------------------------
if (__name__ == '__main__'):
    if (len(sys.argv) < 2):
        print("Usage: python3 load_sentant.py <filename> <host>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2] if (len(sys.argv) > 2) else "localhost")
# ----------------------------------------------------------------------------------------------------