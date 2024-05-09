from __future__ import annotations

import enum
import json
import logging
from datetime import datetime

import structlog


def set_message_field(_, __, event_dict: dict) -> dict:
    if 'message' in event_dict:
        return event_dict
    event_dict['message'] = event_dict['event']
    return event_dict


def set_level_field(_, method_name, event_dict: dict) -> dict:
    if 'level' in event_dict:
        return event_dict
    level = {
        'debug': 'DEBUG',
        'info': 'INFO',
        'msg': 'INFO',
        'warn': 'WARN',
        'warning': 'WARN',
        'err': 'ERROR',
        'error': 'ERROR',
        'exception': 'ERROR',
        'fatal': 'FATAL',
        'critical': 'FATAL',
    }.get(method_name, 'INFO')
    event_dict['level'] = level
    return event_dict


def set_timestamp(_, __, event: dict) -> dict:
    event['timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return event


def remove_sensitive_data(data: dict[str, str]) -> dict:
    if '__keep_sensitive__' in data:
        del data['__keep_sensitive__']
        return data
    for key, value in data.copy().items():
        if isinstance(value, str):
            lowered_key = key.lower()
            for forbidden_word in ['pass', 'secret', 'token', 'key']:
                if forbidden_word in lowered_key:
                    data.pop(key)
        elif isinstance(value, dict):
            remove_sensitive_data(value)
        else:
            continue
    return data


def remove_sensitive_data_from_event(_, __, event_dict: dict) -> dict:
    remove_sensitive_data(event_dict)
    return event_dict


def execute_callables(_, __, event_dict: dict) -> dict:
    for key, value in event_dict.items():
        if callable(value):
            event_dict[key] = value()
    return event_dict


def serialize_enums(_, __, event_dict: dict) -> dict:
    for key, value in event_dict.items():
        if isinstance(value, enum.Enum):
            event_dict[key] = value.value
    return event_dict


def setup_logging() -> None:
    logging.getLogger('uvicorn.error').propagate = False
    logging.getLogger('uvicorn.error').disabled = True
    logging.getLogger('uvicorn.access').propagate = False
    logging.getLogger('uvicorn.access').disabled = True

    processors = [
        set_timestamp,
        remove_sensitive_data_from_event,
        execute_callables,
        serialize_enums,
        structlog.processors.format_exc_info,
    ]
    processors.insert(0, set_message_field)
    processors.insert(0, set_level_field)
    structlog.configure(
        processors=[*processors, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(
                serializer=json.dumps,
                ensure_ascii=False,
            ),
        ],
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
