HALF = (1000000, 1000000)


def save_map(line1, line2):
    with open('map.txt', 'w') as fp:
        fp.write('\n'.join('%s %s' % x for x in line1))
        fp.write('\n')
        fp.write('%s %s' % HALF)
        fp.write('\n')
        fp.write('\n'.join('%s %s' % x for x in line2))


def load_map():
    with open('map.txt') as f:
        return [tuple(map(int, i.split(' '))) for i in f]
