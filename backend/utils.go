package backend

import (
	"log"
	"os"
	"path/filepath"
	"os/exec"
	"fmt"
)

func ReturnVerisons() Config {

	grafanaVersion := os.Getenv("GRAFANA_VERSION")
	grafanaFile := fmt.Sprintf("grafana-%s.windows-amd64", grafanaVersion) 
	grafanaString := fmt.Sprintf("grafana-v%s", grafanaVersion)
	

	prometheusVersion := os.Getenv("PROMETHEUS_VERSION")
	prometheusFile := fmt.Sprintf("prometheus-%s.windows-amd64", prometheusVersion)
    
	return Config {
		GrafanaVersion: grafanaFile,
		GrafanaDir: grafanaFile,
		GrafanaString: grafanaString,
		PrometheusVersion: prometheusVersion,
		PrometheusFile: prometheusFile,
	}
}

func RunGrafana() {
	home, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
	}

	loadedConfig := ReturnVerisons()

	grafanaHome := filepath.Join(home, ".hermes", "grafana", loadedConfig.GrafanaString)
	grafanaExec := filepath.Join(grafanaHome, "bin", "grafana.exe")

	s := []string{"cmd.exe", "/C", "start", grafanaExec, "server", "-homepath", grafanaHome}

	cmd := exec.Command(s[0], s[1:]...)
	
	log.Println(cmd)

	if err := cmd.Run(); err != nil {
		log.Println("Error:", err)
	}
}

func RunPrometheus() {
	home, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
	}

	loadedConfig := ReturnVerisons()

	prometheus := filepath.Join(home, ".hermes", "prometheus", loadedConfig.PrometheusFile, "prometheus.exe")

	s := []string{"cmd.exe", "/C", "start", prometheus}

	cmd := exec.Command(s[0], s[1:]...)

	log.Println(cmd)

	if err := cmd.Run(); err != nil {
		log.Println("Error:", err)
	}

}