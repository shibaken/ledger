from __future__ import unicode_literals
import decimal
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from oscar.apps.order.models import Order
from ledger.payments.bpay.crn import getCRN
from ledger.payments.bpay.models import BpayTransaction
from ledger.payments.bpoint.models import BpointTransaction, TempBankCard

class Invoice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2,max_digits=12)
    order_number = models.CharField(max_length=50,unique=True)
    reference = models.CharField(max_length=50, unique=True)
    system = models.CharField(max_length=4,blank=True,null=True)
    token = models.CharField(max_length=16,null=True,blank=True)

    def __unicode__(self):
        return 'Order #{0} Invoice #{1}'.format(self.reference,self.id)

    # Properties
    # =============================================
    @property
    def biller_code(self):
        ''' Return the biller code for bpay.
        '''
        return settings.BPAY_BILLER_CODE

    @property
    def order(self):
        ''' Get order matched to this invoice.
        '''
        return Order.objects.get(number=self.order_number)

    @property
    def owner(self):
        return self.order.user

    @property
    def num_items(self):
        ''' Get the number of items in this invoice.
        '''
        return self.order.num_items

    @property
    def bpay_transactions(self):
        ''' Get this invoice's bpay transactions.
        '''
        return BpayTransaction.objects.filter(crn=self.reference)

    @property
    def bpoint_transactions(self):
        ''' Get this invoice's bpoint transactions.
        '''
        return BpointTransaction.objects.filter(crn1=self.reference)

    @property
    def payment_amount(self):
        ''' Total amount paid from bpay,bpoint and cash.
        '''
        return self.__calculate_bpay_payments() + self.__calculate_bpoint_payments() + self.__calculate_cash_payments()

    @property
    def balance(self):
        return self.amount - self.payment_amount

    @property
    def payment_status(self):
        ''' Payment status of the invoice.
        '''
        amount_paid = self.__calculate_bpay_payments() + self.__calculate_bpoint_payments() + self.__calculate_cash_payments()

        if amount_paid == decimal.Decimal('0'):
            return 'unpaid'
        elif amount_paid < self.amount:
            return 'partially_paid'
        elif amount_paid == self.amount:
            return 'paid'
        else:
            return 'over_paid'

    # Helper Functions
    # =============================================
    def __calculate_cash_payments(self):
        ''' Calcluate the amount of cash payments made
            less the reversals for this invoice.
        '''
        payments = dict(self.cash_transactions.filter(type='payment').aggregate(amount__sum=Coalesce(Sum('amount'), decimal.Decimal('0')))).get('amount__sum')
        reversals = dict(self.cash_transactions.filter(type='reversal').aggregate(amount__sum=Coalesce(Sum('amount'), decimal.Decimal('0')))).get('amount__sum')

        return payments - reversals

    def __calculate_bpoint_payments(self):
        ''' Calcluate the total amount of bpoint payments and
            captures made less the reversals for this invoice.
        '''
        payments = reversals = 0 
        payments = payments + dict(self.bpoint_transactions.filter(action='payment', response_code='0').aggregate(amount__sum=Coalesce(Sum('amount'), decimal.Decimal('0')))).get('amount__sum')
        payments = payments + dict(self.bpoint_transactions.filter(action='capture', response_code='0').aggregate(amount__sum=Coalesce(Sum('amount'), decimal.Decimal('0')))).get('amount__sum')
        reversals = dict(self.bpoint_transactions.filter(action='reversal', response_code='0').aggregate(amount__sum=Coalesce(Sum('amount'), decimal.Decimal('0')))).get('amount__sum')

        return payments - reversals

    def __calculate_bpay_payments(self):
        ''' Calcluate the amount of bpay payments made
            less the reversals for this invoice.
        '''
        payments = reversals = 0
        if self.bpay_transactions:
            payments = payments + dict(self.bpay_transactions.filter(p_instruction_code='05', type=399).aggregate(amount__sum=Coalesce(Sum('amount'), decimal.Decimal('0')))).get('amount__sum')
            reversals = dict(self.bpay_transactions.filter(p_instruction_code='25', type=699).aggregate(amount__sum=Coalesce(Sum('amount'), decimal.Decimal('0')))).get('amount__sum')

        return payments - reversals    

    # Functions
    # =============================================
    def pay_using_token(self):
        ''' Pay this invoice with the token attached to it.
        :return: BpointTransaction
        '''
        from ledger.payments.facade import bpoint_facade
        try:
            if self.token:
                card_details = self.token.split('|')
                card = TempBankCard(
                    card_details[0],
                    card_details[1]
                )
                return bpoint_facade.pay_with_temptoken(
                        'payment',
                        'telephoneorder',
                        'single',
                        card,
                        self.order_number,
                        self.reference,
                        self.amount,
                        None
                    )
        except:
            raise