package main

import (
	"context"
	"log"

	"github.com/CurtTilmes/meadplugin/internal/config"
	pb "github.com/CurtTilmes/meadplugin/internal/pb"
	"github.com/CurtTilmes/meadplugin/internal/rule"
)

func (s *Server) Identify(_ context.Context, in *pb.IdentifyRequest) (response *pb.IdentifyResponse, err error) {
	log.Printf("IdentifyRequest")

	return &pb.IdentifyResponse{
		Name:    config.Config.Name,
		Version: config.Config.Version,
		Rules:   rule.IdentifyRules(),
	}, nil
}
