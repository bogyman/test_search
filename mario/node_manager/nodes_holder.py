class NodesHolder:
    """
    Store nodes
    """
    nodes = []

    @classmethod
    def add_node(cls, node_id):
        cls.nodes.append(node_id)

    @classmethod
    def nodes_count(cls):
        return len(cls.nodes)

    @classmethod
    def get_nodes(cls):
        return cls.nodes