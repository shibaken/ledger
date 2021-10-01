from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ledger.accounts import models
from django.contrib.auth.models import Group
from ledgergw import models as ledgergw_models
from ledger.api import models as ledgerapi_models
from ledger.api import utils as ledgerapi_utils
#from ledgergw import common
from django.db.models import Q
from ledger.checkout import utils
from oscar.apps.order.models import Order
from ledger.payments.invoice.models import Invoice

from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
import base64

import json
import ipaddress


@csrf_exempt
def user_info_search(request, apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            keyword = request.POST.get('keyword', '')
            jsondata = {'status': 200, 'message': 'No Results'}
            jsondata['users'] = [] 
            ledger_user_json = {}
            search_filter = Q()
            query_str_split = keyword.split(" ")
            search_filter |= Q(email__icontains=keyword.lower())
        
            #search_filter |= Q(first_name__icontains=query_str_split[0].lower())
            if len(query_str_split) == 1:
                  search_filter |= Q(first_name__icontains=query_str_split[0].lower())
            if len(query_str_split) > 1:
                  search_filter |= Q(Q(first_name__icontains=query_str_split[0].lower()) & Q(last_name__icontains=query_str_split[1].lower()))
            #for se_wo in query_str_split:
            #     
            #     search_filter |= Q(first_name__icontains=se_wo.lower()) | Q(last_name__icontains=se_wo.lower())

            ledger_users = models.EmailUser.objects.filter(search_filter)[:20]
            #,last_name__icontains=keyword)
            for ledger_obj in ledger_users:

                    ledger_user_json = {}
                    #if keyword.lower() in ledger_obj.first_name.lower()+' '+ledger_obj.last_name.lower() or keyword.lower() in ledger_obj.email.lower():
                    ledger_user_json['ledgerid'] = ledger_obj.id
                    ledger_user_json['email'] = ledger_obj.email
                    ledger_user_json['first_name'] = ledger_obj.first_name
                    ledger_user_json['last_name'] = ledger_obj.last_name
                    ledger_user_json['is_staff'] = ledger_obj.is_staff
                    ledger_user_json['is_superuser'] = ledger_obj.is_superuser
                    ledger_user_json['is_active'] = ledger_obj.is_active
                    ledger_user_json['date_joined'] = ledger_obj.date_joined.strftime('%d/%m/%Y %H:%M')
                    ledger_user_json['title'] = ledger_obj.title
                    if ledger_obj.dob:
                        ledger_user_json['dob'] = ledger_obj.dob.strftime('%d/%m/%Y %H:%M')
                    else:
                        ledger_user_json['dob'] = None
                    ledger_user_json['phone_number'] = ledger_obj.phone_number
                    ledger_user_json['position_title'] = ledger_obj.position_title
                    ledger_user_json['mobile_number'] = ledger_obj.mobile_number
                    ledger_user_json['fax_number'] = ledger_obj.fax_number
                    ledger_user_json['organisation'] = ledger_obj.organisation
                    #ledger_user_json['identification'] = ledger_obj.identification
                    #ledger_user_json['senior_card'] = ledger_obj.senior_card
                    ledger_user_json['character_flagged'] = ledger_obj.character_flagged
                    ledger_user_json['character_comments'] = ledger_obj.character_comments
                    ledger_user_json['extra_data'] = ledger_obj.extra_data
                    ledger_user_json['fullname'] = ledger_obj.get_full_name()
                    if ledger_obj.dob:
                        ledger_user_json['fullnamedob'] = ledger_obj.get_full_name_dob()
                    else:
                        ledger_user_json['fullnamedob'] = None
                    # Groups
                    #ledger_user_group = []
                    #for g in ledger_obj.groups.all():
                    #    ledger_user_group.append({'group_id': g.id, 'group_name': g.name})
                    #ledger_user_json['groups'] = ledger_user_group

                    jsondata['users'].append(ledger_user_json)
                    jsondata['status'] = 200
                    jsondata['message'] = 'Results'

        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    return HttpResponse(json.dumps(jsondata), content_type='application/json')


@csrf_exempt
def user_info_id(request, userid,apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:

            ledger_user = models.EmailUser.objects.filter(id=int(userid))
            if ledger_user.count() > 0:
                    ledger_obj = ledger_user[0]
                    ledger_user_json['ledgerid'] = ledger_obj.id
                    ledger_user_json['email'] = ledger_obj.email
                    ledger_user_json['first_name'] = ledger_obj.first_name
                    ledger_user_json['last_name'] = ledger_obj.last_name
                    ledger_user_json['is_staff'] = ledger_obj.is_staff
                    ledger_user_json['is_superuser'] = ledger_obj.is_superuser
                    ledger_user_json['is_active'] = ledger_obj.is_active
                    ledger_user_json['date_joined'] = ledger_obj.date_joined.strftime('%d/%m/%Y %H:%M')
                    ledger_user_json['title'] = ledger_obj.title
                    if ledger_obj.dob:
                        ledger_user_json['dob'] = ledger_obj.dob.strftime('%d/%m/%Y %H:%M')
                    else:
                        ledger_user_json['dob'] = None
                    ledger_user_json['phone_number'] = ledger_obj.phone_number
                    ledger_user_json['position_title'] = ledger_obj.position_title
                    ledger_user_json['mobile_number'] = ledger_obj.mobile_number
                    ledger_user_json['fax_number'] = ledger_obj.fax_number
                    ledger_user_json['organisation'] = ledger_obj.organisation
                    #ledger_user_json['identification'] = ledger_obj.identification
                    #ledger_user_json['senior_card'] = ledger_obj.senior_card
                    ledger_user_json['character_flagged'] = ledger_obj.character_flagged
                    ledger_user_json['character_comments'] = ledger_obj.character_comments
                    ledger_user_json['extra_data'] = ledger_obj.extra_data
                    ledger_user_json['fullname'] = ledger_obj.get_full_name()
                    if ledger_obj.dob:
                        ledger_user_json['fullnamedob'] = ledger_obj.get_full_name_dob()
                    else:
                        ledger_user_json['fullnamedob'] = None
                    # Groups
                    ledger_user_group = []
                    for g in ledger_obj.groups.all():
                        ledger_user_group.append({'group_id': g.id, 'group_name': g.name})
                    ledger_user_json['groups'] = ledger_user_group
                    jsondata['user'] = ledger_user_json
                    jsondata['status'] = 200
                    jsondata['message'] = 'User Found'
            else:
                jsondata['status'] = '404'
                jsondata['message'] = 'User not found'
        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    return HttpResponse(json.dumps(jsondata), content_type='application/json')

@csrf_exempt
def user_info(request, ledgeremail,apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            ledgeremail=ledgeremail.lower()
            ledgeremail=ledgeremail.replace(" ","")
            ledger_user = models.EmailUser.objects.filter(email=ledgeremail)
            if ledger_user.count() == 0:
                 first_name = request.POST.get('first_name','')
                 last_name =  request.POST.get('last_name','')
                 a = models.EmailUser.objects.create(email=ledgeremail,first_name=first_name,last_name=last_name)
                 #a.save()
                 #ledger_user = models.EmailUser.objects.filter(email=ledgeremail)
                 #ledger_user.save()


            if ledger_user.count() > 0:
                    ledger_obj = ledger_user[0]
                    ledger_user_json['ledgerid'] = ledger_obj.id
                    ledger_user_json['email'] = ledger_obj.email
                    ledger_user_json['first_name'] = ledger_obj.first_name
                    ledger_user_json['last_name'] = ledger_obj.last_name
                    ledger_user_json['is_staff'] = ledger_obj.is_staff
                    ledger_user_json['is_superuser'] = ledger_obj.is_superuser
                    ledger_user_json['is_active'] = ledger_obj.is_active
                    ledger_user_json['date_joined'] = ledger_obj.date_joined.strftime('%d/%m/%Y %H:%M')
                    ledger_user_json['title'] = ledger_obj.title
                    if ledger_obj.dob:
                        ledger_user_json['dob'] = ledger_obj.dob.strftime('%d/%m/%Y %H:%M')
                    else:
                        ledger_user_json['dob'] = None
                    ledger_user_json['phone_number'] = ledger_obj.phone_number
                    ledger_user_json['position_title'] = ledger_obj.position_title
                    ledger_user_json['mobile_number'] = ledger_obj.mobile_number
                    ledger_user_json['fax_number'] = ledger_obj.fax_number
                    ledger_user_json['organisation'] = ledger_obj.organisation
                    #ledger_user_json['residential_address'] = ledger_obj.residential_address
                    #ledger_user_json['postal_address'] = ledger_obj.postal_address
                    #ledger_user_json['billing_address'] = ledger_obj.billing_address
                    #ledger_user_json['identification'] = ledger_obj.identification
                    #ledger_user_json['senior_card'] = ledger_obj.senior_card
                    ledger_user_json['character_flagged'] = ledger_obj.character_flagged
                    ledger_user_json['character_comments'] = ledger_obj.character_comments
                    ledger_user_json['extra_data'] = ledger_obj.extra_data
                    ledger_user_json['fullname'] = ledger_obj.get_full_name()
                    if ledger_obj.dob:
                        ledger_user_json['fullnamedob'] = ledger_obj.get_full_name_dob()
                    else:
                        ledger_user_json['fullnamedob'] = None
                    # Groups
                    ledger_user_group = []
                    for g in ledger_obj.groups.all():
                        ledger_user_group.append({'group_id': g.id, 'group_name': g.name})
                    ledger_user_json['groups'] = ledger_user_group
                    jsondata['user'] = ledger_user_json
                    jsondata['status'] = 200
                    jsondata['message'] = 'User Found'
            else:
                jsondata['status'] = '404'
                jsondata['message'] = 'User not found'
        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    return HttpResponse(json.dumps(jsondata), content_type='application/json')



@csrf_exempt
def user_group_info(request, ledger_id,apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    query_exists = False
    ledger_user_json  = {}
    filter_post = json.loads(request.POST['filter'])
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            ledger_user = models.EmailUser.objects.filter(id=ledger_id)
            if ledger_user.count() > 0:
                    ledger_obj = ledger_user[0]
                    ledger_user_group = []
                    if len(filter_post) > 0: 
                        if 'name' in filter_post:
                            query = ledger_obj.groups.filter(name=filter_post['name'])
                            for g in query:
                                  ledger_user_group.append({'group_id': g.id, 'group_name': g.name})
                        if 'id' in filter_post:
                            query = ledger_obj.groups.filter(id=int(filter_post['id']))
                            for g in query:
                                ledger_user_group.append({'group_id': g.id, 'group_name': g.name})
                        if 'name' in filter_post and 'id' in filter_post:
                            query = ledger_obj.groups.filter(name=filter_post['name'], id=int(filter_post['id']))
                            for g in query:
                                ledger_user_group.append({'group_id': g.id, 'group_name': g.name})
                        query_exists = query.exists()

                    else:
                        for g in ledger_obj.groups.all():
                             ledger_user_group.append({'group_id': g.id, 'group_name': g.name})
                    ledger_user_json['groups'] = ledger_user_group
                    jsondata['groups'] = ledger_user_json
                    jsondata['query_exists'] = query_exists
                    jsondata['status'] = 200
                    jsondata['message'] = 'User Found'
            else:
                jsondata['status'] = '404'
                jsondata['message'] = 'User not found'
        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    return HttpResponse(json.dumps(jsondata), content_type='application/json')


def group_info(request, apikey):
    ledger_json  = {}
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            groups = Group.objects.all()
            ledger_json['groups_list'] = []
            ledger_json['groups_id_map'] = {}
            ledger_json['groups_name_map'] = {}
            for g in groups:
                ledger_json['groups_list'].append({'group_id': g.id,'group_name': g.name})
                ledger_json['groups_id_map'][g.id] = g.name
                ledger_json['groups_name_map'][g.name] = g.id

            jsondata['groups_list'] = ledger_json['groups_list']
            jsondata['groups_id_map'] = ledger_json['groups_id_map']
            jsondata['groups_name_map'] = ledger_json['groups_name_map']

            jsondata['status'] = 200
            jsondata['message'] = 'Groups Retreived'

        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'

    return HttpResponse(json.dumps(jsondata), content_type='application/json')


@csrf_exempt
def add_update_file_emailuser(request, apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            emailuser_id = request.POST.get('emailuser_id', '')
            file_group_id = request.POST.get('file_group_id', None)
            filebase64 = request.POST['filebase64']
            extension = request.POST.get('extension',None)

            randomfile_name = get_random_string(length=15, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            b64data = filebase64.split(",") 
            cfile = ContentFile(base64.b64decode(b64data[1]), name=randomfile_name+'.'+extension)
            private_document = models.PrivateDocument.objects.create(upload=cfile,name=randomfile_name,file_group=file_group_id,file_group_ref_id=emailuser_id,extension=extension)
            email_user = models.EmailUser.objects.get(id=emailuser_id)
            if int(file_group_id) == 1:
               email_user.identification2=private_document
               email_user.save()
            if int(file_group_id) == 2:
               email_user.senior_card2=private_document
               email_user.save()
            
            jsondata = {'status': 200, 'message': 'Results',}
        else:
           jsondata['status'] = 403
           jsondata['message'] = 'Access Forbidden'

    return HttpResponse(json.dumps(jsondata), content_type='application/json')

@csrf_exempt
def get_private_document(request, apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            private_document_id = request.POST.get('private_document_id', None)
            private_document = models.PrivateDocument.objects.get(id=private_document_id)

            #print (private_document.upload.path)
            with open(private_document.upload.path, "rb") as doc:
                 encoded_doc = base64.b64encode(doc.read())
            #print (encoded_doc)
            jsondata = {'status': 200, 'message': 'Results','data': encoded_doc.decode(), 'filename': private_document.name, 'extension': private_document.extension}
        else:
           jsondata['status'] = 403
           jsondata['message'] = 'Access Forbidden'

    return HttpResponse(json.dumps(jsondata), content_type='application/json')



@csrf_exempt
def create_basket_session(request,apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            print ("API create_basket_session")
            print (request.POST.get('parameters', "{}"))
            parameters = json.loads(request.POST.get('parameters', "{}"))
            emailuser_id = request.POST.get('emailuser_id', None)
            print (parameters)
            #parameters['system'] = '0019'
            print (emailuser_id)
            if parameters['custom_basket'] is True:
                print ("CUSTOM BASKER TEYE")
            basket, basket_hash = utils.create_basket_session_v2(emailuser_id,parameters)
            print ("RESP")
            print (basket.id)
            print (basket,basket_hash)
            jsondata['status'] = 200
            jsondata['message'] = 'Success'
            jsondata['data'] = {'basket_hash': basket_hash}
            print (jsondata)
            #ledger_user = models.EmailUser.objects.filter(email=ledgeremail)
            #if ledger_user.count() == 0:

            #     a = models.EmailUser.objects.create(email=ledgeremail,first_name=request.POST['first_name'],last_name=request.POST['last_name'])
            #     ledger_user = models.EmailUser.objects.filter(email=ledgeremail)
            #     ledger_user.save()
            #else:
            #    jsondata['status'] = '404'
            #    jsondata['message'] = 'User not found'
        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    return HttpResponse(json.dumps(jsondata), content_type='application/json')


@csrf_exempt
def create_checkout_session(request,apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            print ("API create_basket_session")
            checkout_parameters = json.loads(request.POST.get('checkout_parameters', "{}"))
            #emailuser_id = request.POST.get('emailuser_id', None)
            print ("SESSION")
            if 'checkout_data' in request.session:
                print (request.session['checkout_data'])
            print ("END SESSION")
            print (checkout_parameters)
            #parameters['system'] = '0019'
            #print (emailuser_id)
            resp = utils.create_checkout_session(request,checkout_parameters)
            print ("COOKIES")
            #basket, basket_hash = utils.create_checkout_session(request, parameters)
            print ("SESSION 2")
            if 'checkout_data' in request.session:
               print (request.session['checkout_data'])
            print ("RESP!")
            print (resp)
            jsondata['status'] = 200
            jsondata['message'] = 'Success'
            jsondata['data'] = {}
            #jsondata['data'] = {'basket_hash': basket_hash}

            #ledger_user = models.EmailUser.objects.filter(email=ledgeremail)
            #if ledger_user.count() == 0:

            #     a = models.EmailUser.objects.create(email=ledgeremail,first_name=request.POST['first_name'],last_name=request.POST['last_name'])
            #     ledger_user = models.EmailUser.objects.filter(email=ledgeremail)
            #     ledger_user.save()
            #else:
            #    jsondata['status'] = '404'
            #    jsondata['message'] = 'User not found'
        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    response = HttpResponse(json.dumps(jsondata), content_type='application/json')
    response.set_cookie('CookieTest', 'Testing',5)
    return response


@csrf_exempt
def get_order_info(request,apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    ledger_user_json  = {}
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            print ("API get_order_info")
            data = json.loads(request.POST.get('data', "{}"))
            order = Order.objects.get(basket__id=data['basket_id'])
            order_obj = {}
            order_obj['id'] = order.id
            order_obj['number'] = order.number

            jsondata['status'] = 200
            jsondata['message'] = 'Success'
            jsondata['data'] = {'order': order_obj}
        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    response = HttpResponse(json.dumps(jsondata), content_type='application/json')
    response.set_cookie('CookieTest', 'Testing',5)
    return response

@csrf_exempt
def get_invoice_properties(request,apikey):
    jsondata = {'status': 404, 'message': 'API Key Not Found'}
    invoice_json = {}
    print ("API get_invoice_properties 1") 
    if ledgerapi_models.API.objects.filter(api_key=apikey,active=1).count():
        if ledgerapi_utils.api_allow(ledgerapi_utils.get_client_ip(request),apikey) is True:
            print ("API get_invoice_properties 2")
            data = json.loads(request.POST.get('data', "{}"))
            print (data)
            
            if Invoice.objects.filter(id=data['invoice_id']).count() > 0:
                 try:
                       invoice = Invoice.objects.get(id=data['invoice_id'])
                       invoice_obj = {}
                       invoice_obj['id'] = invoice.id
                       invoice_obj['text'] = invoice.text
                       invoice_obj['amount'] = str(invoice.amount)
                       invoice_obj['order_number'] = invoice.order_number
                       invoice_obj['reference'] = invoice.reference
                       invoice_obj['system'] = invoice.system
                       invoice_obj['token'] = invoice.token
                       invoice_obj['voided'] = invoice.voided
                       invoice_obj['previous_invoice'] = invoice.previous_invoice
                       invoice_obj['settlement_date'] = invoice.settlement_date
                       invoice_obj['payment_method'] = invoice.payment_method
                       invoice_obj['biller_code'] = invoice.biller_code
                       invoice_obj['number'] = invoice.number
                       if invoice.owner:
                           invoice_obj['owner'] = invoice.owner.id
                       else:
                           invoice_obj['owner'] = None
                       invoice_obj['refundable_amount'] = str(invoice.refundable_amount)
                       invoice_obj['refundable'] = invoice.refundable
                       invoice_obj['num_items'] = invoice.num_items
                       #invoice_obj['linked_bpay_transactions'] = invoice.linked_bpay_transactions

                       invoice_obj['payment_amount'] = str(invoice.payment_amount)
                       invoice_obj['total_payment_amount'] = str(invoice.total_payment_amount)
                       invoice_obj['refund_amount'] = str(invoice.refund_amount)
                       invoice_obj['deduction_amount'] = str(invoice.deduction_amount)
                       invoice_obj['transferable_amount'] = str(invoice.transferable_amount)
                       invoice_obj['balance'] = str(invoice.balance)
                       invoice_obj['payment_status'] = invoice.payment_status

                       jsondata['status'] = 200
                       jsondata['message'] = 'Success'
                       jsondata['data'] = {'invoice': invoice_obj}
                       print ("YES")
                 except:
                     print ("ERROR")
            else:
                 jsondata['status'] = 404
                 jsondata['message'] = 'not found'
                 jsondata['data'] = {'invoice': None}
        else:
            jsondata['status'] = 403
            jsondata['message'] = 'Access Forbidden'
    else:
        pass
    response = HttpResponse(json.dumps(jsondata), content_type='application/json')
    return response

def ip_check(request):
    ledger_json  = {}
    ipaddress = ledgerapi_utils.get_client_ip(request)
    jsondata = {'status': 200, 'ipaddress': str(ipaddress)}
    return HttpResponse(json.dumps(jsondata), content_type='application/json')
