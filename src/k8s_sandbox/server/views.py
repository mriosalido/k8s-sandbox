import time

import requests
from flask import Blueprint, make_response, current_app, abort, jsonify
import kubernetes


bp = Blueprint('views', __name__, url_prefix='/')

@bp.route('/liveness')
def liveness():
    status = "OK"
    status_code = 200
    if current_app.config["K8S_SANDBOX_LIVENESS_TIME_START"] == 0:
        current_app.config["K8S_SANDBOX_LIVENESS_TIME_START"] = int(time.time())
    if current_app.config["K8S_SANDBOX_LIVENESS_TIME_LAST"] == 0:
        current_app.config["K8S_SANDBOX_LIVENESS_TIME_LAST"] = int(time.time())
    K8S_SANDBOX_LIVENESS_SLEEP = current_app.config["K8S_SANDBOX_LIVENESS_SLEEP"]
    K8S_SANDBOX_LIVENESS_MAX_OK = current_app.config["K8S_SANDBOX_LIVENESS_MAX_OK"]
    K8S_SANDBOX_LIVENESS_MAX_TIME_OK = current_app.config["K8S_SANDBOX_LIVENESS_MAX_TIME_OK"]

    if K8S_SANDBOX_LIVENESS_SLEEP > 0:
        time.sleep(K8S_SANDBOX_LIVENESS_SLEEP)

    if K8S_SANDBOX_LIVENESS_MAX_OK >= 0:
        if current_app.config["K8S_SANDBOX_LIVENESS_COUNT"] >= K8S_SANDBOX_LIVENESS_MAX_OK:
            status = "FAIL"
            status_code = 401
    if K8S_SANDBOX_LIVENESS_MAX_TIME_OK > 0:
        dif = int(time.time()) - current_app.config["K8S_SANDBOX_LIVENESS_TIME_START"]
        if dif > K8S_SANDBOX_LIVENESS_MAX_TIME_OK:
            status = "FAIL"
            status_code = 401

    resp = make_response(status, status_code)
    resp.headers['X-app'] = f'{current_app.config["K8S_SANDBOX_APP_NAME"]}-{current_app.config["K8S_SANDBOX_APP_ID"]}'
    resp.headers['X-liveness-count'] = current_app.config["K8S_SANDBOX_LIVENESS_COUNT"]
    resp.headers['X-liveness-start'] = int(time.time()) - current_app.config["K8S_SANDBOX_LIVENESS_TIME_START"]
    resp.headers['X-liveness-last'] = int(time.time()) - current_app.config["K8S_SANDBOX_LIVENESS_TIME_LAST"]

    current_app.config["K8S_SANDBOX_LIVENESS_TIME_LAST"] = int(time.time())
    current_app.config["K8S_SANDBOX_LIVENESS_COUNT"] += 1
    return resp


@bp.route('/readiness')
def readiness():
    status = "FAIL"
    status_code = 401
    if current_app.config["K8S_SANDBOX_READINESS_TIME_START"] == 0:
        current_app.config["K8S_SANDBOX_READINESS_TIME_START"] = int(time.time())
    if current_app.config["K8S_SANDBOX_READINESS_TIME_LAST"] == 0:
        current_app.config["K8S_SANDBOX_READINESS_TIME_LAST"] = int(time.time())
    K8S_SANDBOX_READINESS_SLEEP = current_app.config["K8S_SANDBOX_READINESS_SLEEP"]
    K8S_SANDBOX_READINESS_MAX_FAIL = current_app.config["K8S_SANDBOX_READINESS_MAX_FAIL"]
    K8S_SANDBOX_READINESS_MAX_TIME_FAIL = current_app.config["K8S_SANDBOX_READINESS_MAX_TIME_FAIL"]

    if K8S_SANDBOX_READINESS_SLEEP > 0:
        time.sleep(K8S_SANDBOX_READINESS_SLEEP)

    if K8S_SANDBOX_READINESS_MAX_FAIL >= 0:
        if current_app.config["K8S_SANDBOX_READINESS_COUNT"] >= K8S_SANDBOX_READINESS_MAX_FAIL:
            status = "OK"
            status_code = 200
    elif K8S_SANDBOX_READINESS_MAX_TIME_FAIL > 0:
        dif = int(time.time()) - current_app.config["K8S_SANDBOX_READINESS_TIME_START"]
        if dif > K8S_SANDBOX_READINESS_MAX_TIME_FAIL:
            status = "OK"
            status_code = 200
    else:
        status = "OK"
        status_code = 200

    resp = make_response(status, status_code)
    resp.headers['X-app'] = f'{current_app.config["K8S_SANDBOX_APP_NAME"]}-{current_app.config["K8S_SANDBOX_APP_ID"]}'
    resp.headers['X-readiness-count'] = current_app.config["K8S_SANDBOX_READINESS_COUNT"]
    resp.headers['X-readiness-start'] = int(time.time()) - current_app.config["K8S_SANDBOX_READINESS_TIME_START"]
    resp.headers['X-readiness-last'] = int(time.time()) - current_app.config["K8S_SANDBOX_READINESS_TIME_LAST"]

    current_app.config["K8S_SANDBOX_READINESS_TIME_LAST"] = int(time.time())
    current_app.config["K8S_SANDBOX_READINESS_COUNT"] += 1
    return resp


@bp.route('/startup')
def startup():
    resp = make_response("OK")
    resp.headers['X-app'] = f'{current_app.config["K8S_SANDBOX_APP_NAME"]}-{current_app.config["K8S_SANDBOX_APP_ID"]}'
    return resp


@bp.route('/reload')
def reloadme():
    resp = make_response("OK")
    config_file = current_app.config.get("K8S_SANDBOX_CONFIG_FILE", None)
    if config_file:
        current_app.config.from_pyfile(config_file)
        current_app.config["K8S_SANDBOX_CONFIG_FILE"] = config_file
    resp.headers['X-app'] = f'{current_app.config["K8S_SANDBOX_APP_NAME"]}-{current_app.config["K8S_SANDBOX_APP_ID"]}'
    return resp

@bp.route('/backend')
def backend():
    resp = make_response("OK")
    resp.headers['X-app'] = f'{current_app.config["K8S_SANDBOX_APP_NAME"]}-{current_app.config["K8S_SANDBOX_APP_ID"]}'
    return resp


@bp.route('/api')
def api():
    resp = jsonify({'return':'OK'})
    resp.headers['X-app'] = f'{current_app.config["K8S_SANDBOX_APP_NAME"]}-{current_app.config["K8S_SANDBOX_APP_ID"]}'
    return resp


@bp.route('/frontend')
def frontend():
    resp = make_response("OK")
    try:
        r = requests.get(current_app.config["KS8_SANDBOX_BACKEND_URL"])
        resp.headers['X-backend-status'] = r.status_code
        resp.headers['X-backend'] = r.headers.get('X-app', 'FAIL')
    except:
        resp.headers['X-backend-status'] = 500
        resp.headers['X-backend'] = 'EXCEPTION'
    resp.headers['X-app'] = f'{current_app.config["K8S_SANDBOX_APP_NAME"]}-{current_app.config["K8S_SANDBOX_APP_ID"]}'
    return resp


@bp.route('/k8s')
def k8s():
    res = []
    kubernetes.config.load_incluster_config()

    v1 = kubernetes.client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        res.append("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    return "\n".join(res)


def init_app(app):
    app.register_blueprint(bp)
