from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext


def main_context_proc(request):
    """ A context processor for each view
    """
    return {}


@login_required
def view_main(request):
    t = get_template('index.html')
    c = RequestContext(request, {
        "items": []
    }, processors=[main_context_proc])

    html = t.render(c)
    return HttpResponse(html)
