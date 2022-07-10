import os


class Config:
    K8S_SANDBOX_APP_ID = os.getpid()
    K8S_SANDBOX_STARTUP_DELAY = 0
    K8S_SANDBOX_LIVENESS_SLEEP = 0
    K8S_SANDBOX_LIVENESS_MAX_OK = -1
    K8S_SANDBOX_LIVENESS_MAX_TIME_OK = 0
    K8S_SANDBOX_LIVENESS_COUNT = 0
    K8S_SANDBOX_LIVENESS_TIME_START = 0
    K8S_SANDBOX_LIVENESS_TIME_LAST = 0
    K8S_SANDBOX_READINESS_SLEEP = 0
    K8S_SANDBOX_READINESS_MAX_FAIL = -1
    K8S_SANDBOX_READINESS_MAX_TIME_FAIL = 0
    K8S_SANDBOX_READINESS_COUNT = 0
    K8S_SANDBOX_READINESS_TIME_START = 0
    K8S_SANDBOX_READINESS_TIME_LAST = 0


class FrontendConfig(Config):
    K8S_SANDBOX_APP_NAME = "frontend"
    KS8_SANDBOX_BACKEND_URL = "http://localhost:5001/backend"


class BackendConfig(Config):
    K8S_SANDBOX_APP_NAME = "backend"


# class default_settings(settings):
#     K8S_SANDBOX_APP_NAME = "backend"
#     K8S_SANDBOX_LIVENESS_STARTUP_DELAY = 0
