class TreeNode:
    def __init__(self, coords, left=None, right=None, jumped=None):
        self.coords = coords # value is going to be a tuple of row and column where a piece can go
        self.jumped = jumped if jumped else []
        self.left = left
        self.right = right

    def insert_right(self, coords, jumped):
        self.right = TreeNode(coords=coords, jumped=jumped)

    def insert_left(self, coords, jumped):
        self.left = TreeNode(coords=coords, jumped=jumped)


def fetch_moves_from_tree(node: TreeNode) -> list:
    move_list = []
    jumped_list = []
    def traverse_move_tree(node: TreeNode) -> None:
        if node is None:
            return
        if node.coords not in move_list:
            move_list.append(node.coords)
            jumped_list.append(node.jumped)
        if node.left:
            traverse_move_tree(node.left)
        if node.right:
            traverse_move_tree(node.right)
    traverse_move_tree(node)
    return move_list, jumped_list

    