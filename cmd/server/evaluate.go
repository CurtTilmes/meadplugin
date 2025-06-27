package main

import (
	"context"
	"log"

	pb "github.com/CurtTilmes/meadplugin/internal/pb"
	"github.com/CurtTilmes/meadplugin/internal/rule"
)

func (s *Server) Evaluate(ctx context.Context, in *pb.EvaluateRequest) (response *pb.EvaluateResponse, err error) {
	log.Printf("EvaluateRequest")
	return rule.Evaluate(ctx, in)
}
