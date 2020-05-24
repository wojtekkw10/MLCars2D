def save_map(start_positions, end_positions):
    with open('map.txt', 'w') as fp:
        edited_map = []
        for i in range(1, len(start_positions)):
            edited_map.append(start_positions[i])
            edited_map.append(end_positions[i])

        fp.write('\n'.join('%s %s' % x for x in edited_map))


def load_map():
    with open('map.txt') as f:
        return [tuple(map(int, i.split(' '))) for i in f]
