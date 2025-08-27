package server

import (
	"context"
	"fmt"
	"log"
	"maps"
	"net"
	"slices"

	"github.com/CurtTilmes/meadplugin"
	"github.com/CurtTilmes/meadplugin/go/rule"
	"google.golang.org/grpc"
)

type ServerOption func(*Server)

type Server struct {
	meadplugin.UnimplementedMeadpluginServer
	PluginName    string
	PluginVersion string
	Listen        string
}

func (s *Server) Serve() (err error) {
	lis, err := net.Listen("tcp", s.Listen)
	if err != nil {
		return fmt.Errorf("listen to %s: %v", s.Listen, err)
	}

	g := grpc.NewServer()

	meadplugin.RegisterMeadpluginServer(g, s)

	log.Printf("Server listening at %v", lis.Addr())

	if err := g.Serve(lis); err != nil {
		return fmt.Errorf("failed to serve: %v", err)
	}

	return nil
}

func (s *Server) Identify(_ context.Context, in *meadplugin.IdentifyRequest) (*meadplugin.IdentifyResponse, error) {
	log.Printf("IdentifyRequest")

	return &meadplugin.IdentifyResponse{
		Name:    s.PluginName,
		Version: s.PluginVersion,
		Rules:   slices.Sorted(maps.Keys(rule.RuleTable)),
	}, nil
}

func (s *Server) Help(_ context.Context, in *meadplugin.HelpRequest) (*meadplugin.HelpResponse, error) {
	log.Printf("HelpRequest %s", in.GetRequestId())

	return &meadplugin.HelpResponse{
		Short: rule.RuleTable[in.GetRule()].ShortHelp,
		Long:  rule.RuleTable[in.GetRule()].LongHelp,
	}, nil
}

func (s *Server) Evaluate(ctx context.Context, in *meadplugin.EvaluateRequest) (resp *meadplugin.EvaluateResponse, err error) {
	log.Printf("EvaluateRequest %s", in.GetRequestId())

	name := in.GetRule()
	params := in.GetParams()

	rule, ok := rule.RuleTable[name]
	if !ok {
		return nil, fmt.Errorf("unknown rule %q", name)
	}

	defer func() {
		if r := recover(); r != nil {
			log.Printf("Evaluate crashed, requestid: %s rule %s", in.GetRequestId(), rule.Name)
			err = fmt.Errorf("Evaluate crashed, rule %s", rule.Name)

		}
	}()

	resp, err = rule.EvalFunc(ctx, params)

	return resp, err
}
