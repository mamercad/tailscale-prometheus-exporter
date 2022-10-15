# [Prometheus](https://prometheus.io) Exporter for [Tailscale](https://tailscale.com)

[![docker-image](https://github.com/mamercad/prometheus-tailscale-exporter/actions/workflows/docker-image.yml/badge.svg)](https://github.com/mamercad/prometheus-tailscale-exporter/actions/workflows/docker-image.yml)

[Prometheus](https://prometheus.io) metrics of your [Tailscale](https://tailscale.com) data.

There's Docker stuff [here](./docker), Kubernetes stuff [here](./kubernetes), and SystemD stuff [here](./systemd).

It behaves like this:

```bash
❯ curl -s localhost:8000 | grep tailscale
# HELP tailscale_total_devices Total devices
# TYPE tailscale_total_devices gauge
tailscale_total_devices 16.0
```

You'll need to set `$TAILSCALE_API_KEY` and `$TAILSCALE_TAILNET`, you can find information on the Tailscale API [here](https://github.com/tailscale/tailscale/blob/main/api.md). Optionally, you can suffix the environment variables with `_FILE` and point to a local file containing the desired value.
