
def translate_search_to_sql(raw_data):
    sql_statement = ''
    first = True
    where_sql = ['Naam','Menselijk Kapitaal','Natuurlijk Kapitaal','Ondernemings nummer','Email','Telefoon nummer','WebAdres','Personeelsbestanden','WCM','B2B']
    join_sql = ['Sector','Adres','Postcode','Gemente','BTW nr','Omzet','Balanstotaal','Netto Toegevoegde Waarde']

    # add join sql 

    
    # add all where sql 
    for pos in where_sql:
        if(pos in raw_data):
            if(raw_data[pos]['Type'] == 'Contains'):
                sql_statement+=where_and(first,pos)
                sql_statement+= " LIKE '%"+raw_data[pos]['input']+"%'"
            if(raw_data[pos]['Type'] == 'Starts with'):
                sql_statement+=where_and(first,pos)
                sql_statement+= " LIKE '"+raw_data[pos]['input']+"%'"
            if(raw_data[pos]['Type'] == 'Ends with'):
                sql_statement+=where_and(first,pos)
                sql_statement+= " LIKE '%"+raw_data[pos]['input']+"'"
            if(raw_data[pos]['Type'] == 'Matches'):
                sql_statement+=where_and(first,pos)
                sql_statement+= "='"+raw_data[pos]['input']+"'"
            if(raw_data[pos]['Type'] == '='):
                sql_statement+=where_and(first,pos)
                sql_statement+= "='"+score_to_number(raw_data[pos]['input'])+"'"
            if(raw_data[pos]['Type'] == '<='):
                sql_statement+=where_and(first,pos)
                sql_statement+= ">='"+score_to_number(raw_data[pos]['input'])+"'"
            if(raw_data[pos]['Type'] == '>='):
                sql_statement+=where_and(first,pos)
                sql_statement+= "<='"+score_to_number(raw_data[pos]['input'])+"'"

    print('''SELECT * FROM dep.KMO {}  limit 100 ;'''.format(sql_statement))
    return  '''SELECT * FROM dep.KMO {}  limit 100 ;'''.format(sql_statement)

def where_and(first,pos):
    att = translate_attribute(pos)
    if(first):
        first=False
        return 'WHERE '+att
    else:
        return ' AND '+att+' '

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
       'Personeelsbestanden': "personeelsbestanden",
       'WCM': "wcm",
       'B2B': "b2b",
       'Sector': "TODO",
       'Adres': "TODO",
       'Postcode': "TODO",
       'Gemente': "TODO",
       'BTW nr': "TODO",
       'Omzet': "TODO",
       'Balanstotaal': "TODO",
       'Netto Toegevoegde Waarde': "TODO",
       }
    return switch.get(raw_attribute)