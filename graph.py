import unittest

class Graph:
    def __init__(self):
        self.nodes = {}         # map: node key -> children
        # each node is a list of its edge partners

    def add_key(self, key):
        if key not in self.nodes:
            self.nodes[key] = []

    def add_edge(self, u, v):
        self.add_key(u)
        self.add_key(v)
        self.nodes[u].append(v)

    def add_undirected_edge(self, u, v):
        self.add_edge(u, v)
        self.add_edge(v, u)

    def has_key(self, key):
        return key in self.nodes

    def adjacent_nodes(self, key):
        return self.nodes.get(key, None)

    def __repr__(self):
        res = [n for n in self.nodes]
        return ",".join(res)

    def dfs(self, key, visited=None):
        if not self.has_key(key):
            return

        if visited is None:
            visited = set()

        visited.add(key)
        yield key

        for adj in self.adjacent_nodes(key):
            if adj not in visited:
                yield from self.dfs(adj, visited)

    def dfs_stack(self, source):
        stack = [source]
        visited = set()
        while len(stack):
            key = stack.pop()
            if key in visited:
                continue

            visited.add(key)
            yield key
            for adj in self.adjacent_nodes(key):
                stack.append(adj)

    def dfs_stack_postorder(self, source, visited=None):
        stack = [source]
        postorder = []
        if not visited:
            visited = set()
        while len(stack):
            key = stack.pop()

            if key not in visited:
                visited.add(key)
                adj = self.adjacent_nodes(key)
                if len(adj):
                    stack.append(key)
                    for a in adj:
                        if a not in visited:
                            stack.append(a)
                else:
                     postorder.append(key)
            else:
                postorder.append(key)
        return (reversed(postorder), visited)

    def topo_sort(self):
        visited = set()
        postorder = []

        def dfs_stack_postorder(source):
            stack = [source]
            while len(stack):
                key = stack.pop()

                if key not in visited:
                    visited.add(key)
                    adj = self.adjacent_nodes(key)
                    if len(adj):
                        stack.append(key)
                        [stack.append(a) for a in adj if a not in visited]
                    else:
                        postorder.append(key)
                else:
                    postorder.append(key)

        for node in self.nodes:
            if node not in visited:
                dfs_stack_postorder(node)
        yield from postorder

    def bfs(self, source):
        queue = [source]
        visited = set()
        while len(queue):
            key = queue.pop(0)
            if key in visited:
                continue

            visited.add(key)
            yield key
            for adj in self.adjacent_nodes(key):
                queue.append(adj)



def load_graph(file):
    g = Graph()
    with open(file) as f:
        for line in f:
            verts = line.strip().split(" ")
            g.add_edge(verts[0], verts[1])
    return g


class TestGraph(unittest.TestCase):
    def test_add_key(self):
        g = Graph()
        g.add_key("A")
        g.add_key("B")
        self.assertEqual(len(g.nodes), 2)

    def test_add_key_noclobber(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_key("A")
        self.assertEqual(g.adjacent_nodes("A"), ["B"])

    def test_add_edge(self):
        g = Graph()
        g.add_edge("A", "B")
        self.assertEqual(g.adjacent_nodes("A"), ["B"])
        self.assertEqual(g.adjacent_nodes("B"), [])

    def test_add_undirected_edge(self):
        g = Graph()
        g.add_undirected_edge("A", "B")
        self.assertEqual(g.adjacent_nodes("A"), ["B"])
        self.assertEqual(g.adjacent_nodes("B"), ["A"])

    def test_bfs(self):
        g = load_graph("medium_dg.txt")
        actual = [x for x in g.bfs("0")]
        expect = ["0", "1", "5", "4", "3", "2"]
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
