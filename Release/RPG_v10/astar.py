class Point:
    """
    stand for a point
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __str__(self):
        return "x:" + str(self.x) + ",y:" + str(self.y)


class AStar:
    """
    AStar in Python3.
    """

    class Node:  # describe node in Astar
        def __init__(self, point, endPoint, g=0):
            self.point = point  # self point position
            self.father = None  # father node
            self.g = g  # g will recalculate when used
            self.h = (abs(endPoint.x - point.x) + abs(endPoint.y - point.y)) * 10  # calculate h

    def __init__(self, map2d, startPoint, endPoint, passTag=0):
        """

        :param map2d: Array2D type array
        :param startPoint: Point where 2d array start
        :param endPoint: Point where 2d array end
        :param passTag: int passable point（while mapdata !=passTag then cannot pass）
        """
        # open list
        self.openList = []
        # close list
        self.closeList = []
        # finding map
        self.map2d = map2d
        # statmap
        if isinstance(startPoint, Point) and isinstance(endPoint, Point):
            self.startPoint = startPoint
            self.endPoint = endPoint
        else:
            self.startPoint = Point(*startPoint)
            self.endPoint = Point(*endPoint)

        # passtag
        self.passTag = passTag

    def getMinNode(self):
        """
        get minimum F variable from open list
        :return: Node
        """
        currentNode = self.openList[0]
        for node in self.openList:
            if node.g + node.h < currentNode.g + currentNode.h:
                currentNode = node
        return currentNode

    def pointInCloseList(self, point):
        for node in self.closeList:
            if node.point == point:
                return True
        return False

    def pointInOpenList(self, point):
        for node in self.openList:
            if node.point == point:
                return node
        return None

    def endPointInCloseList(self):
        for node in self.openList:
            if node.point == self.endPoint:
                return node
        return None

    def searchNear(self, minF, offsetX, offsetY):
        """
        search for nearby node
        :param minF:minimum F
        :param offsetX:offset coordinate
        :param offsetY:
        :return:
        """
        # check offset
        if minF.point.x + offsetX < 0 or minF.point.x + offsetX > self.map2d.w - 1 or minF.point.y + offsetY < 0 or minF.point.y + offsetY > self.map2d.h - 1:
            return
        # if is obstruct then ignore
        if self.map2d[minF.point.x + offsetX][minF.point.y + offsetY] != self.passTag:
            return
        # if in close list，then ignore
        currentPoint = Point(minF.point.x + offsetX, minF.point.y + offsetY)
        if self.pointInCloseList(currentPoint):
            return
        # set unit cost
        if offsetX == 0 or offsetY == 0:
            step = 10
        else:
            step = 14
        # if not in openList，added it in openlist
        currentNode = self.pointInOpenList(currentPoint)
        if not currentNode:
            currentNode = AStar.Node(currentPoint, self.endPoint, g=minF.g + step)
            currentNode.father = minF
            self.openList.append(currentNode)
            return
        # if in openList，if minF to current point G is smaller
        if minF.g + step < currentNode.g:  # if smaller，recalculate g，and change father
            currentNode.g = minF.g + step
            currentNode.father = minF

    def start(self):
        """
        start to find
        :return: None or Point list（path）
        """
        # if end point is obstruct
        if self.map2d[self.endPoint.x][self.endPoint.y] != self.passTag:
            return None

        # 1.put start point in open list
        startNode = AStar.Node(self.startPoint, self.endPoint)
        self.openList.append(startNode)
        # 2.main loop logic
        while True:
            # find minimum F value
            minF = self.getMinNode()
            # put node in closeList，and be able to delete in openList
            self.closeList.append(minF)
            self.openList.remove(minF)
            # search up down left right nodes
            self.searchNear(minF, 0, -1)
            self.searchNear(minF, 0, 1)
            self.searchNear(minF, -1, 0)
            self.searchNear(minF, 1, 0)
            # id ended
            point = self.endPointInCloseList()
            if point:  # if end point in close list then return result
                # print("in closelist")
                cPoint = point
                pathList = []
                while True:
                    if cPoint.father:
                        pathList.append(cPoint.point)
                        cPoint = cPoint.father
                    else:
                        # print(pathList)
                        # print(list(reversed(pathList)))
                        # print(pathList.reverse())
                        return list(reversed(pathList))
            if len(self.openList) == 0:
                return None
