package backend

import (
	"context"
	"log"
)

func (a *App) Startup(ctx context.Context) {
	a.ctx = ctx

	log.Println("[STARTUP] Startup called!")

	log.Println("[STARTUP] Checking for Grafana instance")
}