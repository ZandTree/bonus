import random
import string
from django.utils import timezone

def rand_string(n):
    """
    return a string from ascii chars with random letters and numbers
    """
    mix = string.ascii_letters + string.digits
    final_string = [random.choice(mix) for item in range(n)]
    return "".join(final_string)

def create_uid(instance):
    """
    create unique id for instance based on random letters and digits
    which have attr = uid
    """
    klass = instance.__class__
    start_uid = rand_string(4)
    if klass.objects.filter(uid=start_uid).exists():
        instance.uid = rand_string(4)
        return create_profile_uid(instance)
    return start_uid

def make_avatar(instance,file):
    time = timezone.now().strftime("Y-%m-%d")
    tail = file.split('.')[-1]
    head = file.split('.')[0]
    if len(head) >10:
        head = head[:10]
    file_name = head + '.' + tail
    user_folder = instance.user_id
    return  os.path.join('avatars',user_folder,file_name)
