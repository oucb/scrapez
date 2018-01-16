#!/bin/bash
export C_FORCE_ROOT=true
celery worker -A celeryapp:app -l info
