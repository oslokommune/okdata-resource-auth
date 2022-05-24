## 0.1.4

* `ResourceAuthorizer.has_access` now returns `False` on all 4XX responses from
  Keycloak instead of raising an exception, not only for 403 responses.

## 0.1.3

* Fix retry on POST requests to Keycloak.

## 0.1.2

* Set timeout for requests to Keycloak.

## 0.1.1

* Enabled retry backoff factor for requests to Keycloak.

## 0.1.0

* Initial release.
