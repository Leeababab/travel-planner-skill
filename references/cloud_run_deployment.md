# Google Cloud Run Deployment Guide

## Architecture
Deploy static travel web apps (interactive Leaflet map + in-browser PDF/PNG reader) using lightweight Nginx containers to Google Cloud Run in regional low-latency clusters (e.g. `asia-east2` Hong Kong).

## Multi-Service Deploy Command
```bash
# Deploy New Zealand South Island Site
gcloud run deploy nz-travel-2026   --source=./2026_New_Zealand_South_Island   --project=travel-505803   --region=asia-east2   --allow-unauthenticated   --port=80

# Deploy Osaka Kansai Site
gcloud run deploy kansai-travel-2026   --source=./2026_Osaka_Trip   --project=travel-505803   --region=asia-east2   --allow-unauthenticated   --port=80
```
