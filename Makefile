go:
	protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    meadplugin.proto

python:
	protoc --python_out=. --pyi_out=. meadplugin.proto
