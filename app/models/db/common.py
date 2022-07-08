# -*- coding: utf-8 -*-


class InvalidParticipantIdError(Exception):
  message = "Invalid message participant id."
  
  def __str__(self):
    return InvalidParticipantIdError.message


def try_cast_participant_id(participant_id: str | None):
  if participant_id is None:
    return None

  try:
    return int(participant_id)
  except ValueError:
    raise InvalidParticipantIdError


__all__ = ['InvalidParticipantIdError', 'try_cast_participant_id']
