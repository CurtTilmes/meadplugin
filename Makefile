identify:
	grpcurl -proto internal/pb/meadplugin.proto -plaintext localhost:50051 meadplugin.meadplugin.Identify

evaluate:
	@grpcurl -proto internal/pb/meadplugin.proto -d @ -plaintext localhost:50051 meadplugin.meadplugin.Evaluate
	
protoc:
	cd internal/pb && protoc --go_out=. --go_opt=paths=source_relative \
    --go-grpc_out=. --go-grpc_opt=paths=source_relative \
    meadplugin.proto
