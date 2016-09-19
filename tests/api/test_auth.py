# -*- coding: utf-8 -*-
"""Tests for token based authentication."""
from oneiNote.api.auth import authenticate, identity


class TestAuth:
    """Test JWT functionality."""

    def test_user_can_authenticate(self, user):
        # Use pw and username with authenticate function
        auth_user = authenticate(user.username, 'myprecious')

        # Assert that the returned user equals the test user
        assert auth_user == user

    def test_get_user_from_payload(self, user):
        payload = {}
        payload["identity"] = '1'

        # pass payload to identity function
        id_user = identity(payload)

        # Asser that returned user equals test user
        assert id_user == user
