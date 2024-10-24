import dataclasses

from aoc import helpers


@dataclasses.dataclass
class MapItem:
    src: range
    dst: range

    def apply(self, val: int):
        assert val in self.src
        return val - self.src.start + self.dst.start


@dataclasses.dataclass
class Map:
    src_name: str
    dst_name: str
    items: list[MapItem]

    def get_next_item_index(self, n: int):
        i_min = 0
        i_max = len(self.items)
        i_next = i_max
        while True:
            i = (i_max + i_min) // 2
            item = self.items[i]
            if n < item.src.start:
                i_max = i
                i_next = i
            elif item.src.stop <= n:
                i_min = i + 1
            else:
                return i

            if i_max - i_min == 0:
                return i_next

            assert i_max - i_min > 0

    def apply(self, r: range):
        current = r.start
        item_index = self.get_next_item_index(current)

        res: list[range] = []

        while True:
            if item_index >= len(self.items):
                return res + [range(current, r.stop)]

            item = self.items[item_index]
            if current not in item.src:
                if (r.stop - 1) not in item.src:
                    return res + [range(current, r.stop)]

                res.append(range(current, item.src.start))
                current = item.src.start

            if item.src.stop >= r.stop:
                return res + [range(item.apply(current), item.apply(r.stop - 1) + 1)]

            res.append(range(item.apply(current), item.apply(item.src.stop - 1) + 1))
            current = item.src.stop

            item_index += 1

    def update_with_line(self, line: str):
        dst_start, src_start, length = map(int, line.split())
        self.items.append(
            MapItem(
                src=range(src_start, src_start + length), dst=range(dst_start, dst_start + length)
            )
        )


@dataclasses.dataclass
class Input:
    init_name: str
    init_values: list[int]
    src_name_map_map: dict[str, Map]


def parse_input(lines: list[str]):
    input = Input(init_name='', init_values=[], src_name_map_map={})
    current_map = None
    for line in lines:
        if ':' in line:
            if 'map' in line:
                map_name, _, _ = line.partition('map:')
                source_name, _, target_name = map_name.partition('-to-')
                current_map = Map(
                    src_name=source_name.strip(), dst_name=target_name.strip(), items=[]
                )
                input.src_name_map_map[current_map.src_name] = current_map
            else:
                init_name, values = line.split(':')
                input.init_name = init_name.strip()
                input.init_values = [int(v) for v in values.split()]
        else:
            if line.strip() != '' and current_map is not None:
                current_map.update_with_line(line)

    for map in input.src_name_map_map.values():
        map.items = sorted(map.items, key=lambda vs: vs.src.start)
    return input


def apply(values: list[range], map: Map):
    return [r for v in values for r in map.apply(v)]


def solution(input: list[str]):
    pinput = parse_input(input)
    name = pinput.init_name[:-1]
    values = [range(v, v + 1) for v in pinput.init_values]
    while name != 'location':
        map = pinput.src_name_map_map[name]
        values = apply(values, map)
        name = map.dst_name
    return min(v.start for v in values)


if __name__ == '__main__':
    helpers.run_solution(solution)
