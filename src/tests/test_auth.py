import os
import tempfile

from pulsebot.auth.local_auth import LocalAuth


def test_register_and_authenticate():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, 'test_auth.db')
        auth = LocalAuth(db_path=db_path)
        auth.register_user('alice', 's3cret')
        assert auth.authenticate('alice', 's3cret') is True
        assert auth.authenticate('alice', 'wrong') is False
