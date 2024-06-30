class SuffixTreeNode:
    def __init__(self):
        self.edges = {}
        self.suffix_link = None


class SuffixTree:
    def __init__(self, sequence):
        self.sequence = sequence[:]
        if len(sequence) > 0:
            self.sequence.append("$")
        self.n = len(self.sequence)
        self.root = SuffixTreeNode()
        self.remainder = 1
        self.active_point = {
            "active_node": self.root,
            "active_edge": None,
            "active_length": 0
        }
        self.current_end = 0
        self.build_tree()

    def build_tree(self):
        for i in range(self.n):
            self.current_end = i + 1
            self.update_edges(self.root, self.current_end)
            last_new_node = None

            while self.remainder > 0:
                if self.active_point["active_length"] == 0:
                    if self.sequence[i] in self.root.edges:
                        self.active_point["active_edge"] = self.sequence[i]
                        self.active_point["active_length"] += 1
                        break
                    else:
                        self.root.edges[self.sequence[i]] = (i, self.current_end)
                        self.remainder -= 1
                else:
                    if self.active_point["active_edge"] in self.active_point["active_node"].edges:
                        edge_info = self.active_point["active_node"].edges[self.active_point["active_edge"]]
                        edge_start = edge_info[0]
                        edge_length = edge_info[1] - edge_start

                        if self.sequence[edge_start + self.active_point["active_length"]] == self.sequence[i]:
                            self.active_point["active_length"] += 1

                            if self.active_point["active_length"] == edge_length:
                                self.active_point["active_node"] = edge_info[2] if len(edge_info) > 2 else self.root
                                self.active_point["active_edge"] = None
                                self.active_point["active_length"] = 0

                            break
                        else:
                            split_node = SuffixTreeNode()
                            edge_info = self.active_point["active_node"].edges[self.active_point["active_edge"]]
                            edge_start, edge_end = edge_info[0], edge_info[1]
                            split_pos = edge_start + self.active_point["active_length"]

                            split_node.edges[self.sequence[split_pos]] = (split_pos, edge_end)
                            split_node.edges[self.sequence[i]] = (i, self.current_end)

                            self.active_point["active_node"].edges[self.active_point["active_edge"]] = (
                                edge_start, split_pos, split_node)

                            if last_new_node is not None:
                                last_new_node.suffix_link = split_node

                            last_new_node = split_node
                            self.remainder -= 1

                            if self.active_point["active_node"] == self.root and self.active_point["active_length"] > 0:
                                self.active_point["active_length"] -= 1
                                self.active_point["active_edge"] = self.sequence[i - self.remainder + 1]
                            elif self.active_point["active_node"] != self.root:
                                if self.active_point["active_node"].suffix_link is not None:
                                    self.active_point["active_node"] = self.active_point["active_node"].suffix_link
                                else:
                                    self.active_point["active_node"] = self.root
                    else:
                        if self.active_point["active_node"] == self.root:
                            self.active_point["active_length"] -= 1
                            self.active_point["active_edge"] = self.sequence[i - self.remainder + 1]
                        elif self.active_point["active_node"] != self.root:
                            if self.active_point["active_node"].suffix_link is not None:
                                self.active_point["active_node"] = self.active_point["active_node"].suffix_link
                            else:
                                self.active_point["active_node"] = self.root

            self.remainder += 1

    def update_edges(self, node, current_end):
        for char, edge_info in list(node.edges.items()):
            if len(edge_info) == 2:
                node.edges[char] = (edge_info[0], current_end)
            else:
                edge_start, edge_end, child_node = edge_info
                if edge_end > current_end:
                    new_child_node = SuffixTreeNode()
                    node.edges[char] = (edge_start, current_end, new_child_node)
                    new_child_node.edges[self.sequence[current_end]] = (current_end, edge_end, child_node)
                    self.update_edges(new_child_node, current_end)
                else:
                    self.update_edges(child_node, current_end)

    def print_tree(self):
        self.print_node(self.root, 0)
        print()
        print(f"Remainder: {self.remainder}")
        print(f"Active node: {self.active_point['active_node']}")
        print(f"Active edge: {self.active_point['active_edge']}")
        print(f"Active length: {self.active_point['active_length']}\n")

    def print_node(self, node, depth):
        for char, edge_info in node.edges.items():
            if len(edge_info) == 2:
                print("  " * depth + f"{char}: [{edge_info[0]}, {edge_info[1]})")
            else:
                print("  " * depth + f"{char}: [{edge_info[0]}, {edge_info[1]})")
                self.print_node(edge_info[2], depth + 1)

    def print_suffixes(self):
        self._print_suffixes(self.root, "")

    def _print_suffixes(self, node, prefix):
        for char, edge_info in node.edges.items():
            if len(edge_info) == 2:
                suffix = prefix + ''.join(c for c in self.sequence[edge_info[0]:edge_info[1]])
                print(suffix[:-1])
            else:
                suffix_prefix = prefix + ''.join(c for c in self.sequence[edge_info[0]:edge_info[1]])
                self._print_suffixes(edge_info[2], suffix_prefix)

    def find_longest_repeating_substring(self):
        self.max_depth = 0
        self.max_string = []
        self._find_longest_repeating_substring(self.root, [])
        return self.max_string

    def _find_longest_repeating_substring(self, node, prefix):
        if len(node.edges) > 1:
            valid = True
            for char in prefix:
                if char == "$" or char[0] == "$":
                    valid = False
                    break
            if valid and len(prefix) > self.max_depth:
                self.max_depth = len(prefix)
                self.max_string = prefix[:]

        for char, edge_info in node.edges.items():
            if len(edge_info) == 3:
                new_prefix = prefix + self.sequence[edge_info[0]:edge_info[1]]
                self._find_longest_repeating_substring(edge_info[2], new_prefix)