package main

import (
	"embed"
	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
	"github.com/Spearks/hermes/backend"
	"github.com/wailsapp/wails/v2/pkg/options/windows"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {

	// Create an instance of the app structure
	app := backend.NewApp()

	// Create application with options
	err := wails.Run(&options.App{
		Title:  "Hermes",
		Width:  1024,
		Height: 768,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		
		OnStartup:        app.Startup,
		Bind: []interface{}{
			app,
		},
		Windows: &windows.Options{
            WebviewIsTransparent:              true,
            WindowIsTranslucent:               false,
            BackdropType:                      windows.Mica,
            DisableWindowIcon:                 false,
            DisableFramelessWindowDecorations: false,
            WebviewUserDataPath:               "",
            WebviewBrowserPath:                "",
            Theme:                             windows.SystemDefault,
            CustomTheme: &windows.ThemeSettings{
                DarkModeTitleBar:   windows.RGB(20, 20, 20),
                DarkModeTitleText:  windows.RGB(200, 200, 200),
                DarkModeBorder:     windows.RGB(20, 0, 20),
                LightModeTitleBar:  windows.RGB(200, 200, 200),
                LightModeTitleText: windows.RGB(20, 20, 20),
                LightModeBorder:    windows.RGB(200, 200, 200),
            },
        },
	})

	if err != nil {
		println("Error:", err.Error())
	}
}
