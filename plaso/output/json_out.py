# -*- coding: utf-8 -*-
"""Output module that saves data into a JSON format."""

from __future__ import unicode_literals

import json

from plaso.output import interface
from plaso.output import manager
from plaso.serializer import json_serializer


class JSONOutputModule(interface.LinearOutputModule):
  """Output module for the JSON format."""

  NAME = 'json'
  DESCRIPTION = 'Saves the events into a JSON format.'

  _JSON_SERIALIZER = json_serializer.JSONAttributeContainerSerializer

  def __init__(self, output_mediator):
    """Initializes the output module object.

    Args:
      output_mediator (OutputMediator): mediates interactions between output
          modules and other components, such as storage and dfvfs.
    """
    super(JSONOutputModule, self).__init__(output_mediator)
    self._event_counter = 0

  def WriteEventBody(self, event):
    """Writes the body of an event object to the output.

    Args:
      event (EventObject): event.
    """
    inode = getattr(event, 'inode', None)
    if inode is None:
      event.inode = 0

    json_dict = self._JSON_SERIALIZER.WriteSerializedDict(event)
    json_string = json.dumps(json_dict, sort_keys=True)

    if self._event_counter != 0:
      self._output_writer.Write(', ')

    line = '"event_{0:d}": {1:s}\n'.format(self._event_counter, json_string)
    self._output_writer.Write(line)

    self._event_counter += 1

  def WriteFooter(self):
    """Writes the footer to the output."""
    self._output_writer.Write('}')

  def WriteHeader(self):
    """Writes the header to the output."""
    self._output_writer.Write('{')
    self._event_counter = 0


manager.OutputManager.RegisterOutput(JSONOutputModule)
