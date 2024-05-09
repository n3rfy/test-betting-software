import enum
from uuid import UUID

import fastapi
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import status
from fastapi.responses import Response
from pydantic import BaseModel

from src.api.di import ChangeEventStatusCommandHandlerStub
from src.api.di import CreateEventCommandHandlerStub
from src.api.error_message import ErrorMessage
from src.api.error_message import InternalServerErrorMessage
from src.bets.application.change_event_status import ChangeEventStatusCommand
from src.bets.application.change_event_status import ChangeEventStatusCommandHandler
from src.bets.application.change_event_status import EventNotFoundError
from src.bets.application.change_event_status import EventStatusAlreadyIsFinalError
from src.bets.application.create_event import CreateEventCommand
from src.bets.application.create_event import CreateEventCommandHandler
from src.bets.domain.event import EventStatus


router = fastapi.APIRouter(prefix='/events', tags=['Событие'])


class ChangeEventStatusRequestEventStatus(enum.Enum):
    WIN = 'WIN'
    LOSE = 'LOSE'


EVENT_STATUS_MAPPING = {
    ChangeEventStatusRequestEventStatus.WIN: EventStatus.WIN,
    ChangeEventStatusRequestEventStatus.LOSE: EventStatus.LOSE,
}


class ChangeEventStatusRequest(BaseModel):
    status: ChangeEventStatusRequestEventStatus


class EventStatusAlreadyIsFinalErrorMessage(ErrorMessage):
    status_code = 400
    message_code = 'EVENT_STATUS_ALREADY_IS_FINAL'
    message_description = 'Статус события уже финальный'


@router.put(
    path='/{event_id}',
    summary='Изменить статус события',
    description='Запросить изменение статуса события.',
    responses={
        status.HTTP_200_OK: {'description': 'Successful Response'},
        status.HTTP_404_NOT_FOUND: {'description': 'Not Found'},
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Bad Request',
            'content': {
                'application/json': {
                    'example': EventStatusAlreadyIsFinalErrorMessage.to_content(),
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
async def change_event_status(
        event_id: UUID = Path(),
        request: ChangeEventStatusRequest = Body(),
        change_status_command_handler: ChangeEventStatusCommandHandler = Depends(ChangeEventStatusCommandHandlerStub),
):
    try:
        command = ChangeEventStatusCommand(
            event_id=event_id,
            event_status=EVENT_STATUS_MAPPING[request.status],
        )
        await change_status_command_handler.handle(command)
        return Response(status_code=status.HTTP_200_OK)
    except EventNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    except EventStatusAlreadyIsFinalError:
        return EventStatusAlreadyIsFinalErrorMessage.to_response()


class CreateEventRequest(BaseModel):
    event_id: UUID


@router.post(
    path='/',
    summary='Создать событие',
    description='Запросить создание события.',
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {'description': 'Successful Response'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            'description': 'Internal Server Error',
            'content': {
                'application/json': {'example': InternalServerErrorMessage.to_content()},
            },
        },
    },
)
async def create_event(
        request: CreateEventRequest = Body(),
        create_event_command_handler: CreateEventCommandHandler = Depends(CreateEventCommandHandlerStub),
):
    command = CreateEventCommand(
        event_id=request.event_id,
    )
    await create_event_command_handler.handle(command)
