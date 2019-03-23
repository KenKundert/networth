Networth: Summarize Your Net Worth
==================================

| Version: 0.1.0
| Released: 2019-03-23
|

*Networth* works with `Avendesora <https://avendesora.readthedocs.io>`_ to 
generate a summary of your networth. *Networth* reads *estimated_value* fields 
from *Avendesora* accounts and summarizes the result.  It is often used with 
`PostMortem <https://postmortem.readthedocs.io>`_.

Please report all bugs and suggestions to networth@nurdletech.com

Getting Started
---------------

You download and install *Networth* with::

    git clone https://github.com/KenKundert/networth.git
    pip3 install --user networth

Once installed, you will need at least two configuration files. The 
configuration files are Python code.  The first file contains settings that are 
shared between all profiles.  It is ~/.config/networth/config. The remaining 
files are specific to profiles.  You would generally have one profile for 
yourself, but you might also have profiles for organizations or people that you 
are monitoring.

In general, any setting may be in either the config file or the profile file.  
However, the following two settings should in the config file:

default_profile:

    A string that contains the name of the profile to use if the one is not 
    explicitly specified on the command line.  The name specified in this 
    setting must also be one of the names specified in *profile_names*.

profile_names:

    A list the contains the names of the known profiles.  For every name given 
    there should be a profile file in the settings directory. Thus, if *me* is 
    one of the profile names, then there should be a file 
    ~/.config/networth/me.prof that contains the settings associated to the *me* 
    profile.

In addition, the following settings are available:

avendesora_fieldname:

    The name of the *Avendesora* account field that contains the networth 
    information.

value_updated_subfieldname:

    The name of the subfield of *estimated_value* that contains the date the 
    value was last updated.  Typically *updated*.

max_account_value_age:

    Number of days. Values that are older than this are called out as being 
    stale.

date_formats:

    A string that contains the expected date format of the *updated* subfield in 
    Arrow form.

asset_color:

    The color to used for positive values. May be black, white, blue, cyan, 
    green, red, magenta, or yellow. The default is green.

debt_color:

    The color to used for negative values. May be black, white, blue, cyan, 
    green, red, magenta, or yellow. The default is red.

screen_width:

    An integer that contains the width of the screen.

aliases:

    A dictionary that is used to map an account name to something that is easier 
    to read.

coins:

    A list of crytpocurrency tokens that should be available for use.

coin_prices_filename:

    Name of the file used as the cryptocurrency price cache.

securities:

    A list of security symbols that should be available for use.

security_prices_filename:

    Name of the file used as the security price cache.

max_price_age:

    Maximum age in seconds of the price caches. If the prices are older than 
    this, the cache is flushed and the prices are updated.


Example Configuration Files
---------------------------

Here is an example *config* file::

    default_profile='me'
    profile_names = 'me parents'.split()

    # account value settings
    avendesora_fieldname = 'estimated_value'
    value_updated_subfieldname = 'updated'
    max_account_value_age = 120 # days
    date_formats = 'MMMM YYYY'

    # bar settings
    screen_width = 110

Here is a example profile file::

    # account aliases
    aliases = dict(
        quickenloans = 'mortgage',
        wellsfargo = 'wells fargo',
    )

    # available symbols
    coins = 'USD BTC ETH BCH ZEC EOS'.split()
    securities = 'GOOG AMZN'.split()


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

    class UnitedAirlines(Account):
        ...
        estimated_value = dict(updated='July 2018', miles='7,384_miles')

    class Kraken(Account):
        ...
        estimated_value = dict(updated='August 2018', ETH=2, BTC=4, cash=24.52)

    class TD_Ameritrade(Account):
        ...
        estimated_value = dict(updated='January 2019', GOOG=10, AMZN=5, cash=327.53)

The value of securities are given is number of shares. The value given for 
cryptocurrencies is number of tokens. All other values are assumed to be in 
dollars if the units are not given. If the units are given and they are not 
dollars (such as miles for frequent flyer programs), then those values are 
summarized but not included in your total networth.

Specifying the *updated* date is optional. If specified, then *networth* will 
indicate the values as stale if they exceed *max_account_value_age*.

It is also specify information about a loan, and *networth* will compute its 
current balance.  This is done by giving the principal on a particular date, the 
date for the given principal, the monthly payments, the interest rate, and 
optionally, the share. The rate and the share can be given in percent, meaning 
that an rate of 4% can either be specified as 4% or as 0.04. Similarly a share 
half share can be indicated as 50% or 0.5.  For example:

    class QuickenLoans(Account):
        ...
        estimated_value = dict(
            real_estate = '''
                principal=$294,058
                date=09/04/2013
                payment=$1,500.00
                rate=4.375%
            '''
        )

the key=value pairs can be separated by any white space, but there must be no
white space surrounding the = sign.


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
of your equities and cryptocurrency holdings.
