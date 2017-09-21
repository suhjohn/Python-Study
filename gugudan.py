l = ['%d * %d = %d' % (x, y, x*y) for x in range(2, 10) for y in range(1, 10)]

for items in l:
    if int(items[4]) == 1:
        print('== {}단 =='.format(items[0]))
    print(items)

# Utilizing Dict
full_dict = [{'title' : '{}단'.format(x), 'items' : ['%d * %d = %d' % (x, y, x*y) for y in range(1, 10)]} for x in range(2,10)]

for item in full_dict:
    print('=='+item['title']+'==')
    for item in (item['items']):
        print(item)
