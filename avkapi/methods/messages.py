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
        Добавляет в мультидиалог нового пользователя.
        Чтобы пользователю вернуться в беседу, которую он сам покинул,
        достаточно отправить сообщение в неё (если есть свободные места),
        либо вызвать этот метод, передав свой идентификатор в параметре user_id.
        :param chat_id: идентификатор беседы
        :param user_id: идентификатор пользователя, которого необходимо включить в беседу
        :return: 1
        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.addChatUser", parameters=parameters)
        return result

    async def allow_messages_from_group(self, group_id: typing.Union[base.Integer, base.String],
                                        key: base.String = None) -> int:
        """

        Позволяет разрешить отправку сообщений от сообщества текущему пользователю
        :param group_id: идентификатор сообщества.
        :param key: произвольная строка. Этот параметр можно использовать для идентификации пользователя.
        Его значение будет возвращено в событии message_allow Callback API.
        :return: 1
        """
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.allowMessagesFromGroup", parameters=parameters)
        return result

    async def create_chat(self, user_ids: typing.Union[typing.List, typing.Tuple],
                          title: base.String) -> int:
        """
        Создаёт беседу с несколькими участниками
        :param user_ids: идентификаторы пользователей, которых нужно включить в мультидиалог.
        Должны быть в друзьях у текущего пользователя.
        :param title: название беседы
        :return: После успешного выполнения возвращает идентификатор созданного чата (chat_id).
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
        Удаляет сообщение
        :param message_ids: список идентификаторов сообщений, разделённых через запятую
        :param spam: пометить сообщения как спам.
        :param group_id: идентификатор сообщества (для сообщений сообщества с ключом доступа пользователя).
        :param delete_for_all: 1 — если сообщение нужно удалить для получателей
        (если с момента отправки сообщения прошло не более 24 часов ).
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
        Позволяет удалить фотографию мультидиалога
        :param chat_id: идентификатор беседы
        :param group_id: идентификатор сообщества (для сообщений сообщества с ключом доступа пользователя)
        :return: После успешного выполнения возвращает объект, содержащий следующие поля:
        message_id — идентификатор отправленного системного сообщения;
        chat — объект мультидиалога.
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
        Удаляет личные сообщения в беседе
        :param user_id: идентификатор пользователя. Если требуется очистить историю беседы, используйте peer_id.
        :param peer_id: идентификатор назначения
        :param offset: начиная с какого сообщения нужно удалить переписку.
        (По умолчанию удаляются все сообщения начиная с первого).
        :param count: сколько сообщений нужно удалить. Обратите внимание, что на метод наложено ограничение,
        за один вызов нельзя удалить больше 10000 сообщений,
        поэтому если сообщений в переписке больше — метод нужно вызывать несколько раз.
        :param group_id: идентификатор сообщества (для сообщений сообщества с ключом доступа пользователя)
        :return: 1
        """
        if count > 10000:
            count = 10000
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.deleteConversation", parameters=parameters)
        return result

    async def deny_messages_from_group(self, group_id: typing.Union[base.Integer, base.String]) -> int:
        """
        Позволяет запретить отправку сообщений от сообщества текущему пользователю
        :param group_id: идентификатор сообщества
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
        Редактирует сообщение
        :param peer_id: идентификатор назначения
        :param message_id: идентификатор сообщения
        :param message: текст сообщения. Обязательный параметр, если не задан параметр attachment
        :param lat: географическая широта (от -90 до 90).
        :param long: географическая долгота (от -180 до 180).
        :param attachment: медиавложения к личному сообщению
        :param keep_forward_messages: 1, чтобы сохранить прикреплённые пересланные сообщения
        :param keep_snippets: 1, чтобы сохранить прикреплённые внешние ссылки (сниппеты)
        :param group_id: идентификатор сообщества (для сообщений сообщества с ключом доступа пользователя)
        :param dont_parse_links: 1 — не создавать сниппет ссылки из сообщения
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
        Изменяет название беседы.
        :param chat_id: идентификатор беседы
        :param title: новое название для беседы
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
        Возвращает сообщения по их идентификаторам в рамках беседы или диалога
        :param peer_id: идентификаторы назначений, разделённые запятой
        :param conversation_message_ids: идентификаторы сообщений. Максимум 100 идентификаторов
        :param extended: 1 — возвращать дополнительные поля.
        :param fields: дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        :param group_id: идентификатор сообщества (для сообщений сообщества с ключом доступа пользователя).
        :return: После успешного выполнения возвращает объект,
        содержащий число результатов в поле count и массив объектов, описывающих сообщения, в поле items.
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
        Возвращает сообщения по их идентификаторам
        :param message_ids: идентификаторы сообщений. Максимум 100 идентификаторов
        :param preview_length: количество символов, по которому нужно обрезать сообщение.
        Укажите 0, если Вы не хотите обрезать сообщение. (по умолчанию сообщения не обрезаются)
        :param extended: 1 — возвращать дополнительные поля.
        :param fields: дополнительные поля пользователей и сообществ, которые необходимо вернуть в ответе.
        :param group_id: идентификатор сообщества (для сообщений сообщества с ключом доступа пользователя).
        :return: После успешного выполнения возвращает объект,
        содержащий число результатов в поле count и массив объектов, описывающих сообщения, в поле items.
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
        Возвращает информацию о беседе
        :param chat_id: идентификатор беседы
        :param chat_ids: список идентификаторов бесед
        :param fields: список дополнительных полей профилей, которые необходимо вернуть.
        Доступные значения: nickname, screen_name, sex, bdate, city,
                            country, timezone, photo_50, photo_100,
                            photo_200_orig, has_mobile, contacts, education,
                            online, counters, relation, last_seen, status,
                            can_write_private_message, can_see_all_posts,
                            can_post, universities
        :param name_case: падеж для склонения имени и фамилии пользователя.
        Возможные значения: nom — именительный,
                            gen — родительный,
                            dat — дательный,
                            acc — винительный,
                            ins — творительный,
                            abl — предложный
        :return: После успешного выполнения возвращает объект (или список объектов) мультидиалога.

                 Если был задан параметр fields, поле users содержит список объектов пользователей с
                 дополнительным полем invited_by, содержащим идентификатор пользователя, пригласившего в беседу.
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
        Получает данные для превью чата с приглашением по ссылке
        :param link: ссылка-приглашение
        :param fields: список полей профилей, данные о которых нужно получить.
                       Полный список смотрите на https://vk.com/dev/objects/user

        :return: Возвращает объект, который содержит следующие поля:
        preview object, profiles (array), groups (array), emails (array)
        """
        if fields:
            fields = ",".join(fields)
        parameters = generate_payload(**locals())
        result = await self._api_request(method_name="messages.getChatPreview", parameters=parameters)
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
        Отправляет сообщение
        :param user_id: идентификатор пользователя, которому отправляется сообщение
        :param random_id: уникальный (в привязке к API_ID и ID отправителя) идентификатор,
                          предназначенный для предотвращения повторной отправки одинакового сообщения.
                          Сохраняется вместе с сообщением и доступен в истории сообщений.
                          Заданный random_id используется для проверки уникальности за всю историю сообщений,
                          поэтому используйте большой диапазон(до int32).
        :param peer_id: идентификатор назначения
        :param domain: короткий адрес пользователя (например, illarionov).
        :param chat_id: идентификатор беседы, к которой будет относиться сообщение
        :param user_ids: идентификаторы получателей сообщения (при необходимости отправить сообщение сразу
                         нескольким пользователям).
                         Доступно только для ключа доступа сообщества.
                         Максимальное количество идентификаторов: 100.
        :param message: текст личного сообщения. Обязательный параметр, если не задан параметр attachment.
        :param lat: географическая широта (от -90 до 90).
        :param long: географическая долгота (от -180 до 180).
        :param attachment: медиавложения к личному сообщению, перечисленные через запятую
        :param reply_to: идентификатор сообщения, на которое требуется ответить
        :param forward_messages: идентификаторы пересылаемых сообщений, перечисленные через запятую.
                                 Перечисленные сообщения отправителя будут отображаться в теле письма у получателя.
                                 Не более 100 значений на верхнем уровне, максимальный уровень вложенности: 45,
                                 максимальное количество пересылаемых сообщений 500
        :param sticker_id: идентификатор стикера
        :param group_id: идентификатор сообщества (для сообщений сообщества с ключом доступа пользователя).
        :param keyboard: объект, описывающий клавиатуру для бота.  https://vk.com/dev/bots_docs_3
        :param payload: Полезная нагрузка
        :param dont_parse_links: 1 — не создавать сниппет ссылки из сообщения
        :return:
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
