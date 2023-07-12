from fastapi import FastAPI
from general_back.main import include_routers


import pytest

"""
Code Analysis

Objective:
The objective of this code snippet is to define a function that includes multiple routers in a FastAPI application.

Inputs:
- app: a FastAPI application instance
- prefix: a string representing the prefix for the routers
- *routers: a variable number of routers to be included in the application

Flow:
1. Create an empty set to store the prefixes of the routers
2. Iterate over the routers passed as arguments
3. If the prefix of the current router is already in the set, skip to the next router
4. Add the prefix of the current router to the set
5. Include the current router in the FastAPI application with the specified prefix

Outputs:
- None

Additional aspects:
- This function allows for a more modular approach to building FastAPI applications by separating the routing logic into multiple files.
- The function ensures that routers with the same prefix are not included multiple times in the application.
"""
class TestMain:
    # Tests that a single router can be included in the app
    def test_include_one_router(self):
        app = FastAPI()
        include_routers(app, user_router)
        assert len(app.routes) == len(user_router.routes)

    # Tests that multiple routers can be included in the app
    def test_include_multiple_routers(self):
        app = FastAPI()
        include_routers(app, "", user_router, auth_router)
        assert len(app.routes) == 9

    # Tests that a router with an empty prefix can be included in the app
    def test_include_router_with_empty_prefix(self):
        app = FastAPI()
        include_routers(app, '', user_router)
        assert len(app.routes) >= len(user_router.routes)

    # Tests that a router with a nested prefix can be included in the app
    def test_include_router_with_nested_prefix(self):
        app = FastAPI()
        include_routers(app, '/api', user_router)
        assert '/api/user/{id}' in [route.path for route in app.routes]