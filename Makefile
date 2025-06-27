protoc:
	protoc --go_out=./internal/pb --go_opt=paths=source_relative \
    --go-grpc_out=./internal/pb --go-grpc_opt=paths=source_relative \
    ./meadplugin.proto

list:
	grpcurl -plaintext localhost:50051 list

describe:
	grpcurl -plaintext localhost:50051 describe meaditerator.Iterator
	grpcurl -plaintext localhost:50051 describe meaditerator.Iterator.Iterate
	grpcurl -plaintext localhost:50051 describe meaditerat
	or.IterateRequest
	grpcurl -plaintext localhost:50051 describe meaditerator.IterateResponse

ORBIT_PARAMS = '{"iteration_type": 1, \
                 "max_iterations": 4, \
				 "params": { "startorbit": "4", "endorbit": "16" } }'

example_orbital:
	@grpcurl -d $(ORBIT_PARAMS) -plaintext localhost:50051 meaditerator.Iterator.Iterate

RRULE_PARAMS = '{"iteration_type": 2, \
                 "max_iterations": 3, \
				 "params": { "DTSTART" : "20250101T000000Z", \
				             "RRULE" : "FREQ=MINUTELY;INTERVAL=5;COUNT=288", \
							 "Format": "2006003.1504" } }'
example_rrule:
	@grpcurl -d $(RRULE_PARAMS) -plaintext localhost:50051 meaditerator.Iterator.Iterate
