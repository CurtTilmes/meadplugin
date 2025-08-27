package main

import (
	"log"
	"os"

	"github.com/CurtTilmes/meadplugin/go/server"
	_ "github.com/CurtTilmes/meadplugin/sample/rule" // Register rules
)

func main() {
	listen := ":50051"

	if len(os.Args) > 1 && os.Args[1] != "" {
		listen = os.Args[1]
	}

	s := &server.Server{
		PluginName:    "Sample",
		PluginVersion: "1.0.0-1",
		Listen:        listen,
	}

	if err := s.Serve(); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}
