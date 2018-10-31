import pytest

import common.app


@pytest.fixture
def app():
    app = common.app.create()
    app.debug = True
    return app
