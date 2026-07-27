import numpy as np
from collections import deque

#region XSet

(Neutral, Midair, Acc, Walk, Run) = range(0, 5)
(Stand, FrontDuck, BackDuck) = range(51, 54)
(Normal, Star, Ice, Water, Wind, LowG) = range(100, 700, 100)

AccsX = {\

Normal: {\
	Neutral: [0.00, 0.00, 0.00, 0.00],\
	Midair: [0.08, 0.03, 0.03, 0.03],\
	Acc: [0.08, 0.06, 0.029, 0.021],\
	Walk: [0.10, 0.03, 0.03, 0.03],\
	Run: [0.10, 0.06, 0.029, 0.035],\
	Stand: [0.05, 0.05, 0.035, 0.035],\
	FrontDuck: [0.06, 0.06, 0.05, 0.05],\
	BackDuck: [0.07, 0.07, 0.07, 0.07]\
},\

Star: {\
	Neutral: [0.00, 0.00, 0.00, 0.00],\
    Midair: [0.11, 0.04, 0.04, 0.04],\
    Acc: [0.11, 0.78, 0.039, 0.039],\
    Walk: [0.13, 0.04, 0.04, 0.04],\
    Run: [0.13, 0.078, 0.039, 0.039],\
    Stand: [0.05, 0.05, 0.035, 0.035],\
    FrontDuck: [0.06, 0.06, 0.05, 0.05],\
    BackDuck: [0.07, 0.07, 0.07, 0.07]\
},\

Ice: {\
	Neutral: [0.00, 0.00, 0.00, 0.00],\
    Midair: [0.08, 0.03, 0.03, 0.03],\
    Acc: [0.08, 0.06, 0.029, 0.021],
    Walk: [0.02, 0.04, 0.04, 0.04],
    Run: [0.02, 0.06, 0.028, 0.013],
    Stand: [0.015, 0.015, 0.013, 0.013],
    FrontDuck: [0.18, 0.18, 0.015, 0.015],
    BackDuck: [0.018, 0.018, 0.018, 0.018]\
},\

Water: {\
	Neutral: [0.025, 0.025, 0.025, 0.025],\
    Midair: [0.025, 0.025, 0.025, 0.025],\
    Acc: [0.025, 0.025, 0.025, 0.025],\
    Walk: [0.025, 0.025, 0.025, 0.025],\
    Run: [0.025, 0.025, 0.025, 0.025],\
    Stand: [0.04, 0.04, 0.04, 0.04],\
    FrontDuck: [0.04, 0.04, 0.04, 0.04],\
    BackDuck: [0.04, 0.04, 0.04, 0.04]\
},\

LowG: {\
	Neutral: [0.00, 0.00, 0.00, 0.00],\
	Midair: [0.08, 0.03, 0.03, 0.03],\
	Acc: [0.08, 0.06, 0.029, 0.021],\
	Walk: [0.10, 0.03, 0.03, 0.03],\
	Run: [0.10, 0.06, 0.029, 0.035],\
	Stand: [0.05, 0.05, 0.035, 0.035],\
	FrontDuck: [0.06, 0.06, 0.05, 0.05],\
	BackDuck: [0.07, 0.07, 0.07, 0.07]\
},\

Wind: {\
	Neutral: [0.00, 0.00, 0.00, 0.00],\
	Midair: [0.08, 0.03, 0.03, 0.03],\
	Acc: [0.08, 0.06, 0.029, 0.021],\
	Walk: [0.10, 0.03, 0.03, 0.03],\
	Run: [0.10, 0.06, 0.029, 0.035],\
	Stand: [0.05, 0.05, 0.035, 0.035],\
	FrontDuck: [0.06, 0.06, 0.05, 0.05],\
	BackDuck: [0.07, 0.07, 0.07, 0.07]\
},\
}


Borders_x = {\
	Normal: [0.5, 1.5, 2.25, 3],\
	Star: [0.5, 2, 4, 4],\
	Ice: [0.5, 1.5, 2.25, 3],\
	Water: [0, 0, 0, 0],\
	LowG: [0.5, 1.5, 2.25, 3],\
	Wind: [0.5, 1.5, 2.25, 3],\
}

max_speed_x = {\
	Normal: {\
		0: 3, 1: 1.5\
	},
	Star: {\
		0: 4, 1: 2\
	},
	Ice: {\
		0: 3, 1: 1.5\
	},
	Water: {\
		0: 0.5625, 1: 1.125\
	},
	LowG: {\
		0: 1.5, 1: 1.5\
	},
	Wind: {\
		0: 3, 1: 1.5\
	},
}

Reverse_Acc = {\
	Normal: {0: [0.09, 0.09, 0.09, 0.09], 1: [0.1, 0.1, 0.1, 0.1]},\
	Star: {0: [0.12, 0.12, 0.12, 0.12], 1: [0.1, 0.1, 0.1, 0.1]},\
	Ice: {0: [0.09, 0.09, 0.09, 0.09], 1: [0.02, 0.02, 0.02, 0.02]},\
	Water: {0: [0.03, 0.03, 0.03, 0.03], 1: [0.05, 0.05, 0.05, 0.05]},\
	LowG: {0: [0.09, 0.09, 0.09, 0.09], 1: [0.1, 0.1, 0.1, 0.1]},\
	Wind: {0: [0.09, 0.09, 0.09, 0.09], 1: [0.1, 0.1, 0.1, 0.1]},\
}

Scenes = {\
	'Star': Star, 'Ice': Ice, 'Water': Water, 'Wind': Wind, 'LowG': LowG\
}


#endregion

#region YSet

AccsY = {\
	Normal: ([-0.06, -0.25, -0.34, -0.08, -0.31, -0.34],\
		   [-0.34, -0.34, -0.34, -0.25, -0.34, -0.34]),\
	LowG: ([-0.012, -0.05, -0.068, -0.016, -0.062, -0.062],\
		   [-0.068, -0.068, -0.068, -0.05, -0.068, -0.068]),\
	Water: ([-0.043, -0.027, -0.027, -0.027, -0.027, -0.027],\
		   [-0.043, -0.027, -0.027, -0.027, -0.027, -0.027])
}

SpeedY = {\
	Normal: ([3.568, 3.748, 3.808, 3.868],\
          [3.288, 3.468, 3.528, 3.588]),\
	LowG: ([2.5276, 2.6536, 2.688, 2.688],\
          [2.4716, 2.5976, 2.632, 2.632]),\
	Water: ([1.25, 1.25, 1.25, 1.25],\
		  [1.25, 1.25, 1.25, 1.25])
}

max_speed_y = {\
	Normal: -4,\
	LowG: -2,\
	Water: -1.5
}

Borders_y = {
	Normal: [-3, -0.15, 0.3, 1.5, 2.5],
	LowG: [-3, -0.15, 0.3, 1.5, 2.5],
	Water: [0, 0, 0, 0, 0],
}

#endregion

def tof(value):
	return np.float32(value)

def Calculate_x(pos_x, speed, inputs, scene):
	pos_x = tof(pos_x)
	speed = tof(speed)
	scene = Scenes.get(scene, Normal)
	border = Borders_x[scene]
	spd_x_his = [speed]
	pos_x_his = [pos_x]
	for i in range(0, len(inputs), 2):
		input,  direction, frame = inputs[i][0], inputs[i][1], inputs[i+1]
		for _ in range(frame):
			
			if input is not None:
				type = input % 100
				slow = (type == 1 or type == 3) if scene != Water else (type == 1 or type == 2)
				groundmove = type == 3 or type == 4
				maximum = max_speed_x[scene][slow]
			
				a = AccsX[scene].get(type, None)
				if a is not None:
					if speed * direction < 0 and type % 50 != 0:
						a = Reverse_Acc[scene][groundmove]
		
					s = abs(speed)
					if s <= border[0]:
						zone = 0
					elif s <= border[1]:
						zone = 1
					elif s <= border[2]:
						zone = 2
					else:
						zone = 3
			
					if not direction:
						dif = float(abs(speed)) - a[zone]
						dif_32 = tof(max(0.0, dif))
						speed = tof(dif_32 if speed > 0 else -dif_32)
					else:
						speed = tof(float(speed) + a[zone] * float(direction))
					if abs(speed) > maximum and speed * direction > 0:
						speed = tof(maximum) if speed > 0 else np.float32(-maximum)
			speed = tof(float(speed))
			spd_x_his.append(speed)
			pos_x = tof(float(pos_x) + float(speed) + 1) if scene == Wind else tof(float(pos_x + float(speed)))
			pos_x_his.append(pos_x)
	return pos_x_his, spd_x_his

def Calculate_y(pos_y, speed_x_his, speed_y, inputs, scene):
	pos_y = tof(pos_y)
	speed_y = tof(speed_y)
	Jumping = False
	JumpWhileFall = False
	scene = Scenes.get(scene, Normal)
	spd_y_his = [speed_y]
	pos_y_his = [pos_y]
	maximum = max_speed_y.get(scene, max_speed_y[Normal])
	border = Borders_y.get(scene, Borders_y[Normal])
	t = -1
	for i in range(0, len(inputs), 2):
		input, frame = inputs[i][0], inputs[i+1]
		for j in range(frame):
			t += 1
			if input is not None:
				ifJump = input // 100 == 1
				GroundCom = 3 <= input <= 100
				if GroundCom:
					speed_y = tof(0)
					Jumping = False
					spd_y_his.append(speed_y)
					pos_y = tof(float(pos_y) + float(speed_y))
					pos_y_his.append(pos_y)
					continue
				if not Jumping and ifJump:
					speed_y = SpeedY.get(scene, SpeedY[Normal])
					spd_x = speed_x_his[t]
					s = abs(spd_x)
					if s < 0.7:
						zone = 0
					elif s < 1.5:
						zone = 1
					elif s < 2.8:
						zone = 2
					else:
						zone = 3
					speed_y = tof(float(speed_y[input == 103 or input == 104][zone]))
					Jumping = True
					spd_y_his.append(speed_y)
					pos_y = tof(float(pos_y) + float(speed_y))
					pos_y_his.append(pos_y)
					continue
				elif scene == Water and ifJump:
					JumpWhileFall = True


				a = AccsY.get(scene, AccsY[Normal])
				if a is not None:
					s = speed_y
					if s <= border[0]:
						zone = 0
					elif s <= border[1]:
						zone = 1
					elif s <= border[2]:
						zone = 2
					elif s <= border[3]:
						zone = 3
					elif s <= border[4]:
						zone = 4
					else:
						zone = 5
			
					speed_y = tof(float(speed_y) + a[not ifJump][5-zone])
					if speed_y < maximum:
						speed_y = tof(maximum)
			speed_y = tof(float(speed_y) + JumpWhileFall)
			spd_y_his.append(speed_y)
			pos_y = tof(float(pos_y) + float(speed_y))
			pos_y_his.append(pos_y)
			JumpWhileFall = False
	return pos_y_his, spd_y_his

def pose(command, speed_his_x, speed_his_y, skin):
	pose_his = [('Stand', 1)]
	isground = True
	dir = 1
	for i in range(0, len(command), 2):
		com = command[i]
		frame = command[i+1]

		for _ in range(frame):
			if com[2] == 1:
				pose_mid = ('Jump', 'Fall', 'Swim', 'Swim')[(speed_his_y[i // 2] < 0) + 2 * (skin == 'Water')]
				if isground:
					dir =  com[1]
					isground = False
				pose_his.append((pose_mid, dir))
			elif com[2] == 2:
				isground = True
				dir = com[1]
				pose_gra = 'Run' if not speed_his_x[i] else 'Stand'
				pose_his.append((pose_gra, dir))
			elif com[2] == 3:
				isground = True
				dir = 1  *  np.sign(speed_his_x[i]) if com[0] == 52  else -1  * np.sign(speed_his_x[i])
				pose_his.append(('Duck', dir))
	return pose_his

def spike_hispoints(spike_str):
	spike_list = spike_str.split()
	hitpoints = []
	for i in range(0, len(spike_list), 2):
		x, y = 16 * float(spike_list[i]), 16 * float(spike_list[i+1])
		hitpoints.extend([
			(x+3.1, y), (x+12.9, y), 
			(x+0.1, y+4.0), (x+3.1, y+4.0), (x+12.9, y+4.0), (x+15.9, y+4.0),
			(x+0.1, y+12.0), (x+6.1, y+12.0), (x+12.0, y+12.0), (x+15.9, y+12.0),
			(x+6.0, y+16.0), (x+12.0, y+16.0)
			])
	return hitpoints

def IfDead(x, y, spike_points):
	for point in spike_points:
		if x < point[0] < x + 16 and y < point[1] < y + 12:
			return True
	return False


def Calculate_x_bfs(pos_x, speed, input, scene):
	pos_x = tof(pos_x)
	speed = tof(speed)
	scene = Scenes.get(scene, Normal)
	border = Borders_x[scene]
	input,  direction = input[0], input[1]
			
	if input is not None:
		type = input % 100
		slow = (type == 1 or type == 3) if scene != Water else (type == 1 or type == 2)
		groundmove = type == 3 or type == 4
		maximum = max_speed_x[scene][slow]
			
		a = AccsX[scene].get(type, None)
		if a is not None:
			if speed * direction < 0:
				a = Reverse_Acc[scene][groundmove]
		
			s = abs(speed)
			if s <= border[0]:
				zone = 0
			elif s <= border[1]:
				zone = 1
			elif s <= border[2]:
				zone = 2
			else:
				zone = 3
			
			if not direction:
				dif = float(abs(speed)) - a[zone]
				dif_32 = tof(max(0.0, dif))
				speed = tof(dif_32 if speed > 0 else -dif_32)
			else:
				speed = tof(float(speed) + a[zone] * float(direction))
			if abs(speed) > maximum and speed * direction > 0:
				speed = tof(maximum) if speed > 0 else np.float32(-maximum)
	speed = tof(float(speed) + 1) if scene == Wind else tof(speed)
	pos_x =tof(float(pos_x) + float(speed))

	return pos_x, speed

def Calculate_y_bfs(spd_x, pos_y, spd_y, input, scene, Jumping):
	pos_y = tof(pos_y)
	spd_y = tof(spd_y)
	JumpWhileFall = False
	scene = Scenes.get(scene, Normal)
	maximum = max_speed_y.get(scene, max_speed_y[Normal])
	border = Borders_y.get(scene, Borders_y[Normal])
	input = input[0]
	if input is not None:
		ifJump = input // 100 == 1
		GroundCom = 3 <= input <= 100
		if GroundCom:
			spd_y = tof(0)
			pos_y = tof(float(pos_y) + float(spd_y))
			return pos_y, spd_y, Jumping
		if not Jumping and ifJump:
			spd_y = SpeedY.get(scene, SpeedY[Normal])
			s = abs(spd_x)
			if s < 0.7:
				zone = 0
			elif s < 1.5:
				zone = 1
			elif s < 2.8:
				zone = 2
			else:
				zone = 3
			spd_y = tof(float(spd_y[input == 103 or input == 104][zone]))
			Jumping = True
			pos_y = tof(float(pos_y) + float(spd_y))
			return pos_y, spd_y, Jumping
		elif scene == Water and ifJump:
			JumpWhileFall = True

		a = AccsY.get(scene, AccsY[Normal])
		if a is not None:
			s = spd_y
			if s <= border[0]:
				zone = 0
			elif s <= border[1]:
				zone = 1
			elif s <= border[2]:
				zone = 2
			elif s <= border[3]:
				zone = 3
			elif s <= border[4]:
				zone = 4
			else:
				zone = 5
	
			spd_y = tof(float(spd_y) + a[not ifJump][5-zone])
			if spd_y < maximum:
				spd_y = tof(maximum)
	spd_y = tof(float(spd_y) + JumpWhileFall)
	pos_y = tof(float(pos_y) + float(spd_y))
	JumpWhileFall = False
	return pos_y, spd_y, Jumping

def Solution(pos_x, spd_x, scene, switch_lim, tar_point, frame_lim, IfSubp): 
	queue = deque()
	visited = set()
	queue.append((pos_x, []))
	tar_x = tof(tar_point[0])
	grace = tof(0) if IfSubp else tof(0.1)
	result = []
	def v(t):
		return t[1]

	coms = ((3, 1), (3, -1), (4, 1), (4, -1))
	coms_stop = ((51, 0), (52, 0), (53, 0))

	for _ in range(switch_lim):
		if not queue:
			break
		for _ in range(len(queue)):

			x, his = queue.popleft()
			for com in coms:
				for d in coms_stop:
					frame = 0
					while True:
						frame += 1
						if frame >= frame_lim:
							break
						nx, nsx = Calculate_x(x, tof(0), (com, frame), scene)
						new_x = nx[-1]
						new_sx = nsx[-1]
						while round(new_sx, 4) != 0:
							new_x, new_sx = Calculate_x_bfs(new_x, new_sx, d, scene)
						if new_x in visited:
							continue

						#trim 
						if ((new_x > tar_x + grace + 1 or pos_x - 0.5 > new_x) and tar_x > pos_x) or ((tar_x - grace - 1 > new_x or new_x - 0.5 > pos_x) and tar_x < pos_x):
							break
						if tar_x - grace <= new_x <= tar_x + grace:
							result.append((his + [com] * frame + [d], abs(tar_x - new_x)))
						visited.add(new_x)
						queue.append((new_x, his + [com] * frame + [d]))
	if len(result) > 0:
		result.sort(key = v, reverse=False)
		return [tuple(i[0]) for i in result]
	return None


def Solution_Beam(pos_x, spd_x, pos_y, spd_y, scene, map_str, switch_lim, tar_point, frame_lim, BEAM_WIDTH=500):
    # 状態: (x, sx, y, sy, history, switch_count, jumping)
    current_beam = [(pos_x, spd_x, pos_y, spd_y, [], 0, False)]
    visited = set()
    spike_map = spike_hispoints(map_str)
    tar_x, tar_y = float(tar_point[0]), float(tar_point[1])
    coms_jump = ((0, 1), (1, 1), (1, -1), (2, 1), (2, -1), (101, 1), (101, -1), (102, 1), (102, -1), (150, 1))
    coms_notjump = coms_jump + ((3, 1), (3, -1), (4, 1), (4, -1), (51, 0), (52, 0), (53, 0))

    for frame in range(frame_lim):
        next_candidates = []
        for x, sx, y, sy, his, switch, jumping in current_beam:
            # ゴール判定 (マリオの16x12ヒットボックス内にターゲットが入ったか)
            if x <= tar_x <= x + 16 and y <= tar_y <= y + 12:
                return his

            coms = coms_jump if jumping else coms_notjump
            for com in coms:
                nx, nsx = Calculate_x_bfs(x, sx, com, scene)
                ny, nsy, njump = Calculate_y_bfs(sx, y, sy, com, scene, jumping)

                # 画面外・トゲ死亡の枝刈り
                if ny < -32 or IfDead(nx, ny, spike_map):
                    continue

                # 切り替え数の上限チェック
                new_switch = switch + (1 if len(his) > 0 and his[-1] != com else 0)
                if new_switch > switch_lim:
                    continue

                # 状態空間の量子化 (Subpixel Quantization) で枝刈り
                state_key = (round(nx * 4), round(nsx * 10), round(ny * 4), round(nsy * 10), njump)
                if state_key in visited:
                    continue
                visited.add(state_key)

                # ゴールまでの推定距離 (ヒューリスティック)
                h_dist = abs(tar_x - nx) + abs(tar_y - ny)
                next_candidates.append((h_dist, nx, nsx, ny, nsy, his + [com], new_switch, njump))

        if not next_candidates:
            break

        # 推定距離順にソートして上位 BEAM_WIDTH 個だけを残す (爆速化の核心)
        next_candidates.sort(key=lambda item: item[0])
        current_beam = [item[1:] for item in next_candidates[:BEAM_WIDTH]]

    return None
