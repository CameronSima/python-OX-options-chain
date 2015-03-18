'''
Created on Mar 17, 2015

@author: TJ
'''

from pyquery import PyQuery as pq
import urllib2
import sys
import datetime as dt

def query_chain(s_symbol="SPY",dt_date=dt.datetime.now()):
    
    s_url_core = 'http://finance.yahoo.com/q/op'
    s_url_sym = '?s=%s' % s_symbol
    
    #convert dt to seconds since epoch
    dt_date = dt_date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    i_epoch_sec = (dt_date - dt.datetime(1970,1,1)).total_seconds()
    
    s_url_date = '&date=%i' % i_epoch_sec #converts to seconds since epoch
    

    pq_html = pq(s_url_core + s_url_sym + s_url_date)
    
    
    s_html_calls_table = pq_html("#optionsCallsTable table.quote-table")
    
    d_calls = parse_table(s_html_calls_table)
    
    s_html_puts_table = pq_html("#optionsPutsTable table.quote-table")
    d_puts = parse_table(s_html_puts_table)
    
    return {"calls": d_calls, "puts": d_puts}
    
def parse_table(pq_table):
    pq_rows = pq_table("tbody tr")
    
    lsd_itm = []
    lsd_otm = []
    
    for pq_row in pq_rows:
        d_contract = parse_contract_row(pq(pq_row))
        
        if d_contract["b_itm"]:
            lsd_itm.append(d_contract)
        else:
            lsd_otm.append(d_contract)
        
    return {"itm": lsd_itm, "otm": lsd_otm}
        
    
def parse_contract_row(pq_contract_row):
    
    pq_cells = pq_contract_row.find("td")
    pq_cells = [pq(x) for x in pq_cells]
    
    d_contract = {}
    d_contract["b_itm"] = pq_contract_row.hasClass("in-the-money")
    d_contract["f_strike"] = float(pq_cells[0].find("a").text())
    d_contract["s_contract_name"] = pq_cells[1].find("a").text()
    d_contract["f_last"] = float(pq_cells[2].find("div").text())
    d_contract["f_bid"] = float(pq_cells[3].find("div").text())
    d_contract["f_ask"] = float(pq_cells[4].find("div").text())
    d_contract["f_change"] = float(pq_cells[5].find("div").text())
    d_contract["s_change_percent"] = pq_cells[6].find("div").text()
    d_contract["i_volume"] = float(pq_cells[7].find("strong").text())
    d_contract["i_open_interest"] = float(pq_cells[8].find("div").text())
    d_contract["s_iv"] = pq_cells[9].find("div").text()
    
    return d_contract

if __name__ == '__main__':
    d_chain = None
    if len(sys.argv) > 1:
        d_chain = query_chain(sys.argv[1])
    else:
        d_chain = query_chain("MSFT", dt.datetime(2015,3,20))
        
    print d_chain
