# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this item except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

#grpc server setup for protobuf
import grpc
import meadplugin_pb2
import meadplugin_pb2_grpc

#MEAD server interface
from server.run_rules import run_rule, get_help, Request

#Defined MEAD processing plugin
import rule.sample as plugin

class meadplugin(meadplugin_pb2_grpc.meadpluginServicer):
    def Identify(self, request, context):
        return meadplugin_pb2.IdentifyResponse(name=plugin.PLUGIN,version=plugin.VERSION,rules=plugin.RULES)    
    
    def Help(self,request,context):
        print("starting help function")
        print(f"request rule is {request.rule}")
        #get the short and long description of the rule
        short,long = get_help(plugin,request.rule) 
        return meadplugin_pb2.HelpResponse(short=short,long=long)  

    def Evaluate(self, request, context):  
        print(f"request.rule = {request.rule}")
        #Initialize Request data (rd) Class
        rd = Request(request.request_id,request.rule,meadplugin_pb2.RuleStatus.RULE_STATUS_UNSPECIFIED,"",request.params,[])
        print(f"rule is {rd.rule}\nparams is {rd.params}\nrequest_id is {rd.request_id}")        
        return run_rule(meadplugin_pb2,plugin,rd)        

    def Insert(self, request, context):
        message = "insert not available"
        return meadplugin_pb2.InsertResponse(status=meadplugin_pb2.RuleStatus.RULE_STATUS_FAILURE,message=message)
   

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    meadplugin_pb2_grpc.add_meadpluginServicer_to_server(meadplugin(), server)
    server.add_insecure_port(f"[::]:{plugin.PORT}")
    server.start()
    print(f"Server started, listening on {plugin.PORT}")
    try: 
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Server terminated by KeyboardInterrupt (Ctrl+C).")
    

if __name__ == "__main__":
    logging.basicConfig()
    serve()