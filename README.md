# elance2freshbooks.py

This script will read a CSV of invoices and payments from Elance and 
create these invoices and payments on Freshbooks.

This worked for me so I could prepare my tax return, but it's hardly 
a well-tested, finished product. Use at your own risk (as per the LICENSE).

# Installation

    $ git clone https://github.com/jdillworth/elance2freshbooks.git
    $ cd elance2freshbooks
    $ sudo pip install -r requirements.txt

# Getting Elance Data

Now login to Elance, click Manage > Transactions.

Now click the menu option "Download Data".

Select the appropriate dates and click "Download".

# Getting your Freshbooks API Key

Login to Freshbooks and click "Account" > "Freshbooks API".

You need 2 pieces of info, your site domain and your API key.

DON'T USE the https://example.freshbooks.com/api/2.1/xml-in link at the top.

You need only your_company.freshbooks.com.

You also need the API key from this screen.

You also need the cliend ID for these invoices. In Freshbooks click 
"People" and click the client whose invoices you're loading. The
URL of the page will contain "userid=X" where X is the client ID.

# Running elance2freshbooks

    $ python elance2freshbooks.py csv-from-elance.csv url key client_id

The script will output a line for each invoice and payment like this:

    created invoice 111111
    created payment 111111

# Recovering from a Mistake

Copy the "created invoice..." output into a file.

Run the read_log_delete_created.py script passing it this file.

    $ python read_log_delete_created.py url key log_of_prior_results

It will delete all payments first, then delete invoices.