"""Usage:

    python elance2freshbooks.py csv-from-elance.csv url key client_id

"""

from refreshbooks import api
import csv, sys, os, re
from dateutil.parser import parse as parse_date

FIELD_DATE_PAID = 'Date of Payment/Deposit'
FIELD_DATE_INV = 'Invoice date'
FIELD_PAY_DESC = 'Payment Description'
FIELD_AMT = 'Amount of Payment/Deposit'
FIELD_PROJECT = 'Name of Project (if applicable)'
FIELD_CLIENT = 'Name of Client'
FIELD_INV_NUM = 'Invoice #'
CHECK_FIELDS = [
    FIELD_DATE_PAID,
    FIELD_DATE_INV,
    FIELD_PAY_DESC,
    FIELD_AMT,
    FIELD_PROJECT,
    FIELD_CLIENT,
    FIELD_INV_NUM,
]

def main(args):
    if len(args) != 4:
        print __doc__
        return

    csv_name, url, key, client_id = args

    if not os.path.isfile(csv_name):
        print 'Could not find csv', csv_name
        return

    if not re.search(r'^\w+\.freshbooks\.com$', url):
        print 'URL should be in the format something.freshbooks.com'
        return

    if not re.search(r'^[0-9a-fA-F]{10,}$', key):
        print 'Key invalid'
        return

    if not re.search(r'^[0-9a-fA-F]{10,}$', key):
        print 'Key invalid'
        return
    try:
        client_id = int(client_id)
    except ValueError:
        print 'client_id invalid'
        return

    
    invoices, payments = [], []


    # invoices_response = client.invoice.list() # <request method="invoice.list" />
    # for invoice in invoices_response.invoices.invoice:
    #     # print "Invoice %s total: %s" % (
    #     #     invoice.note,
    #     #     invoice.amount
    #     # )
    #     for c in invoice.iterchildren():
    #         print c.tag, c.text
    #     break

    # return

    with open(csv_name, 'r') as csv_file:

        reader = csv.DictReader(csv_file)
        for i, row in enumerate(reader):
            if i == 0:
                for field in CHECK_FIELDS:
                    if field not in row:
                        print 'CSV invalid, missing field', field
                        return

            # skip withdrawals
            if 'T_ACH_WITHDRAWAL_DESC' in row[FIELD_PAY_DESC]:
                continue


            amt = float(row[FIELD_AMT])

            # skip expenses
            if amt <= 0.0:
                continue

            invoices.append(dict(
                client_id=str(client_id),
                date=parse_date(row[FIELD_DATE_INV]).strftime('%Y-%m-%d'),
                lines=[
                    api.types.line(
                        name='Elance Invoice %s' % row[FIELD_INV_NUM], 
                        unit_cost='%0.2f' % amt, 
                        quantity='1')
                ]
            ))
            payments.append(dict(
                date=parse_date(row[FIELD_DATE_PAID]).strftime('%Y-%m-%d'),
                amount='%0.2f' % amt, 
                type='Credit'
            ))


    client = api.TokenClient(
        url,
        key,
        user_agent='elance2freshbooks/0.1'
    )
    for invoice, payment in zip(invoices, payments):

        invoice_resp = client.invoice.create(invoice=invoice)
        print 'created invoice', invoice_resp.invoice_id

        payment['invoice_id'] = invoice_resp.invoice_id
        payment_resp = client.payment.create(payment=payment)
        print 'created payment', payment_resp.payment_id



if __name__ == '__main__':
    main(sys.argv[1:])