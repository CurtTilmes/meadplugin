protoc:
	protoc --go_out=./internal/pb --go_opt=paths=source_relative \
    --go-grpc_out=./internal/pb --go-grpc_opt=paths=source_relative \
    ./meadplugin.proto

list:
	grpcurl -plaintext localhost:50051 list

PARAMS = '{"rule_name": "samplerule", \
           "params": { \
		     "some-param": "some-value", \
			 "another-param": "foobar" } }'

evaluate:
	@grpcurl -d $(PARAMS) -plaintext localhost:50051 meadplugin.meadplugin.Evaluate
	
identify:
	grpcurl -d '{}' -plaintext localhost:50051 meadplugin.meadplugin.Identify
