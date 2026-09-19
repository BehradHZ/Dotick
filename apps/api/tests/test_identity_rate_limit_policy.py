import json
from pathlib import Path

from django.conf import settings

REPO_ROOT = Path(__file__).resolve().parents[3]
ENV_EXAMPLE_PATH = REPO_ROOT / ".env.example"
OPENAPI_PATH = REPO_ROOT / "docs" / "design" / "openapi.json"
POLICY_PATH = REPO_ROOT / "docs" / "operations" / "identity-rate-limit-policy.json"


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _example_environment():
    return {
        name: value
        for line in ENV_EXAMPLE_PATH.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#") and "=" in line
        for name, value in [line.split("=", 1)]
    }


def test_identity_ceremony_thresholds_match_deployment_environment_contract():
    policy = _json(POLICY_PATH)
    environment = _example_environment()

    assert policy["policy"] == "identity-ceremony"
    assert policy["enforcement"] == "deployment-edge"
    assert policy["key"] == "verified-client-ip"
    for threshold in policy["thresholds"].values():
        assert int(environment[threshold["requests_variable"]]) == threshold["requests"]
        assert int(environment[threshold["window_seconds_variable"]]) == threshold["window_seconds"]
        assert threshold["requests"] > 0
        assert threshold["window_seconds"] > 0


def test_identity_ceremony_policy_exactly_matches_openapi_classification():
    policy = _json(POLICY_PATH)
    contract = _json(OPENAPI_PATH)
    configured_operations = {
        (operation["path"], operation["method"].lower()) for operation in policy["operations"]
    }
    classified_operations = {
        (path, method)
        for path, path_item in contract["paths"].items()
        for method, operation in path_item.items()
        if isinstance(operation, dict)
        and operation.get("x-edge-rate-limit-policy") == policy["policy"]
    }

    assert configured_operations == classified_operations


def test_identity_ceremony_limits_are_not_claimed_as_process_local_throttling():
    assert "DEFAULT_THROTTLE_CLASSES" not in settings.REST_FRAMEWORK
    assert "DEFAULT_THROTTLE_RATES" not in settings.REST_FRAMEWORK
