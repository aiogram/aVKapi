from . import base
from .base import BaseMethod
import typing
from ..types.attachment import Attachment
from ..types.keyboard import Keyboard
from ..utils.payload import generate_payload, prepare_arg


class Messages(BaseMethod):

    async def add_chat_user(self, chat_id: typing.Union[base.Integer, base.String],
                            user_id: typing.Union[base.Integer, base.String]) -> int:
        """
        Adds a new user to a chat.
        https://vk.com/dev/messages.addChatUser

        :param chat_id: Chat ID.
        :param user_id: ID of the user to be added to the chat
        :return: 1
        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.addChatUser", parameters=parameters)
        return result

    async def allow_messages_from_group(self, group_id: typing.Union[base.Integer, base.String],
                                        key: base.String = None) -> int:
        """
        Allows sending messages from community to the current user
        https://vk.com/dev/messages.allowMessagesFromGroup

        :param group_id: Community ID..
        :param key: Random string, can be used for the user identification. It returns with message_allow event in Callback API.

        :return: 1
        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.allowMessagesFromGroup", parameters=parameters)
        return result

    async def create_chat(self, user_ids: typing.Union[typing.List, typing.Tuple],
                          title: base.String) -> int:
        """
        Creates a chat with several participants
        https://vk.com/dev/messages.createChat

        :param user_ids: IDs of the users to be added to the chat.
        :param title: Chat title.

        :return: Returns the ID of the created chat (chat_id).
        """
        if user_ids:
            user_ids = ",".join(user_ids)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.createChat", parameters=parameters)
        return result

    async def delete(self, message_ids: typing.Union[typing.List, typing.Tuple],
                     spam: base.Boolean = False,
                     group_id: typing.Union[base.Integer, base.String, None] = None,
                     delete_for_all: base.Boolean = False) -> int:
        """
        Deletes one or more messages
        https://vk.com/dev/messages.delete

        :param message_ids: Message IDs
        :param spam: 1 — to mark message as spam.
        :param group_id: group ID (for community messages with a user access token).
        :param delete_for_all: 1 — to delete message for recipient (in 24 hours from the sending time).

        :return:
        """
        if message_ids:
            message_ids = ",".join(message_ids)
        spam = int(spam)
        delete_for_all = int(delete_for_all)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.delete", parameters=parameters)
        return result

    async def delete_chat_photo(self, chat_id: typing.Union[base.Integer, base.String],
                                group_id: typing.Union[base.Integer, base.String, None] = None) -> int:
        """
        Deletes a chat's cover picture
        https://vk.com/dev/messages.deleteChatPhoto

        :param chat_id: Chat ID.
        :param group_id: Group ID

        :return: Returns an object with the following fields:
                 message_id ­– ID of the system message sent.
                 chat – chat object.

        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.deleteChatPhoto", parameters=parameters)
        return result

    async def delete_conversation(self, user_id: typing.Union[base.Integer, base.String],
                                  peer_id: typing.Union[base.Integer, base.String, None] = None,
                                  offset: base.Integer = 0,
                                  count: base.Integer = None,
                                  group_id: typing.Union[base.Integer, base.String, None] = None) -> int:
        """
        Deletes private messages in a conversation
        https://vk.com/dev/messages.deleteConversation

        :param user_id: User ID.
        :param peer_id: Destination ID
        :param offset: Offset needed to return a specific subset of messages.
        :param count: Number of messages to delete. Less then 10,000
        :param group_id: Group ID
        :return: 1
        """
        if count > 10000:
            count = 10000
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.deleteConversation", parameters=parameters)
        return result

    async def deny_messages_from_group(self, group_id: typing.Union[base.Integer, base.String]) -> int:
        """
        Denies sending message from community to the current user
        https://vk.com/dev/messages.denyMessagesFromGroup

        :param group_id: Community ID.

        :return:
        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.denyMessagesFromGroup", parameters=parameters)
        return result

    async def edit(self, peer_id: typing.Union[base.Integer, base.String],
                   message_id: base.Integer,
                   message: typing.Union[base.String, None] = None,
                   lat: base.Float = None,
                   long: base.Float = None,
                   attachment: Attachment = None,
                   keep_forward_messages: base.Boolean = False,
                   keep_snippets: base.Boolean = False,
                   group_id: typing.Union[base.Integer, base.String, None] = None,
                   dont_parse_links: base.Boolean = False) -> int:
        """
        Edits the message.
        You can edit sent message during 24 hours.
        https://vk.com/dev/messages.edit

        :param peer_id: Destination ID
        :param message_id: Message ID.
        :param message:  (Required if attachments is not set.) Text of the message
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param attachment: (Required if message is not set.)
                           List of objects attached to the message, separated by commas
        :param keep_forward_messages: 1 — to keep forwarded, messages
        :param keep_snippets: 1 — to keep attached snippets
        :param group_id: group ID
        :param dont_parse_links: flag, either 1 or 0, default

        :return: 1
        """
        keep_forward_messages = int(keep_forward_messages)
        keep_snippets = int(keep_snippets)
        dont_parse_links = int(dont_parse_links)
        if not message and not attachment:
            raise TypeError("missing 1 required positional argument: message or attachment")
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.edit", parameters=parameters)
        return result

    async def edit_chat(self, chat_id: typing.Union[base.Integer, base.String],
                        title: base.String) -> int:
        """
        Edits the title of a chat
        https://vk.com/dev/messages.editChat

        :param chat_id:
        :param title:
        :return: 1
        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.editChat", parameters=parameters)
        return result

    async def get_by_conversation_message_id(self, peer_id: typing.Union[base.Integer, base.String],
                                             conversation_message_ids: typing.Union[typing.List, typing.Tuple],
                                             extended: base.Boolean = False,
                                             fields: typing.Union[typing.List, typing.Tuple, None] = None,
                                             group_id: typing.Union[base.Integer, base.String, None] = None):
        """
        Returns conversations by their ids
        https://vk.com/dev/messages.getByConversationMessageId

        :param peer_id:
        :param conversation_message_ids: Maximum 100
        :param extended: 1 — return additional fields
        :param fields: additional fields
        :param group_id:

        :return:
        """
        extended = int(extended)
        if conversation_message_ids:
            conversation_message_ids = ",".join(conversation_message_ids)
        fields = ",".join(fields)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getByConversationMessageId", parameters=parameters)
        return result

    async def get_by_id(self, message_ids: typing.Union[typing.List, typing.Tuple],
                        preview_length: base.Integer = 0,
                        extended: base.Boolean = False,
                        fields: typing.Union[typing.List, typing.Tuple, None] = None,
                        group_id: typing.Union[base.Integer, base.String, None] = None):
        """
        Returns messages by their IDs.
        https://vk.com/dev/messages.getById

        :param message_ids: Maximum 100
        :param preview_length: Number of characters after which to truncate a previewed message.
                               To preview the full message, specify 0.
        :param extended: 1 — return additional fields
        :param fields: additional fields
        :param group_id:

        :return:
        """
        extended = int(extended)
        if fields:
            fields = ",".join(fields)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getById", parameters=parameters)
        return result

    async def get_chat(self, chat_id: typing.Union[base.Integer, base.String],
                       chat_ids: typing.Union[typing.List, typing.Tuple, None] = None,
                       fields: typing.Union[typing.List, typing.Tuple, None] = None,
                       name_case: base.String = "nom"):
        """
        Returns information about a chat.
        https://vk.com/dev/messages.getChat

        :param chat_id:
        :param chat_ids:
        :param fields: Profile fields to return.
        Allowed fields: nickname, screen_name, sex, bdate, city,
                        country, timezone, photo_50, photo_100,
                        photo_200_orig, has_mobile, contacts, education,
                        online, counters, relation, last_seen, status,
                        can_write_private_message, can_see_all_posts,
                        can_post, universities

        :param name_case: Case for declension of user name and surname.
        Возможные значения: nom — nominative,
                            gen — genitive,
                            dat — dative,
                            acc — accusative,
                            ins — instrumental,
                            abl — prepositional

        :return: Returns a list of chat objects.
                 If the fields parameter is set, the users field contains a list of user objects
                 with an additional invited_by field containing the ID of the user who invited the current user to chat.
        """
        if chat_ids:
            chat_ids = ",".join(chat_ids)
        if fields:
            fields = ",".join(fields)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getChat", parameters=parameters)
        return result

    async def get_chat_preview(self, link: base.String,
                               fields: typing.Union[typing.List, typing.Tuple, None] = None):
        """
        Allows to receive chat preview by the invitation link
        https://vk.com/dev/messages.getChatPreview

        :param link: Invitation link
        :param fields: List of profile fields to return.
                       Full list of fields: https://vk.com/dev/objects/user

        :return:
        """
        if fields:
            fields = ",".join(fields)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getChatPreview", parameters=parameters)
        return result

    async def get_conversation_members(self, peer_id: typing.Union[base.Integer, base.String],
                                       group_id: base.Integer = None,
                                       fields: typing.Union[typing.List, typing.Tuple, None] = None):
        """
        Returns a list of IDs of users participating in a conversation
        https://vk.com/dev/messages.getConversationMembers

        :param peer_id:
        :param group_id:
        :param fields: https://vk.com/dev/objects/user  https://vk.com/dev/objects/group

        :return:
        """
        if fields:
            fields = ",".join(fields)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getConversationMembers", parameters=parameters)
        return result

    async def get_conversations(self, offset: base.Integer = 0,
                                count: base.Integer = 20,
                                filter: base.String = "all",
                                extended: base.Boolean = False,
                                start_message_id: base.Integer = None,
                                fields: typing.Union[typing.List, typing.Tuple, None] = None,
                                group_id: base.Integer = None):
        """
        Returns a list of conversations.
        https://vk.com/dev/messages.getConversations

        :param offset: offset needed to return a specific subset of conversations
        :param count: number of conversations to return
        :param filter: types of conversations to return; possible values:
                       all — all conversations;
                       unread — conversations with unread messages;
                       important — conversations marked as important (only for community messages);
                       unanswered — conversations marked as unanswered (only for community messages).
        :param extended: return additional fields for users and communities.
        :param start_message_id: ID of the message from what to return conversations.
        :param fields: list of additional fields for users and communities.
                       https://vk.com/dev/objects/group https://vk.com/dev/objects/user
        :param group_id: group ID (for community messages with a user access token).

        :return:
        """
        if fields:
            fields = ",".join(fields)
        if extended:
            extended = int(extended)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getConversations", parameters=parameters)
        return result

    async def get_conversations_by_id(self, peer_ids: typing.Union[typing.List, typing.Tuple],
                                      extended: base.Boolean = False,
                                      fields: typing.Union[typing.List, typing.Tuple, None] = None,
                                      group_id: base.Integer = None):
        """
        Returns conversations by their IDs
        https://vk.com/dev/messages.getConversationsById

        :param peer_ids: list of comma-separated destination IDs.
        :param extended: 1 – return additional information about users and communities in users and communities fields.
        :param fields: list of additional fields for users and communities.
                       https://vk.com/dev/objects/group https://vk.com/dev/objects/user
        :param group_id: group ID (for community messages with a user access token).

        :return: Returns the total number of conversations in count field (integer) and
                 array of conversations in items field.
        """
        if peer_ids:
            peer_ids = ",".join(peer_ids)
        if fields:
            fields = ",".join(fields)
        if extended:
            extended = int(extended)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getConversationsById", parameters=parameters)
        return result

    async def get_history(self, offset: base.Integer,
                          user_id: typing.Union[base.Integer, base.String],
                          peer_id: typing.Union[base.Integer, base.String, None] = None,
                          count: base.Integer = 20,
                          start_message_id: base.Integer = None,
                          rev: base.Boolean = True,
                          extended: base.Boolean = False,
                          fields: typing.Union[typing.List, typing.Tuple, None] = None,
                          group_id: base.Integer = None):
        """
        Returns message history for the specified user or group chat.
        https://vk.com/dev/messages.getHistory

        :param offset: Offset needed to return a specific subset of messages.
        :param user_id: Number of messages to return.
        :param peer_id: ID of the user whose message history you want to return.
        :param count:
        :param start_message_id: Starting message ID from which to return history.
        :param rev: Sort order:
                    1 — return messages in chronological order.
                    0 — return messages in reverse chronological order.
        :param extended:
        :param fields:
        :param group_id:

        :return:
        """
        if fields:
            fields = ",".join(fields)
        if extended:
            extended = int(extended)
        if rev:
            rev = int(rev)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getHistory", parameters=parameters)
        return result

    async def get_history_attachments(self,
                                      peer_id: typing.Union[base.Integer, base.String],
                                      media_type: base.String = "photo",
                                      start_from: base.Integer = None,
                                      count: base.Integer = 20,
                                      photo_sizes: base.Boolean = None,
                                      fields: typing.Union[typing.List, typing.Tuple, None] = None,
                                      group_id: base.Integer = None):
        """
        Returns media files from the dialog or group chat
        https://vk.com/dev/messages.getHistoryAttachments

        :param peer_id:
        :param media_type: Type of media files to return:
                           photo;
                           video;
                           audio;
                           doc;
                           link
        :param start_from: Message ID to start return results from
        :param count: Number of objects to return
        :param photo_sizes: 1 — to return photo sizes in a special format
                            https://vk.com/dev/photo_sizes
        :param fields: Additional profile fields to return. https://vk.com/dev/fields
        :param group_id:

        :return: Returns a list of photo, video, audio or doc objects depending on
                 media_type parameter value and additional next_from field containing new offset value.
        """
        if fields:
            fields = ",".join(fields)
        if photo_sizes:
            photo_sizes = int(photo_sizes)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getHistoryAttachments", parameters=parameters)
        return result

    async def get_important_messages(self,
                                     count: base.Integer = 20,
                                     offset: base.Integer = None,
                                     start_message_id: base.Integer = None,
                                     preview_length: base.Integer = None,
                                     extended: base.Boolean = False,
                                     fields: typing.Union[typing.List, typing.Tuple, None] = None,
                                     group_id: base.Integer = None):
        """
        https://vk.com/dev/messages.getImportantMessages

        :param count:
        :param offset:
        :param start_message_id:
        :param preview_length:
        :param extended:
        :param fields:
        :param group_id:
        :return:
        """
        if fields:
            fields = ",".join(fields)
        if extended:
            extended = int(extended)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getImportantMessages", parameters=parameters)
        return result

    async def get_invite_link(self,
                              peer_id: typing.Union[base.Integer, base.String],
                              reset: base.Boolean = False,
                              group_id: base.Integer = None):
        """
        Receives a link to invite a user to the chat
        https://vk.com/dev/messages.getInviteLink

        :param peer_id:
        :param reset:
        :param group_id:

        :return: Returns an objects with the only field link (string) containing the link for inviting
        """
        if reset:
            reset = int(reset)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getInviteLink", parameters=parameters)
        return result

    async def get_last_activity(self, user_id: typing.Union[base.Integer, base.String]):
        """
        Returns a user's current status and date of last activity
        https://vk.com/dev/messages.getLastActivity

        :param user_id:

        :return: Returns an object with the following fields:
                 online — User's current status (0 — offline, 1 — online).
                 time — Date (in Unix time) of the user's last activity.
        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getLastActivity", parameters=parameters)
        return result

    async def get_long_poll_history(self, ts: base.Integer,
                                    pts: base.Integer,
                                    preview_length: base.Integer = 0,
                                    onlines: base.Boolean = None,
                                    fields: typing.Union[typing.List, typing.Tuple, None] = None,
                                    events_limit: base.Integer = 1000,
                                    msgs_limit: base.Integer = 200,
                                    max_msg_id: base.Integer = None,
                                    group_id: base.Integer = None,
                                    lp_version: base.Integer = None,
                                    last_n: base.Integer = 0):
        """
        Returns updates in user's private messages.
        To speed up handling of private messages, it can be useful to cache previously
        loaded messages on a user's mobile device/desktop, to prevent re-receipt at each call.
        With this method, you can synchronize a local copy of the message list with the actual version.
        https://vk.com/dev/messages.getLongPollHistory

        :param ts: Last value of the ts parameter returned from the Long Poll server
                    or by using messages.getLongPollServer method.
        :param pts: Last value of pts parameter returned from the Long Poll server
                    or by using messages.getLongPollServer method.
        :param preview_length: Number of characters after which to truncate a previewed message.
                               To preview the full message, specify 0.
        :param onlines: 1 — to return history with online users only
        :param fields: Additional profile fileds to return.
                       list of comma-separated words, default photo,photo_medium_rec,sex,online,screen_name
        :param events_limit: Maximum number of events to return.
        :param msgs_limit: Maximum number of messages to return.
        :param max_msg_id: Maximum ID of the message among existing ones in the local copy.
                           Both messages received with API methods
                           (for example, messages.getDialogs, messages.getHistory), and data received
                           from a Long Poll server (events with code 4) are taken into account.
        :param group_id:
        :param lp_version: Long Poll version.
        :param last_n: positive number, default 0, maximum value 2000

        :return: Returns an object
        """

        if fields:
            fields = ",".join(fields)
        if onlines:
            onlines = int(onlines)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getLongPollHistory", parameters=parameters)
        return result

    async def send(self, user_id: typing.Union[base.Integer, base.String, None] = None,
                   random_id=None,
                   peer_id: typing.Union[base.Integer, base.String, None] = None,
                   domain: base.String = None,
                   chat_id: typing.Union[base.Integer, base.String, None] = None,
                   user_ids: typing.Union[typing.List, typing.Tuple, None] = None,
                   message: typing.Union[base.String, None] = None,
                   lat: base.Float = None,
                   long: base.Float = None,
                   attachment: Attachment = None,
                   reply_to: typing.Union[base.Integer, base.String, None] = None,
                   forward_messages: typing.Union[typing.List, typing.Tuple, None] = None,
                   sticker_id: base.Integer = None,
                   group_id: typing.Union[base.Integer, base.String, None] = None,
                   keyboard: Keyboard = None,
                   payload=None,
                   dont_parse_links: base.Boolean = False):
        """
        Sends a message
        https://vk.com/dev/messages.send

        :param user_id: User ID (by default — current user).
        :param random_id: Unique identifier to avoid resending the message
        :param peer_id: Destination ID.
        :param domain: User's short address (for example, illarionov).
        :param chat_id: ID of conversation the message will relate to
        :param user_ids: IDs of message recipients (if new conversation shall be started).
        :param message: (Required if attachments is not set.) Text of the message.
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param attachment: Array of attachments
        :param reply_to: Reply to message id
        :param forward_messages: ID of forwarded messages, separated with a comma.
                                 Listed messages of the sender will be shown in the message body at the recipient's
        :param sticker_id:
        :param group_id:
        :param keyboard: Keyboard object
        :param payload:
        :param dont_parse_links: flag, either 1 or 0

        :return: Returns sent message ID
        """
        if user_ids:
            user_ids = ",".join(user_ids)
        if forward_messages:
            forward_messages = ",".join(forward_messages)
        dont_parse_links = int(dont_parse_links)
        keyboard = prepare_arg(keyboard)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name='messages.send', parameters=parameters)
        return result
