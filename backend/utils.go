package backend

import (
	"log"
	"os"
	"path/filepath"
	"os/exec"
)

func RunGrafana() {
	home, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
	}

	grafanaHome := filepath.Join(home, ".hermes", "grafana", "grafana-v10.2.3")
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

	// C:\Users\Ace\.hermes\prometheus\prometheus-2.45.2.windows-amd64

	prometheus := filepath.Join(home, ".hermes", "prometheus", "prometheus-2.45.2.windows-amd64", "prometheus.exe")

	s := []string{"cmd.exe", "/C", "start", prometheus}

	cmd := exec.Command(s[0], s[1:]...)


	log.Println(cmd)

	if err := cmd.Run(); err != nil {
		log.Println("Error:", err)
	}

}