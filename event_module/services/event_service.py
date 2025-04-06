from datetime import timedelta, timezone


def check_status_event(event):
    """
    Check if the event is completed or cancelled based on its status.
    """
    
    if event.status == 1:
        return True
    elif event.status == 2:
        return False
    else:
        return None

def check_event_capacity_and_cancel(event):
    """
    Check if the event has reached its capacity and cancel it if it has.
    """
    
    time_remaining = event.start_date - timezone.now()
    
    if time_remaining <= timedelta.now(hours=1):
      if event.participants.count() < event.capacity:
        event.status = 2  # Assuming 2 is the status code for cancelled
        event.save()
        return True
    return False

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