from ks.models import ECell, EDirection, Agent
from covid.square import Square

class Covid_404():
    def __init__(self):
        self.curr_square_index = 0
        self.prev_square_index = 0
        self.reaching_path_index = 0
        self.next_square_index = 0
        self.team_name = 'Blue'
        self.reaching_path = []
        self.squares = []
        self.board = []
        
    def set_requirements(self, agent = None, board = None, team_name = None):
        self.agent = agent
        self.board = board
        self.team_name = team_name
        
    def make_squares(self):
        pos_y = pos_x = 1
        while pos_y < len(self.board) - 1:
            pos_y_steps = [0, 0, 1, 1]
            pos_x_steps = [0, 1, 1, 0]
            all_positions = []
            for k in range(4):
                i = pos_y + pos_y_steps[k]
                j = pos_x + pos_x_steps[k]
                if self.board[i][j] == ECell.AreaWall:
                    continue
                
                all_positions.append([i, j])
            
            squares_pos = []
            if len(all_positions) == 4:
                squares_pos.append([all_positions[0], all_positions[2]])
            else:
                for position in all_positions:
                    squares_pos.append([position, position])

            for square_pos in squares_pos:
                square = Square()
                first_pos, second_pos = square_pos[0], square_pos[1]
                square.position = (first_pos, second_pos)
                self.squares.append(square)
                
            pos_x += 2
            if pos_x > len(self.board[0]) - 1:
                pos_x = 1
                pos_y += 2
    
        agent_pos = [self.agent.position.y, self.agent.position.x]
        self.curr_square_index = self.find_square_index(agent_pos[0], agent_pos[1])
        self.prev_square_index = self.curr_square_index
        
    def find_near_squares(self):
        for k in range(len(self.squares)):
            square_pos = self.squares[k].position
            sides_num = square_pos[1][0] - square_pos[0][0] + 1
            near_squares = []
            n = 0
            i_steps = [-1, n, sides_num, n]
            j_steps = [n, sides_num, n, -1]
            for m in range(sides_num):
                for l in range(4):
                    i = square_pos[0][0] + i_steps[l]
                    j = square_pos[0][1] + j_steps[l]
                    
                    if self.board[i][j] == ECell.AreaWall:
                        continue
                    
                    square_index = self.find_square_index(i, j)
                    square_count = near_squares.count(square_index)
                    if square_count == 0:
                        near_squares.append(square_index)

                n += 1
                i_steps = [-1, n, sides_num, n]
                j_steps = [n, sides_num, n, -1]
            
            self.squares[k].near_squares = near_squares.copy()
                
    def set_entry_positions(self):
        for i in range(len(self.squares)):
            for j in range(len(self.squares[i].near_squares)):
                near_square = self.squares[i].near_squares[j]
                self.squares[i].near_squares_entry_pos[near_square] = []
        
        for k in range(len(self.squares)):
            square_pos = self.squares[k].position
            sides_num = square_pos[1][0] - square_pos[0][0] + 1
            n = 0
            i_steps = [-1, n, sides_num, n]
            j_steps = [n, sides_num, n, -1]
            
            for m in range(sides_num):
                for l in range(4):
                    i = square_pos[0][0] + i_steps[l]
                    j = square_pos[0][1] + j_steps[l]
                    if self.board[i][j] == ECell.AreaWall:
                        continue
                    
                    near_square_index = self.find_square_index(i, j)
                    near_entries = self.squares[k].near_squares_entry_pos[near_square_index]
                    reached_count = near_entries.count([i, j])
                    if reached_count == 0:
                        near_square_pos = self.squares[near_square_index].position
                        if (near_square_pos[0][0] <= i and i <= near_square_pos[1][0]) and (near_square_pos[0][1] <= j and j <= near_square_pos[1][1]):
                            self.squares[k].near_squares_entry_pos[near_square_index].append([i, j])
                        
                n += 1
                i_steps = [-1, n, sides_num, n]
                j_steps = [n, sides_num, n, -1]

    
    def find_square_index(self, pos_y, pos_x):
        for square in self.squares:
            square_pos_1 = square.position[0]
            square_pos_2 = square.position[1]
            if (square_pos_1[0] <= pos_y and pos_y <= square_pos_2[0]) and (square_pos_1[1] <= pos_x and pos_x <= square_pos_2[1]):
                index = self.squares.index(square)
                return index
            
    def find_all_routes(self, start_pos, dest_pos):
        all_routes = []
        square_pos = self.squares[self.curr_square_index].position
        vertices = {}
        for i in range(square_pos[0][0], square_pos[1][0] + 1):
            for j in range(square_pos[0][1], square_pos[1][1] + 1):
                vertices[(i, j)] = []
        
        i, j = start_pos[0], start_pos[1]
        stack = [[i, j]] 
        route = [[i, j]]
        loop = True
        while loop:
            row_steps = [-1, 1, 0, 0]
            column_steps = [0, 0, 1, -1]
            current_vertex = stack.pop()
            i, j = current_vertex[0], current_vertex[1]
            k = 0
            while k < 4:
                ii = i + row_steps[k]
                jj = j + column_steps[k]
                k += 1
                if ii > square_pos[1][0] or ii < square_pos[0][0] or jj > square_pos[1][1] or jj < square_pos[0][1]:
                    if ii != dest_pos[0] or jj != dest_pos[1]:
                        continue
                
                count_pos = route.count([ii, jj])
                if count_pos == 0:
                    reached_neighbors = vertices[(i, j)].copy()
                    count_neighbor = reached_neighbors.count([ii, jj])
                    if count_neighbor == 0:
                        vertices[(i, j)].append([ii, jj])
                        if ii == dest_pos[0] and jj == dest_pos[1]:
                            route_copy = route.copy()
                            route_copy.append([ii, jj])
                            all_routes.append(route_copy)
                        else:
                            stack.append([i, j])
                            route.append([ii, jj])
                            i, j = ii, jj
                            k = 0
                    
            vertices[(i, j)].clear()
            route.pop(-1)
            
            if len(stack) == 0:
                loop = False
                
        return all_routes
    
    def find_route_weight(self, route):
        if self.team_name == 'Blue':
            my_wall = ECell.BlueWall
        else:
            my_wall = ECell.YellowWall
        
        my_walls = enemy_walls = empty_walls = 0
        for position in route[1:]:
            i, j = position[0], position[1]
            if self.board[i][j] == my_wall:
                my_walls += 1
            elif self.board[i][j] == ECell.Empty:
                empty_walls += 1
            else:
                enemy_walls += 1
        
        weight = (empty_walls * 10) + (my_walls * -20) + (enemy_walls * 1)
        return weight
    
    def is_route_reachable(self, route):
        for position in route[1:]:
            i, j = position[0], position[1]
            reached_walls = 0
            if self.board[i][j] == ECell.YellowWall or self.board[i][j] == ECell.BlueWall:
                reached_walls += 1
            
            if reached_walls <= self.agent.wall_breaker_rem_time:
                    return True
            else:
                if reached_walls < self.agent.health:
                    return True
                else:
                    return False
    
    def find_best_route(self):
        choosed_routes = []
        entry_positions = self.squares[self.curr_square_index].near_squares_entry_pos[self.next_square_index]
        agent_pos = [self.agent.position.y, self.agent.position.x]
        for entry_pos in entry_positions:
            all_routes = self.find_all_routes(agent_pos, entry_pos)
            
            # reachable_routes = []
            # for route in all_routes:
            #     is_reachable = self.is_route_reachable(route)
            #     if is_reachable == True:
            #         reachable_routes.append(route)
            
            # routes_weights = []
            # for route in reachable_routes:
            #     weight = self.find_route_weight(route)
            #     routes_weights.append(weight)
            
            # average = sum(routes_weights) // len(routes_weights)
            
            # min_weight, max_weight = 1000, -1000
            # for weight in routes_weights:
            #     if weight > max_weight:
            #         max_weight = weight
            #     if weight < min_weight:
            #         min_weight = weight
            
            # average = (min_weight + max_weight) // 2
            # if average < 0:
            #     average *= -1
                
            # index, min_diff = 0, 1000
            # for weight in routes_weights:
            #     diff = weight - average
            #     if diff < 0:
            #         diff *= -1
            #     if diff < min_diff:
            #         index = routes_weights.index(weight)
            #         min_diff = diff
                    
            # choosed_routes.append(reachable_routes[index])
            for route in all_routes:
                choosed_routes.append(route)
        
        routes_weights = []
        for route in choosed_routes:
            route_weight = self.find_route_weight(route)
            routes_weights.append(route_weight)
        
        min_weight = min(routes_weights)
        max_weight = max(routes_weights)
        
        average = (min_weight + max_weight) // 2
        average *= -1 if average < 0 else 1
        
        weight_diffs = []            
        for weight in routes_weights:
            diff = weight - average
            if diff < 0:
                diff *= -1
            weight_diffs.append(diff)
        
        min_diff = min(weight_diffs)
        index = weight_diffs.index(min_diff)
        
        best_route = choosed_routes[index]   
        return best_route
    
    def update_curr_square_index(self):
        near_square_indexes = self.squares[self.curr_square_index].near_squares
        agent_pos = [self.agent.position.y, self.agent.position.x]
        i, j = agent_pos[0], agent_pos[1]
        for near_index in near_square_indexes:
            near_square_pos = self.squares[near_index].position
            if (near_square_pos[0][0] <= i and i <= near_square_pos[1][0]) and (near_square_pos[0][1] <= j and j <= near_square_pos[1][1]):
                self.prev_square_index = self.curr_square_index
                self.curr_square_index = near_index
                break

    def is_new_square(self):
        curr_square_pos = self.squares[self.curr_square_index].position
        pos1, pos2 = curr_square_pos[0], curr_square_pos[1]
        agent_pos = [self.agent.position.y, self.agent.position.x]
        if pos1[0] > agent_pos[0] or pos2[0] < agent_pos[0] or pos1[1] > agent_pos[1] or pos2[1] < agent_pos[1]:
            return True
        else:
            return False
    
    def find_next_square_index(self):
        if self.team_name == 'Blue':
            my_wall = ECell.BlueWall
        else:
            my_wall = ECell.YellowWall
            
        near_squares = self.squares[self.curr_square_index].near_squares
        near_squares_weight = []
        
        for near_index in near_squares:
            near_square_pos = self.squares[near_index].position
            my_walls = enemy_walls = empty_walls = 0
            for i in range(near_square_pos[0][0], near_square_pos[1][0] + 1):
                for j in range(near_square_pos[0][1], near_square_pos[1][1] + 1):
                    if self.board[i][j] == my_wall:
                        my_walls += 1
                    elif self.board[i][j] == ECell.Empty:
                        empty_walls += 1
                    else:
                        enemy_walls += 1
            
            weight = (empty_walls * 10) + (my_walls * -20) + (enemy_walls * 1)
            near_squares_weight.append(weight)
        
        curr_square_pos = self.squares[self.curr_square_index].position
        
        # find top and bottom squares and choose the most weighted square between them
        vertical_weight, vertical_index = -1000, 0
        for i in range(len(near_squares)):
            near_index = near_squares[i]
            pos1_i, pos2_i = curr_square_pos[0][0], curr_square_pos[1][0]
            for j in range(2):
                if j == 0:
                    new_row = pos1_i - 1
                else:
                    new_row = pos2_i + 1
                    
                near_square_pos = self.squares[near_index].position
                near_pos1_i, near_pos2_i = near_square_pos[0][0], near_square_pos[1][0]
                if near_pos1_i <= new_row and new_row <= near_pos2_i:
                    weight = near_squares_weight[i]
                    if weight > vertical_weight and near_index != self.prev_square_index:
                        vertical_weight = weight
                        vertical_index = near_index
                    break
        
        # find left and right squares weight and index
        left_weight, left_index = -1000, 0
        right_weight, right_index = -1000, 0
        for i in range(len(near_squares)):
            near_index = near_squares[i]
            pos1_j, pos2_j = curr_square_pos[0][1], curr_square_pos[1][1]
            for j in range(2):
                if j == 0:
                    new_column = pos1_j - 1
                else:
                    new_column = pos2_j + 1
                
                near_square_pos = self.squares[near_index].position
                near_pos1_j, near_pos2_j = near_square_pos[0][1], near_square_pos[1][1]
                if near_pos1_j <= new_column and new_column <= near_pos2_j:
                    weight = near_squares_weight[i]
                    if new_column == (pos1_j - 1):
                        left_weight = weight
                        left_index = near_index
                    else:
                        right_weight = weight
                        right_index = near_index
                    break
        
        horizontal_weight, horizontal_index = -1000, 0
        if left_weight > right_weight and left_index != self.prev_square_index:
            horizontal_index = left_index
            horizontal_weight = left_weight
        elif left_weight < right_weight and right_index != self.prev_square_index:
            horizontal_index = right_index
            horizontal_weight = right_weight
        else:
            if self.team_name == "Blue" and right_index != self.prev_square_index:
                horizontal_index = right_index
                horizontal_weight = right_weight
            elif self.team_name == "Yellow" and left_index != self.prev_square_index:
                horizontal_index = left_index
                horizontal_weight = left_weight

        if horizontal_weight > vertical_weight:
            return horizontal_index
        else:
            return vertical_index
        
    def find_next_square(self):
        self.next_square_index = self.find_next_square_index()
    
    def find_new_reaching_path(self):
        self.reaching_path = self.find_best_route()
        self.reaching_path_index = 1
    
    def is_next_square_changed(self):
        square_index = self.find_next_square_index()
        if square_index != self.next_square_index:
            return True
        else:
            return False
        
    def is_wallbreaker_needed(self):
        size = len(self.reaching_path)
        if self.reaching_path_index != (size - 1):
            i, j = self.reaching_path[self.reaching_path_index + 1][0], self.reaching_path[self.reaching_path_index + 1][1]
        else:
            i, j = self.reaching_path[self.reaching_path_index][0], self.reaching_path[self.reaching_path_index][1]
            
        if self.board[i][j] != ECell.Empty:
            return True
        else:
            return False
        
    def say_welcome(self):
        welcome_banner = [
            ['\n'],
            ['''
                                                    ·▪      ▄▄ 
             ▄▄·        ▌ ▐·▪  ·▄▄▄▄        ▪█▀   █ ▀████▪· █    █
            ▐█ ▌▪▪     ▪█·█▌██ ██▪ ██        ██ ·▪█  ██  █▌ ██ ·▪█
            ██ ▄▄ ▄█▀▄ ▐█▐█•▐█·▐█· ▐█▌·▪███▀  █████  ██  ██  █████
            ▐███▌▐█▌.▐▌ ███ ▐█▌██. ██            ██  ██· ██·    ██
            ·▀▀▀  ▀█▄▀▪. ▀  ▀▀▀▀▀▀▀▀•         ·▪▐██▀· ████▌· ·▪▐██▀▪▪
            '''],
            ['\n']
        ]
        for line in welcome_banner:
            print(line[0])
            
    def next_dir(self):
        agent_pos = [self.agent.position.y, self.agent.position.x]
        next_dir = EDirection.Right
        index = self.reaching_path_index
        
        if agent_pos[0] == self.reaching_path[index][0]:
            if self.reaching_path[index][1] - agent_pos[1] == 1:
                next_dir = EDirection.Right
            else:
                next_dir = EDirection.Left
        else:
            if self.reaching_path[index][0] - agent_pos[0] == 1:
                next_dir = EDirection.Down
            else:
                next_dir = EDirection.Up
        self.reaching_path_index += 1
        return next_dir