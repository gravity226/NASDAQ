import numpy as np

def get_companies():
    company_list = []

    with open('../data/companies.txt') as f:
        for line in f:
            company_list.append(line.split('('))

    for n in xrange(len(company_list)):
        company_list[n][0] = company_list[n][0].strip()
        company_list[n][1] = company_list[n][1].strip().replace('\n', '').replace(')', '').strip()

    #company_list = np.array(set(np.array(company_list)[:,1]))
    names = []
    symbols = []
    for cell in company_list:
        if cell[1] not in symbols:
            names.append(cell[0])
            symbols.append("#" + cell[1])

    company_list = zip(names, symbols)
    company_list.append(("Thomson Reuters Corp", "TRI"))
    company_list.append(("Arrow Electronics, Inc", "ARW"))
    company_list.append(("Level 3 Communications, Inc", "LVLT"))
    company_list.append(("Oracle Corporation", "ORCL"))
    return company_list

def hand_made_list():
    company_list = []

    search_dict = {
        'SPY': ['SPDR S&P 500 ETF Trust', '$SP500', '#SP500', '$SPY', '#SPY'],
        'EEM': ['iShares MSCI Emerging Markets ETF', '$EEM', '$EFT', '#EEM', '#EFT']
        }

    with open('../data/hand_picked_companies.txt') as f:
        for line in f:
            company_list.append(line.split('('))

    company_list.append(["Thomson Reuters Corp", "TRI"])
    company_list.append(["Arrow Electronics, Inc", "ARW"])
    company_list.append(["Level 3 Communications, Inc", "LVLT"])
    company_list.append(["Oracle Corporation", "ORCL"])
    company_list.append(["Google", "GOOG"])
    
    company_list.append(["EURUSD", "EURUSD"])
    company_list.append(["USDJPY", "USDJPY"])
    company_list.append(["GBPUSD", "GBPUSD"])
    company_list.append(["USDCHF", "USDCHF"])
    company_list.append(["EURJPY", "EURJPY"])
    company_list.append(["EURGBP", "EURGBP"])
    company_list.append(["USD", "USD"])
    company_list.append(["EUR", "EUR"])
    company_list.append(["JPY", "JPY"])
    company_list.append(["GBP", "GBP"])
    company_list.append(["CHF", "CHF"])


    for n in xrange(len(company_list)):
        temp_list = []

        # company name
        temp_list.append(company_list[n][0].strip())

        company_symbol = company_list[n][1].strip().replace('\n', '').replace(')', '').strip()
        # #company symbol
        temp_list.append('#' + company_symbol)
        # $company symbol
        temp_list.append('$' + company_symbol)

        search_dict[company_symbol] = temp_list



    return search_dict

# search_dict = {
#     'SPY': ['SPDR S&P 500 ETF Trust', '$SP500', '#SP500', '$SPY', '#SPY'],
#     'EEM': ['iShares MSCI Emerging Markets ETF', '$EEM', '$EFT', '#EEM', '#EFT'],
#     'DUST': ['Direxion Daily Gold Miners Index Bear 3x Shares', '$DUST', '#DUST'],
#     'GDX' : ['Market Vectors Gold Miners ETF', '$GDX', '#GDX'],
#     'EWJ' : ['iShares MSCI Japan ETF', '$EWJ', '#EWJ'],
#     'XLF' : ['Financial Select Sector SPDR ETF', '$XLF', '#XLF'],
#     'UVXY' : ['ProShares Ultra VIX Short-Term Futures ETF', '$UVXY', '#UVXY'],
#     'EFA' : ['iShares MSCI EAFE ETF (EFA)'
#     'iShares Russell 2000 ETF (IWM)'
#     'VelocityShares 3x Long Crude ETN (UWTI)'
#     'iShares MSCI Brazil Capped ETF (EWZ)'
#     'Vanguard FTSE Emerging Markets ETF (VWO)'
#     'ProShares Ultra Bloomberg Crude Oil (UCO)'
#     'iShares China Large-Cap ETF (FXI)'
#     'SPDR S&P Oil&Gas Exploration&Production ETF (XOP)'
#     'Utilities Select Sector SPDR ETF (XLU)'
#     'SPDR Barclays High Yield Bond ETF (JNK)'
#     'Industrial Select Sector SPDR ETF (XLI)'
#     'Consumer Staples Select Sector SPDR ETF (XLP)'
#     'SunEdison (SUNE)'
#     'Bank of America (BAC)'
#     'Ford Motor (F)'
#     'Pfizer (PFE)'
#     'Freeport-McMoRan (FCX)'
#     'Valeant Pharmaceuticals International (VRX)'
#     'General Electric (GE)'
#     'Vale ADR (VALE)'
#     'Sprint (S)'
#     'Marathon Oil (MRO)'
#     'Chesapeake Energy (CHK)'
#     'AT&T (T)'
#     'Whiting Petroleum (WLL)'
#     'Transocean (RIG)'
#     'Petroleo Brasileiro ADR (PBR)'
#     'Twitter (TWTR)'
#     'Schlumberger (SLB)'
#     'Kinder Morgan (KMI)'
#     'California Resources (CRC)'
#     'Cameron International (CAM)'
#     'Sirius XM Holdings (SIRI)'
#     'VelocityShares Daily 2x VIX Short Term ETN (TVIX)'
#     'Micron Technology (MU)'
#     'Apple (AAPL)'
#     'PowerShares QQQ Trust Series 1 (QQQ)'
#     'Facebook Cl A (FB)'
#     'BlackBerry (BBRY)'
#     'Microsoft (MSFT)'
#     'Zynga (ZNGA)'
#     'Cisco Systems (CSCO)'
#     'Marriott International Cl A (MAR)'
#     'VelocityShares Daily Inverse VIX Short Term ETN (XIV)'
#     'Intel (INTC)'
#     'Frontier Communications (FTR)'
#     'Tesla Motors (TSLA)'
#     'Genocea Biosciences (GNCA)'
#     'Gaming&Leisure Properties (GLPI)'
#     'Netflix (NFLX)'
#     'Yahoo! (YHOO)'
#     'Office Depot (ODP)'
#
#
#
#
#
#
#
#
#
#
#
#

    #
