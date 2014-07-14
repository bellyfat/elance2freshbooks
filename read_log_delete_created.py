"""Usage:

    python read_log_delete_created.py url key log_of_prior_results

"""

import sys, re
from refreshbooks import api
from refreshbooks.client import FailedRequest

def main(args):
    if len(args) != 3:
        print __doc__
        return

    url, key, log_name = args

    client = api.TokenClient(
        url,
        key,
        user_agent='refreshbooks/2.0'
    )

    with open(log_name, 'r') as log_file:
        for line in log_file:
            m = re.search('^created payment (\d+)$', line.rstrip())
            if m:
                try:
                    client.payment.delete(payment_id=int(m.group(1)))
                    print 'deleted payment', m.group(1)
                except FailedRequest:
                    print 'FAILED deleting payment', m.group(1)
                continue

    with open(log_name, 'r') as log_file:
        for line in log_file:
            m = re.search('^created invoice (\d+)$', line.rstrip())
            if m:
                try:
                    client.invoice.delete(invoice_id=int(m.group(1)))
                    print 'deleted invoice', m.group(1)
                except FailedRequest:
                    print 'FAILED deleting invoice', m.group(1)
                continue


if __name__ == '__main__':
    main(sys.argv[1:])