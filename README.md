# meadplugin
Template MEAD plugin in Go, with gRPC

# Test the server

(If you ran the server on a port other than the default ```localhost:50051``` just change the lines below)

Execute The plugin's Identify() RPC
```
grpcurl -proto internal/pb/meadplugin.proto -plaintext localhost:50051 meadplugin.meadplugin.Identify
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

Call the Evaluate RPC on one of the examples:
```
grpcurl -proto internal/pb/meadplugin.proto -d @ -plaintext localhost:50051 meadplugin.meadplugin.Evaluate < examples/ex1.json
```
(```make evaluate < examples/ex1.json``` will do this too)
