package backend

import (
	"archive/zip"
	"context"
	"github.com/wailsapp/wails/v2/pkg/runtime"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func Unzip(src, dest string) error {
    r, err := zip.OpenReader(src)
    if err != nil {
        return err
    }
    defer r.Close()

    for _, f := range r.File {
        rc, err := f.Open()
        if err != nil {
            return err
        }
        defer rc.Close()

        fpath := filepath.Join(dest, f.Name)
        if f.FileInfo().IsDir() {
            os.MkdirAll(fpath, os.ModePerm)
        } else {
            var fdir string
            if lastIndex := strings.LastIndex(fpath, string(os.PathSeparator)); lastIndex > -1 {
                fdir = fpath[:lastIndex]
            }

            err = os.MkdirAll(fdir, os.ModePerm)
            if err != nil {
                log.Fatal(err)
                return err
            }
            f, err := os.OpenFile(
                fpath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
            if err != nil {
                return err
            }
            defer f.Close()

            _, err = io.Copy(f, rc)
            if err != nil {
                return err
            }
        }
    }
    return nil
}

func CheckAndInstallPrometheus(a *App) {
    home, err := os.UserHomeDir()
    if err != nil {
        log.Fatal(err)
    }

    prometheusDir := filepath.Join(home, ".hermes", "prometheus")

    if _, err := os.Stat(prometheusDir); os.IsNotExist(err) {
        runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{Title: "Grafana setup", Message: "Prometheus not found. This is required for Hermes to work. Click 'OK' to install Prometheus"})
        log.Println("[STARTUP] Prometheus not found, downloading...")

        resp, err := http.Get("https://github.com/prometheus/prometheus/releases/download/v2.45.2/prometheus-2.45.2.windows-amd64.zip")
        if err != nil {
            log.Fatal(err)
        }
        defer resp.Body.Close()

        out, err := os.Create(filepath.Join(home, ".hermes", "prometheus.zip"))
        if err != nil {
            log.Fatal(err)
        }
        defer out.Close()

        _, err = io.Copy(out, resp.Body)
        if err != nil {
            log.Fatal(err)
        }

        err = Unzip(filepath.Join(home, ".hermes", "prometheus.zip"), prometheusDir)
        if err != nil {
            log.Fatal(err)
        }
    }
}

func CheckAndInstallGrafana(a *App) {
	home, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
	}

	grafanaDir := filepath.Join(home, ".hermes", "grafana")

	if _, err := os.Stat(grafanaDir); os.IsNotExist(err) {
		runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{Title: "Grafana setup", Message: "Grafana not found. This is required for Hermes to work. Click 'OK' to install Grafana"})
		log.Println("[STARTUP] Grafana not found, downloading...")

		resp, err := http.Get("https://dl.grafana.com/oss/release/grafana-10.2.3.windows-amd64.zip")
		if err != nil {
			log.Fatal(err)
		}
		defer resp.Body.Close()

		out, err := os.Create(filepath.Join(home, ".hermes", "grafana.zip"))
		if err != nil {
			log.Fatal(err)
		}
		defer out.Close()

		_, err = io.Copy(out, resp.Body)
		if err != nil {
			log.Fatal(err)
		}

		log.Println("[STARTUP] Unzipping Grafana...")

        err = Unzip(filepath.Join(home, ".hermes", "grafana.zip"), grafanaDir)
        if err != nil {
            log.Fatal(err)
        }

		// log.Println("[STARTUP] Grafana installed! Purging pre-made provisioning files")
		// provisioningDir := filepath.Join(grafanaDir, "grafana-v10.2.3", "conf", "provisioning")
		// err = os.RemoveAll(provisioningDir)
		// if err != nil {
		// 	log.Fatal(err)
		// }

		// log.Println("[STARTUP] Provisioning directory purged")
	} else {
		log.Println("[STARTUP] Grafana already installed!")
	}
}

func (a *App) Startup(ctx context.Context) {
	
	log.Println("[STARTUP] Startup called!")
	a.ctx = ctx

	log.Println("[STARTUP] Checking for Prometheus instance")
	CheckAndInstallPrometheus(a)

	log.Println("[STARTUP] Checking for Grafana instance")
	CheckAndInstallGrafana(a)

	log.Println("[STARTUP] Starting Grafana")
	RunGrafana()

	log.Println("[STARTUP] Starting Prometheus")
	RunPrometheus()
}
