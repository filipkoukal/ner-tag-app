# NER Labeling App
## How to run
### Prerequisites
- Python 3 libraries
    - eel
    - nltk
- Entities must be set up in config.ini
    - Each entity must be on its own line in the <code>[entites]</code> section in format <code>Entity_tag = Entity description</code>
    - App currently supports a maximum of 8 entities
    - Example: <code>PC = Computer</code>
    - Refer to default config.ini if unsure 

Necessary libraries can be installed with <code>pip install -r requirements.txt</code>.
Use command <code>python3 main.py</code> to start the application.

## Usage
### Input file format
To load a file you have to press the "Load text file" button. You should use a plain .txt file as the input with each document on its own line. Once loaded the documents will be automatically tokenized (you can change/customize this behaviour in the function <code>load_and_tokenize_file(file_name)</code> in main.py)

### General usage and app overview
![Token with history](https://user-images.githubusercontent.com/60878671/211325965-898552ca-c01c-42d5-aa62-27131dddc923.png)

1. Progress bar
    - Progress bar shows how many documents have been marked as finished out of all documents
2. Document browser
    - You can select a document to label by clicking on it 
3. Token view
    - After selecting a document, its token will appear in the token view
    - From here you can click on any token and assign a named entity to it from the entity picker
4. Entity picker
    - Used to assign entites to the selected token
5. Token options and history
    - Only shows up when a token is selected
    - If a token has been labeled previously, its history will appear here
6. Document options
    - Used to mark the currently selected document or all in progress (orange) documents as finished
explain general usage (have a picture of app in a real scenario) 

### Token history
If an entity has been assigned to a particular token, then that token has a recorded history of all previous assignments (in the currently selected document and other documents). A small H in the upper right corner of the token is used to signalize if it has been previously tagged. In addition, a token with an existing history will have its previous assignments listed under the Token history section in right part of the window, under individual tokens. 

![Token with history](https://user-images.githubusercontent.com/60878671/211316729-c0e783b9-9c8f-467b-a1a6-06f9b6f888b7.png)

### Entity spreading
If you have assigned an entity to a token, then that entity can be spread to all other documents containing said token by clicking the "Apply token entity to all documents" button in lower right part of the window, under Token options, when a token is selected.

### Mark document as finished
Once you have identified all named entities in a document, you can mark it as finished by clicking the "Mark document as finished". You can additionally mark all in progress (orange) documents as finished by clicking the "Mark all in progress documents as finished" below the previously mentioned checkbox. 

### Exporting
Once finished labeling, you can export your work by pressing the export button. Two main formats are available, JSON and CoNLL-2003. In addition, you can choose to export only documents marked as finished (green).

### Saving progress
It is possible to save your current progress and resume labeling in a future session. To do this, simply export your work as JSON (preferably export all documents) and once you are ready to continue, open the app again and choose your exported JSON file as the input when you press the "Load text file" button. All document states (finished, in progress, unlabeled) and named entity assignments will be loaded from the saved file. 

