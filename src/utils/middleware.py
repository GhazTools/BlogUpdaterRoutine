"""
file_name = middleware.py
Created On: 2024/06/16
Lasted Updated: 2024/06/16
Description: _FILL OUT HERE_
Edit Log:
2024/06/16
    - Created file
"""

# STANDARD LIBRARY IMPORTS
from typing import Any

# THIRD PARTY LIBRARY IMPORTS
from sanic.request import Request
from sanic.response import text, HTTPResponse
from sanic.log import logger
from pydantic import ValidationError
from token_granter_wrapper.token_granter_bindings import TokenGranter  # pylint: disable=E0611 Exists binding just needs to be updated
from metric_producer.metric_producer import MetricProducer

# LOCAL LIBRARY IMPORTS
from src.models.base_request_model import BaseRequest
from src.utils.environment import Environment, EnvironmentVariableKeys


class Middleware:
    """
    A class that contains the middleware for the sanic app
    """

    def __init__(self: "Middleware") -> None:
        self._token_granter = TokenGranter(
            Environment.get_environment_variable(
                EnvironmentVariableKeys.TOKEN_GRANTER_URL
            )
        )
        self._metric_producer = MetricProducer()

    async def request_middleware(
        self: "Middleware", request: Request
    ) -> None | HTTPResponse:
        """
        A function to process a request made to the service before passing it on to the intended endpoint
        """

        logger.info("request received %s", request.path)

        if request.method == "POST":
            token_granter = request.app.config["TOKEN_GRANTER"]
            try:
                # Parse request body into Pydantic model
                user_token = BaseRequest(**request.json)

                # If needed, use user_token.user and user_token.token for further processing
                is_valid: bool = token_granter.validate_token(
                    user_token.user, user_token.token
                )

                if not is_valid:
                    raise ValueError("Inavlid token")

            except ValidationError as e:
                print("Invalid error", e)
                return text("Unsupported endpoint.")
            except ValueError as e:
                print("Invalid token", e)
                return text("Unsupported endpoint.")

        print(request, request.path)
        return None

    async def response_middleware(
        self: "Middleware", request: Request, response: Any
    ) -> None:
        """
        A function to handle the response after it is returned from an endpoint
        """

        print(request, response)
        print("success")

    # PRIVATE METHODS HERE