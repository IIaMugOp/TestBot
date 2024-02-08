def find_user_by_message_id(message_id_to_find, message_dict):
    for user_id, message_id in message_dict.items():
        if message_id == message_id_to_find:
            return user_id
    return None