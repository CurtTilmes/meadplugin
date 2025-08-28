#get help

def get_help(function_module,rule):

    try:
        rule_function = getattr(function_module, rule) 
        help_string = rule_function.__doc__    
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
        return "rule not found","N/A"