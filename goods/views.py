from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required

import computing
from aglaia.settings import LOGIN_URL, ACCOUNT_HOME_URL, EMAIL_AUTH_PREFIX, USER_RETURN_MESSAGE, USER_MISS_MESSAGE
from aglaia.views import show_message, get_context_list, no_excp_post, no_excp_get
from aglaia.decorators import permission_required, method_required, http_denied, show_denied_message
from aglaia.messages import *
from account.views import get_context_user
from account.models import *
from goods.models import *
from account.interface import *
from computing.interface import *
from goods.interface import *
from aglaia.mail_tools import *


from computing.views import get_context_computing, get_context_pack
import json
import xlrd
import xlwt

sgl_sta_map = {
    'available':AVALIABLE_KEY,
    'unavailable':UNAVALIABLE_KEY,
    'destroyed':DESTROYED_KEY,
    'borrowed':BORROWED_KEY,
    'lost':LOST_KEY,
    'repairing':REPAIRING_KEY,
    'purchasing':PURCHASE_AUTHING_KEY
}


#===============================================
#===============================================
#===============================================
#===============================================
#===============================================
#===============================================

def get_pack_name(pack):
    return pack.name


def get_context_single(sgl):
    good = sgl.goods
    tp = good.gtype
    dc = {}
    dc['id'] = sgl.id
    dc['name'] = good.name
    dc['type_id'] = tp.id
    dc['type_name'] = tp.name
    dc['sn'] = sgl.sn
    dc['status'] = sgl.get_status_display()
    try:
        acc = Account.objects.get(user__username=sgl.user_name)
        dc['user_name'] = acc.real_name
        dc['user_id'] = sgl.user_name
        dc['user_realid'] = acc.user.id
    except:
        dc['user_id'] = ''
        dc['user_name'] = ''
        dc['user_realid'] = ''
    dc['note'] = sgl.note
    props = []
    for i in range(0,tp.get_pronum()):
        props.append({'pro_count': 'pro' + str(i),
                      'pro_name':tp.get_proname(i),
                      'pro_value':good.get_pro(i)})
    dc['prop'] = props
    return dc

def get_context_borrow(brw):
    dc = {}
    dc['id'] = brw.id
    dc['sn'] = brw.single.sn
    dc['goods_name'] = brw.single.goods.name
    dc['borrower_name'] = brw.account.user.username
    dc['note'] = brw.user_note
    return dc

def get_context_userbrw(brw):
    dc = {}
    dc['id'] = brw.id
    dc['sn'] = brw.single.sn
    dc['name'] = brw.single.goods.name
    dc['note'] = brw.manager_note
    return dc

def get_context_purchase(pur):
    dc = {}
    dc['id'] = pur.id
    dc['name'] = pur.account.real_name
    dc['note'] = pur.user_note
    dc['single'] = get_context_single(pur.single)
    dc['manufacturer'] = pur.manufacturer
    dc['version'] = pur.version
    dc['other'] = pur.other
    return dc
    
def import_goods(request, gl):
    if "" in gl[0:3]:
        raise Exception('value cannot be null')
    try:
        sn = str(int(float(gl[0])))
    except Exception as e:
        raise Exception('sn号必须为纯数字! ')
    name = gl[1]
    type_name = gl[2]
    
    tp = find_gtypes(type_name)
    if not tp or len(tp) > 1:
        raise Exception('No Such Goods Type')
    tp = tp[0]
    
    type_value = []
    for i in range(tp.get_pronum()):
        type_value.append(str(gl[3+i]))
        
    gd = packed_create_goods(request, name, tp, type_value)
    sns = [sn]
    packed_create_single(request, gd, sns, AVALIABLE_KEY, '')
    
    
def init_download_excel(request, num):
    f = xlwt.Workbook()
    table = f.add_sheet('Sheet1')
    
    def add_a_row(row, lst):
        for i in range(len(lst)):
            table.write(row, i, lst[i])
    
    if num == '1':
        add_a_row(0, ['状态','sn', '资源', '类型', '属性1', '属性2', '属性3', '……'])
    else:
        add_a_row(0, ['sn', '资源', '类型', '属性1', '属性2', '属性3', '……'])
    
    singles = Single.objects.exclude(status=DESTROYED_KEY)\
                .exclude(status=PURCHASE_AUTHING_KEY).exclude(status=PURCHASED_KEY)
    sgl_list = get_context_list(singles, get_context_single)
    
    status_dict = {"available":"在库", "unavailable":"不在库", "borrowed":"已借出",
                   "lost":"已挂失", "repairing":"维修中"}
    
    for i in range(len(sgl_list)):
        now_sgl = sgl_list[i]
        status = []
        if num == '1':
            status = [status_dict[now_sgl['status']]]
            
        sgl_data_list = [now_sgl['sn'], now_sgl['name'], now_sgl['type_name']]
        
        for pro in now_sgl['prop']:
            sgl_data_list.append(pro['pro_value'])
            
        add_a_row(i+1, status + sgl_data_list)
        
    
    f.save('data/temp_download.xls')

#===============================================
#===============================================
#===============================================
#===============================================
#===============================================
#===============================================
@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def add_goods(request):
    ''' Add new goods with new pro values '''
    try:
        name = request.POST['name']
        type_name = request.POST['type_name']
        
        tp = packed_find_gtypes(request, type_name)
        if not tp or len(tp) > 1:
            raise Exception('No Such Goods Type')
        tp = tp[0]

        type_value = []
        for i in range(1, tp.get_pronum()+1):
            prop_key = "pro" + str(i) + "_value"
            type_value.append(request.POST[prop_key])

        gd = packed_create_goods(request, name, tp, type_value)
        sns = request.POST['sn'].split(',')
        packed_create_single(request, gd, sns, AVALIABLE_KEY, '')

        return HttpResponseRedirect(reverse("goods.views.show_list"))
    except KeyError as e:
        return show_message(request, 'Key not found: '+e.__str__())
    except Exception as e:
        return show_message(request, "Add goods failed: "+e.__str__())

@method_required('POST')
def do_type_props(request):
    '''list all the properties' name of a type'''
    try:
        type_name = request.POST['type_name']
        gtype = packed_find_gtypes(request, type_name)
        pros = []
        if gtype:
            pros = gtype[0].get_all_pros()
        return HttpResponse(json.dumps({
            "pro_names":pros
        }))
    except Exception as e:
        #print(e)
        return show_message(request, "Find goods type failed: " + e.__str__())


@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def add_type(request):
    '''list all the properties' name of a type'''
    try:
        type_name = request.POST['type_name']

        gtype = packed_find_gtypes(request, type_name)
        if gtype:
            raise Exception('type name exist!')

        type_key = []
        for i in range(1, 33):
            prop_key = "pro" + str(i) + "_name"
            pv = no_excp_post(request, prop_key)
            if pv:
                type_key.append(pv)
        if not type_key:
            raise Exception('No Type contrib Added!')
        # Add new type to the database
        packed_create_gtype(request, type_name, type_key)
        # On success
        return HttpResponseRedirect(reverse('goods.views.show_add_goods'))
    except Exception as e:
        return show_message(request, 'Some thing Wrong While adding type: ' + e.__str__())

@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_accept_borrow(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        brw_list = Borrow.objects.filter(single = brw.single, status = BORROW_AUTHING_KEY)
        if len(brw_list) > 1:
            return show_message(request, '有多人同时借用该物品，请先拒绝多余的借用请求')


        if not brw.status == BORROW_AUTHING_KEY:
            return show_message(request, 'This Request is not under verifying!')
        if not brw.single.status == AVALIABLE_KEY:
            return show_message(request, 'The good is not avaliable!')

        packed_update_borrow(request, id, {'status':ACCEPTED_KEY, 'user_note':note}, log=get_accept_brw_log())
        send_notify_mail(request, AcceptBrwMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_manage'))
    except Exception as e:
        return show_message(request, 'Accept borrow failed: '+e.__str__())
    
def do_accept_purchase(request):
    try:
        id = request.POST['id']
        note = request.POST['note']
        
        pur = Purchase.objects.get(id = id)
        
        if not pur.status == PURCHASE_AUTHING_KEY:
            return show_message(request, 'This Request is not under verifying')
        packed_update_purchase(request, id,{'status':ACCEPTED_KEY, 'user_note':note})
        #我偷偷把邮件功能删了，你来打我啊
        
        return HttpResponseRedirect(reverse('goods.views.show_manage'))
    except Exception as e:
        return show_message(request, 'Accept purchase failed: '+e.__str__())

        

@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_reject_borrow(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        if not brw.status == BORROW_AUTHING_KEY:
            return show_message(request, 'This Request is not under verifying!')

        packed_update_borrow(request, id, {'status':REJECTED_KEY, 'user_note':note}, log=get_reject_brw_log(brw))
        send_notify_mail(request, RejectBrwMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_manage'))
    except Exception as e:
        return show_message(request, 'Reject borrow failed: '+e.__str__())

def do_reject_purchase(request):
    try:
        id = request.POST['id']
        note = request.POST['note']
        
        pur = Purchase.objects.get(id=id)
        
        if not pur.status == PURCHASE_AUTHING_KEY:
            return show_message(request, 'This Request is not under verifying!')
        
        packed_update_purchase(request, id, {'status':REJECTED_KEY, 'user_note':note})
        #我又删了邮件功能，打我啊  
        #打他，良辰必有重谢 23333333
        
        return show_message(request, '已拒绝付款!')
    except Exception as e:
        return show_message(request, 'Reject purchase failed: '+e.__str__())
        
@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_finish_borrow(request):
    try:
        id = request.POST['id']

        brw = Borrow.objects.get(id=id)

        if not brw.status == ACCEPTED_KEY:
            return show_message(request, 'This Request is not accepted!')
        if not brw.single.status == AVALIABLE_KEY:
            packed_update_borrow(request, id, {'status':BORROW_AUTHING_KEY}, log=get_wrong_goods_status_log())
            return show_message(request, 'The good is not avaliable!')

        packed_update_single(request, brw.single.id, {'status':BORROWED_KEY, 'user_name':brw.account.user.username}, log=get_good_brwed_log())
        packed_update_borrow(request, id, {'status':BORROWED_KEY}, log=get_finish_brw_log())

        return HttpResponseRedirect(reverse('goods.views.show_manage'))
    except Exception as e:
        return show_message(request, 'Finish borrow failed: '+e.__str__())

def do_finish_purchase(request):
    try:
        id = request.POST['id']
        desc = ''
        if request.POST['build_account'] == 'true':
            desc = '建账'
        else:
            desc = '不建账'
        
        pur = Purchase.objects.get(id = id)
        
        if not pur.status == ACCEPTED_KEY:
            return show_message(request, 'This Request is not accepted!')
        
        packed_update_purchase(request, id, {'status':PURCHASED_KEY, 'user_note':''})
        packed_update_single(request, pur.single.id, {'status':AVALIABLE_KEY, 'user_name':pur.account.user.username}, log='')
        packed_update_borrow(request, id, {'status':AVALIABLE_KEY}, log = '')
        create_log('purchase', user_id = request.user.id,
                   target=Single.objects.get(id=pur.single.id), action='采购物品',
                   description=desc)
        
        return HttpResponseRedirect(reverse('goods.views.show_manage'))
    except Exception as e:
        return show_message(request, 'Finish purchased failed: '+e.__str__())

@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_accept_return(request):
    try:
        id = request.POST['id']

        brw = Borrow.objects.get(id=id)
        note = request.POST['note']
        lost = request.POST['lost']

        if not brw.status == RETURN_AUTHING_KEY:
            return show_message(request, 'This Request is not in a return auth status!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')

        if(lost == 'false'):
            packed_update_borrow(request, id, {'status':RETURN_PENDING_KEY, 'manager_note':note}, log=get_accept_ret_log())
        else:
            packed_update_borrow(request, id, {'status':LOST_KEY, 'manager_note':note}, log=get_lost_ret_log())
            packed_update_single(request, brw.single.id, {'status':LOST_KEY}, log=get_good_lost_log())
        return HttpResponseRedirect(reverse('goods.views.show_manage'))
    except Exception as e:
        return show_message(request, 'Accept return failed: '+e.__str__())



@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_finish_return(request):
    try:
        id = request.POST['id']
        intect = request.POST['intact']

        brw = Borrow.objects.get(id=id)

        if not brw.status == RETURN_PENDING_KEY:
            return show_message(request, 'This Request is not accepted to return!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')
        if intect == 'true':
            packed_update_single(request, brw.single.id, {'status':AVALIABLE_KEY,'user_name':''}, log=get_good_reted_log())
            packed_update_borrow(request, id, {'status':RETURNED_KEY}, log=get_brw_reted_log())
        else:
            packed_update_single(request, brw.single.id, {'status':UNAVALIABLE_KEY}, log=get_good_dmg_log())
            packed_update_borrow(request, id, {'status':DAMAGED_KEY}, log=get_brw_dmg_log())

        return HttpResponseRedirect(reverse('goods.views.show_manage'))
    except Exception as e:
        return show_message(request, 'Finish return failed: '+e.__str__())

@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_accept_repair(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        if not brw.status == REPAIR_APPLY_KEY:
            return show_message(request, 'This Request is not in a repair apply status!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')

        packed_update_borrow(request, id, {'status':REPAIR_PEND_KEY, 'user_note':note}, log=get_accept_repair_log())
        send_notify_mail(request, AcceptRepairMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_manage'))

    except Exception as e:
        return show_message(request, 'Accept Repair failed: ' + e.__str__())

@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_reject_repair(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        if not brw.status == REPAIR_APPLY_KEY:
            return show_message(request, 'This Request is not in a repair apply status!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')

        packed_update_borrow(request, id, {'status':BORROWED_KEY, 'user_note':note}, log=get_reject_repair_log())
        send_notify_mail(request, RejectRepairMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_manage'))

    except Exception as e:
        return show_message(request, 'Reject Repair failed: ' + e.__str__())


@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_start_repair(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        if not brw.status == REPAIR_PEND_KEY:
            return show_message(request, 'This Request is not in a repair pend status!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')

        packed_update_borrow(request, id, {'status':REPAIRING_KEY, 'user_note':note}, log=get_brw_repairing_log())
        packed_update_single(request, brw.single.id, {'status':REPAIRING_KEY}, log=get_good_repairing_log())

        return HttpResponseRedirect(reverse('goods.views.show_manage'))

    except Exception as e:
        return show_message(request, 'Start Repair failed: ' + e.__str__())


@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_finish_repair(request):
    try:
        id = request.POST['id']        
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        if not brw.status == REPAIRING_KEY:
            return show_message(request, 'This Request is not in a repairing status!')
        if not brw.single.status == REPAIRING_KEY:
            return show_message(request, 'The good is not in a repairing status!')
  
        repair_record = ''
        if 'repair_record' in request.POST:    
            repair_record = request.POST['repair_record']
            if 'repair_record2' in request.POST:
                repair_record = '故障现象: ' + note + '  ' + '故障原因: ' + repair_record \
                               + '  ' +'解决办法: ' + request.POST['repair_record2']
  
        packed_update_borrow(request, id, {'status':FINISH_REPAIR_KEY, 'user_note':note}, 
                             log=get_finish_repair_log(), repair_record = repair_record)
        send_notify_mail(request, FinishRepairMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_manage'))

    except Exception as e:
        return show_message(request, 'Finish Repair failed: ' + e.__str__())


@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_return_repair(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        if not brw.status == FINISH_REPAIR_KEY:
            return show_message(request, 'This Request is not in a finish repair status!')
        if not brw.single.status == REPAIRING_KEY:
            return show_message(request, 'The good is not in a repairing status!')

        packed_update_borrow(request, id, {'status':BORROWED_KEY, 'manager_note':note}, log=get_ret_repaired_log())
        packed_update_single(request, brw.single.id, {'status':BORROWED_KEY}, log=get_good_repaired_log())

        return HttpResponseRedirect(reverse('goods.views.show_manage'))

    except Exception as e:
        return show_message(request, 'Return Repair failed: ' + e.__str__())
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
#-------------------------
@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_set_unavailable(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        sgl = Single.objects.get(id=id)
        if not sgl.status == AVALIABLE_KEY:
            return show_message(request, 'The goods cannot be set to unavailable!')
        packed_update_single(request, id, {'status':UNAVALIABLE_KEY,'note':note}, log=get_good_unvail_log())
        return HttpResponseRedirect(reverse("goods.views.show_list"))
    except Exception as e:
        return show_message(request, 'Set single good unavailable failed: ' + e.__str__())


@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_set_available(request):
    try:
        id = request.POST['id']

        sgl = Single.objects.get(id=id)
        if not sgl.status == UNAVALIABLE_KEY:
            return show_message(request, 'The goods cannot be set to available!')

        packed_update_single(request, id, {'status':AVALIABLE_KEY}, log=get_good_avail_log())

        return HttpResponseRedirect(reverse("goods.views.show_list"))
    except Exception as e:
        return show_message(request, 'Set single good available failed: ' + e.__str__())

@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_destroy(request):
    try:
        id = request.POST['id']
        desc = request.POST['note']

        packed_update_single(request, id, {'status':DESTROYED_KEY}, log=get_good_destroy_log())
        create_log('destroy', user_id = request.user.id,
                   target=Single.objects.get(id=id), action='销毁物品',
                   description=desc)

        return HttpResponseRedirect(reverse("goods.views.show_list"))
    except Exception as e:
        return show_message(request, 'Set single good destroyed failed: ' + e.__str__())

@method_required('POST')
@permission_required(PERM_NORMAL)
def do_borrow(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        sgl = Single.objects.get(id=id)
        if not sgl.status == AVALIABLE_KEY:
            return show_message(request, 'The good is not avaliable!')
        account = Account.objects.get(user=request.user)
        brw = packed_create_borrow(request, sn=sgl.sn, status=BORROW_AUTHING_KEY, manager_note=note, account=account, log=get_brw_requst_log())

        send_notify_mail(request, BrwRequstMail, borrow=brw)

        return HttpResponseRedirect(reverse("goods.views.show_borrow"))
    except Exception as e:
        return show_message(request, 'Borrow request failed: ' + e.__str__())

@method_required('POST')
@permission_required(PERM_NORMAL)
def do_purchase(request):
    try:
        name = request.POST['name']
        type_name = request.POST['type_name']
        manufacturer = request.POST['manufacturer']
        version = request.POST['version']
        other = request.POST['other_value']
        

        tp = packed_find_gtypes(request, type_name)
        if not tp or len(tp) > 1:
            raise Exception('No Such Goods Type')
        tp = tp[0]

        type_value = []
        for i in range(1, tp.get_pronum()+1):
            prop_key = "pro" + str(i) + "_value"
            type_value.append(request.POST[prop_key])

        gd = packed_create_goods(request, name, tp, type_value)
        sns = request.POST['sn'].split(',')
        sgl=packed_create_single(request, gd, sns, PURCHASE_AUTHING_KEY, '')
        account = Account.objects.get(user=request.user)
        packed_create_purchase(request,sns, PURCHASE_AUTHING_KEY, account, manufacturer, version, other)

        return HttpResponseRedirect(reverse("goods.views.show_list"))
    except KeyError as e:
        return show_message(request, 'Key not found: '+e.__str__())
    except Exception as e:
        return show_message(request, "Purchase failed: "+e.__str__())

@method_required('POST')
@permission_required(PERM_NORMAL)
def do_return_goods(request):
    try:
        id = request.POST['id']
        note = USER_RETURN_MESSAGE

        brw = Borrow.objects.get(id=id)

        if not brw.status == BORROWED_KEY:
            return show_message(request, 'This Request is not in a borrowed status!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')

        packed_update_borrow(request, id, {'status':RETURN_AUTHING_KEY, 'user_note':note, 'manager_note':note}, log=get_ret_request_log())
        send_notify_mail(request, RetRequstMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_borrow'))
    except Exception as e:
        return show_message(request, 'Return request failed: '+e.__str__())

@method_required('POST')
@permission_required(PERM_NORMAL)
def do_miss_goods(request):
    try:
        id = request.POST['id']
        note = USER_MISS_MESSAGE

        brw = Borrow.objects.get(id=id)

        if not brw.status == BORROWED_KEY:
            return show_message(request, 'This Request is not in a borrowed status!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')

        packed_update_borrow(request, id, {'status':RETURN_AUTHING_KEY, 'user_note':note, 'manager_note':note}, log=get_miss_request_log())
        send_notify_mail(request, MissRequstMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_borrow'))
    except Exception as e:
        return show_message(request, 'Miss request failed: '+e.__str__())

@method_required('POST')
@permission_required(PERM_NORMAL)
def do_repair_goods(request):
    try:
        id = request.POST['id']
        note = request.POST['note']

        brw = Borrow.objects.get(id=id)

        if not brw.status == BORROWED_KEY:
            return show_message(request, 'This Request is not in a borrowed status!')
        if not brw.single.status == BORROWED_KEY:
            return show_message(request, 'The good is not in a borrowed status!')

        packed_update_borrow(request, id, {'status':REPAIR_APPLY_KEY, 'manager_note':note, 'user_note':note}, 
                             log=get_repair_apply_log(), repair_record = '故障现象: ' + note)
        send_notify_mail(request, RepairRequstMail, borrow=brw)

        return HttpResponseRedirect(reverse('goods.views.show_borrow'))

    except Exception as e:
        return show_message(request, 'Repair apply failed: ' + e.__str__())



#===============================================
#===============================================
#===============================================
#===============================================
#===============================================
#===============================================

@method_required('GET')
@permission_required(PERM_GOODS_AUTH)
def show_add_goods(request):
    type_list = []
    for t in GType.objects.all():
        type_list.append(t.name)
    return render(request, "add_goods.html", {
        'user': get_context_user(request.user),
        "type_list": type_list,
    })

@method_required('GET')
def show_request_purchase(request):

    
    type_list = []
    for t in GType.objects.all():
        type_list.append(t.name)
    return render(request, "request_purchase.html", {
        'user': get_context_user(request.user),
        "type_list": type_list,
    })

@method_required('GET')
def show_request_exist_purchase(request):
    sgl = Single.objects.get(id=request.GET['id'])
    pro_list = get_context_single(sgl)['prop']
    
    type_list = []
    for t in GType.objects.all():
        type_list.append(t.name)    
        
    return render(request, "request_exist_purchase.html", {
        'user': get_context_user(request.user),
        'type_list': type_list,
        'type':sgl.goods.gtype.name,
        'pro_list': pro_list,
        })
                                                    

@method_required('GET')
@permission_required(PERM_NORMAL)
def show_list(request):

    status = no_excp_get(request, "status")
    name = no_excp_get(request, "name")
    type_name = no_excp_get(request, "type")

    tp_list = []
    for tp in GType.objects.all():
        tp_list.append(tp.name)
    
    singles = None
    if not status or status == 'all':
        singles = Single.objects.exclude(status=DESTROYED_KEY)
    else:
        singles = Single.objects.filter(status=sgl_sta_map[status])

    if type_name:
        singles = singles.filter(goods__gtype__name__startswith=type_name)
    if name:
        singles = singles.filter(goods__name__startswith=name)

    sgl_list = get_context_list(singles, get_context_single)
    return render(request, "goods_list.html", {
        'user': get_context_user(request.user),
        "goods_list": sgl_list,
        "type_list": tp_list 
        })




@login_required
def show_borrow(request):

    cont = {}
    cont['curpage'] = 'borrow'

    account = Account.objects.get(user = request.user)

    inuse = packed_find_computing(request, {'account':account, 'status':computing.models.BORROWED_KEY},{})
    borrow = packed_find_computing(request, {'account':account, 'status':computing.models.VERIFYING_KEY},{})
    ret = packed_find_computing(request, {'account':account, 'status':computing.models.RETURNING_KEY},{})
    modif = packed_find_computing(request, {'account':account, 'status':computing.models.MODIFY_APPLY_KEY},{})

    packs = Package.objects.all()
    pack_list = get_context_list(packs, get_pack_name)
    cont['package_list'] = pack_list

    cont['num_res_used'] = len(inuse)
    cont['num_res_borrow'] = len(borrow)
    cont['num_res_release'] = len(ret)
    cont['num_res_modif'] = len(modif)

    cont['borrowing_list'] = get_context_list(borrow, get_context_computing)
    cont['inuse_list'] = get_context_list(inuse, get_context_computing)
    cont['modifying_list'] = get_context_list(modif, get_context_computing)
    cont['returning_list'] = get_context_list(ret, get_context_computing)

    brws = packed_find_borrow(request, {'account':account},{})
    brwing = brws.filter(status=BORROW_AUTHING_KEY)
    brw_pend = brws.filter(status=ACCEPTED_KEY)
    brw_fail = brws.filter(status=REJECTED_KEY)
    brw_inuse = brws.filter(status=BORROWED_KEY)
    reting = brws.filter(status=RETURN_AUTHING_KEY)
    ret_pend = brws.filter(status=RETURN_PENDING_KEY)

    rp_apply = brws.filter(status=REPAIR_APPLY_KEY)
    rp_pend = brws.filter(status=REPAIR_PEND_KEY)
    rping = brws.filter(status=REPAIRING_KEY)
    rped = brws.filter(status=FINISH_REPAIR_KEY)

    cont['num_goods_used'] = len(brw_inuse)
    cont['num_goods_borrow'] = len(brwing) + len(brw_pend)
    cont['num_goods_return'] = len(reting) + len(ret_pend)

    cont['goods_borrowing_list'] = get_context_list(brwing, get_context_userbrw)
    cont['goods_borrow_pending_list'] = get_context_list(brw_pend, get_context_userbrw)
    cont['goods_borrow_failed_list'] = get_context_list(brw_fail, get_context_userbrw)
    cont['goods_inuse_list'] = get_context_list(brw_inuse, get_context_userbrw)
    cont['goods_returning_list'] = get_context_list(reting, get_context_userbrw)
    cont['goods_return_pending_list'] = get_context_list(ret_pend, get_context_userbrw)

    cont['goods_torepair_list'] = get_context_list(rp_apply, get_context_userbrw)
    cont['goods_repair_list'] = get_context_list(rp_pend, get_context_userbrw)
    cont['goods_repairing_list'] = get_context_list(rping, get_context_userbrw)
    cont['goods_repaired_list'] = get_context_list(rped, get_context_userbrw)

    cont['user'] = get_context_user(request.user)
    return render(request, 'borrow.html', cont)

@method_required('GET')
@permission_required(PERM_GOODS_AUTH)
def show_add_type(request):
    return render(request, "add_type.html",{
        'user': get_context_user(request.user),
        })

@method_required('GET')
@permission_required(PERM_GOODS_AUTH)
def show_manage(request):
    
    b_req = packed_find_borrow(request, {'status':BORROW_AUTHING_KEY},{})
    b_pend = packed_find_borrow(request, {'status':ACCEPTED_KEY},{})
    r_req = packed_find_borrow(request, {'status':RETURN_AUTHING_KEY},{})
    r_pend = packed_find_borrow(request, {'status':RETURN_PENDING_KEY},{})

    pr_req = Purchase.objects.filter(status=PURCHASE_AUTHING_KEY)
    pr_pend = Purchase.objects.filter(status=ACCEPTED_KEY)


    rp_apply = packed_find_borrow(request, {'status':REPAIR_APPLY_KEY},{})
    rp_pend = packed_find_borrow(request, {'status':REPAIR_PEND_KEY},{})
    rping = packed_find_borrow(request, {'status':REPAIRING_KEY},{})
    rped = packed_find_borrow(request, {'status':FINISH_REPAIR_KEY},{})

    b_req_list = get_context_list(b_req, get_context_borrow)
    b_pend_list = get_context_list(b_pend, get_context_borrow)
    r_req_list = get_context_list(r_req, get_context_borrow)
    r_pend_list = get_context_list(r_pend, get_context_borrow)
    
    pr_req_list = get_context_list(pr_req, get_context_purchase)
    pr_pend_list = get_context_list(pr_pend, get_context_purchase)


    rp_apply_list = get_context_list(rp_apply, get_context_borrow)
    rp_pend_list = get_context_list(rp_pend, get_context_borrow)
    rping_list = get_context_list(rping, get_context_borrow)
    rped_list = get_context_list(rped, get_context_borrow)
    return render(request, 'goods_manage.html', {
        'user': get_context_user(request.user),
        'borrow_requests': b_req_list,
        'return_requests': r_req_list,
        'borrow_pending_requests': b_pend_list,
        'return_pending_requests': r_pend_list,
        'torepair_requests': rp_apply_list,
        'repair_requests': rp_pend_list,
        'repairing_requests': rping_list,
        'repaired_requests': rped_list,
        'purchase_requests': pr_req_list,
        'purchase_pending_requests': pr_pend_list
    })

@method_required('GET')
@permission_required(PERM_VIEW_ALL)
def show_borrow_list(request):
    try:
        brw = Borrow.objects.all()
        blist = get_context_list(brw, get_context_userbrw)
        return render(request, 'log_borrow.html', {
            'user':get_context_user(request.user),
            'borrows': blist,
            'page':1,
            'page_num':1
            })
    except Exception as e:
        return show_message(request, 'Error when show borrows: ' + e.__str__())



@method_required('POST')
@permission_required(PERM_GOODS_AUTH)
def do_upload_excel(request):
    try:
        upload_excel = request.FILES['excel']
    
        if upload_excel.name.split('.')[-1] != 'xlsx':
            return show_message(request, '不是xlsx文件!')
    
        with open('data/temp_upload_excel.xlsx', 'wb') as f:
            f.write(upload_excel.read())
    
        excel = xlrd.open_workbook('data/temp_upload_excel.xlsx')
        table = excel.sheets()[0]
        
        if table.row_values(0)[0:3] != ['sn', '资源', '类型']:
            return show_message(request, '上传excel格式错误! ')
    
        for i in range(1, table.nrows):
            import_goods(request, table.row_values(i))
    
        return HttpResponseRedirect(reverse('goods.views.show_list'))

    except Exception as e:
        return show_message(request, 'Error : ' + e.__str__())
    
    

@method_required('GET')
@permission_required(PERM_GOODS_AUTH)
def download_excel(request, num):
    try:
        init_download_excel(request, num)
    
        excel = b''
        with open('data/temp_download.xls', 'rb') as f:
            excel = f.read()
        
        response = HttpResponse(excel)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="download_' + num + '.xls"'
        
        return response 
    
    except Exception as e:
        return show_message(request, 'Error : ' + e.__str__())



@method_required('GET')
def download_excel_template(request):
    excel = b''
    with open('data/template.xlsx', 'rb') as f:
        excel = f.read()
        
    response = HttpResponse(excel)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="template.xlsx"'
    
    return response


        

