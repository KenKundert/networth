Networth — Summarize Your Net Worth
===================================

.. image:: https://pepy.tech/badge/networth/month
    :target: https://pepy.tech/project/networth

.. image:: https://img.shields.io/pypi/v/networth.svg
    :target: https://pypi.python.org/pypi/networth

.. image:: https://img.shields.io/pypi/pyversions/networth.svg
    :target: https://pypi.python.org/pypi/networth/


| Version: 1.2
| Released: 2023-04-22

*Networth* works with `Avendesora <https://avendesora.readthedocs.io>`_ to 
generate a summary of your networth. *Networth* reads *estimated_value* fields 
from *Avendesora* accounts and summarizes the result.  It is often used with, 
and shares fields with, `PostMortem <https://github.com/KenKundert/postmortem>`_.
Works with data services to download up-to-date prices for securities and 
cryptocurrencies.

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

default profile:
    A string that contains the name of the profile to use if the one is not 
    explicitly specified on the command line.

In addition, the following settings are available:

avendesora fieldname:
    The name of the *Avendesora* account field that contains the networth 
    information.  Typically *estimated_value*.

value updated subfieldname:
    The name of the subfield of *estimated_value* that contains the date the 
    value was last updated.  Typically *updated*.

max account value age:
    Number of days. Values that are older than this are called out as being 
    stale. Default is 120 days.

date formats:
    The list of allowed date formats. May be specified as a list or as a string
    string that contains the allowed date formats separated by white space.  Any 
    spaces is a specific format is replaced by an underscore so that it is not 
    confused as more than one format. For example a format of 'MMMM YYYY' would 
    be represented as 'MMMM_YYYY'. The formats allowed are those supported by 
    Arrow.

    By default the following formats are accepted: 'MMMM YYYY', 'MMM YYYY', 
    'YYYY-M-D', and 'YYMMDD'. So the following dates would be accepted: 'January 
    2019', 'Jan 2019', '2019-1-1' and '190101'.

asset color:
    The color to used for positive values. May be black, white, blue, cyan, 
    green, red, magenta, or yellow. The default is green.

debt color:
    The color to used for negative values. May be black, white, blue, cyan, 
    green, red, magenta, or yellow. The default is red.

screen width:
    An integer that contains the width of the screen.

aliases:
    A dictionary that is used to map an account name to something that is easier 
    to read.

cryptocompare:
    A dictionary containing information about cryptocurrency prices that are to 
    be downloaded from cryptocompare.com.

    To avoid caching issues it is recommended that *cryptocompare* files be 
    placed in the shared *config* file if multiple profiles need it.

    tokens:
        A dictionary of crytpocurrency tokens that should be available for use.
        The key of the dictionary is the token symbol, the value is the category 
        it should associate with.

    ttl:
        Cache time to live.  If the cache is older than this time, it is 
        refreshed.  Here are example times: 600s, 10m, 6h, 1d.  The default is 
        10m.

    api key:
        The coin prices are downloaded from cryptocompare.com. Specifying the 
        API key is optional.  Providing an API key increases your limits, but 
        limits are generally not a problem for *Networth* because it is run so 
        infrequently.

    api key account field:
        You may place the API key in *Avendesora* and use this key to specify the 
        account and field name for the API key.

iexcloud:
    A dictionary containing information about security prices that are to be 
    downloaded from iexcloud.io.  This dictionary takes the same fields as 
    *cryptocompare*.  An API key is required.

    To avoid caching issues it is recommended that *iexcloud* files be placed in 
    the shared *config* file if multiple profiles need it.

twelve data:
    A dictionary containing information about security prices that are to be 
    downloaded from twelvedata.com.  This dictionary takes the same fields as 
    *cryptocompare*.  An API key is required.

    To avoid caching issues it is recommended that *twelvedata* files be placed 
    in the shared *config* file if multiple profiles need it.

    *Twelve Data* provides real time values, but have very low limits unless you 
    get an expensive subscription.  If you do not have a subscription, it is 
    recommended that you limit the number of tokens to 8 or less.

metals api:
    A dictionary containing information about precious metals prices that are to 
    be downloaded from metals-api.com.  This dictionary takes the same fields as 
    *cryptocompare*.  An API key is required.

    To avoid caching issues it is recommended that *metals* files be placed in 
    the shared *config* file if multiple profiles need it.

    Metals API has dropped their free tier.

metals live:
    A dictionary containing information about precious metals prices that are to 
    be downloaded from metals-api.com.  This dictionary only requires the 
    *tokens* field. An API key is not required.

estimated value overrides file:
    A path to a file of *estimated_value* overrides. Give as a NestedText file 
    that contains a dictionary of dictionaries.  The keys for the top level are 
    account names, and the value contains the estimated value dictionary that 
    would normally be found in the *Avendesora* accounts file.


Example Configuration Files
---------------------------

Here is an example *config* file::

    default profile: me

    # account value settings
    avendesora fieldname: estimated_value
    value updated subfieldname: updated
    max account value age: 120
    date formats: M/D/YY M/D/YYYY

    # bar settings
    screen width: 110

    # cryptocurrency prices
    cryptocompare:
        tokens:
            USD: cash
            BTC: cryptocurrency
            ETH: cryptocurrency

    # securities prices
    iexcloud:
        api key: pk_9eb3acfc7dbe4055a795ff179d46a980
        tokens:
            GOOG: equities
            AMZN: equities
            GBTC: cryptocurrency

Here is a example profile file::

    # account aliases
    aliases:
        quickenloans: mortgage
        wellsfargo: wells fargo


Here is a example estimated value overrides file::

    chase:
        updated: February 2021
        cash:
            > $4,425.71 +       # checking
            > $1,896.26         # savings


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
            ''',
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


History
-------

If you would like to be able to plot your net worth over time you run the 
following regularly::

    networth -w <profile>

Each time you do, the networth values are added to a data file 
(~/.local/share/networth/<profile>.nt).

You can then plot the historical values using::

    plot-networth <name>...

You can get a list of the values you can plot using::

    plot-networth -l


Releases
--------
**Latest Development Version**:
    | Version: 1.2
    | Released: 2023-04-22

**1.2 (2023-04-22)**:
    - add metals.live data service

**1.1 (2021-03-11)**:
    - clean up and minor refinements.

**1.0 (2021-02-13)**:
    - Add *estimated value overrides file* setting.
    - Add --details option.
    - Add --write-data option.
    - Add *plot-networth* command.
    - Allow categories to be specified for downloaded token prices.

**0.8 (2020-10-10)**:
    - Add support for downloading prices of precious metals.
    - Switch to *NestedText* for the settings files.

**0.7 (2020-03-06)**:
    - Now uses `QuantiPhy Eval <https://github.com/KenKundert/quantiphy_eval>`_ 
      to allow you to use expressions within strings for estimated values.

**0.6 (2020-01-08)**:
    - Added --prices and --clear-cache command line options.
    - Support using a proxy.

**0.5 (2019-07-18)**:

**0.4 (2019-06-15)**:
    - Convert to using new IEXcloud API for downloading security prices.

**0.3 (2019-04-20)**:
    - Allow arbitrary date format in mortgages.
    - Improve error reporting.
    - Change the sign of the principal in mortgages.

**0.1 (2019-03-23)**:
    - Initial release.
    - Add mortgage balance calculations.

**0.0 (2019-01-31)**:
    - Initial version.

