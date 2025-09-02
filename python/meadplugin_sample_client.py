# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import meadplugin_pb2
import meadplugin_pb2_grpc

from rule.sample import PORT
from google.protobuf.json_format import MessageToDict
import json

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    porthost = f"localhost:{PORT}"
    with grpc.insecure_channel(porthost) as channel:       
        
        stub = meadplugin_pb2_grpc.meadpluginStub(channel) 

        #Example request ID
        request_id = "616bb6a-d8a7-4ba4-b27f-b566fef2163b"

        #### Identify Response ####
        response = stub.Identify(meadplugin_pb2.IdentifyResponse())  
        responsedict = MessageToDict(response)
        print(f"Identify Response:")
        print(json.dumps(responsedict, indent=2))           
        rule = response.rules[0] # get the first rule from the sample

        #### Help Response ####
        request = meadplugin_pb2.HelpRequest(request_id=request_id,rule=rule)  
        response = stub.Help(request)
        print(f"Help Response:")
        responsedict = MessageToDict(response)
        print(json.dumps(responsedict, indent=2))   
        
        #### Evaluate Request ####        
        params = {}
        params["some-param"] = "some-value"
        params["another-param"] = "foobar"
        request = meadplugin_pb2.EvaluateRequest(request_id=request_id,rule=rule, params=params)        
        print(f"Evaluate Request:")
        requestdict = MessageToDict(request)
        print(json.dumps(requestdict, indent=2))   

        #### Evaluate Response ####
        response = stub.Evaluate(request)
        responsedict = MessageToDict(response)
        print(f"Evaluate Response:")
        print(json.dumps(responsedict, indent=2))   

if __name__ == "__main__":
    logging.basicConfig()
    run()