import os
import urllib.parse

import requests


class ResourceAuthorizer:
    def __init__(self):
        self.keycloak_server_url = os.environ["KEYCLOAK_SERVER"]
        self.keycloak_realm = os.environ["KEYCLOAK_REALM"]
        self.resource_server_name = os.environ["RESOURCE_SERVER_CLIENT_ID"]

    def has_access(self, bearer_token, scope, resource_name=None):
        payload = [
            ("grant_type", "urn:ietf:params:oauth:grant-type:uma-ticket"),
            ("audience", self.resource_server_name),
            ("response_mode", "decision"),
            ("permission", "#".join([resource_name or "", scope])),
        ]
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(
            url=urllib.parse.urljoin(
                self.keycloak_server_url,
                f"/auth/realms/{self.keycloak_realm}/protocol/openid-connect/token",
            ),
            data=payload,
            headers=headers,
        )

        if response.status_code == 403:
            return False

        response.raise_for_status()

        return response.json()["result"]
