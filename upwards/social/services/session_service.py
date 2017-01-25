import json

from django.utils.crypto import get_random_string

from social.models import Login, Customer
from social_service import SocialProfile


def get_opposite_platform(platform):
    platform_opposites = {
        'facebook': 'google',
        'google': 'facebook'
    }
    return platform_opposites.get(platform)


def generate_session_token(customer_id):
    return 'upwards_' + str(customer_id) + '_' + get_random_string(length=32)


def session_success_data(login_object):
    return {
        'session_token': login_object.session_token,
        'customer_id': login_object.customer_id
    }


def email_related_sessions(email_id):
    sessions = Login.email_related_logins(email_id)
    if not sessions:
        return {}
    else:
        platform_sessions = {
            'facebook': None,
            'google': None
        }
        for session in sessions:
            platform_sessions[session.platform] = session
        return platform_sessions


# def type_of_customer(email_sessions, platform):
#     if email_sessions:
#         if email_sessions.get(platform):
#             if email_sessions[platform].session_token:
#                 return "returning_live_session_customer"
#             else:
#                 if email_sessions[get_opposite_platform(platform)]:
#         else:

#     else:
#         return "first_time_customer"


def email_related_sessionss(email_id):
    sessions = Login.email_related_logins(email_id)
    platform_sessions_data = {
        'facebook': {
            "customer_record": False,
            "session_token": "",
            "active": False,
            "object": None
        },
        'google': {
            "customer_record": False,
            "session_token": "",
            "active": False,
            "object": None
        }
    }
    if sessions:
        for session in sessions:
            platform_sessions_data[session.platform] = {
                "customer_record": True,
                "session_token": session.session_token,
                "active": session.is_active,
                "object": session
            }
    return platform_sessions_data


def create_new_session(session_input, social_profile):
    new_customer = Customer.objects.create()
    session_object_dict = {
        'platform_token': session_input['platform_token'],
        'source': session_input['source'],
        'platform': session_input['platform'],
        'customer': new_customer,
        'social_data': json.dumps(social_profile.data),
        'email_id': social_profile.email_id,
        'session_token': generate_session_token(new_customer.customer_id)
    }
    new_session = Login.objects.create(**login_object_dict)
    return session_success_data(new_session)


def update_session(session_pk, session_data):
    Login.objects.filter(pk=session_pk).update(**session_data)
    session_obj = Login.objects.get(pk=session_pk)
    return session_success_data(session_obj)


def create_session_from_obj(session_obj, session_input, social_profile, new_session_token=False):
    session_obj.id = None
    session_obj.platform_token = session_input['platform_token']
    session_obj.platform = session_input['platform']
    session_obj.social_data = json.dumps(social_profile.data)
    if new_session_token:
        session_obj.session_token = generate_session_token(
            session_obj.customer_id)
    session_obj.save()
    return session_success_data(session_obj)


def get_or_create_sessionss(session_input):
    platform = session_input['platform']
    platform_token = session_input['platform_token']
    source = session_input['source']
    social_profile = SocialProfile(platform, platform_token)
    email_sessions = email_related_sessionss(social_profile.email_id)
    opposite_platform = get_opposite_platform(platform)

    if not (email_sessions['facebook']['customer_record'] or email_sessions['google']['customer_record']):
        # CASE: First Time user with no record in database
        # ACTION: Create new session and return new session_token and
        # customer_id
        return create_new_session(session_input, social_profile)
    else:
        if email_sessions[platform]["customer_record"]:
            if email_sessions[platform]["active"]:
                # CASE: DB has record of this Customer and his Session is Active
                # ACTION: Update the Session with the new platform token and
                # updated time and return old session_token and customer_id
                session_data = {
                    "platform_token": platform_token,
                    "social_data": json.dumps(social_profile.data)
                }
                return update_session(email_sessions[platform]["object"].id, session_data)

            else:
                if email_sessions[opposite_platform]["active"]:
                    # CASE: DB has record of this Customer and but his Session is InActive and Opposite Session Active
                    # ACTION: Activate this session by the opposite platform
                    # session_token, put this platform token and return old
                    # session_token and customer
                    session_data = {
                        "platform_token": platform_token,
                        "social_data": json.dumps(social_profile.data),
                        "session_token": email_sessions[opposite_platform].session_token,
                        "is_active": True
                    }
                    return update_session(email_sessions[platform]["object"].id, session_data)
                else:
                    if email_sessions[opposite_platform]["customer_record"]:
                        # CASE: DB has record of this Customer and but his Session is InActive and Opposite Session is In Active
                        # ACTION: Activate this session by the new session
                        # token and return session_token and customer_id
                        session_data = {
                            "platform_token": platform_token,
                            "social_data": json.dumps(social_profile.data),
                            "session_token": generate_session_token(email_sessions[platform]["object"].customer_id),
                            "is_active": True
                        }
                        return update_session(email_sessions[platform]["object"].id, session_data)
                    else:
                        # CASE: DB has record of this Customer and but his Session is InActive and Opposite Session has no Record
                        # ACTION: Activate this session by the new session
                        # token and return session_token and customer_id
                        session_data = {
                            "platform_token": platform_token,
                            "social_data": json.dumps(social_profile.data),
                            "session_token": generate_session_token(email_sessions[platform]["object"].customer_id),
                            "is_active": True
                        }
                        return update_session(email_sessions[platform]["object"].id, session_data)
        else:
            if email_sessions[opposite_platform]["customer_record"]:
                if email_sessions[opposite_platform]["active"]:
                    # CASE: DB has a record of this Customer, but his platform session record is not there and his other platform is active
                    # ACTION: Copy the Session with the other platform
                    # session_token and cust_id and return the session token
                    # and cust_id
                    return create_session_from_obj(email_sessions[opposite_platform]["object"], session_input, social_profile)
                else:
                    # CASE: DB has record of this Customer, this platform session record is not there  and his other platform session Inactive
                    # ACTION: Create a the Session and copy the cust_id and
                    # return the session_token and cust_id
                    return create_session_from_obj(email_sessions[opposite_platform]["object"], session_input, social_profile, True)
            else:
                pass
                # Not Possible


# def get_or_create_session(session_input):
#     platform = session_input['platform']
#     platform_token = session_input['platform_token']
#     source = session_input['source']
#     social_profile = SocialProfile(platform, platform_token)
#     email_sessions = email_related_sessions(social_profile.email_id)
#     if email_sessions:
#         session = email_sessions.get(
#             platform)
#         if session:
#             if not session.session_token:
#                 opposite_platform_session = email_sessions.get(
#                     get_opposite_platform(platform))
#                 if opposite_platform_session:
#                     if opposite_platform.session_token:
#                         session_token = generate_session_token(
#                             opposite_platform.customer_id)
#                         session.session_token = session_token
#                         session.is_active = True
#                         session.deleted_at = None
#                         session.save()
#                 else:

#                 session_token = generate_session_token(
#                     session.customer_id)
#                 session.session_token = session_token
#                 session.is_active = True
#                 session.deleted_at = None
#                 session.save()
#             return session_success_data(session)
#         else:
#             print 101001
#             new_session = email_sessions.get(
#                 get_opposite_platform(platform))
#             new_session.id = None
#             new_session.platform = platform
#             new_session.platform_token = platform_token
#             print new_session.session_token
#             print new_session.is_active
#             if not new_session.session_token:
#                 session_token = generate_session_token(
#                     new_session.customer_id)
#                 new_session.session_token = session_token
#                 new_session.is_active = True
#                 new_session.deleted_at = None
#             new_session.save()
#             return session_success_data(new_session)
#     else:
#         new_customer = Customer.objects.create()
#         login_object_dict = {
#             'platform_token': session_input['platform_token'],
#             'source': session_input['source'],
#             'platform': session_input['platform'],
#             'customer': new_customer,
#             'social_data': json.dumps(social_profile.data),
#             'email_id': social_profile.email_id,
#             'session_token': generate_session_token(new_customer.customer_id)
#         }
#         new_session = Login.objects.create(**login_object_dict)
#         print new_session.is_active
#         return session_success_data(new_session)
