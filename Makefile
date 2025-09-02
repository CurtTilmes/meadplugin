DEFAULTLISTEN = localhost:50051

all: go python

go:
	protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    meadplugin.proto

python:
	pip install grpcio grpcio-tools protobuf 
	python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. meadplugin.proto

protoc:
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

sample_go:
	go run ./sample_go/ $(DEFAULTLISTEN)

describe:
	@grpcurl -proto meadplugin.proto -plaintext describe meadplugin.meadplugin     

identify:
	@grpcurl -proto meadplugin.proto -plaintext $(DEFAULTLISTEN) meadplugin.meadplugin.Identify      

help:
	@grpcurl -proto meadplugin.proto -d '{"rule":"samplerule"}' -plaintext $(DEFAULTLISTEN) meadplugin.meadplugin.Help

# Reads the request as JSON on STDIN, run like "make evaluate < example/ex1.json
evaluate:
	@grpcurl -proto meadplugin.proto -d @ -plaintext $(DEFAULTLISTEN) meadplugin.meadplugin.Evaluate

.PHONY: all go protoc python sample_go describe identify help evaluate
