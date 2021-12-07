# okdata-resource-auth


Client library for authorizing logged-in users against Keycloak resources and scopes.

## Setup

```sh
git clone git@github.com:oslokommune/okdata-resource-auth.git
python3 -m venv .venv
source .venv/bin/activate
make init
make test
```

## Publish

```sh
make clean test         # Test
make bump-patch build   # Bump version and build
make publish            # Publish module to PyPI
git push --tags         # Push version bump commit and generated tag
```
