# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Decodes and verifies the signature of auth tokens."""

from __future__ import absolute_import

from past.builtins import basestring
from builtins import object
import datetime
import jwkest
import time

from dogpile import cache
from jwkest import jws
from jwkest import jwt

from . import suppliers

INT_TYPES = (int, int)


class Authenticator(object):  # pylint: disable=too-few-public-methods
    """Decodes and verifies the signature of auth tokens."""

    def __init__(self, issuers_to_provider_ids, jwks_supplier, cache_capacity=200):
        """Construct an instance of AuthTokenDecoder.

        Args:
          issuers_to_provider_ids: a dictionary mapping from issuers to provider
            IDs defined in the service configuration.
          jwks_supplier: an instance of JwksSupplier that supplies JWKS based on
            issuer.
          cache_capacity: the cache_capacity with default value of 200.
        """
        self._issuers_to_provider_ids = issuers_to_provider_ids
        self._jwks_supplier = jwks_supplier

        arguments = {u"capacity": cache_capacity}
        expiration_time = datetime.timedelta(minutes=5)
        self._cache = cache.make_region().configure(u"lru_cache",
                                                    arguments=arguments,
                                                    expiration_time=expiration_time)

    def authenticate(self, auth_token, auth_info, service_name):
        """Authenticates the current auth token.

        Args:
          auth_token: the auth token.
          auth_info: the auth configurations of the API method being called.
          service_name: the name of this service.

        Returns:
          A constructed UserInfo object representing the identity of the caller.

        Raises:
          UnauthenticatedException: When
            * the issuer is not allowed;
            * the audiences are not allowed;
            * the auth token has already expired.
        """
        try:
            jwt_claims = self.get_jwt_claims(auth_token)
        except Exception as error:
            raise suppliers.UnauthenticatedException(u"Cannot decode the auth token",
                                                     error)
        _check_jwt_claims(jwt_claims)

        user_info = UserInfo(jwt_claims)

        issuer = user_info.issuer
        if issuer not in self._issuers_to_provider_ids:
            raise suppliers.UnauthenticatedException(u"Unknown issuer: " + issuer)
        provider_id = self._issuers_to_provider_ids[issuer]

        if not auth_info.is_provider_allowed(provider_id):
            raise suppliers.UnauthenticatedException(u"The requested method does not "
                                                     u"allow provider id: " + provider_id)

        # Check the audiences decoded from the auth token. The auth token is
        # allowed when 1) an audience is equal to the service name, or 2) at least
        # one audience is allowed in the method configuration.
        audiences = user_info.audiences
        has_service_name = service_name in audiences

        allowed_audiences = auth_info.get_allowed_audiences(provider_id)
        intersected_audiences = set(allowed_audiences).intersection(audiences)
        if not has_service_name and not intersected_audiences:
            raise suppliers.UnauthenticatedException(u"Audiences not allowed")

        return user_info

    def get_jwt_claims(self, auth_token):
        """Decodes the auth_token into JWT claims represented as a JSON object.

        This method first tries to look up the cache and returns the result
        immediately in case of a cache hit. When cache misses, the method tries to
        decode the given auth token, verify its signature, and check the existence
        of required JWT claims. When successful, the decoded JWT claims are loaded
        into the cache and then returned.

        Args:
          auth_token: the auth token to be decoded.

        Returns:
          The decoded JWT claims.

        Raises:
          UnauthenticatedException: When the signature verification fails, or when
            required claims are missing.
        """

        def _decode_and_verify():
            jwt_claims = jwt.JWT().unpack(auth_token).payload()
            _verify_required_claims_exist(jwt_claims)

            issuer = jwt_claims[u"iss"]
            keys = self._jwks_supplier.supply(issuer)
            try:
                return jws.JWS().verify_compact(auth_token, keys)
            except (jwkest.BadSignature, jws.NoSuitableSigningKeys,
                    jws.SignerAlgError) as exception:
                raise suppliers.UnauthenticatedException(u"Signature verification failed",
                                                         exception)

        return self._cache.get_or_create(auth_token, _decode_and_verify)


class UserInfo(object):
    """An object that holds the authentication results."""

    def __init__(self, jwt_claims):
        audiences = jwt_claims[u"aud"]
        if isinstance(audiences, basestring):
            audiences = [audiences]
        self._audiences = audiences

        # email is not required
        self._email = jwt_claims[u"email"] if u"email" in jwt_claims else None
        self._subject_id = jwt_claims[u"sub"]
        self._issuer = jwt_claims[u"iss"]

    @property
    def audiences(self):
        return self._audiences

    @property
    def email(self):
        return self._email

    @property
    def subject_id(self):
        return self._subject_id

    @property
    def issuer(self):
        return self._issuer


def _check_jwt_claims(jwt_claims):
    """Checks whether the JWT claims should be accepted.

    Specifically, this method checks the "exp" claim and the "nbf" claim (if
    present), and raises UnauthenticatedException if 1) the current time is
    before the time identified by the "nbf" claim, or 2) the current time is
    equal to or after the time identified by the "exp" claim.

    Args:
      jwt_claims: the JWT claims whose expiratio to be checked.

    Raises:
      UnauthenticatedException: When the "exp" claim is malformed or the JWT has
        already expired.
    """
    current_time = time.time()

    expiration = jwt_claims[u"exp"]
    if not isinstance(expiration, INT_TYPES):
        raise suppliers.UnauthenticatedException(u'Malformed claim: "exp" must be an integer')
    if current_time >= expiration:
        raise suppliers.UnauthenticatedException(u"The auth token has already expired")

    if u"nbf" not in jwt_claims:
        return

    not_before_time = jwt_claims[u"nbf"]
    if not isinstance(not_before_time, INT_TYPES):
        raise suppliers.UnauthenticatedException(u'Malformed claim: "nbf" must be an integer')
    if current_time < not_before_time:
        raise suppliers.UnauthenticatedException(u'Current time is less than the "nbf" time')


def _verify_required_claims_exist(jwt_claims):
    """Verifies that the required claims exist.

    Args:
      jwt_claims: the JWT claims to be verified.

    Raises:
      UnauthenticatedException: if some claim doesn't exist.
    """
    for claim_name in [u"aud", u"exp", u"iss", u"sub"]:
        if claim_name not in jwt_claims:
            raise suppliers.UnauthenticatedException(u'Missing "%s" claim' % claim_name)
