__author__ = 'Ostico <ostico@gmail.com>'

from ..exceptions import PyOrientBadMethodCallException
from .base import BaseMessage
from ..constants import CONNECT_OP, FIELD_BYTE, FIELD_INT, FIELD_SHORT, \
    FIELD_STRINGS, NAME, SERIALIZATION_DOCUMENT2CSV, SUPPORTED_PROTOCOL, \
    VERSION, SERIALIZATION_SERIAL_BIN, SERIALIZATION_TYPES, SHUTDOWN_OP
from ..utils import need_connected


#
# Connect
#
class ConnectMessage(BaseMessage):

    def __init__(self, _orient_socket):
        super( ConnectMessage, self ).__init__(_orient_socket)

        self._user = ''
        self._pass = ''
        self._client_id = ''
        self._serialization_type = SERIALIZATION_DOCUMENT2CSV

        self._append( ( FIELD_BYTE, CONNECT_OP ) )

    def prepare(self, params=None ):

        if isinstance( params, tuple ) or isinstance( params, list ):
            try:
                self._user = params[0]
                self._pass = params[1]
                self._client_id = params[2]

                self.set_serialization_type( params[3] )
            except IndexError:
                # Use default for non existent indexes
                pass

        if self.get_protocol() > 21:
            connect_string = (FIELD_STRINGS, [self._client_id,
                                              self._serialization_type,
                                              self._user, self._pass])
        else:
            connect_string = (FIELD_STRINGS, [self._client_id,
                                              self._user, self._pass])

        self._append( ( FIELD_STRINGS, [NAME, VERSION] ) )
        self._append( ( FIELD_SHORT, SUPPORTED_PROTOCOL ) )
        self._append( connect_string )
        return super( ConnectMessage, self ).prepare()

    def fetch_response(self):
        self._append( FIELD_INT )
        self._session_id = super( ConnectMessage, self ).fetch_response()[0]

        # IMPORTANT needed to pass the id to other messages
        self._update_socket_id()

        return self._session_id

    def set_user(self, _user):
        self._user = _user
        return self

    def set_pass(self, _pass):
        self._pass = _pass
        return self

    def set_client_id(self, _cid):
        self._client_id = _cid
        return self

    def set_serialization_type(self, serialization_type):
        #TODO Implement version 22 of the protocol
        if serialization_type == SERIALIZATION_SERIAL_BIN:
            raise NotImplementedError

        if serialization_type in SERIALIZATION_TYPES:
            # user choice storage if present
            self._serialization_type = serialization_type
        else:
            raise PyOrientBadMethodCallException(
                serialization_type + ' is not a valid serialization type', []
            )
        return self



#
# Shutdown
#
class ShutdownMessage(BaseMessage):

    def __init__(self, _orient_socket ):
        super( ShutdownMessage, self ).__init__(_orient_socket)

        self._user = ''
        self._pass = ''

        # order matters
        self._append( ( FIELD_BYTE, SHUTDOWN_OP ) )

    @need_connected
    def prepare(self, params=None):

        if isinstance( params, tuple ) or isinstance( params, list ):
            try:
                self._user = params[0]
                self._pass = params[1]
            except IndexError:
                # Use default for non existent indexes
                pass

        self._append( (FIELD_STRINGS, [self._user, self._pass]) )

        return super( ShutdownMessage, self ).prepare()

    def fetch_response(self):
        return super( ShutdownMessage, self ).fetch_response()

    def set_user(self, _user):
        self._user = _user
        return self

    def set_pass(self, _pass):
        self._pass = _pass
        return self