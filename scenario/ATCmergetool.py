filename = 'extrapoints.scn'
f = open(filename,'r')
text = f.read().split('\n')
newt = ''
for line in text:
    if '*' in line and len(line)-2 <= line.index('*'):
        newt += line+'\n'
f = open('r'+filename,'w')
f.write(newt)
f.close()