import pytest
from requests import HTTPError

from okdata.resource_auth import ResourceAuthorizer


resource_authorizer = ResourceAuthorizer()


def test_has_access_authorized(requests_mock):
    requests_mock.register_uri(
        "POST",
        "/auth/realms/some-realm/protocol/openid-connect/token",
        json={"result": True},
        status_code=200,
    )

    assert resource_authorizer.has_access(
        bearer_token="abc123",
        scope="okdata:dataset:read",
        resource_name="okdata:dataset:test-dataset",
    )


def test_has_access_not_authorized(requests_mock):
    requests_mock.register_uri(
        "POST",
        "/auth/realms/some-realm/protocol/openid-connect/token",
        json={"error": "access_denied"},
        status_code=403,
    )

    assert not resource_authorizer.has_access(
        bearer_token="def456",
        scope="okdata:dataset:read",
        resource_name="okdata:dataset:test-dataset",
    )


def test_has_access_invalid_token(requests_mock):
    requests_mock.register_uri(
        "POST",
        "/auth/realms/some-realm/protocol/openid-connect/token",
        json={"error": "invalid_grant"},
        status_code=401,
    )

    with pytest.raises(HTTPError):
        resource_authorizer.has_access(
            bearer_token="ghi789",
            scope="okdata:dataset:read",
            resource_name="okdata:dataset:test-dataset",
        )
