# MEAD Plugin

This is part of the _Adaptive Processing System_ (APS) _Metadata Extract and Access Database_ (MEAD).

MEAD uses an extensible collection of Plugins to operate.

The MEAD central server communicates with plugins using [gRPC](https://grpc.io).

The MEAD communication protocol, built on top of Protocol Buffers or [protobuf](https://protobuf.dev/)s is
described in this repository.

The ```meadplugin.proto``` establishes the *contract* between MEAD and its plugins.  The protocol is 
summarized here, but the details in that file define the protocol precisely.

MEAD plugins can be developed in any language as long as the comply with the gRPC/protobuf/meadplugin protocol.

# Services

Each plugin can offer a number of services to MEAD.  All are optional except for _Identify_ with must be offered.

## Identify

On startup and periodically, MEAD calls each plugin with an _Identify_ request.

Response:
```
     name: MyPlugin
     version: 1.2.3-4
     rules:
       - some_rule
       - another_rule 
```

## Evaluate

Evaluate Request:
```
request_id: a616bb6a-d8a7-4ba4-b27f-b566fef2163b
rule: some_rule
params:
  ESDT: MOD03
  collection: "061"
  key: 2025156.1150
```

Evaluate Response:
```
request_id: a616bb6a-d8a7-4ba4-b27f-b566fef2163b
status: SUCCESS or FAILURE or RETRY or SKIP
message: "arbitrary string"
params:
  some_key: some_value
files:
  - modaps-lads/MOD03/MOD03.A2025156.1150.061.2025156165003.hdf
```

If the rule succeeds, status will be set to ```SUCCESS``` and any additional params for the job
or input files needed for execution of the job will be returned.

If the job should be skipped, status will be set to ```SKIP``` (for example, the required input
data were not captured by the observatory due to some maneuver, or land processing is being
performed, but the tile is all water, or daytime processing is needed, but the data are all night.)
This is a perfectly normal response, and will cause the Job to go immediately to the complete state.

If some data needed by the rule is unavailable, but may become available later, ```RETRY``` is
returned. 

If something is required by the rule, but is unavailable and will NEVER become available ```FAILURE```
can be returned.   Note this is distinct from an Error.  This causes the Job to immediately go to
the error state.

An ```Error``` can also be returned from the call.  This could be due to a down database or
external service, or the plugin is broken in some way.  It doesn't necessarily indicate a problem
with the Plan or Job, just that something in the infrastructure isn't able to successfully execute
the rule at this time.  The Job is treated the same as a ```RETRY``` but an ```Error``` should be brought
to the attention of an administrator.

For any return, either a normal return, or an Error return, a message can accompany the return.

# License
Copyright © 2023 United States Government as represented by the Administrator 
of the National Aeronautics and Space Administration. No copyright is claimed 
in the United States under Title 17, U.S. Code. All Other Rights Reserved.
