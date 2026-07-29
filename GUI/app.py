import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
from  concurrent.futures import ThreadPoolExecutor
import time

def loaddata():
    with open(BASE.parent / 'strats.json', 'r') as f:
        return json.load(f)
    
def describe():
    pos_x = np.float32(st.session_state.pos_x)
    spd_x = np.float32(st.session_state.spd_x)
    pos_y = np.float32(st.session_state.pos_y)
    spd_y = np.float32(st.session_state.spd_y)
    scene = st.session_state.scene
    commands = st.session_state.commands if not st.session_state.IfJXMai else CC.JtoW(st.session_state.commands)
#generate field and number
    field = [[back] * width for _ in range(height)]

    st.session_state.background = Image.new('RGBA', (width * 80, height * 80))
    draw = ImageDraw.Draw(st.session_state.background)
    textfont = ImageFont.truetype('arial.ttf', size = 80)
    for y, row in enumerate(field):
        for x, tile in enumerate(row):
            st.session_state.background.paste(images[tile], (x*80, y*80))


    #paste ground and spikes 
    for koblock, array in enumerate((st.session_state.ground_pos, st.session_state.spike_pos)):
        try:
            block = 'Spike' if koblock else 'Ground'
            array = array.split()
            for i in range(0, len(array), 2):
                x, y = array[i], array[i + 1]
                st.session_state.background.paste(images[block], (int(x)*80, (height - int(y) - 1)*80), images[block])
        except (ValueError, IndexError):
            st.error('Enter in Correct Format!')
            return

    #add number
    for y in range(len(field)):
        draw.text((0, (height - y - 1) * 80), str(y), fill = 'white', font = textfont)
    for x in range(len(field[0])):
        draw.text((x * 80, (height - 1) * 80), str(x), fill = 'white', font = textfont)
    commands = commands.split()
    new_commands = []
    try:
        for i in range(0, len(commands), 2):
            new_commands.extend([Types.get(commands[i], (0, 0, 1)), int(commands[i+1])])
    except (IndexError, ValueError):
        st.error('Enter in correct format!')
        return 'Error'
    p_x, s_x = Cal.Calculate_x(pos_x, spd_x, new_commands, scene)
    p_y, s_y = Cal.Calculate_y(pos_y, s_x, spd_y, new_commands, scene)
    pose = Cal.pose(new_commands, s_x, s_y, scene)
    if AllDuck:
        for i in range(len(pose)):
            pose[i] = ('Duck', pose[i][1])
    
    coms = ['Stand',] + [commands[i] for i in range(0, len(commands), 2) for _ in range(int(commands[i+1]))]

    spike_hitboxes = Cal.spike_hispoints(st.session_state.spike_pos)
    st.session_state.dead = False
    for i in range(len(p_x)):
        Dead = Cal.IfDead(p_x[i], p_y[i], spike_hitboxes)
        if Dead:
            st.session_state.dead = True

        if i == len(p_x) - 1 or i == 0 or coms[i] != coms[i + 1]:
            chara = charas[pose[i][0]] if not Dead else charas_gray[pose[i][0]]
            st.session_state.background.paste((chara), (int(p_x[i] * 5), int((height - 1)* 16 - p_y[i] + 1) * 5), chara)
        elif trail:
            chara = charas_half[pose[i][0]] if not Dead else charas_gray_half[pose[i][0]]
            st.session_state.background.paste((chara), (int(p_x[i] * 5), int((height - 1)* 16 - p_y[i] + 1) * 5), chara)

    if st.session_state.hex:
        for array in (p_x, s_x, p_y, s_y):
            for i, v in enumerate(array):
                array[i] = tohex(v)

    st.session_state.result = f'X pos: {p_x[-1]} X spd: {s_x[-1]} Y pos: {p_y[-1]} Y spd: {s_y[-1]}, Dead: {st.session_state.dead}'
    st.session_state.df = pd.DataFrame({
		'Speed_x': [str(x) for x in s_x],
		'Speed_y': [str(y) for y in s_y],
	})

def load_callback():
    chosen = st.session_state.chosen
    data = strats_data[chosen]

    try:
        st.session_state.commands = data['action'] if not st.session_state.IfJXMai else  CC.WtoJ(data['action'])
    except (ValueError, IndexError):
        st.error('Not Saved In Correct Format!')
        return
    st.session_state._pos_x = data['pos_x']
    st.session_state._spd_x = data['spd_x']
    st.session_state._pos_y = data['pos_y']
    st.session_state._spd_y = data['spd_y']
    st.session_state.scene = data['scene']

    sync()
    describe()

def add_callback():
    if st.session_state.hex:
        st.error('Add in non-hex mode!')
        return
    if st.session_state.name in strats_data.keys():
        st.error('That strat already exists!')
        return
    try:
        Check = describe()
        strats_data[st.session_state.name] = {
        "pos_x": st.session_state._pos_x,
        "spd_x": st.session_state._spd_x,
        "pos_y": st.session_state._pos_y,
        "spd_y": st.session_state._spd_y,
        "scene": st.session_state.scene,
        "action": st.session_state.commands if not st.session_state.IfJXMai else CC.JtoW(st.session_state.commands)
        }
    except (ValueError, IndexError, KeyError):
        return
    if Check == 'Error':
        return

    with open(BASE.parent / 'strats.json', 'w', encoding = 'utf-8') as f:
        json.dump(strats_data, f, indent = 4)
    st.write('Added successfully!')

def half_alpha(image):
    r, g, b, a = image.split()
    a.paste(Image.new('L', a.size, 64), mask = a)
    return Image.merge('RGBA', (r, g, b, a))

def grayout(image):
    r, g, b, a = image.split()
    zero_channel = Image.new('L', b.size, 0)
    return Image.merge('RGBA', (zero_channel, zero_channel, b, a))

def search(x, sx, scene, switch_lim, tar_point, frame_lim, IS):
    target = tar_point.split()
    future = executer.submit(Cal.Solution, x, sx, scene, switch_lim, target, frame_lim, IS)
    if not future.done:
        with st.spinner('Searching in Progress...'):
            time.sleep(5)
            st.rerun()
    else:
        sol = future.result()
    if sol is not None:
        st.write(f'{len(sol)} Hit!')
        result = []
        for n, s in enumerate(sol):
            st.write(f'{n+1}th Solution:')
            for i in s:
                result.append(Types_search[tuple(i)])
            st.write(format(result))
            st.write()

def format(command_list):
    t = -1
    result = ''
    previous_com = command_list[0]
    for com in command_list:
        t += 1
        if com != previous_com:
            result += f' {previous_com} {t}'
            t = 0
            previous_com = com
    result += f' {previous_com} {1}'
    return result

def tohex(n):
    n = np.float32(n)
    bit_repr = n.view(np.uint32)
    return f"0x{bit_repr:08x}"

def _tohex():
    for k in ('_pos_x', '_spd_x', '_pos_y', '_spd_y'):
        try:
            st.session_state[k] = tohex(st.session_state[k])
        except ValueError:
            st.session_state[k] = str(to32(st.session_state[k]))

def to32(n):
    int_val = np.uint32(int(n, 16))
    return int_val.view(np.float32)

def sync():
    for k, _k in (('pos_x', '_pos_x'), ('spd_x', '_spd_x'), ('pos_y', '_pos_y'), ('spd_y', '_spd_y')):
        try:
            st.session_state[k] = np.float32(st.session_state[_k])
        except ValueError:
            st.session_state[k] = to32(st.session_state[_k])

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
import Calculator.CalCalculate as Cal
import Calculator.ChangeCode as CC

executer = ThreadPoolExecutor(max_workers=1)

BASE = Path(__file__).resolve().parent
if 'clicked' not in st.session_state:
    st.session_state.clicked = 0
if 'loadsetup' not in st.session_state:
    st.session_state.loadsetup = 0
if 'pos_x' not in st.session_state:
    st.session_state.pos_x = 64.0
if 'spd_x' not in st.session_state:
    st.session_state.spd_x = 0.0
if 'pos_y' not in st.session_state:
    st.session_state.pos_y = 32.0
if 'spd_y' not in st.session_state:
    st.session_state.spd_y = 0.0
if 'commands' not in st.session_state:
    st.session_state.commands = ''
if 'scene' not in st.session_state:
    st.session_state.scene = 0
if 'ground_pos' not in st.session_state:
    str_pos = ''
    for i in range(7):
        for j in range(2):
            str_pos += f'{i} {j} '
    st.session_state.ground_pos = str_pos
if 'spike_pos' not in st.session_state:
    st.session_state.spike_pos = '7 1 9 1'
if '_pos_x' not in st.session_state:
    st.session_state._pos_x = '64.0'
if '_spd_x' not in st.session_state:
    st.session_state._spd_x = '0.0'
if '_pos_y' not in st.session_state:
    st.session_state._pos_y = '32.0'
if '_spd_y' not in st.session_state:
    st.session_state._spd_y = '0.0'
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({'Speed_x': ['0'], 'Speed_y': ['0'],})
if 'background' not in st.session_state:
    st.session_state.background = None
if 'dead' not in st.session_state:
    st.session_state.dead = False
if 'result' not in st.session_state:
    st.session_state.result = f'X pos: {st.session_state.pos_x} X spd: {st.session_state.spd_x} Y pos: {st.session_state.pos_y} Y spd: {st.session_state.spd_y}, Dead: {st.session_state.dead}'
if 'IfJXMai' not in st.session_state:
    st.session_state.IfJXMai = False 


#1: midair, 2: ground, 3: duck
Types = {\
	'Airbone': (0, 1, 1), 'Right': (1, 1, 1), 'Left': (1, -1, 1), 'AccRight': (2, 1, 1), 'AccLeft': (2, -1, 1), 'RightWalk': (3, 1, 2), 'LeftWalk': (3, -1, 2), 'RightRun': (4, 1, 2), 'LeftRun': (4, -1, 2), 'Stand': (51, 0, 2), 'FrontDuck': (52, 0, 3), 'BackDuck': (53, 0, 3),\
	'RightJump': (101, 1, 1), 'LeftJump': (101, -1, 1), 'AccRightJump': (102, 1, 1), 'AccLeftJump': (102, -1, 1), 'RightBufferJump': (103, 1, 1), 'LeftBufferJump': (103, -1, 1), 'AccRightBufferJump': (104, 1, 1), 'AccLeftBufferJump': (104, -1, 1), 'Jump': (150, 1, 1)\
}

Types_search = {(v[0], v[1]): k for k, v in Types.items()}

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title('CALCULATOR')

strats_data = loaddata()

mode = st.sidebar.selectbox('Mode', ['Calculate', 'Find setups'])


Ifhex = st.checkbox('Input/Get as hex', on_change = _tohex, key = 'hex')

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.text_input('x Pos', key = '_pos_x', on_change=sync())
with col2:
    st.text_input('x Spd', key = '_spd_x', on_change=sync())
with col3:
    st.text_input('y Pos', key = '_pos_y', on_change=sync())
with col4:
    st.text_input('y Spd', key = '_spd_y', on_change=sync())
with col5:
    width = st.number_input('Width', value = 12, step = 1)
with col6:
    height = st.number_input('Height', value = 8, step = 1)


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    gamemode = st.selectbox('GameMode', ['M1', 'M3', 'MW'], disabled=True)
with col2: 
    skin = st.selectbox('Skin', ['Overworld','Underground', 'Water', 'Desert', 'Snow', 'Sky', 'Forest', 'Ghost', 'Airship', 'Castle'])
with col3:
    IfWater = (skin == 'Water')
    if IfWater:
        st.session_state.scene = 'Water'
    scene = st.selectbox('Condition', ['Normal', 'Star', 'Ice', 'Water', 'Wind', 'LowG'], key ='scene', disabled = IfWater)
with col4:
    back = st.selectbox('BackGround', ['Back1', 'Back2', 'Back3', 'Mushroom', 'ON Back', 'OFF Back', 'P Back'], index = 1)
with col5:
    trail = st.checkbox('Trail', value = True)
    AllDuck = st.checkbox('Duck', value = False)


col1, col2 = st.columns([4, 2])
titles = [key for key in strats_data.keys()]

with col1:
    strat_chosen = st.selectbox('Setups', titles, key = 'chosen')
    st.checkbox('Enter Commands in JXMai format', key = 'IfJXMai')
with col2:
    col3, col4 = st.columns(2)
    st.text_input('New Strat Name', key = 'name', disabled=True)
    with col3:
        st.button('Load the Setup', on_click = load_callback)
    with col4:
        st.button('Add the Setup', on_click = add_callback, disabled=True)

           
    
if mode == 'Calculate':
    ph = 'Example: LeftJump 2 RightJump 4 LeftJump 2' if not st.session_state.IfJXMai else 'Example: 左跳2 右跳4 左跳2'
    st.text_area(label ='Commands', placeholder = ph, key = 'commands')
elif mode == 'Find setups':
    col1, col2, col3, col4 = st.columns(4)
    st.session_state.commands = ''
    with col1:
        tar = st.text_input('Target point')
        if tar:
            if st.session_state.hex:
                try:
                    tar = str(to32(tar))
                except ValueError:
                    st.error('Enter in Correct Format!')
    with col2:
        switch = st.number_input('Difficulty', value = 3)
    with col3:
        frame = st.number_input('Lim Frames', value = 30)
    with col4:
        IfSubp = st.checkbox('Subpixel')
st.write(st.session_state.result)


images = {
    'Spike': Image.open(BASE / 'Anims' / gamemode / 'Any' / 'Spike.png').resize((80, 80), Image.Resampling.NEAREST),
    'Ground': Image.open(BASE / 'Anims' / gamemode / skin / 'Ground.png').resize((80, 80), Image.Resampling.NEAREST),
    'Back1': Image.open(BASE / 'Anims' / gamemode / skin / 'Back1.png').resize((80, 80), Image.Resampling.NEAREST),
    'Back2': Image.open(BASE / 'Anims' / gamemode / skin / 'Back2.png').resize((80, 80), Image.Resampling.NEAREST),
    'Back3': Image.open(BASE / 'Anims' / gamemode / skin / 'Back3.png').resize((80, 80), Image.Resampling.NEAREST),
    'Mushroom': Image.open(BASE / 'Anims' / gamemode / skin / 'Mush.png').resize((80, 80), Image.Resampling.NEAREST),
    'ON Block': Image.open(BASE / 'Anims' / gamemode / 'Any' / 'On_active.png').resize((80, 80), Image.Resampling.NEAREST),
    'ON Back': Image.open(BASE / 'Anims' / gamemode / 'Any' / 'On_inactive.png').resize((80, 80), Image.Resampling.NEAREST),
    'OFF Block': Image.open(BASE / 'Anims' / gamemode / 'Any' / 'Off_active.png').resize((80, 80), Image.Resampling.NEAREST),
    'OFF Back': Image.open(BASE / 'Anims' / gamemode / 'Any' / 'Off_inactive.png').resize((80, 80), Image.Resampling.NEAREST),
    'P Block': Image.open(BASE / 'Anims' / gamemode / 'Any' / 'P_active.png').resize((80, 80), Image.Resampling.NEAREST),
    'P Back': Image.open(BASE / 'Anims' / gamemode / 'Any' / 'P_inactive.png').resize((80, 80), Image.Resampling.NEAREST),
}

charas = {
    'Stand': Image.open(BASE / 'Anims' / gamemode / 'chara' / 'MarioStand.png').resize((80, 80), Image.Resampling.NEAREST),
    'Duck': Image.open(BASE / 'Anims' / gamemode / 'chara' / 'MarioDuck.png').resize((80, 80), Image.Resampling.NEAREST),
    'Jump': Image.open(BASE / 'Anims' / gamemode / 'chara' / 'MarioJump.png').resize((80, 80), Image.Resampling.NEAREST),
    'Fall': Image.open(BASE / 'Anims' / gamemode / 'chara' / 'MarioFall.png').resize((80, 80), Image.Resampling.NEAREST),
    'Run': Image.open(BASE / 'Anims' / gamemode / 'chara' / 'MarioRun.png').resize((80, 80), Image.Resampling.NEAREST),
    'Swim': Image.open(BASE / 'Anims' / gamemode / 'chara' / 'MarioSwim.png').resize((80, 80), Image.Resampling.NEAREST),
}

charas_gray = {
    key: grayout(value) for key, value in charas.items()
}

charas_half = {
    key: half_alpha(value) for key, value in charas.items()
}

charas_gray_half = {
    key: grayout(value) for key, value in charas_half.items()
}

if st.session_state.background is None:
    describe()

col1, col2, col3, col4 = st.columns([2, 5, 2, 2])
with col1:
    if mode == 'Calculate':
        if st.button('Calculate!', on_click = describe):
            st.session_state.clicked = True
    elif st.button('Search!'):
        search(st.session_state.pos_x, st.session_state.spd_x, scene, switch, tar, frame, IfSubp)
with col2:
    pos_input = st.text_input('Spike Position')
with col3:
    if st.button('Add Spikes'):
        spike_arranged = ' '.join(pos_input.split())
        st.session_state.spike_pos += ' ' + pos_input

    if st.button('Erace Spikes'):
        spike_input_t = pos_input.split()
        spike_pos_t = st.session_state.spike_pos.split()
        if len(spike_input_t) % 2 == 0:
            spike_input_s = set()
            for i in range(0, len(spike_input_t), 2):
                spike_input_s.add((spike_input_t[i], spike_input_t[i+1]))

            st.session_state.spike_pos = ''
            for i in range(0, len(spike_pos_t), 2):
                if (spike_pos_t[i], spike_pos_t[i+1]) not in spike_input_s:
                    st.session_state.spike_pos += f'{spike_pos_t[i]} {spike_pos_t[i+1]} '

            pos_input = ''
        else:
            st.write('Enter in Correct Format!')

    if st.button('Erace All Spikes'):
        st.session_state.spike_pos = ''
        pos_input = ''

with col4:
    if st.button('Add Grounds'):
        ground_arranged = ' '.join(pos_input.split())
        st.session_state.ground_pos += ' ' + pos_input

    if st.button('Erace Grounds'):
        ground_input_t = pos_input.split()
        ground_pos_t = st.session_state.ground_pos.split()
        if len(ground_input_t) % 2 == 0:
            ground_input_s = set()
            for i in range(0, len(ground_input_t), 2):
                ground_input_s.add((ground_input_t[i], ground_input_t[i+1]))

            st.session_state.ground_pos = ''
            for i in range(0, len(ground_pos_t), 2):
                if (ground_pos_t[i], ground_pos_t[i+1]) not in ground_input_s:
                    st.session_state.ground_pos += f'{ground_pos_t[i]} {ground_pos_t[i+1]} '

            pos_input = ''
        else:
            st.write('Enter in correct format!')
    if st.button('Erace All grounds'):
        str_pos = ''
        for i in range(7):
            for j in range(2):
                str_pos += f'{i} {j} '
        st.session_state.ground_pos = str_pos
        pos_input = ''

if st.button('Describe spike positions'):
    st.code(st.session_state.spike_pos)

st.image(st.session_state.background, width = 'content')
st.write(st.session_state.df)


try:
    with st.expander('About This App'):
        with open(BASE.parent / 'README.md') as f:
            st.markdown(f.read())
except FileNotFoundError:
    st.error('README.md Not Found')

try:
    with st.expander('LICENSE'):
        with open(BASE.parent / 'LICENSE') as f:
            st.code(f.read())
except FileNotFoundError:
    st.error('LICENSE Not Found')
