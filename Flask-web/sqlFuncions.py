from cmath import log
import numpy as np

where_sql = ['Naam','Menselijk Kapitaal','Natuurlijk Kapitaal','Ondernemings nummer','Email','Telefoon nummer','WebAdres','Aantal werknemers','WCM','B2B']
sector_sql = ['Sector']
adres_sql = ['Adres','Postcode','Gemente']
bank_sql = ['Bank ID','Omzet','Balanstotaal','Netto Toegevoegde Waarde']
first = True
def translate_search_to_sql(raw_data):
    global where_sql
    global sector_sql
    global adres_sql
    global bank_sql
    global first
    sql_statement = 'SELECT * FROM dep.KMO k'
    joins_added = [False,False,False]
    for item in raw_data:
        if((item in sector_sql) and (joins_added[0] is not True)):
           sql_statement+=" INNER JOIN dep.Sector s ON k.ibid = s.sectorID "
           joins_added[0] = True
        if((item in adres_sql) and (joins_added[1] is not True)):
           sql_statement+=" INNER JOIN dep.Locatie l ON k.LocatieID = l.adres "
           joins_added[1] = True
        if((item in bank_sql) and (joins_added[2] is not True)):
           sql_statement+=" INNER JOIN dep.Balans b ON k.BalansID = b.bvdIDnr "
           joins_added[2] = True
    first = True
    # add all where sql 
    for pos in np.concatenate([where_sql,sector_sql,adres_sql,bank_sql]):
        if(pos in raw_data):
            if(raw_data[pos]['Type'] == 'Contains'):
                sql_statement+=where_and(pos)
                sql_statement+= " LIKE '%"+raw_data[pos]['input']+"%'"
            if(raw_data[pos]['Type'] == 'Starts with'):
                sql_statement+=where_and(pos)
                sql_statement+= " LIKE '"+raw_data[pos]['input']+"%'"
            if(raw_data[pos]['Type'] == 'Ends with'):
                sql_statement+=where_and(pos)
                sql_statement+= " LIKE '%"+raw_data[pos]['input']+"'"
            if(raw_data[pos]['Type'] == 'Matches'):
                sql_statement+=where_and(pos)
                sql_statement+= "='"+raw_data[pos]['input']+"'"
            if(raw_data[pos]['Type'] == '='):
                sql_statement+=where_and(pos)
                sql_statement+= "="+raw_data[pos]['input']
            if(raw_data[pos]['Type'] == '<='):
                sql_statement+=where_and(pos)
                sql_statement+= "<="+raw_data[pos]['input']
            if(raw_data[pos]['Type'] == '>='):
                sql_statement+=where_and(pos)
                sql_statement+= ">="+raw_data[pos]['input']

    print('''{}  limit 100 ;'''.format(sql_statement))
    return  '''{}  limit 100 ;'''.format(sql_statement)
    



def where_and(pos):
    global first
    att = translate_attribute(pos)
    if(first):
        first=False
        return ' WHERE '+pos_to_join_letter(pos)+'.'+att
    else:
        return ' AND '+pos_to_join_letter(pos)+'.'+att+' '

def pos_to_join_letter(pos):
    global sector_sql
    global adres_sql
    global bank_sql
    if(pos in sector_sql):
        return "s"
    if(pos in adres_sql):
        return "l"
    if(pos in bank_sql):
        return "b"
    return "k"

def translate_order(order):
    switch={
    'Ascending': "ASC",
    'Descending': "DESC",
    } 
    return switch.get(order)

def score_to_number(letter):
    switch={
    'A': "1",
    'B': "2",
    'C': "3",
    }
    return switch.get(letter)

def translate_attribute(raw_attribute):
    switch={
       'Naam': "naam",
       'Menselijk Kapitaal': "duurzaamheid",
       'Natuurlijk Kapitaal': "beursnotatie",
       'Ondernemings nummer': "onderneminsNr",
       'Email': "email",
       'Telefoon nummer': "telefoonNr",
       'WebAdres': "webAdres",
       'Aantal werknemers': "personeelsbestanden",
       'WCM': "wcm",
       'B2B': "b2b",
       'Sector': "sector",
       'Adres': "adres",
       'Postcode': "postcode",
       'Gemente': "gemeente",
       'Bank ID': "bvdIDnr",
       'Omzet': "omzet",
       'Balanstotaal': "balanstotaal",
       'Netto Toegevoegde Waarde': "nettoToegevoegdeWaarde",
       }
    return switch.get(raw_attribute)