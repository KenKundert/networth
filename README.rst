Networth: Summarize Your Net Worth
==================================

| Version: 0.8.0
| Released: 2020-10-10
|

*Networth* works with `Avendesora <https://avendesora.readthedocs.io>`_ to 
generate a summary of your networth. *Networth* reads *estimated_value* fields 
from *Avendesora* accounts and summarizes the result.  It is often used with, 
and shares fields with, `PostMortem <https://github.com/KenKundert/postmortem>`_.

Please report all bugs and suggestions to networth@nurdletech.com

Getting Started
---------------

You download and install *Networth* with::

    pip3 install --user networth

Once installed, you will need at least two configuration files. The 
configuration files are `NestedText <https://nestedtext.readthedocs.io>`_.  The 
first file contains settings that are shared between all profiles.  It is 
~/.config/networth/config.  The remaining files are specific to profiles.  You 
would generally have one profile for yourself, but you might also have profiles 
for organizations or people that you are monitoring.

Profile files have a .prof suffix, and the name of the profile is the name of 
the profile file without the suffix.

In general, any setting may be in either the config file or the profile file.  
However, the following setting should in the config file:

**default profile**

A string that contains the name of the profile to use if the one is not 
explicitly specified on the command line.

In addition, the following settings are available:

**avendesora fieldname**

The name of the *Avendesora* account field that contains the networth 
information.

**value updated subfieldname**

The name of the subfield of *estimated_value* that contains the date the 
value was last updated.  Typically *updated*.

**max account value age**

Number of days. Values that are older than this are called out as being 
stale.

**date formats**

A string that contains the allowed date formats separated by white space.  
Any spaces is a specific format is replaced by an underscore so that it is 
not confused as more than one format. For example a format of 'MMMM YYYY' 
would be represented as 'MMMM_YYYY'. The formats allowed are those supported 
by Arrow.

May also be a list of strings, where each represents a valid date format.  

By default the following formats are accepted: 'MMMM YYYY', 'MMM YYYY', 
'YYYY-M-D', and 'YYMMDD'. So the following dates would be accepted: 'January 
2019', 'Jan 2019', '2019-1-1' and '190101'.

**asset color**

The color to used for positive values. May be black, white, blue, cyan, 
green, red, magenta, or yellow. The default is green.

**debt color**

The color to used for negative values. May be black, white, blue, cyan, 
green, red, magenta, or yellow. The default is red.

**screen width**

An integer that contains the width of the screen.

**aliases**

A dictionary that is used to map an account name to something that is easier 
to read.

**coins**

A list of crytpocurrency tokens that should be available for use.

**coins max price age**

Maximum age in seconds of the coins price caches. If the prices are older than 
this, the cache is flushed and the prices are updated.

**coin prices filename**

Name of the file used as the cryptocurrency price cache.

**securities**

A list of security symbols that should be available for use.

**securities max price age**

Maximum age in seconds of the securities price caches. If the prices are older 
than this, the cache is flushed and the prices are updated.

**security prices filename**

Name of the file used as the security price cache.

**iexcloud api key** or **iexcloud api key avendesora account**

The security prices are downloaded from IEXcloud.io. You must sign up with them 
to use this service. The free account is more than sufficient for your needs.  
Once you sign up you can get an API token, which you give as the value for this 
field.  This field must be given if you specify securities.  You may specify the 
API token directly using *iexcloud api key* or you can specify the account and 
field name for the API key if it is held by *Avendesora* with 
*iexcloud api key avendesora account*.

**metals**

A list of precious metal tokens that should be available for use.

**metals max price age**

Maximum age in seconds of the metals price caches. If the prices are older than 
this, the cache is flushed and the prices are updated.

**metal prices filename**

Name of the file used as the precious metal price cache.

**metals api key** or **metals api key avendesora account**

The precious metal prices are downloaded from metals-api.com. You must sign up 
with them to use this service. The free account is generally sufficient for your 
needs.  Once you sign up you can get an API token, which you give as the value 
for this field.  This field must be given if you specify precious metals.  You 
may specify the API token directly using *metals api key* or you can specify the 
account and field name for the API key if it is held by *Avendesora* with 
*metals api key avendesora account*.


Example Configuration Files
---------------------------

Here is an example *config* file::

    default profile: me

    # account value settings
    avendesora fieldname: estimated_value
    value updated subfieldname: updated
    max account value age: 120
    date formats: MMMM YYYY

    # bar settings
    screen width: 110

    # API token needed to download securities
    iexcloud token: pk_9eb3acfc7dbe4055a795ff179d46a980

Here is a example profile file::

    # account aliases
    aliases:
        quickenloans: mortgage
        wellsfargo: wells fargo

    # available symbols
    coins: USD BTC ETH BCH ZEC EOS
    securities: GOOG AMZN


Estimated Values
----------------

Next, you need to add *estimated_value* fields to your *Avendesora* accounts, 
the value of which is a dictionary. It may contain a *updated* subfield that 
gives the date the value was last updated.  In addition, it may contain 
subfields for various asset classes or coins or securities.  The values may 
either be real numbers or strings that contain quantities (values plus units).  
Here are some examples::

    class ChaseBank(Account):
        ...
        estimated_value = dict(updated='December 2018', cash=2181.16+5121.79)

    class QuickenLoans(Account):
        ...
        estimated_value = dict(updated='October 2018', real_estate='-$294,058')

    class Vanguard(Account):
        ...
        estimated_value = dict(updated='November 2018', retirement='$74,327')

    class TDAmeritrade(Account):
        ...
        estimated_value = dict( updated='November 2018', retirement='$74,327+$111,554')

    class Fidelity(Account):
        ...
        estimated_value = dict( updated='November 2018', retirement='''
            $62,976.22 +    # 401k
            $26,704.85      # IRA
        ''')

    class UnitedAirlines(Account):
        ...
        estimated_value = dict(updated='July 2018', miles='7,384_miles')

    class CoinBase(Account):
        ...
        estimated_value = dict(updated='August 2018', ETH=2, BTC=4, cash=24.52)

    class TD_Ameritrade(Account):
        ...
        estimated_value = dict(updated='January 2019', GOOG=10, AMZN=5, cash=327.53)

The value of securities are given is number of shares. The value given for 
cryptocurrencies is number of tokens. All other values are assumed to be in 
dollars if the units are not given. If the units are given and they are not 
dollars (such as miles for frequent flier programs), then those values are 
summarized but not included in your total networth.

Specifying the *updated* date is optional. If specified, then *networth* will 
indicate the values as stale if they exceed *max_account_value_age*.

It is also specify information about a loan, and *networth* will compute its 
current balance.  This is done by giving the principal on a particular date, the 
date for the given principal, the monthly payments, the interest rate, and 
optionally, the share. The rate and the share can be given in percent, meaning 
that an rate of 4% can either be specified as 4% or as 0.04. Similarly a share 
half share can be indicated as 50% or 0.5.  For example::

    class QuickenLoans(Account):
        ...
        estimated_value = dict(
            real_estate = '''
                principal=-$294,058
                date=09/04/2013
                payment=$1,500.00
                rate=4.375%
                share=50%
            '''
        )

the key=value pairs can be separated by any white space, but there must be no
white space surrounding the = sign. For mortgages that you owe, the principal 
should be negative. You can also use this feature to describe an automatic 
savings plan into an interest bearing account.  In this case the principal would 
be your starting balance and the payment would be your monthly investment 
amount.  In this case the starting balance would be positive.


Usage
-----

When running the command, you may specify a profile. If you do not, you get the 
default profile.  For example::

    > networth me
    By Account:
            betterment:    $22k equities=$9k, cash=$3k, retirement=$9k
                 chase:     $7k cash
             southwest:      $0 miles=78kmiles
              coindesk:  $15.3k cryptocurrency

    By Type:
        cryptocurrency:  $15.3k (35.3%) ██████████████████████████████████████████
                  cash:    $10k (23.1%) ███████████████████████████████
              equities:     $9k (20.8%) ███████████████████████████
            retirement:     $9k (20.8%) ███████████████████████████

                 TOTAL:  $43.3k (assets = $43.3k, debt = $0)

In this run, the values associated with the various asset classes (ex. equities, 
cash, retirement, etc.) are taken as is. As such, you must be diligent about 
keeping these values up to date, which is a manual operation. You might consider 
updating your *estimated values* every 3-6 months.  However the current prices 
for your configured securities and cryptocurrencies are downloaded and 
multiplied by the given number of shares or tokens to get the up-to-date values 
of your equities and cryptocurrency holdings. Thus you only need update them 
after a transaction. Finally, mortgage balances are also kept up to date. You 
only need update mortgages if you decide to change the payment amount in order 
to pay off the loan faster.


Releases
--------
**Latest Development Version**:
    | Version: 0.8.0
    | Released: 2020-10-10

**0.8 (2020-10-10)**:
    - Add support for downloading prices of precious metals.
    - Switch to *NestedText* for the settings files.

**0.7 (2020-03-06)**:
    - Now uses `QuantiPhy Eval <https://github.com/KenKundert/quantiphy_eval>`_ 
      to allow you to use expressions within strings for estimated values.

**0.6 (2020-01-08)**:
    - Added --prices and --clear-cache command line options.
    - Support using a proxy

**0.5 (2019-07-18)**:

**0.4 (2019-06-15)**:
    - Convert to using new IEXcloud API for downloading security prices.

**0.3 (2019-04-20)**:
    - Allow arbitrary date format in mortgages
    - Improve error reporting
    - Change the sign of the principal in mortgages

**0.1 (2019-03-23)**:
    - Initial release
    - Add mortgage balance calculations

**0.0 (2019-01-31)**:
    - Initial version

