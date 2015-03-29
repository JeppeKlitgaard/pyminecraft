"""
Handles authentication with the Mojang authentication server.
"""
import requests
import json
from ..exceptions import YggdrasilError

AUTHSERVER = "https://authserver.mojang.com"

# Need this content type, or authserver will complain
CONTENT_TYPE = "application/json"
HEADERS = {"content-type": CONTENT_TYPE}


class AuthenticationToken(object):
    """
    Represents an authentication token.

    See http://wiki.vg/Authentication.
    """
    AGENT_NAME = "Minecraft"
    AGENT_VERSION = 1

    def __init__(self, access_token=None, client_token=None):
        """
        Constructs an `AuthenticationToken` based on `access_token` and
        `client_token`.

        Parameters:
            access_token - An `str` object containing the `access_token`.
            client_token - An `str` object containing the `client_token`.

        Returns:
            A `AuthenticationToken` with `access_token` and `client_token` set.
        """
        self.access_token = access_token
        self.client_token = client_token

    def authenticate(self, username, password):
        """
        Authenticates the user against https://authserver.mojang.com using
        `username` and `password` parameters.

        Parameters:
            username - An `str` object with the username (unmigrated accounts)
                or email address for a Mojang account.
            password - An `str` object with the password.

        Returns:
            Returns `True` if successful.
            Otherwise it will raise an exception.

        Raises:
            minecraft.exceptions.YggdrasilError
        """
        payload = {
            "agent": {
                "name": self.AGENT_NAME,
                "version": self.AGENT_VERSION
            },
            "username": username,
            "password": password
        }

        req = _make_request("authenticate", payload)

        _raise_from_request(req)

        json_resp = req.json()

        self.access_token = json_resp["accessToken"]
        self.client_token = json_resp["clientToken"]

        return True

    def refresh(self):
        """
        Refreshes the `AuthenticationToken`. Used to keep a user logged in
        between sessions and is preferred over storing a user's password in a
        file.

        Returns:
            Returns `True` if `AuthenticationToken` was successfully refreshed.
            Otherwise it raises an exception.

        Raises:
            minecraft.exceptions.YggdrasilError
            ValueError - if `AuthenticationToken.access_token` or
                `AuthenticationToken.client_token` isn't set.
        """
        if self.access_token is None:
            raise ValueError("'access_token' not set!'")

        if self.client_token is None:
            raise ValueError("'client_token' is not set!")

        req = _make_request("refresh", {"accessToken": self.access_token,
                                        "clientToken": self.client_token})

        _raise_from_request(req)

        json_resp = req.json()

        self.access_token = json_resp["accessToken"]
        self.client_token = json_resp["clientToken"]

    def validate(self):
        """
        Validates the AuthenticationToken.

        `AuthenticationToken.access_token` must be set!

        Returns:
            Returns `True` if `AuthenticationToken` is valid.
            Otherwise it will raise an exception.

        Raises:
            minecraft.exceptions.YggdrasilError
            ValueError - if `AuthenticationToken.access_token` is not set.
        """
        if self.access_token is None:
            raise ValueError("'access_token' not set!")

        req = _make_request("validate", {"accessToken": self.access_token})

        if _raise_from_request(req) is None:
            return True

    @staticmethod
    def sign_out(username, password):
        """
        Invalidates `access_token`s using an account's
        `username` and `password`.

        Parameters:
            TODO

        Returns:
            Returns `True` if sign out was successful.
            Otherwise it will raise an exception.

        Raises:
            minecraft.exceptions.YggdrasilError
        """
        req = _make_request("signout", {"username": username,
                                        "password": password})

        if _raise_from_request(req) is None:
            return True

    def invalidate(self):
        """
        Invalidates `access_token`s using the token pair stored in
        the `AuthenticationToken`.

        Returns:
            TODO

        Raises:
            TODO
        """


def _make_request(endpoint, data):
    """
    Fires a POST with json-packed data to the given endpoint and returns
    response.

    Parameters:
        endpoint - An `str` object with the endpoint, e.g. "authenticate"
        data - A `dict` containing the payload data.

    Returns:
        A `requests.Request` object.
    """
    req = requests.post(AUTHSERVER + "/" + endpoint, data=json.dumps(data),
                        headers=HEADERS)
    return req


def _raise_from_request(req):
    """
    Raises an appropriate `YggdrasilError` based on the `status_code` and
    `json` of a `requests.Request` object.
    """
    if req.status_code == requests.codes.ok:
        return None

    json_resp = req.json()

    if "error" not in json_resp and "errorMessage" not in json_resp:
        raise YggdrasilError("Malformed error message.")

    message = "[{status_code}] {error}: '{error_message}'"
    message = message.format(status_code=str(req.status_code),
                             error=json_resp["error"],
                             error_message=json_resp["errorMessage"])

    raise YggdrasilError(message)
