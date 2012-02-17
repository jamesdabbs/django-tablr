import json
import re
import urllib2

from django.shortcuts import redirect, render
    
def _acc(obj, accessors, default=[]):
    """ Simplies dealing with deeply-nested JSON """
    for a in accessors:
        if isinstance(a, str) and a in obj:
            obj = obj[a]
        elif isinstance(a, int) and isinstance(obj, list) and len(obj) > a:
            obj = obj[a]
        else:
            return default
    return obj


def home(request):
    """ Displays information about the tablr and a selection of AMAs """
    # Handle the page-selection 
    if request.method == 'POST':
        url = request.POST.get('page', '')
        m = re.search('(.*comments/)?([a-z0-9]+)(/.*)?', url)
        if m:
            return redirect('render_qa', id=m.groups()[1]) 
        else:
            error = True
        
    # Otherwise, display the current AMA frontpage (minus requests)
    data = urllib2.urlopen('http://www.reddit.com/r/IAmA/.json')
    data = json.load(data)
    
    # Get the (non-request) AMAs
    amas = []
    for d in _acc(data, ['data', 'children']):
        if 'request' not in _acc(d, ['data', 'title'], '').lower():
            amas.append(d['data'])
    
    return render(request, 'tablr/home.html', locals())
    
    
def render_qa(request, id):
    """ Renders the requested AMA in a Q&A format. """
    # Get a JSON dump of the requested AMA
    data = urllib2.urlopen('http://www.reddit.com/r/IAmA/comments/%s/.json?sort=top' % id)
    data = json.load(data)
    
    post = _acc(data, [0, 'data', 'children', 0, 'data'], {})
    author = post.get('author', None)
    
    # Get the top-level posts that the author has responded to
    responses = []
    for q in _acc(data, [1, 'data', 'children']):
        for r in _acc(q, ['data', 'replies', 'data', 'children']):
            if _acc(r, ['data', 'author']) == author:
                responses.append((q['data'], r['data']))
                break

    return render(request, 'tablr/render.html', locals())
