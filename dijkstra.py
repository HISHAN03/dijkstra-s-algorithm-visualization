import heapq

class Dijkstra:
    def __init__(self, grid):
        self.grid = grid
        self.priority_queue = []
        self.came_from = {}
        self.distances = {}
        self.current_distance = 0
        self.current_node = None

    def init(self, start_point):
        self.distances = { (i, j): float('inf') for i in range(self.grid.size[0]) for j in range(self.grid.size[1]) }
        self.distances[start_point] = 0
        self.priority_queue = [(0, start_point)]
        self.came_from = {}
        self.current_distance = 0
        self.current_node = None

    def step(self):
        if self.priority_queue:
            self.current_distance, self.current_node = heapq.heappop(self.priority_queue)
            if self.current_node in self.grid.visited:
                return False
            self.grid.visited.append(self.current_node)
            if self.current_node == self.grid.goal_point:
                self.grid.path = self.reconstruct_path(self.grid.start_point, self.grid.goal_point)
                return True
            neighbors = self.get_neighbors(self.current_node, self.grid.size[0], self.grid.size[1])
            for neighbor in neighbors:
                if neighbor in self.grid.visited:
                    continue
                distance = self.current_distance + 1  # Adjust this to reflect the actual distance if necessary
                if distance < self.distances[neighbor]:
                    self.distances[neighbor] = distance
                    heapq.heappush(self.priority_queue, (distance, neighbor))
                    self.came_from[neighbor] = self.current_node
            return False
        else:
            self.grid.path = self.reconstruct_path(self.grid.start_point, self.grid.goal_point)
            return True

    def get_neighbors(self, node, rows, cols):
        x, y = node
        neighbors = []
        if x > 0: neighbors.append((x - 1, y))
        if x < rows - 1: neighbors.append((x + 1, y))
        if y > 0: neighbors.append((x, y - 1))
        if y < cols - 1: neighbors.append((x, y + 1))
        # Add diagonal neighbors
        if x > 0 and y > 0: neighbors.append((x - 1, y - 1))
        if x > 0 and y < cols - 1: neighbors.append((x - 1, y + 1))
        if x < rows - 1 and y > 0: neighbors.append((x + 1, y - 1))
        if x < rows - 1 and y < cols - 1: neighbors.append((x + 1, y + 1))
        return neighbors

    def reconstruct_path(self, start, goal):
        current = goal
        path = []
        while current != start:
            if current not in self.came_from:
                return []  # No path found
            path.append(current)
            current = self.came_from[current]
        path.append(start)
        path.reverse()
        return path
