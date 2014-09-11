class TreeNode(object):
    """docstring for TreeNode"""

    def __init__(self, left, right, f, val, level):
        super(TreeNode, self).__init__()
        self.left = left
        self.right = right
        self.feature = f
        self.val = val
        self.level = level

    def __str__(self):
        return "|" + "----" * self.level + "[level: " + str(self.level) + " feature: " + str(
            self.feature) + ", value: " + str(self.val) + " ]"