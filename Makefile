DEFAULTLISTEN = localhost:50051

all: go python

go:
	protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    meadplugin.proto

protoc:
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

python:
	grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. meadplugin.proto

start:
	go run ./sample/ $(DEFAULTLISTEN)

describe:
	@grpcurl -proto meadplugin.proto -plaintext describe meadplugin.meadplugin     

identify:
	@grpcurl -proto meadplugin.proto -plaintext $(DEFAULTLISTEN) meadplugin.meadplugin.Identify      

help:
	@grpcurl -proto meadplugin.proto -d '{"rule":"samplerule"}' -plaintext $(DEFAULTLISTEN) meadplugin.meadplugin.Help

evaluate:
	@grpcurl -proto meadplugin.proto -d @ -plaintext $(DEFAULTLISTEN) meadplugin.meadplugin.Evaluate

.PHONY: all go protoc python start describe identify help evaluate
