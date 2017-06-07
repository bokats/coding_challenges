class Node(object):
    def __init__(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound):
        self.x_lower_bound = x_lower_bound
        self.x_upper_bound = x_upper_bound
        self.y_lower_bound = y_lower_bound
        self.y_upper_bound = y_upper_bound
        self.children = []
        self.current_point = None

    def taken(self):
        if self.current_point:
            return True
        else:
            return False

    def has_children(self):
        if len(self.children) > 0:
            return True
        else:
            return False

class Quadtree(object):
    def __init__(self, root):
        self.root = root

    def insert_coordinates(self, x, y):

        current_node = self.root

        while True:
            if current_node.taken():
                if not current_node.has_children():
                    self.create_children(current_node)
                child = self.find_child(x, y, current_node)
                current_node = current_node.children[child]
            else:
                current_node.current_point = [x,y]
                return current_node

    def create_children(self, parent):
        center_x = parent.x_upper_bound / 2
        center_y = parent.y_upper_bound / 2

        parent.children.append(Node(parent.x_lower_bound, center_x, \
        parent.y_lower_bound, center_y))

        parent.children.append(Node(parent.x_lower_bound, center_x, \
        center_y, parent.y_upper_bound))

        parent.children.append(Node(center_x, parent.x_upper_bound, \
        parent.y_lower_bound, center_y))

        parent.children.append(Node(center_x, parent.x_upper_bound, \
        center_y, parent.y_upper_bound))

    def find_child(self, x, y, parent):
        if x <= parent.x_upper_bound / 2:
            if y <= parent.y_upper_bound / 2:
                return 0
            else:
                return 1
        else:
            if y <= parent.y_upper_bound / 2:
                return 2
            else:
                return 3


# Tests
root = Node(0,100,0,20)
q = Quadtree(root)
assert q.root.x_upper_bound == 100
assert q.root.y_upper_bound == 20

q.insert_coordinates(0,5)
assert q.root.x_upper_bound == 100
assert q.root.taken()
assert q.root.current_point == [0,5]

q.insert_coordinates(0,10)
assert q.root.has_children()
assert q.root.children[0].current_point == [0,10]
assert q.root.children[1].current_point == None

q.insert_coordinates(60, 15)
assert q.root.current_point == [0,5]
# print(q.root.children[3].current_point)
assert q.root.children[3].current_point == [60,15]

q.insert_coordinates(98, 18)
assert q.root.children[3].children[3].current_point == [98,18]
