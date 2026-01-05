# ESP01S Web Server

Simple Flask server to control ESP01S relay via HTTP.

Endpoints:
- GET /relay
- POST /relay { "state": "ON" | "OFF" }

Designed for Render free hosting.
