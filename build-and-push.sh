#!/usr/bin/env bash

set -euo pipefail

docker buildx build --platform linux/amd64 -t hitchhiker-bot-frontend:main .

gcloud auth configure-docker europe-west1-docker.pkg.dev && \
docker tag hitchhiker-bot-frontend:main europe-west1-docker.pkg.dev/data-engineering-lab-411011/gar/hitchhiker-bot-frontend:"$(git rev-parse --short HEAD)" && \
docker tag hitchhiker-bot-frontend:main europe-west1-docker.pkg.dev/data-engineering-lab-411011/gar/hitchhiker-bot-frontend:latest && \
docker push europe-west1-docker.pkg.dev/data-engineering-lab-411011/gar/hitchhiker-bot-frontend --all-tags
