#Sample Rule# plugin
import meadplugin_pb2

#Here rules are functions
PLUGIN = "Sample" #Name of plugin
VERSION = "1.0.0-1" #Version of this plugin
RULES = ["samplerule"]  #List of Rules of this plugin
PORT = 50050 #Listening port for this plugin

def samplerule(rule,params):
    """
* User Help:

** Short Description:
   This is a sample rule.

** Long Description:
   Long help for sample rule. Can include *markdown*.
   
    """
#As shown above, samplerule description information must follow formatting as shown below from """ to """
    try:    
        print("Evaluating samplerule")

        if params["makeanerror"] != "":
            return "", meadplugin_pb2.RuleStatus.RULE_STATUS_FAILURE
        
        if params["panic"] != "":
            return "Panic", meadplugin_pb2.RuleStatus.RULE_STATUS_UNSPECIFIED
        
        if params["skipthisone"] != "":
            return "Skip", meadplugin_pb2.RuleStatus.RULE_STATUS_SKIP
        
        if params["retry"] != "":
            return "Retry", meadplugin_pb2.RuleStatus.RULE_STATUS_RETRY
        
        if params["failure"] != "":
            return "Failure", meadplugin_pb2.RuleStatus.RULE_STATUS_FAILURE
        #remove the error flag keys to match params output in example
        keys_to_remove = [key for key, value in params.items() if value == '']
        for key in keys_to_remove: 
            del params[key]
        
        params["ESDT"] = "MOD02HKM"
        params["something"] = "whatever you want"

        #rule response items
        json_items = [{"id":"group/prefix/filename.hdf", \
                        "metadata": { \
                                    "ESDT":"someesdt" \
                                    } } ]
        
        item2 = {"id" : "modaps-lads/MOD03/MOD03.blahblah.hdf"}
        json_items.append(item2)
        items = {"items":json_items}

        return "Success",meadplugin_pb2.RuleStatus.RULE_STATUS_SUCCESS,items,params

    except Exception as e:
        print(f"{PLUGIN}.{rule}: inside server exeception")
        return str(e), meadplugin_pb2.RuleStatus.RULE_STATUS_FAILURE,[],{}