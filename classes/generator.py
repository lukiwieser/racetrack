from random import Random

import cv2.cv2 as cv2
import numpy as np


class Generator:
    def __init__(self, random_state: int | None):
        """
        Generator for generating random racetracks.

        :param random_state: Used for generating the randomness of the racetrack. Pass an int for reproducible output across multiple function calls
        """
        self.rnd = Random(random_state)

    def generate_racetrack_safely(self, size: int, n_edges: int, kernel_size: int, max_iterations: int = 10) -> np.ndarray:
        """
        Generate a random racetrack. Guarantees that the racetrack will have Start and Finish cells.

        :param size: specifies the size of the whole racetrack in x and y direction (square)
        :param n_edges: number of edges the racetrack should have
        :param kernel_size: basically specifies the size of the track iseven
        :param max_iterations: how many times to try to generate a racetrack, if the generation fails (i.e. there are no start or end cells)
        :return: Returns a 2d numpy array, where each element represents a cell of the racetrack. The first dimension is the row, the second is the colum.
        """
        for i in range(0, max_iterations):
            track = self.generate_racetrack(size, n_edges, kernel_size)
            start_cells = np.where(track == 2)[0]
            end_cells = np.where(track == 3)[0]
            if len(start_cells) > 0 and len(end_cells) > 0:
                return track

        raise RuntimeError("Could not generate a racetrack with start and finish cells. Tried 10 times.")

    def generate_racetrack(self, size: int, n_edges: int, kernel_size: int) -> np.ndarray:
        """
        Generate a random racetrack.

        :param size: specifies the size of the whole racetrack in x and y direction (square)
        :param n_edges: number of edges the racetrack should have
        :param kernel_size: basically specifies the size of the track iseven
        :return: Returns a 2d numpy array, where each element represents a cell of the racetrack. The first dimension is the row, the second is the colum.
        """

        def dis(p1, p2):
            return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        size_of_land = size
        land = np.zeros((size_of_land, size_of_land), np.uint8)
        mask = np.zeros((size_of_land, size_of_land), np.uint8)  # used later to make start-cell to whole start-line

        # randomly determine one start and one end cell
        rand_edge = ['up', 'down', 'left', 'right']
        rand_edge = self.rnd.sample(rand_edge, 2)
        rand_id = self.rnd.sample([0, 1], 2)
        if rand_edge[rand_id[0]] == 'up':
            start = [0, self.rnd.randint(0, size_of_land - 1)]
            mask[:, 0] = 1
        if rand_edge[rand_id[1]] == 'up':
            end = [0, self.rnd.randint(0, size_of_land - 1)]
            mask[:, 0] = 1
        if rand_edge[rand_id[0]] == 'down':
            start = [size_of_land - 1, self.rnd.randint(0, size_of_land - 1)]
            mask[:, size_of_land - 1] = 1
        if rand_edge[rand_id[1]] == 'down':
            end = [size_of_land - 1, self.rnd.randint(0, size_of_land - 1)]
            mask[:, size_of_land - 1] = 1
        if rand_edge[rand_id[0]] == 'left':
            start = [self.rnd.randint(0, size_of_land - 1), 0]
            mask[0, :] = 1
        if rand_edge[rand_id[1]] == 'left':
            end = [self.rnd.randint(0, size_of_land - 1), 0]
            mask[0, :] = 1
        if rand_edge[rand_id[0]] == 'right':
            start = [self.rnd.randint(0, size_of_land - 1), size_of_land - 1]
            mask[size_of_land - 1, :] = 1
        if rand_edge[rand_id[1]] == 'right':
            end = [self.rnd.randint(0, size_of_land - 1), size_of_land - 1]
            mask[size_of_land - 1, :] = 1

        # determine random points
        # these points are used to define the track between the start and finish cells
        rand_points = []
        number_of_points = n_edges - 1
        for i in range(number_of_points):
            rand_points.append([self.rnd.randint(0, size_of_land - 1), self.rnd.randint(0, size_of_land - 1)])

        # find paths to connect the points together (incl start and end)
        tmp_start = start
        tmp_end = end
        id_min_dis = []
        short_lines = []
        end_point_1 = []
        end_point_2 = []
        for j in range(number_of_points):  # number of edge
            min_dis = np.sqrt(size_of_land ** 2 * 2) + 10
            if_start = True  # or end = false
            for i in range(len(rand_points)):  # number of short lines
                # find nearest point to the previous poit, begin with start
                dis_to_tmp_start = dis(tmp_start, rand_points[i])
                dis_to_tmp_end = dis(tmp_end, rand_points[i])

                if dis_to_tmp_start < dis_to_tmp_end and dis_to_tmp_start < min_dis:
                    if_start = True
                    min_dis = dis_to_tmp_start
                    id_min_dis = i
                else:
                    if dis_to_tmp_end < min_dis:
                        if_start = False
                        min_dis = dis_to_tmp_end
                        id_min_dis = i

            if if_start:
                short_lines.append([tmp_start, rand_points[id_min_dis]])
                tmp_start = rand_points[id_min_dis]
                end_point_1 = rand_points[id_min_dis]
            else:
                short_lines.append([tmp_end, rand_points[id_min_dis]])
                tmp_end = rand_points[id_min_dis]
                end_point_2 = rand_points[id_min_dis]
            rand_points.pop(id_min_dis)

        # it may happen, that after finding the lines the start and end are not at the ends of the whole track
        # thus we set a new start/end if necessary
        if not end_point_1:
            end_point_1 = start
        if not end_point_2:
            end_point_2 = end
        short_lines.append([end_point_1, end_point_2])

        # "draw" the lines
        for i in range(len(short_lines)):
            cv2.line(land, short_lines[i][0], short_lines[i][1], 1, 1)

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        img_dilation = cv2.dilate(land, kernel, iterations=2)

        # make start and end cell to a start-line adn finish-line
        mask = mask * img_dilation
        labeled = cv2.connectedComponents(mask)
        start_id = []
        end_id = []
        for i in range(1, labeled[0]):
            indexes = np.where(labeled[1] == i)
            for j in range(len(indexes[0])):
                if indexes[0][j] == start[1] and indexes[1][j] == start[0]:
                    start_id = i
                if indexes[0][j] == end[1] and indexes[1][j] == end[0]:
                    end_id = i

        race_field = img_dilation.astype('int8')
        race_field[np.where(labeled[1] == start_id)] = 2
        race_field[np.where(labeled[1] == end_id)] = 3

        return race_field.astype(np.float64)
