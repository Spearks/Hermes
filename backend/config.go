package backend

import (
	"log"
	"os"
	"path/filepath"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

func CheckIfConfigExists() error {
	home, err := os.UserHomeDir()
    if err != nil {
        log.Fatal(err)
    }

    grafanaDir := filepath.Join(home, ".hermes", "json")

    if _, err := os.Stat(grafanaDir); os.IsNotExist(err) {
		log.Println("[backend.config.CheckIfConfigExists] Config does not exists")
		return err
	} else {
		log.Println("[backend.config.CheckIfConfigExists] Config exists")
		return nil
	}
}

func AskForConfigFile(a *App) {
	err := CheckIfConfigExists()
	if err != nil {
		log.Println("[backend.config.AskForConfigFile] Config does not exists")

		file, err := runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
			Title: "Select a config file",
			DefaultDirectory: "",
		})
	
		if err != nil {
			log.Println("[backend.config.AskForConfigFile] Error opening file dialog")
		} 
		log.Println(file)

	} else {
		log.Println("[backend.config.AskForConfigFile] Config exists")
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