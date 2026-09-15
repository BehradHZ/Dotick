from unittest.mock import patch

import pytest
from dotick.identity.google_identity import _StandardLibraryRequest
from google.auth import exceptions as google_exceptions


class _FakeResponse:
    status = 200
    headers = {"content-type": "application/json"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return b'{"keys": []}'


def test_standard_library_transport_adapts_successful_http_response():
    with patch(
        "dotick.identity.google_identity.urlopen",
        return_value=_FakeResponse(),
    ) as urlopen:
        response = _StandardLibraryRequest()(
            "https://www.googleapis.com/oauth2/v1/certs",
            headers={"Authorization": "Bearer test"},
            timeout=5,
        )

    request = urlopen.call_args.args[0]
    assert request.full_url == "https://www.googleapis.com/oauth2/v1/certs"
    assert request.get_method() == "GET"
    assert request.get_header("Authorization") == "Bearer test"
    assert urlopen.call_args.kwargs == {"timeout": 5}
    assert response.status == 200
    assert response.headers == {"content-type": "application/json"}
    assert response.data == b'{"keys": []}'


def test_standard_library_transport_maps_network_failures_to_google_transport_error():
    with (
        patch(
            "dotick.identity.google_identity.urlopen",
            side_effect=OSError("network unavailable"),
        ),
        pytest.raises(google_exceptions.TransportError),
    ):
        _StandardLibraryRequest()("https://www.googleapis.com/oauth2/v1/certs")
