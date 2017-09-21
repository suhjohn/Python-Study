import re

f = open('sample.txt', 'rt')
source = f.read().strip().replace('\t', '')

p = re.compile(r'<td class="title">.*?</td>', re.DOTALL)
info = re.findall(p, source)

for index, e in enumerate(info):
    print('== index %s ==' % index)
    
    new_e = re.sub(r'>\s*?<', r'>\n<', e, flags=re.DOTALL)

    print(new_e)
    title = re.sub(r'<td.*?(.*?)</td>', r'\g<1>', new_e)
    print(title)
