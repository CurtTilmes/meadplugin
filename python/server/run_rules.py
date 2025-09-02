from google.protobuf import json_format

def get_help(function_module,rule):
    print(f"inside get help, rule is {rule}")
    try:
        rule_function = getattr(function_module, rule) 
        print(f"getting help for {rule}")
        help_string = rule_function.__doc__    
        print(f"help string is \n {help_string}")
        sections = help_string.split("\n** ")

        try:
            short_description = [section for section in sections if section.startswith("Short Description")][0]
            short = short_description.split(":")[1:]
            
            chars_to_remove = ['\n', ' ']
            short = short[0] #convert list to string
            for char in chars_to_remove:
                short = short.replace(char,"")  
        except:
            return "short description not defined","N/A"
        
        try:
            long_description = [section for section in sections if section.startswith("Long Description")][0]        
            long = long_description.split(":",1)[1]            
            long = long.replace("* Developer Help:","")
        except:
            return short,"long description not defined"      

        return short,long    
    except AttributeError as e:
        return "rule not found in Help","N/A"
    
class Request:
    def __init__(self, request_id, rule, status, message, params, items):
        self.request_id = request_id
        self.rule = rule
        self.status = status
        self.message = message
        self.params = params
        self.items = items

    def update_status(self, new_status):
        self.status = new_status
    
    def update_message(self, new_message):
        self.message = new_message   

    def update_items(self, new_items):
        self.items = new_items

    def update_params(self, new_params):
        self.params = new_params

    def update_message_group(self, new_message, new_status):
        self.update_message(new_message)
        self.update_status(new_status)

    def update_items_group(self, new_message, new_status, new_items):
        self.update_message_group(new_message, new_status)
        self.update_items(new_items)      
    
    def update_params_group(self, new_message, new_status, new_items, new_params):
        self.update_items_group(new_message, new_status, new_items)
        self.update_params(new_params)

def process_items(meadplugin_pb2, items):
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

def run_rule(meadplugin_pb2,function_module,rd):
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
    message, status, item_request_object = process_items(meadplugin_pb2,rd.items)
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