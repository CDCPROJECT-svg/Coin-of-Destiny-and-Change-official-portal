#!/bin/bash
# Protect the previous code and environment
export SUPABASE_DB_URL="your_supabase_url_here"
echo "Starting CDC Sovereign Portal in Production Mode..."
gunicorn -w 4 -b 0.0.0.0:8080 app:app --daemon
echo "Portal is now running in the background (Daemon Mode)."
