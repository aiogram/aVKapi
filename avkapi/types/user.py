from . import base
from . import fields
from .base import VKObject
from ..types.photo import Photo
from ..utils.helper import Item, HelperMode
import typing


class Career(VKObject):
    group_id: base.Integer = fields.Field()
    company: base.String = fields.Field()
    country_id: base.Integer = fields.Field()
    city_id: base.Integer = fields.Field()
    city_name: base.Integer = fields.Field()
    from_year: base.Integer = fields.Field()
    until_year: base.Integer = fields.Field()
    position: base.String = fields.Field()


class City(VKObject):
    city_id: base.Integer = fields.Field()
    title: base.String = fields.Field()


class Country(VKObject):
    country_id: base.Integer = fields.Field()
    title: base.String = fields.Field()


class Connections(VKObject):
    skype: base.String = fields.Field()
    facebook: base.String = fields.Field()
    twitter: base.String = fields.Field()
    livejournal: base.String = fields.Field()
    instagram: base.String = fields.Field()


class Contacts(VKObject):
    mobile_phone: base.String = fields.Field()
    home_phone: base.String = fields.Field()


class Counters(VKObject):
    albums: base.Integer = fields.Field()
    videos: base.Integer = fields.Field()
    audios: base.Integer = fields.Field()
    photos: base.Integer = fields.Field()
    notes: base.Integer = fields.Field()
    friends: base.Integer = fields.Field()
    groups: base.Integer = fields.Field()
    online_friends: base.Integer = fields.Field()
    mutual_friends: base.Integer = fields.Field()
    user_videos: base.Integer = fields.Field()
    followers: base.Integer = fields.Field()
    pages: base.Integer = fields.Field()


class Crop(VKObject):
    x: base.Integer = fields.Field()
    y: base.Integer = fields.Field()
    x1: base.Integer = fields.Field()
    y2: base.Integer = fields.Field()


class CropPhotoInfo(VKObject):
    photo: Photo = fields.Field(base=Photo)
    crop: Crop = fields.Field(base=Crop)
    rect: Crop = fields.Field(base=Crop)


class Education(VKObject):
    university: base.Integer = fields.Field()
    university_name: base.String = fields.Field()
    faculty: base.Integer = fields.Field()
    faculty_name: base.String = fields.Field()
    graduation: base.Integer = fields.Field()


class LastSeen(VKObject):
    time: base.Integer = fields.Field()
    platform: base.Integer = fields.Field()


class Military(VKObject):
    unit: base.String = fields.Field()
    unit_id: base.Integer = fields.Field()
    country_id: base.Integer = fields.Field()
    from_year: base.Integer = fields.Field()
    until_year: base.Integer = fields.Field()


class Occupation(VKObject):
    type: base.String = fields.Field()
    school_id: base.Integer = fields.Field()
    name: base.String = fields.Field()


class Relative(VKObject):
    relative_id: base.Integer = fields.Field()
    name: base.String = fields.Field()
    type: base.String = fields.Field()


class PersonalInfo(VKObject):
    political: base.Integer = fields.Field()
    langs: typing.List = fields.Field()
    religion: base.String = fields.Field()
    inspired_by: base.String = fields.Field()
    people_main: base.Integer = fields.Field()
    life_main: base.Integer = fields.Field()
    smoking: base.Integer = fields.Field()
    alcohol: base.Integer = fields.Field()


class School(VKObject):
    school_id: base.Integer = fields.Field()
    country: base.Integer = fields.Field()
    city: base.Integer = fields.Field()
    name: base.String = fields.Field()
    year_from: base.Integer = fields.Field()
    year_to: base.Integer = fields.Field()
    year_graduated: base.Integer = fields.Field()
    class_name: base.String = fields.Field()
    speciality: base.String = fields.Field()
    type: base.Integer = fields.Field()
    type_str: base.Integer = fields.Field()


class University(VKObject):
    university_id: base.Integer = fields.Field()
    country: base.Integer = fields.Field()
    city: base.Integer = fields.Field()
    name: base.String = fields.Field()
    faculty: base.Integer = fields.Field()
    faculty_name: base.String = fields.Field()
    chair: base.Integer = fields.Field()
    chair_name: base.String = fields.Field()
    graduation: base.Integer = fields.Field()
    education_form: base.String = fields.Field()
    education_status: base.String = fields.Field()


class NameCase:
    mode = HelperMode.lowercase
    NOM = Item()
    GEN = Item()
    DAT = Item()
    ACC = Item()
    INS = Item()
    ABL = Item()


class UserFields:
    mode = HelperMode.lowercase

    USER_ID = Item()
    FIRST_NAME = Item()
    LAST_NAME = Item()
    DEACTIVATED = Item()
    IS_CLOSED = Item()
    CAN_ACCESS_CLOSED = Item()
    ABOUT = Item()
    ACTIVITIES = Item()
    BDATE = Item()
    BLACKLISTED = Item()
    BLACKLISTED_BY_ME = Item()
    BOOKS = Item()
    CAN_POST = Item()
    CAN_SEE_ALL_POSTS = Item()
    CAN_SEE_AUDIO = Item()
    CAN_SEND_FRIEND_REQUEST = Item()
    CAN_WRITE_PRIVATE_MESSAGE = Item()
    CAREER = Item()
    CITY = Item()
    COMMON_COUNT = Item()
    CONNECTIONS = Item()
    CONTACTS = Item()
    COUNTERS = Item()
    COUNTRY = Item()
    CROP_PHOTO = Item()
    DOMAIN = Item()
    EDUCATION = Item()
    EXPORTS = Item()
    # first_name_{case} = Item()
    FOLLOWERS_COUNT = Item()
    FRIEND_STATUS = Item()
    GAMES = Item()
    HAS_MOBILE = Item()
    HAS_PHOTO = Item()
    HOME_TOWN = Item()
    INTERESTS = Item()
    IS_FAVORITE = Item()
    IS_FRIEND = Item()
    IS_HIDDEN_FROM_FEED = Item()
    # last_name_{case} = Item()
    LAST_SEEN = Item()
    LISTS = Item()
    MAIDEN_NAME = Item()
    MILITARY = Item()
    MOVIES = Item()
    MUSIC = Item()
    NICKNAME = Item()
    OCCUPATION = Item()
    ONLINE = Item()
    PERSONAL = Item()
    PHOTO_50 = Item()
    PHOTO_100 = Item()
    PHOTO_200_ORIG = Item()
    PHOTO_200 = Item()
    PHOTO_400_ORIG = Item()
    PHOTO_ID = Item()
    PHOTO_MAX = Item()
    PHOTO_MAX_ORIG = Item()
    QUOTES = Item()
    RELATIVES = Item()
    RELATION = Item()
    SCHOOLS = Item()
    SCREEN_NAME = Item()
    SEX = Item()
    SITE = Item()
    STATUS = Item()
    STATUS_AUDIO = Item()
    TIMEZONE = Item()
    TRENDING = Item()
    TV = Item()
    UNIVERSITIES = Item()
    VERIFIED = Item()
    WALL_DEFAULT = Item()


class User(VKObject):
    """
    https://vk.com/dev/objects/user
    """
    user_id: base.Integer = fields.Field()
    first_name: base.String = fields.Field()
    last_name: base.String = fields.Field()
    deactivated: base.String = fields.Field()
    is_closed: base.Boolean = fields.Field()
    can_access_closed: base.Boolean = fields.Field()

    about: base.String = fields.Field()
    activities: base.String = fields.Field()
    bdate: base.String = fields.Field()
    blacklisted: base.Integer = fields.Field()
    blacklisted_by_me: base.Integer = fields.Field()
    books: base.String = fields.Field()
    can_post: base.Integer = fields.Field()
    can_see_all_posts: base.Integer = fields.Field()
    can_see_audio: base.Integer = fields.Field()
    can_send_friend_request: base.Integer = fields.Field()
    can_write_private_message: base.Integer = fields.Field()
    career: Career = fields.Field(base=Career)
    city: City = fields.Field(base=City)
    common_count: base.Integer = fields.Field()
    connections: Connections = fields.Field(base=Connections)
    contacts: Contacts = fields.Field(base=Contacts)
    counters: Counters = fields.Field(base=Counters)
    country: Country = fields.Field(base=Country)
    crop_photo: CropPhotoInfo = fields.Field(base=CropPhotoInfo)
    domain: base.String = fields.Field()
    education: Education = fields.Field(base=Education)
    exports: base.String = fields.Field()  # Not sure which type. Not specified
    # first_name_{case}: base.String = fields.Field()  ??????
    followers_count: base.Integer = fields.Field()
    friend_status: base.Integer = fields.Field()
    games: base.String = fields.Field()
    has_mobile: base.Integer = fields.Field()
    has_photo: base.Integer = fields.Field()
    home_town: base.String = fields.Field()
    interests: base.String = fields.Field()
    is_favorite: base.Integer = fields.Field()
    is_friend: base.Integer = fields.Field()
    is_hidden_from_feed: base.Integer = fields.Field()
    # last_name_{case}: base.String = fields.Field()  ????????
    last_seen: LastSeen = fields.Field(base=LastSeen)
    lists: base.String = fields.Field()
    maiden_name: base.String = fields.Field()
    military: Military = fields.Field(base=Military)
    movies: base.String = fields.Field()
    music: base.String = fields.Field()
    nickname: base.String = fields.Field()
    occupation: Occupation = fields.Field(base=Occupation)
    online: base.Integer = fields.Field()
    personal: PersonalInfo = fields.Field(base=PersonalInfo)
    photo_50: base.String = fields.Field()
    photo_100: base.String = fields.Field()
    photo_200_orig: base.String = fields.Field()
    photo_200: base.String = fields.Field()
    photo_400_orig: base.String = fields.Field()
    photo_id: base.String = fields.Field()
    photo_max: base.String = fields.Field()
    photo_max_orig: base.String = fields.Field()
    quotes: base.String = fields.Field()
    relatives: typing.List[Relative] = fields.Field()
    relation: base.Integer = fields.Field()
    schools: typing.List[School] = fields.Field()
    screen_name: base.String = fields.Field()
    sex: base.Integer = fields.Field()
    site: base.String = fields.Field()
    status: base.String = fields.Field()
    status_audio: base.String = fields.Field()
    timezone: base.Integer = fields.Field()
    trending: base.Integer = fields.Field()
    tv: base.String = fields.Field()
    universities: typing.List[University] = fields.Field()
    verified: base.Integer = fields.Field()
    wall_default: base.String = fields.Field()
