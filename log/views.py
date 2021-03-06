import json

from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from aglaia.settings import LOGIN_URL, ACCOUNT_HOME_URL, EMAIL_AUTH_PREFIX
from aglaia.decorators import *
from aglaia.views import show_message, get_context_list, no_excp_post, no_excp_get

from account.views import get_context_user
from computing.models import *
from computing.interface import *
from goods.interface import *
from goods.models import *
from log.models import *
from log.interface import *

def get_context_log(lg):
    dc = {}
    dc['actor'] = User.objects.get(id=lg.user_id)
    dc['target'] = lg.get_target_str()
    dc['action'] = lg.action
    dc['time'] = lg.time
    dc['desc'] = lg.description
    return dc


def get_borrow_loglist_context(id, is_actor):        
    l = LogBorrow.objects.filter(target__id=id).order_by('time')
    return get_context_list(l, lambda lg: dict(get_context_log(lg), repair_record = lg.repair_record))

def get_computing_loglist_context(id, is_actor):
    l = LogComputing.objects.filter(target__id=id).order_by('time')
    return get_context_list(l, get_context_log)

def get_goods_loglist_context(id, is_actor):
    l = LogSingle.objects.filter(target__id=id).order_by('time')
    return get_context_list(l, get_context_log)

def get_account_loglist_context(id, is_actor):
    from itertools import chain
    from django.db.models import Q
    from operator import attrgetter
    l = None
    if is_actor == 'true':
        accountLog = LogAccount.objects.filter(user_id=id)
        brwLog = LogBorrow.objects.filter(user_id=id)
        compLog = LogComputing.objects.filter(user_id=id)
        goodLog = LogSingle.objects.filter(user_id=id)
        l = sorted(chain(accountLog, brwLog, compLog, goodLog), key=attrgetter('time'), reverse=False)
    elif is_actor == 'false':
        l = LogAccount.objects.filter(target__user__id=id).order_by('time')
    else:
        accountLog = LogAccount.objects.filter(Q(user_id=id)|Q(target__user__id=id))
        brwLog = LogBorrow.objects.filter(user_id=id)
        compLog = LogComputing.objects.filter(user_id=id)
        goodLog = LogSingle.objects.filter(user_id=id)
        l = sorted(chain(accountLog, brwLog, compLog, goodLog), key=attrgetter('time'), reverse=False)
    return get_context_list(l, get_context_log)


def get_purchase_destroy_context_log(lg):
    dc = {}
    dc['actor'] = User.objects.get(id=lg.user_id)
    dc['target'] = lg.get_target_str()
    dc['action'] = lg.action
    dc['time'] = lg.time
    dc['desc'] = lg.description
    sgl = lg.target
    good = sgl.goods
    tp = good.gtype    
    try:
        pur = Purchase.objects.get(single=sgl)
        dc['manufacturer'] = pur.manufacturer
        dc['version'] = pur.version
        dc['other'] = pur.other
    except Exception as e:
        pass
        
    dc['gtype'] = tp.name
    
    props = []
    for i in range(0,tp.get_pronum()):
        props.append({'pro_name':tp.get_proname(i),
                      'pro_value':good.get_pro(i)})
    dc['prop'] = props    
    return dc


def get_purchase_destroy_context():
    l = LogPurchaseDestroy.objects.filter().order_by('-time')
    return get_context_list(l, get_purchase_destroy_context_log)
    

log_list_func = {
    'goods':get_goods_loglist_context,
    'computing':get_computing_loglist_context,
    'user':get_account_loglist_context,
    'borrow':get_borrow_loglist_context
}
    

@method_required('GET')
@login_required       
def show_log(request):
    try:
        g = request.GET
        is_actor = None
        if 'is_actor' in g:
            is_actor = g['is_actor']
        llist = log_list_func[g['type']](g['id'], is_actor)
        
 
        def show_repair_log():
            return render(request, 'borrow_log.html', {
                'user':get_context_user(request.user),
                'logs': llist
                })           
        
        @permission_required(PERM_VIEW_ALL)
        def show_other_log(request):
            if g['type'] == 'borrow':
                return show_repair_log()
            else:
                return render(request, 'log.html', {
                    'user':get_context_user(request.user),
                    'logs': llist
                    })
        
        if g['type'] == 'borrow'and Borrow.objects.get(id=g['id']).account.user == request.user: #判断是否是借用人
            return show_repair_log()
        else:
            
            return show_other_log(request)
        
    except Exception as e:
        return show_message(request, 'Show log Error: ' + e.__str__())



@method_required('GET')
@permission_required(PERM_VIEW_ALL)
def show_purchase_destroy_list(request):
    try:
        llist = get_purchase_destroy_context()
        return render(request, 'purchase_destroy_log.html', {
            'user':get_context_user(request.user),
            'logs': llist
            })
        
        
    except Exception as e:
        return show_message(request, 'Show log Error: ' + e.__str__())
