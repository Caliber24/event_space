def check_capacity(event):
    """
    Check if the event has reached its capacity.
    """
    if event.participants.count() >= event.capacity:
        return False
    return True

def check_event_creator(event, user):
    """
    Check if the user is the creator of the event.
    """
    if event.creator == user:
        return True
    return False

def check_event_participant(event, user):
    """
    Check if the user is a participant of the event.
    """
    if event.participants.filter(id=user.id).exists():
        return True
    return False

def add_participant(event, user):
    """
    Add a user to the event participants.
    """
    
    event.participants.add(user)
    event.save()