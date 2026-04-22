#!/bin/bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
[auth]
redirect_uri = "${AUTH0_REDIRECT_URI}"
cookie_secret = "${COOKIE_SECRET}"

[auth.auth0]
client_id = "${AUTH0_CLIENT_ID}"
client_secret = "${AUTH0_CLIENT_SECRET}"
server_metadata_url = "https://${AUTH0_DOMAIN}/.well-known/openid-configuration"
EOF
streamlit run app.py --server.port $PORT --server.address 0.0.0.0