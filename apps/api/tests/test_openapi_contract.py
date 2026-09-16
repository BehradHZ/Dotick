import hashlib
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OPENAPI_PATH = REPO_ROOT / "docs" / "design" / "openapi.json"
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}
REVIEWED_CONTRACT_SHA256 = "413160a1a2ed98284d2a30fab7edcd8a5893841dcd94a3d165a355202a9d09da"


def _load_contract():
    return json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))


def _operations(contract):
    for path, path_item in contract["paths"].items():
        for method, operation in path_item.items():
            if method in HTTP_METHODS:
                yield path, method, operation


def test_published_contract_changes_require_a_reviewed_test_update():
    contract = _load_contract()
    canonical = json.dumps(
        contract,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()

    assert hashlib.sha256(canonical).hexdigest() == REVIEWED_CONTRACT_SHA256


def test_openapi_is_the_executable_increment_1_contract():
    contract = _load_contract()

    assert contract["openapi"] == "3.1.0"
    assert contract["paths"]
    assert all(path.startswith("/api/v1/") for path in contract["paths"])

    operations = list(_operations(contract))
    assert operations
    assert all(operation.get("operationId") for _, _, operation in operations)
    assert all(operation.get("responses") for _, _, operation in operations)

    request_bodies = contract["components"]["requestBodies"].values()
    assert all(set(body["content"]) == {"application/json"} for body in request_bodies)

    error = contract["components"]["schemas"]["Error"]
    assert error["required"] == ["error"]
    assert set(error["properties"]["error"]["required"]) == {"code", "details"}
