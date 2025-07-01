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
     name: My Cool Plugin
     version: 1.2.3-4
     rules:
       - name: some_rule
         version: 2.3.1-5
         rule_params:
           some_key: some_value
           key2: value2
         job_params:
          - key
          - ESDT
       
```

The ```rule_params``` defines specific parameters that must be true for this rule to be successfully 
executed by this plugins.  For example, if the rule was ```get-orbital-parameters```, the
```rule_params``` might include ```sensor=Aura-OMI``` to note that this plugin knows how to look up
orbital parameters for that sensor.

```job_params``` are other parameters that the rule uses to evaluate the rule.

## Evaluate

Evaluate Request:
```
rule_name: some_rule
params:
  ESDT: MOD03
  collection: "061"
  key: 2025156.1150
```

The ```params``` in an _Evaluate_ call will match those described for the rule in _Identify_.

Evaluate Response:
```
status: SUCCESS or SKIP or RETRY or FAILURE
message: "arbitrary string"
job_params:
  some_key: some_value
files:
  - modaps-lads/MOD03/MOD03.A2025156.1150.061.2025156165003.hdf
```

If the rule succeeds, status will be set to ```SUCCESS``` and any additional params for the job
or input files needed for execution of the job will be returned.

If the job should be skipped, status will be set to ```SKIP``` (for example, the required input
data were not captured by the observatory due to some maneuver, or land processing is being
performed, but the tile is all water, or daytime processing is needed, but the data are all night.)
This is a perfectly normal response.

If the required input is not available, but might be available later, ```RETRY``` is returned.

If something went wrong in the rule evaluation, ```FAILURE``` is returned.  This indicates that
evaluation proceeded normally, but due to something, the evaluation as submitted can never
succeed.  The Job should move to the error state and be brought to the attention of someone.  The
Plan and Jobs will need to be reworked.  Note this is distinct from an Error.

An ```Error``` can also be returned from the call.  This could be due to a down database or
external service, or the plugin is broken in some way.  It doesn't necessarily indicate a problem
with the Plan or Job, just that something in the infrastructure isn't able to successfully execute
the rule at this time.  The Job is treated the same as a ```RETRY``` but an ```Error``` should be brought
to the attention of an administrator.

# License
Copyright © 2023 United States Government as represented by the Administrator 
of the National Aeronautics and Space Administration. No copyright is claimed 
in the United States under Title 17, U.S. Code. All Other Rights Reserved.
