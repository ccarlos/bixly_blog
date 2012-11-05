from django.template import Library

register = Library()


@register.filter
def reverse(value):
    """Reverse a list. Used inside the template enviroment.

    http://dmitko.ru/get_comment_list-reversed/
    """

    value.reverse()
    return value


@register.filter
def liked_comment(value, arg):
    """Has the user liked the comment?"""

    like = value.likes.filter(creator=arg)

    if like:
        return True
    return False
