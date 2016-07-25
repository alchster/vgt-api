import os
import binascii

settings = dict(
        DEBUG=True,
        TESTING=True,
        PRESERVE_CONTEXT_ON_EXCEPTION=True,
        SECRET_KEY=binascii.hexlify(os.urandom(24)),
        PERMANENT_SESSION_LIFETIME=300,
        USE_X_SENDFILE=False,
        LOGGER_NAME='api',
        SERVER_NAME='VGT API Server',
        MAX_CONTENT_LENGTH=10485760,
        TRAP_HTTP_EXCEPTIONS=False,
        TRAP_BAD_REQUEST_ERRORS=False,
        JSON_AS_ASCII=False,
        JSON_SORT_KEYS=False,
        JSONIFY_PRETTYPRINT_REGULAR=True
)
