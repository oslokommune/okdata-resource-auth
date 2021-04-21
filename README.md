# okdata-resource-auth

Helpers for authorizing users against Keycloak resources for [Origo
Dataplattform](https://oslokommune.github.io/dataplattform/).

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
