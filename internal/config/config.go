package config

import (
	"log"
	"os"
	"regexp"

	_ "github.com/joho/godotenv/autoload"
	"gopkg.in/yaml.v3"
)

var Config meadpluginConfig

type meadpluginConfig struct {
	Listen  string `yaml:"listen"`
	Name    string `yaml:"name"`
	Version string `yaml:"version"`
}

func init() {
	configFile := os.Getenv("MEADPLUGIN_CONFIG")
	if configFile == "" {
		log.Fatal("Must specify MEADPLUGIN_CONFIG")
	}

	config, err := os.ReadFile(configFile)
	if err != nil {
		log.Fatalf("Couldn't read config file %q", configFile)
	}

	err = yaml.Unmarshal(config, &Config)
	if err != nil {
		log.Fatalf("Couldn't parse config file %q", configFile)
	}

	if Config.Listen == "" {
		log.Fatalf("Must specify listen in config")
	}

	if Config.Name == "" {
		log.Fatalf("Must specify name in config")
	}

	if Config.Version == "" {
		log.Fatalf("Must specify version in config")
	}

	r := regexp.MustCompile(`^\d+\.\d+\.\d+-\d+$`)
	if !r.MatchString(Config.Version) {
		log.Fatalf("Bad Version for %q", Config.Version)
	}
}
