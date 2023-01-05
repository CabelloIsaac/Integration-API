from fastapi import APIRouter

from . import controller

router = APIRouter(
    prefix="/hubspot",
    tags=["hubspot"]
)

@router.get(
    "/deals/",
    summary="Get deals",
    description="Get deals from Hubspot",
    response_description="Deals",
)
def get_deals():
    return controller.get_deals()


@router.get(
    "/deals/process",
    summary="Process deals",
    description="Process deals from Hubspot",
    response_description="Deals",
)
def process_deals():
    return controller.process_deals()