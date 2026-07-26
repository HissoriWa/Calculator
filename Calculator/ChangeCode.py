JtoW_dict = {
    '右走': 'RightWalk', '左走': 'LeftWalk', '右跑': 'RightRun', '左跑': 'LeftRun', '站立': 'Stand', '正蹲': 'FrontDuck', '反蹲': 'BackDuck', '站停': 'Stand', '正停': 'FrontDuck', '反停': 'BackDuck', '跳': 'Jump', '右跳': 'RightJump', '左跳': 'LeftJump', '右': 'Right', '左': 'Left', '加速右': 'AccRight', '加速左': 'AccLeft', '加速右跳': 'AccRightJump', '加速左跳': 'AccLeftJump', '右缓冲跳': 'RightBufferJump', '左缓冲跳': 'LeftBufferJump', '加速右缓冲跳': 'AccRightBufferJump', '加速左缓冲跳': 'AccLeftBufferJump', '滞空': 'Jump', '落体': 'Airbone', '坐莲': 'GroundPound', '滞空坐莲': 'FloatGroundPound', '缓冲跳': 'BufferJump', '弹簧跳': 'TrampolineJump', '无敌右走': 'RightWalk', '无敌左走': 'LeftWalk', '无敌右跑': 'RightRun', '无敌左跑': 'LeftRun', '无敌站立': 'Stand', '无敌正蹲': 'FrontDuck', '无敌反蹲': 'BackDuck', '无敌站停': 'StandToStop', '无敌正停': 'FrontDuckToStop', '无敌反停': 'BackDuckToStop', '无敌右': 'Right', '无敌左': 'Left', '无敌右跳': 'RightJump', '无敌左跳': 'LeftJump', '无敌加速右': 'AccRight', '无敌加速左': 'AccLeft', '无敌加速右跳': 'AccRightJump', '无敌加速左跳': 'AccLeftJump', '落体正': 'DropFront', '落体反': 'DropBack', '落体站': 'DropStand', '冰右走': 'RightWalk', '冰左走': 'LeftWalk', '冰右跑': 'RightRun', '冰左跑': 'LeftRun', '冰站立': 'Stand', '冰正蹲': 'FrontDuck', '冰反蹲': 'BackDuck', '右旋转跳': 'RightSpinJump', '左旋转跳': 'LeftSpinJump', '加速右旋转跳': 'AccRightSpinJump', '加速左旋转跳': 'AccLeftSpinJump', '旋转': 'Spin', '右旋转': 'RightSpin', '左旋转': 'LeftSpin', '加速右旋转': 'AccRightSpin', '加速左旋转': 'AccLeftSpin', '右反墙': 'RightWallKick', '左反墙': 'LeftWallKick', '低重右': 'Right', '低重左': 'Left', '低重右跳': 'RightJump', '低重左跳': 'LeftJump', '低重加速右': 'AccRight', '低重加速左': 'AccLeft', '低重加速右跳': 'AccRightJump', '低重加速左跳': 'AccLeftJump', '低重右缓冲跳': 'RightBufferJump', '低重左缓冲跳': 'LeftBufferJump', '低重加速右缓冲跳': 'AccRightBufferJump', '低重加速左缓冲跳': 'AccLeftBufferJump', '低重跳': 'Jump', '低重滞空': 'FloatJump', '低重落体': 'Airbone', '低重坐莲': 'GroundPound', '低重滞空坐莲': 'FloatGroundPound', '水右走': 'RightWalk', '水左走': 'LeftWalk', '水站': 'Stand', '水右': 'Right', '水左': 'Left', '水右跳': 'RightSwim', '水左跳': 'LeftSwim', '水跳': 'Swim', '水落': 'Airbone', '风右跳': 'RightJump', '风左跳': 'LeftJump', '风右跑跳': 'AccRightJump', '风左跑跳': 'AccLeftJump', '风右走': 'RightWalk', '风左走': 'LeftWalk', '风右跑': 'RightRun', '风左跑': 'LeftRun', '风站立': 'Stand', '岩浆右走': 'LavaRightWalk', '岩浆左走': 'LavaLeftWalk', '岩浆站立': 'LavaStand', '岩浆站停': 'LavaStandToStop', '右陡坡右走': 'RSteepSlopeRightWalk', '右陡坡左走': 'RSteepSlopeLeftWalk', '右陡坡右跑': 'RSteepSlopeRightRun', '右陡坡左跑': 'RSteepSlopeLeftRun', '右缓坡右走': 'RGentleSlopeRightWalk', '右缓坡左走': 'RGentleSlopeLeftWalk', '右缓坡右跑': 'RGentleSlopeRightRun', '右缓坡左跑': 'RGentleSlopeLeftRun', '左陡坡右走': 'LSteepSlopeRightWalk', '左陡坡左走': 'LSteepSlopeLeftWalk', '左陡坡右跑': 'LSteepSlopeRightRun', '左陡坡左跑': 'LSteepSlopeLeftRun', '左缓坡右走': 'LGentleSlopeRightWalk', '左缓坡左走': 'LGentleSlopeLeftWalk', '左缓坡右跑': 'LGentleSlopeRightRun', '左缓坡左跑': 'LGentleSlopeLeftRun'
}

WtoJ_dict = {}
for k, v in JtoW_dict.items():
    if v not in WtoJ_dict.keys():
        WtoJ_dict[v] = k

def JtoW(code_J):
    code_J = code_J.split()
    code_W = ''
    for J in code_J:
        let = ''
        num = ''
        for i, letter in enumerate(J):
            try:
                float(letter)
                num += letter
            except ValueError:
                let += letter
        code_W += f'{JtoW_dict.get(let, 'Airbone')} {num} '
    return code_W

def WtoJ(code_W):
    code_W = code_W.split()
    code_J = ''
    for i in range(0, len(code_W), 2):

        code_J += f'{WtoJ_dict.get(code_W[i], '落体')}{code_W[i+1]} '
    return code_J

print(JtoW('右走16 正蹲100 左走1 站立10 右1 正蹲10'))
print(WtoJ_dict)