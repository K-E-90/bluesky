ACCOM = ['CRE','ALT','SPD','ORIG','DEST','HDG','LNAV','VNAV']
ACLST = ['KLM646','KML347','TRA728','KLM492','KLM440','KLM571',
         'KLM821','KLM648','KLM108','KLM398','TRA879','KLM713',
         'TRA460','KLM300','KLM351','KLM236','TRA581','TRA825',
         'KLM653','TRA589','TRA251','KLM951','KLM726','KLM680']

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
f = open('r'+filename,'w')
f.write(newt)
f.close()