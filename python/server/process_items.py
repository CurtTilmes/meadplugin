from google.protobuf import json_format
import meadplugin_pb2

def process_items(items):
    #create empty object
    item_list_message = meadplugin_pb2.EvaluateResponse()
    try: 
        json_format.ParseDict(items,item_list_message)   
        message = "Successfully parsed input dictionary"
        status = meadplugin_pb2.RuleStatus.RULE_STATUS_SUCCESS
        return message, status, item_list_message
    except:
        message = "process_items: Could not convert plugin reponse to protobuf format"
        status = meadplugin_pb2.RuleStatus.RULE_STATUS_FAILURE
        return message, status, item_list_message   