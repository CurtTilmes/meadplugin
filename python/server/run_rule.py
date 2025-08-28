
import meadplugin_pb2
import process_items

def run_rule(function_module,rd):

#####################################
##### FIND RULES ####################
#####################################

    print(f"checking rule: {rd.rule}")
    try:
        rule_function = getattr(function_module, rd.rule)     
        message, status, items, params = rule_function(rd.rule,rd.params)
    except AttributeError as e:
        message = (f"run_rules: Could not find the requested rule called {rd.rule}")
        status = meadplugin_pb2.RuleStatus.RULE_STATUS_FAILURE
        return meadplugin_pb2.EvaluateResponse(status=status,message=message,items=rd.items,params=rd.params)
            
####################################
##### PROCESS RULES ################
####################################

    #Update the request data with latest information returned from the rule
    rd.update_params_group(message, status, items, params)
    if rd.status != meadplugin_pb2.RuleStatus.RULE_STATUS_SUCCESS:
        return meadplugin_pb2.EvaluateResponse(status=rd.status,message=rd.message,items=rd.items,params=rd.params)

    #print(f"item is {items}")
    #create protobuf instance and map to items object
    message, status, item_request_object = process_items(rd.items)
    rd.update_items_group(message, status, item_request_object.items)
    if rd.status != meadplugin_pb2.RuleStatus.RULE_STATUS_SUCCESS:
        return meadplugin_pb2.EvaluateResponse(status=rd.status,message=rd.message,items=rd.items,params=rd.params)            
    
    num_items = len(rd.items)
    print(f"num items: {num_items}")
    #Check the retrieved file count is sufficient
    if num_items > 0:
        return meadplugin_pb2.EvaluateResponse(status=rd.status,message=rd.message,items=rd.items,params=rd.params)    
    else:
        message = f"run_rule.{rd.rule}: Could not find any items"
        status = meadplugin_pb2.RuleStatus.RULE_STATUS_FAILURE
        rd.update_message_group(message,status)
        return meadplugin_pb2.EvaluateResponse(status=rd.status,message=rd.message,items=rd.items,params=rd.params)  