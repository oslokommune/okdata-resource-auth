from urllib import parse

import pytest
from requests import HTTPError
from requests_mock.response import create_response

from okdata.resource_auth import ResourceAuthorizer


resource_authorizer = ResourceAuthorizer()


token_authorized = "abc123"
token_not_authorized = "def456"
token_invalid = "ghi789"
token_whitelisted = "jkl101"
scope = "okdata:dataset:read"
resource_name = "okdata:dataset:test-dataset"
permission_resource_read = f"{resource_name}#{scope}"
permission_whitelist = "#okdata:dataset:whitelist"


@pytest.fixture
def keycloak_mock(requests_mock):
    def matcher(request):
        if request.path != "/auth/realms/some-realm/protocol/openid-connect/token":
            return None

        access_token = request.headers["Authorization"].split("Bearer ")[1]
        permission = dict(parse.parse_qsl(request.body))["permission"]

        if (access_token == token_not_authorized) or (
            access_token == token_whitelisted and permission == permission_resource_read
        ):
            return create_response(
                request, json={"error": "access_denied"}, status_code=403
            )

        if (access_token == token_authorized) or (
            access_token == token_whitelisted and permission == permission_whitelist
        ):
            return create_response(request, json={"result": True}, status_code=200)

        return create_response(
            request, json={"error": "invalid_grant"}, status_code=401
        )

    requests_mock._adapter.add_matcher(matcher)
    yield


def test_has_access_authorized(keycloak_mock):
    assert resource_authorizer.has_access(token_authorized, scope, resource_name)


def test_has_access_not_authorized(keycloak_mock):
    assert not resource_authorizer.has_access(
        token_not_authorized, scope, resource_name
    )


def test_has_access_invalid_token(keycloak_mock):
    with pytest.raises(HTTPError):
        resource_authorizer.has_access(token_invalid, scope, resource_name)


def test_has_access_whitelisted(keycloak_mock):
    assert resource_authorizer.has_access(
        token_whitelisted, scope, resource_name, use_whitelist=True
    )
