
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