package backend

import (
	"log"
	"os"
	"path/filepath"

)

func (a *App) CheckIfConfigExists() error {
	home, err := os.UserHomeDir()
    if err != nil {
        log.Fatal(err)
    }

    grafanaDir := filepath.Join(home, ".hermes", "grafana", "grafana-v10.2.3")

    if _, err := os.Stat(grafanaDir); os.IsNotExist(err) {
		log.Println("[backend.config.CheckIfConfigExists] Config does not exists")
		return err
	} else {
		log.Println("[backend.config.CheckIfConfigExists] Config exists")
		return nil
	}
}

func (a *App) EntryConfig(directory string) error {
	log.Println("[backend.config.EntryConfig] Checking for config's")


	// file, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
	// 	Title: "Select a config file",
	// 	DefaultDirectory: "",
	// })

	// if err != nil {
	// 	log.Println("[backend.config.EntryConfig] Error opening file dialog")
	// 	return err
	// } else {
	// 	log.Println(file)
	// }

	return nil
}