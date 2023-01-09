import eel
from datetime import datetime as dt
from nltk.tokenize import word_tokenize
import json
import os
import configparser

data_dict = {}
token_history = {}

entity_list = {}


def load_config_file(file_name):
    global entity_list
    try:
        config = configparser.ConfigParser()
        config.read(file_name)
        entities = dict(config.items('entities'))
        entity_list["O"] = (0, "None")
        for i, (key, value) in enumerate(entities.items()):
            entity_list[key.upper()] = (i+1, value)
    except:
        entity_list = {
            "O": (0, "None")
        }

@eel.expose                  # Expose this function to Javascript
def load_and_tokenize_file(file_name):
    global data_dict
    split_tup = os.path.splitext(file_name)
    eel.load_entities(entity_list)
    if split_tup[1].lower() != ".json":
        # load file
        with open(file_name, "r", encoding="utf8") as fp:
            lines = fp.readlines()
        
        for i, line in enumerate(lines):
            tokens = tokenize_doc(line)
            doc_dict = {
                "text" : line, 
                "tokens" : tokens,
                "entities" : ["O" for token in tokens],
                "state": "unlabeled"
            }
            data_dict[str(i)] = doc_dict

        eel.display_docs(lines, [doc["state"] for doc in data_dict.values()])
    else:
        # resume labeling from json file
        with open(file_name, "r", encoding="utf8") as json_fp:
            data_dict = json.load(json_fp)
        
        lines = []
        for doc in data_dict.values():
            lines.append(doc["text"])

            # recreate token history
            if not all(ent == "O" for ent in doc["entities"]):
                for token, entity in zip(doc["tokens"], doc["entities"]):
                    if entity != "O":
                        update_token_history(token, entity, "O")
        
        eel.display_docs(lines, [doc["state"] for doc in data_dict.values()])

        


def tokenize_doc(text):
    for mark in ('.', ',', '?', '!', '-', '–', '/'):
        text = text.replace(mark, f' {mark} ')
    tokens = word_tokenize(text)
    return tokens

@eel.expose
def get_doc_tokens(doc_id):
    doc_num_id = doc_id.split("-")[1]
    tokens = data_dict[doc_num_id]["tokens"]
    token_entities = [ entity_list[entity][0] for entity in data_dict[doc_num_id]["entities"] ]
    token_histories = []
    for token_id, token in enumerate(tokens):
        history_exists = True if len(get_token_history(doc_num_id, token_id)) > 0 else False
        token_histories.append(history_exists)
    eel.display_tokens(tokens, token_entities, token_histories)

@eel.expose
def check_token_entity(doc_id, token_id):
    entity_id = entity_list[data_dict[doc_id]["entities"][int(token_id)]][0]
    eel.check_token_entity(entity_id)
    history = get_token_history(doc_id, token_id)
    eel.display_token_history(history)
        

def get_token_history(doc_id, token_id):
    # calculate token history and send over
    token = data_dict[doc_id]["tokens"][int(token_id)]
    try:
        history = token_history[token]
        history = dict(sorted(history.items(), key=lambda item: item[1], reverse=True))
    except KeyError as error:
        history = {}
    
    return history


@eel.expose
def update_entity(doc_id, token_id, entity_id):
    #print(doc_id, token_id, entity_id)
    key = list({i for i in entity_list if entity_list[i][0] == int(entity_id)})[0]
    previous_entity = data_dict[doc_id]["entities"][int(token_id)]
    data_dict[doc_id]["entities"][int(token_id)] = key
    update_token_history(data_dict[doc_id]["tokens"][int(token_id)],key, previous_entity)
    history = get_token_history(doc_id, token_id)
    
    previous_state = data_dict[doc_id]["state"]
    # change state of doc
    if not all(ent == "O" for ent in data_dict[doc_id]["entities"]):
        data_dict[doc_id]["state"] = "inprogress"
    else:
        data_dict[doc_id]["state"] = "unlabeled"
    eel.display_token_history(history)
    eel.highlight_doc_based_on_state(data_dict[doc_id]["state"], previous_state)

def update_token_history(token, entity, previous_entity):
    # adding new entity to history
    if entity != "O":
        if token in token_history:
            if entity in token_history[token]:
                token_history[token][entity] += 1
            else:
                token_history[token][entity] = 1
        else:
            token_history[token] = {entity:1}
    
    # subtract old entity from history if was changed and was not blank
    if previous_entity != "O":
        token_history[token][previous_entity] -= 1
        # delete key if entity was subtracted to zero, feels kinka wonky, maybe change later
        if token_history[token][previous_entity] == 0:
            del token_history[token][previous_entity]

@eel.expose
def export_file(format, export_only_finished, path):
    if format == "jsonradio":
        export_file_as_json(path, export_only_finished)
    elif format == "conllradio":
        export_file_as_conll(path, export_only_finished)

def export_file_as_json(path, export_only_finished):
    if not export_only_finished:
        json_object = json.dumps(data_dict, indent = 4) 
        with open(os.path.join(path, "export.json"), "w", encoding="utf8") as outfile:
            outfile.write(json_object)
    else:
        finished_only_dict = {doc_id:doc for doc_id, doc in data_dict.items() if doc["state"] == "finished"}
        json_object = json.dumps(finished_only_dict, indent = 4) 
        with open(os.path.join(path, "export_finished_only.json"), "w", encoding="utf8") as outfile:
            outfile.write(json_object)

def export_file_as_conll(path, export_only_finished):
    if not export_only_finished:
        with open(os.path.join(path, "export_conll.txt"), "w", encoding="utf8") as outfile:
            for doc in data_dict.values():
                for token, entity in zip(doc["tokens"], doc["entities"]):
                    outfile.write(token + " " + entity + "\n")
                outfile.write("\n")
    else:
        finished_only_dict = {doc_id:doc for doc_id, doc in data_dict.items() if doc["state"] == "finished"}
        with open(os.path.join(path, "export_finished_only_conll.txt"), "w", encoding="utf8") as outfile:
            for doc in finished_only_dict.values():
                for token, entity in zip(doc["tokens"], doc["entities"]):
                    outfile.write(token + " " + entity + "\n")
                outfile.write("\n")
@eel.expose
def display_doc_checkbox(doc_id):
    state = data_dict[doc_id]["state"]
    eel.display_doc_checkbox(state)

@eel.expose
def set_doc_state(doc_id, state):
    if state:
        data_dict[doc_id]["state"] = "finished"
    else:
        # else change to unlabeled if no tokens have been labeled or in progress if some tokens have been labeled (do an any check)
        if not all(ent == "O" for ent in data_dict[doc_id]["entities"]):
            data_dict[doc_id]["state"] = "inprogress"
        else:
            data_dict[doc_id]["state"] = "unlabeled"
    eel.highlight_doc_based_on_state(data_dict[doc_id]["state"])

@eel.expose
def spread_entity(doc_id, token_id, entity_id):
    token = data_dict[doc_id]["tokens"][int(token_id)]
    entity = data_dict[doc_id]["entities"][int(token_id)]

    # spread to all docs
    total_occurences = 0
    for document_id, doc in data_dict.items():
        if token in set(doc["tokens"]):
            token_indices = [i for i, x in enumerate(doc["tokens"]) if x == token]
            total_occurences += len(token_indices)          

            for index in token_indices:
                doc["entities"][index] = entity

            # states
            if not all(ent == "O" for ent in doc["entities"]):
                doc["state"] = "inprogress" 
            else:
                doc["state"] = "unlabeled"   

    # update history
    if entity != "O":
        token_history[token] = {entity: total_occurences}
    else:
        token_history[token] = {}

    states = [doc["state"] for doc in data_dict.values()]
    eel.update_ui_on_token_spread(states)

@eel.expose
def mark_all_inprogress_finished(doc_id):
    states = []
    for doc in data_dict.values():
        if doc["state"] == "inprogress":
            doc["state"] = "finished"
        states.append(doc["state"])
    eel.update_document_colors(states, data_dict[doc_id]["state"])



# Load config file before app start
load_config_file("config.ini")
# Set web files folder
eel.init('web')
# Start app
eel.start("index.html") # dont block on this function call
