from pathlib import Path
import cv2
import numpy as np
import os
import random


def dis(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


size_of_land = 300
land = np.zeros((size_of_land, size_of_land), np.uint8)
race_field = np.zeros((size_of_land, size_of_land), np.int8)
mask = np.zeros((size_of_land, size_of_land), np.uint8)

rand_edge = ['up', 'down', 'left', 'right']

rand_edge = random.sample(rand_edge, 2)
rand_id = random.sample([0, 1], 2)
start_edge = []
end_edge = []
if rand_edge[rand_id[0]] == 'up':
    start = [0, random.randint(0, size_of_land - 1)]
    start_edge = 'up'
    mask[:, 0] = 1
if rand_edge[rand_id[1]] == 'up':
    end = [0, random.randint(0, size_of_land - 1)]
    end_edge = 'up'
    mask[:, 0] = 1
if rand_edge[rand_id[0]] == 'down':
    start = [size_of_land - 1, random.randint(0, size_of_land - 1)]
    start_edge = 'down'
    mask[:, size_of_land - 1] = 1
if rand_edge[rand_id[1]] == 'down':
    end = [size_of_land - 1, random.randint(0, size_of_land - 1)]
    end_edge = 'down'
    mask[:, size_of_land - 1] = 1
if rand_edge[rand_id[0]] == 'left':
    start = [random.randint(0, size_of_land - 1), 0]
    start_edge = 'left'
    mask[0, :] = 1
if rand_edge[rand_id[1]] == 'left':
    end = [random.randint(0, size_of_land - 1), 0]
    end_edge = 'left'
    mask[0, :] = 1
if rand_edge[rand_id[0]] == 'right':
    start = [random.randint(0, size_of_land - 1), size_of_land - 1]
    start_edge = 'right'
    mask[size_of_land - 1, :] = 1
if rand_edge[rand_id[1]] == 'right':
    end = [random.randint(0, size_of_land - 1), size_of_land - 1]
    end_edge = 'right'
    mask[size_of_land - 1, :] = 1

rand_points = []
number_of_points = 5
for i in range(number_of_points):
    rand_points.append([random.randint(0, size_of_land - 1), random.randint(0, size_of_land - 1)])

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

# short_lines.append([end_point_1, end])
if not end_point_1:
    end_point_1 = start
if not end_point_2:
    end_point_2 = end
short_lines.append([end_point_1, end_point_2])

for i in range(len(short_lines)):
    cv2.line(land, short_lines[i][0], short_lines[i][1], 1, 1)

kernel = np.ones((7, 7), np.uint8)
img_dilation = cv2.dilate(land, kernel, iterations=2)

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

race_field = img_dilation.astype('int8') - 1
race_field[np.where(labeled[1] == start_id)] = 1
race_field[np.where(labeled[1] == end_id)] = 2

cv2.imshow("hello", img_dilation * 250)
cv2.imshow("hello2", race_field * 100)

cv2.waitKey(20000)
