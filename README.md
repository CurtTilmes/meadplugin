# meadplugin
Template MEAD plugin in Go, with gRPC

# Test the server

(If you ran the server on a port other than the default ```localhost:50051``` just change the lines below)

Ask the server to list its services:
```
grpcurl -plaintext localhost:50051 list
```

```
grpc.reflection.v1.ServerReflection
grpc.reflection.v1alpha.ServerReflection
meadplugin.meadplugin
```

Describe the plugin service rpcs:
```
grpcurl -plaintext localhost:50051 describe meadplugin.meadplugin
```
```
meadplugin.meadplugin is a service:
service meadplugin {
  rpc Evaluate ( .meadplugin.EvaluateRequest ) returns ( .meadplugin.EvaluateResponse );
  rpc Identify ( .meadplugin.IdentifyRequest ) returns ( .meadplugin.IdentifyResponse );
  rpc Insert ( .meadplugin.InsertRequest ) returns ( .meadplugin.InsertResponse );
}

You can describe each of those services and messages further:
```
grpcurl -plaintext localhost:50051 describe meadplugin.meadplugin.Evaluate
grpcurl -plaintext localhost:50051 describe meadplugin.EvaluateRequest
grpcurl -plaintext localhost:50051 describe meadplugin.EvaluateResponse
```
etc.

Execute Identify()
```
grpcurl -d '{}' -plaintext localhost:50051 meadplugin.meadplugin.Identify
```

(```make identify``` will do this too.)

It will describe the rules offered by the plugin:
```
{
  "name": "MEAD Plugin Template",
  "version": "1.0.0-1",
  "rules": [
    {
      "name": "samplerule",
      "version": "1.2.3-4",
      "ruleParams": {
        "some-param": "some-value"
      },
      "jobParams": [
        "another-param"
      ]
    }
  ]
}
```
