IMAGE = ghcr.io/mamercad/prometheus-tailscale-exporter:devel
.DEFAULT_GOAL = build

.PHONY: requirements
requirements:
	poetry export \
		--format requirements.txt \
		--output requirements.txt \
		--without-hashes

.PHONY: build
build: requirements
	docker build \
		--tag $(IMAGE) .

.PHONY: run
run: build
	docker run \
		--rm --interactive --tty \
		--publish 8000:8000/tcp \
		--env TAILSCALE_API_KEY \
		--env TAILSCALE_TAILNET \
		$(IMAGE)
