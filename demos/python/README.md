# Python Demos

This folder contains some sentant and swarm definitions, as well as some code written in python to load them.

The library `reality2.py` manages the GraphQL API, and the python script `load_sentant.py` can used to load any sentant definition, and provide some basic command-line style interactivity.

## Prerequisites

To run these, use python3, and install the following libraries:

```bash
pip3 install gql
pip3 install requests
pip3 install requests_toolbelt
pip3 install websockets
pip3 install getkey
pip3 install ruamel.yaml
```

## Encryption keys and other private data

Some of the scripts require encryption / decryption keys, and API keys.  These may be stored in a file called `variables.json` at the level above the root directory for the node.

```json
{
    "__openai_api_key__": "YOUR OPENAI API KEY",
    "__encryption_key__": "Base64 encoded key",
    "__decryption_key__": "Base64 encoded key"
}
```

The encryption and decryption keys are used to protect data stored in the database using the `reality2_backup` plugin.  They can be created like this:

```python
key = os.random(32)
encryption_key = base64.b64encode(key).decode('utf-8')
decryption_key = base64.b64encode(key).decode('utf-8')
```

At present, the algorithm uses symmetric encryption so both the keys are the same.  These should be stored safely somewhere.

## Loading a Sentant

To load a sentant, the following may be used:

```bash
python3 load_sentant.py sentant_definition.yaml node
```

Where `sentant_definition.yaml` is the name of the file to load that contains the sentant - this may be yaml, json or toml formatted, and node is either the IP address or domain name of the Reality2 node to load the sentant onto.  If no node is given, then `localhost` is assumed.

So, for example:
```bash
python3 load_sentant.py sentant_chatgpt.yaml localhost
```
```text
Joined: wss://localhost:4001/reality2/websocket
Subscribed to 8c2fc93c-3298-11ef-9799-de59b61f7ba3|debug
Joined: wss://localhost:4001/reality2/websocket
Subscribed to 8c2fc93c-3298-11ef-9799-de59b61f7ba3|ChatGPT Answer
---------- Send Events ----------
 Press 0 followed by the enter key for [ Ask ChatGPT {'question': 'string'} ]
 Press h, followed by the enter key for this help.
 Press q, followed by the enter key to quit.
---------------------------------
0
Type in a string for question :What is the meaning of pi 
Sending event [ Ask ChatGPT ]
ChatGPT Answer  :  {'answer': "Pi (π) is a mathematical constant representing the ratio of a circle's circumference to its diameter. It is approximately equal to 3.14159 and is an irrational number, meaning it cannot be expressed as a simple fraction and its decimal representation goes on infinitely without repeating. It is a fundamental and important constant in mathematics and is used in various calculations and formulas in geometry, trigonometry, and other branches of mathematics and science.", 'question': 'What is the meaning of pi'}  ::  {}
```