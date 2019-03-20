ACCOM = ['CRE','ALT','SPD','ORIG','DEST','HDG','LNAV','VNAV']
ACLST = ['KLM263','TRA164','KLM935','TRA985','TRA699','KLM958','TRA651',
'TRA295','TRA282','J-905','KLM157','AL787','KLM276','EI313','KLM848',
'J-980','KLM182','KLM981','J-486','TRA449','J-922','KLM960','KLM941','KLM288',
'KLM796','QO309','KLM113']

filename = 'trafficSW_MASTER.scn'

f = open(filename,'r')
text = f.read().split('\n')
newt = ''
for line in text:
    add = True
    for COM in ACCOM:
        if COM in line:
            noac = True
            for AC in ACLST:
                if AC in line:
                    noac = False
            if noac:
                add = False
    if add:
        newt += line+'\n'
f = open('b'+filename,'w')
f.write(newt)
f.close()
