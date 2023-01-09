# NER Labeling App
## How to run
### Prerequisites
- Python 3 libraries
    - eel
    - ntlk
- Entities must be set up in config.ini
    - Each entity must be on its own line in the <code>[entites]</code> section in format <code>Entity_tag = Entity description</code>
    - App currently supports a maximum of 8 entities
    - Example: <code>PC = Computer</code>
    - Refer to default config.ini if unsure 

Necessary libraries can be installed with <code>pip install -r requirements.txt</code>.
Use command <code>python main.py</code> to start the application.

## Usage
explain input txt file format

explain general usage (have a picture of app in a real scenario) 

explain history (have a picture of token with history)

explain spreading entity

explain tagging docs as finished

explain exporting as json / conll

explain loading exported json to continue a saved session
