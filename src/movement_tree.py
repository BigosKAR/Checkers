class TreeNode:
    def __init__(self, coords, jumped=None, left=None, right=None):
        """
        Each node is going to store two arrays:
        - first one is going to be a list of two element tuples representing coordinates (row, column)
        - second one is going to be a list containing the coordinates (row, column) of pieces you are able to jump over
        """
        self.coords = coords
        self.jumped = jumped if jumped else []
        self.left = left
        self.right = right

    def insert_right(self, coords, jumped):
        self.right = TreeNode(coords=coords, jumped=jumped)

    def insert_left(self, coords, jumped):
        self.left = TreeNode(coords=coords, jumped=jumped)


def fetch_moves_from_tree(node: TreeNode) -> list:
    """
    Transforms a root of the tree to two arrays:
    - move_list: containing ALL possible movements
    - jumped_list: ALL possible coordinates of pieces you can jump over
    Because of how we append the coords and jumped lists, they should be accessed by the same index
    For example:
        You want to access the possible coordinates of the pieces you will jump over if you go to the coordinates moves_list[5].
        Then, you will be able to access all those piece with the same index in jumped_list -> jumped_list[5]
        Each element of the jumped_list is a list
    """
    move_list = []
    jumped_list = []
    """
    One of the algorithms we learned from class. 
    It works like a DFS but it is not searching for anything.
    It visits the nodes in a pre-order way.
    """
    def traverse_move_tree(node: TreeNode) -> None:
        if node is None:
            return
        move_list.append(node.coords)
        jumped_list.append(node.jumped)
        if node.left:
            traverse_move_tree(node.left)
        if node.right:
            traverse_move_tree(node.right)
    traverse_move_tree(node)
    return move_list, jumped_list


class KingTreeNode():
    def __init__(self, coords, jumped=None, left_up=None, right_up=None, left_down=None, right_down=None):
        """
        Each node is going to store two arrays:
        - first one is going to be a list of two element tuples representing coordinates (row, column)
        - second one is going to be a list containing the coordinates (row, column) of pieces you are able to jump over
        """
        self.coords = coords
        self.jumped = jumped if jumped else []
        self.left_up = left_up
        self.right_up = right_up

        self.left_down = left_down
        self.right_down = right_down

    def insert_right_up(self, coords, jumped):
        self.right_up = KingTreeNode(coords=coords, jumped=jumped)

    def insert_right_down(self, coords, jumped):
        self.right_down = KingTreeNode(coords=coords, jumped=jumped)

    def insert_left_up(self, coords, jumped):
        self.left_up = KingTreeNode(coords=coords, jumped=jumped)

    def insert_left_down(self, coords, jumped):
        self.left_down = KingTreeNode(coords=coords, jumped=jumped)

def fetch_moves_from_king_tree(node: KingTreeNode) -> list:
    """
    VERSION FOR KINGS
    Transforms a root of the tree to two arrays:
    - move_list: containing ALL possible movements
    - jumped_list: ALL possible coordinates of pieces you can jump over
    Because of how we append the coords and jumped lists, they should be accessed by the same index
    For example:
        You want to access the possible coordinates of the pieces you will jump over if you go to the coordinates moves_list[5].
        Then, you will be able to access all those piece with the same index in jumped_list -> jumped_list[5]
        Each element of the jumped_list is a list
    """
    move_list = []
    jumped_list = []
    """
    One of the algorithms we learned from class. 
    It works like a DFS but it is not searching for anything.
    It visits the nodes in a pre-order way.
    """
    def traverse_move_tree(node: KingTreeNode) -> None:
        if node is None:
            return
        move_list.append(node.coords)
        jumped_list.append(node.jumped)
        if node.left_up:
            traverse_move_tree(node.left_up)
        if node.left_down:
            traverse_move_tree(node.left_down)
        if node.right_up:
            traverse_move_tree(node.right_up)
        if node.right_down:
            traverse_move_tree(node.right_down)
    traverse_move_tree(node)
    return move_list, jumped_list