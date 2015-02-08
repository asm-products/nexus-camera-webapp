import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

import users

class UserInfoRequest(messages.Message):
    username = messages.StringField(2, required=True)

class UserInfoResponse(messages.Message):
    id = messages.StringField(1, required=True)
    username = messages.StringField(2, required=True)


class UserId(messages.Message):
    id = messages.StringField(1)


@endpoints.api(name='nexusCameraAPI', version='v1', description='the api for Nexus Camera.',
               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID], audiences=['898555901179-jbffm9b3fjo8f4dki486jakvvmcchib1.apps.googleusercontent.com'])
class NexusCameraService(remote.Service):

    @endpoints.method(UserId, UserInfoResponse)
    def getUser(self, request):
        """Gets the user with the given user id. Use 'me' for the currently authenticated user."""
        if request.id == 'me':
            if not endpoints.get_current_user():
                raise endpoints.UnauthorizedException("You need to be logged in to use 'me' as a user id.")
            user = users.User.get_by_user(endpoints.get_current_user())
        else:
            user = users.User.get_by_id(request.id)

        if not user:
            raise endpoints.NotFoundException("No such user.")

        return UserInfoResponse(id=user.key.id(), username=user.username)

    @endpoints.method(message_types.VoidMessage, message_types.VoidMessage)
    def deleteUser(self, request):
        """Deletes the currently authenticated user's account."""
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException("You need to be logged in to delete your account.")

        users.User.get_by_user(user).delete()

    @endpoints.method(UserInfoRequest, UserInfoResponse)
    def createOrUpdateUser(self, request):
        """Update the authenticated user's account, creating it if it doesn't exist."""
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException("You need to be logged in to edit user info.")

        user = users.User.create_or_update(user, request.username)
        return UserInfoResponse(id=user.key.id(), username=user.username)

app = endpoints.api_server([NexusCameraService])