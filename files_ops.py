def save_map(start_positions, end_positions):
    with open('map.txt', 'w') as fp:
        fp.write('\n'.join('%s %s' % x for x in start_positions))
        fp.write('\n')
        fp.write('\n'.join('%s %s' % x for x in end_positions))


def load_map():
    with open('map.txt') as f:
        return [tuple(map(int, i.split(' '))) for i in f]
