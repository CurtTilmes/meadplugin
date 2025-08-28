# MEAD Plugin

This is part of the _Adaptive Processing System_ (APS) _Metadata Extract and Access Database_ (MEAD).

MEAD uses an extensible collection of Plugins to operate.

The MEAD central server communicates with plugins using [gRPC](https://grpc.io).

The MEAD communication protocol, built on top of Protocol Buffers or [protobuf](https://protobuf.dev/)s is
described in this repository.

The ```meadplugin.proto``` establishes the *contract* between MEAD and its plugins.  The protocol is 
summarized here, but the details in that file define the protocol precisely.

MEAD plugins can be developed in any language as long as they comply with the gRPC/protobuf/meadplugin protocol.

The tool [gRPCurl](https://github.com/fullstorydev/grpcurl) can be useful in development and testing MEAD plugins.

# Services

Each plugin can offer a number of services to MEAD.   The ```Makefile``` has a few targets that call ```grpcurl```
to interact with the sample plugin:

```
make describe                              # Describe the meadplugin services
make sample_go                             # Start the sample Go server
make identify                              # Call the sample Identify service
make help                                  # Call the sample Help service
make evaluate < sample/example/ex1.json    # Call the sample Evaluate service with one of the example calls
```

## Identify

On startup and periodically, MEAD calls each plugin with an _Identify_ request.

Response:
```
{
  "name": "Sample",
  "version": "1.0.0-1",
  "rules": [
    "samplerule"
  ]
}
```

## Help

Short/Long help for each rule can be displayed to potential users of the rule and should describe why/how to use the rule.
The APS rule browser tools render the long help with markdown.

Help Request:
```
{"rule":"samplerule"}
```

Help Response:
```
{
  "short": "This is a sample rule.",
  "long": "Long help for sample rule. Can include *markdown*."
}
```

## Evaluate

Evaluate Request:
```
{
    "request_id": "616bb6a-d8a7-4ba4-b27f-b566fef2163b",
    "rule": "samplerule",
    "params":
    {
        "some-param": "some-value",
        "another-param": "foobar"
    }
}
```

Evaluate Response:
```
{
  "status": "RULE_STATUS_SUCCESS",
  "params": {
    "ESDT": "MOD02HKM",
    "something": "whatever you want"
  },
  "items": [
    {
      "id": "group/prefix/filename.hdf",
      "metadata": {
        "ESDT": "someesdt"
      }
    },
    {
      "id": "modaps-lads/MOD03/MOD03.blahblah.hdf"
    }
  ]
}
```

If the rule succeeds, status will be set to ```SUCCESS``` and any additional params for the job
or input files needed for execution of the job will be returned.

```params``` are arbitrary key/value pairs that will be used in production for this job.

```items``` is an array of files, each items includes at least an ```id``` and can optionally include
arbtrary key/value pairs as associated metadata for the item.  Typical fields might include ESDT
with type of data in a file, or a digital signature for a file.

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
to the attention of an administrator to investigate.

For any return, either a normal return, or an Error return, a message can accompany the return.

# Building a MEAD Plugin in Go

The top level directory includes basic gRPC boilerplate for constructing a ```meadplugin```.

The ```go``` subdirectory includes a little more that might be helpful to build a meadplugin.

A sample plugin that implements a sample rule using that infrastructue is included in the ```sample``` 
subdirectory.  It includes ```main.go``` that starts a basic server, and ```sample.go``` that shows
a little bit of how a rule might work, including creating a response structure, setting parameters, 
and adding files to return.

To create a new MEAD plugin in Go, start with those files.

# License
Copyright © 2025 United States Government as represented by the Administrator 
of the National Aeronautics and Space Administration. No copyright is claimed 
in the United States under Title 17, U.S. Code. All Other Rights Reserved.
