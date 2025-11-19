#!/usr/bin/env bash
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
