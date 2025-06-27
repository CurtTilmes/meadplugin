package main

import (
	"log"
	"net"

	"github.com/CurtTilmes/meadplugin/internal/config"
	pb "github.com/CurtTilmes/meadplugin/internal/pb"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

type Server struct {
	pb.UnimplementedMeadpluginServer
}

func main() {
	lis, err := net.Listen("tcp", config.Listen())
	if err != nil {
		log.Fatalf("failed to listen to %q: %v", config.Listen(), err)
	}
	s := grpc.NewServer()
	pb.RegisterMeadpluginServer(s, &Server{})
	reflection.Register(s) // useful for testing, remove for production
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
