"""
file_name = image_blueprint.py
Created On: 2024/07/10
Lasted Updated: 2024/07/10
Description: _FILL OUT HERE_
Edit Log:
2024/07/10
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS
from sanic import Blueprint, Request
from sanic.response import HTTPResponse
from pydantic import ValidationError

# LOCAL LIBRARY IMPORTS
from src.database.models.image import Image
from src.database.repositories.image_repository import ImageRepository

from src.models.image_model import ImageFilterModel, ImageReleaseUpdateRequest

IMAGES_BLUEPRINT = Blueprint("image_blueprint", url_prefix="/images")


@IMAGES_BLUEPRINT.route("/<image_name>", methods=["GET"])
async def base_route(
    _request: Request,
    image_name: str,
) -> HTTPResponse:
    """
    Gets images from the database that have been released
    """
    image: Image | None = None

    with ImageRepository() as repository:
        image_filters: ImageFilterModel = ImageFilterModel(
            image_name=image_name, released=True
        )
        images: list[Image] = repository.get_images(image_filters)

        if not images:
            return HTTPResponse("Image not found", status=404)

        image = images[0]

    mime_type = "image/jpeg" if image.image_name.endswith(".jpg") else "image/png"
    return HTTPResponse(body=image.image_data, content_type=mime_type)


@IMAGES_BLUEPRINT.route("/getImage", methods=["POST"])
async def get_image(request: Request) -> HTTPResponse:
    """
    Gets images from the database that have been released

    Filtering requires auth
    """
    try:
        image_filters: ImageFilterModel = ImageFilterModel(**request.json)
    except ValidationError:
        return HTTPResponse("Invalid request body", status=400)

    image: Image | None = None

    with ImageRepository() as repository:
        images: list[Image] = repository.get_images(image_filters)

        if not images:
            return HTTPResponse("Image not found", status=404)

        image = images[0]

    mime_type = "image/jpeg" if image.image_name.endswith(".jpg") else "image/png"
    return HTTPResponse(body=image.image_data, content_type=mime_type)


@IMAGES_BLUEPRINT.route("/updateImageRelease", methods=["POST"])
async def update_image_release(request: Request) -> HTTPResponse:
    """
    Updates the release status of an image
    """
    try:
        image_release_update_request: ImageReleaseUpdateRequest = (
            ImageReleaseUpdateRequest(**request.json)
        )
    except ValidationError:
        return HTTPResponse("Invalid request body", status=400)

    with ImageRepository() as repository:
        try:
            repository.update_release(
                image_release_update_request.image_name,
                image_release_update_request.released,
            )
        except ValueError:
            return HTTPResponse("Image not found", status=404)

    return HTTPResponse("Image release status updated", status=200)