import enum
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import status
from pydantic import BaseModel
from pydantic import condecimal

from src.api.di import CreateBetCommandHandlerStub
from src.api.di import GetBetsCommandHandlerStub
from src.api.error_message import ErrorMessage
from src.api.error_message import InternalServerErrorMessage
from src.bets.application.create_bet import CreateBetCommand
from src.bets.application.create_bet import CreateBetCommandHandler
from src.bets.application.create_bet import EventNotFoundError
from src.bets.application.create_bet import EventStatusAlreadyIsFinalError
from src.bets.application.get_bets import GetBetsCommand
from src.bets.application.get_bets import GetBetsCommandHandler
from src.bets.domain.bet import Bet
from src.bets.domain.event import EventStatus


router = fastapi.APIRouter(prefix='/bets', tags=['Ставка'])


class GetBetsResponseEventStatus(enum.Enum):
    PENDING = 'PENDING'
    WIN = 'WIN'
    LOSE = 'LOSE'


EVENT_STATUS_MAPPING = {
    EventStatus.WIN: GetBetsResponseEventStatus.WIN,
    EventStatus.LOSE: GetBetsResponseEventStatus.LOSE,
    EventStatus.PENDING: GetBetsResponseEventStatus.PENDING,
}


class GetBetsResponseEvent(BaseModel):
    id: UUID
    status: GetBetsResponseEventStatus
    created_at: datetime


class GetBetsResponseItem(BaseModel):
    id: UUID
    amount: Decimal = condecimal(gt=0, decimal_places=2)
    created_at: datetime
    event: GetBetsResponseEvent


class GetBetsResponse(BaseModel):
    bets: list[GetBetsResponseItem]


def convert_bets_to_response(bets: list[Bet]) -> GetBetsResponse:
    bets_response = []
    for bet in bets:
        bet_response = GetBetsResponseItem(
            id=bet.id,
            amount=bet.amount,
            created_at=bet.created_at,
            event=GetBetsResponseEvent(
                id=bet.event.id,
                status=EVENT_STATUS_MAPPING[bet.event.status],
                created_at=bet.event.created_at,
            ),
        )
        bets_response.append(bet_response)
    return GetBetsResponse(bets=bets_response)


@router.get(
    path='/',
    summary='Получить ставки',
    description='Запросить получение ставок.',
    responses={
        status.HTTP_200_OK: {'description': 'Successful Response', 'model': GetBetsResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Internal Server Error',
            'content': {
                'application/json': {
                    'example': {'example': InternalServerErrorMessage.to_content()},
                },
            },
        },
    },
)
async def get_bets(
        get_bets_command_handler: GetBetsCommandHandler = Depends(GetBetsCommandHandlerStub),
):
    command = GetBetsCommand()
    bets = await get_bets_command_handler.handle(command)
    return convert_bets_to_response(bets)


class CreateBetRequest(BaseModel):
    id: UUID
    event_id: UUID
    amount: condecimal(gt=0, decimal_places=2)


class EventStatusAlreadyIsFinalErrorMessage(ErrorMessage):
    status_code = 400
    message_code = 'EVENT_STATUS_ALREADY_IS_FINAL'
    message_description = 'Статус события уже финальный'


class EventNotFoundErrorMessage(ErrorMessage):
    status_code = 400
    message_code = 'EVENT_NOT_FOUND'
    message_description = 'Событие не найдено'


@router.post(
    path='/',
    summary='Создать ставку',
    description='Запросить создание ставки.',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'description': 'Successful Response'},
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Bad Request',
            'content': {
                'application/json': {
                    'example': [
                        EventNotFoundErrorMessage.to_content(),
                        EventStatusAlreadyIsFinalErrorMessage.to_content(),
                    ],
                },
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Internal Server Error',
            'content': {
                'application/json': {'example': InternalServerErrorMessage.to_content()},
            },
        },
    },
)
async def create_bet(
        request: CreateBetRequest = Body(),
        create_bet_command_handler: CreateBetCommandHandler = Depends(CreateBetCommandHandlerStub),
):
    try:
        command = CreateBetCommand(
            event_id=request.event_id,
            bet_id=request.id,
            bet_amount=request.amount,
        )
        await create_bet_command_handler.handle(command)
    except EventNotFoundError:
        return EventNotFoundErrorMessage.to_response()
    except EventStatusAlreadyIsFinalError:
        return EventStatusAlreadyIsFinalErrorMessage.to_response()
