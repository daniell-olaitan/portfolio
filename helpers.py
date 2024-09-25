#!/usr/bin/env python3
import requests
import typing as t


def get_provider_cfg() -> t.Dict:
    """
    Function fetches the configuration document of a provider

    Returns:
        The document or error
    """
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except requests.RequestException as re:
        return {'error': re}
