import pygame
import sys
import json
import random
import os
import math
import asyncio

# ==========================================
# 1. 初始化與跨平台設定
# ==========================================
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("元氣日語勇者傳 - 手機網頁移植版")

clock = pygame.time.Clock()
FPS = 60

WORLD_WIDTH = 1152
WORLD_HEIGHT = 810

# 色彩定義
COLOR_BG_DARK   = (18, 20, 26)
COLOR_DUNGEON_1 = (32, 36, 46)
COLOR_DUNGEON_2 = (24, 28, 36)
COLOR_PANEL     = (30, 36, 48)
COLOR_WHITE     = (240, 242, 245)
COLOR_GOLD      = (255, 204, 0)
COLOR_GREEN     = (46, 204, 113)
COLOR_RED       = (231, 76, 60)
COLOR_BLUE      = (52, 152, 219)
COLOR_PURPLE    = (155, 89, 182)
COLOR_GRAY      = (100, 110, 125)
COLOR_ORANGE    = (230, 126, 34)

def get_safe_font(size):
    font_path = "font.ttf"
    if os.path.exists(font_path):
        return pygame.font.Font(font_path, size)
    return pygame.font.SysFont(None, size)

font_sm = get_safe_font(16)
font_md = get_safe_font(22)
font_lg = get_safe_font(30)
font_huge = get_safe_font(72)

# ==========================================
# 2. 梯度平衡數據庫 (20武器、20食物、20寵物、20怪物、30單字)
# ==========================================
WEAPONS_DB = [
    {"name": "破舊短劍", "atk": 5, "weight": 50, "type": "sword"},
    {"name": "木弓",     "atk": 7, "weight": 45, "type": "bow"},
    {"name": "破舊手槍", "atk": 8, "weight": 40, "type": "gun"},
    {"name": "精鋼長劍", "atk": 11, "weight": 35, "type": "sword"},
    {"name": "木法杖",   "atk": 13, "weight": 30, "type": "staff"},
    {"name": "左輪手槍", "atk": 15, "weight": 28, "type": "gun"},
    {"name": "獵人長弓", "atk": 17, "weight": 25, "type": "bow"},
    {"name": "武士刀",   "atk": 19, "weight": 22, "type": "sword"},
    {"name": "大蔥戰刃", "atk": 21, "weight": 20, "type": "leek"},
    {"name": "神奇鹹魚", "atk": 23, "weight": 18, "type": "fish"},
    {"name": "火焰法杖", "atk": 25, "weight": 16, "type": "staff"},
    {"name": "疾風之弓", "atk": 27, "weight": 14, "type": "bow"},
    {"name": "霰彈槍",   "atk": 29, "weight": 12, "type": "gun"},
    {"name": "騎士巨劍", "atk": 32, "weight": 10, "type": "sword"},
    {"name": "寒冰法杖", "atk": 34, "weight": 8, "type": "staff"},
    {"name": "衝鋒槍",   "atk": 36, "weight": 6, "type": "gun"},
    {"name": "精靈星弓", "atk": 39, "weight": 5, "type": "bow"},
    {"name": "雷電法杖", "atk": 42, "weight": 4, "type": "staff"},
    {"name": "光劍-紅",  "atk": 45, "weight": 3, "type": "light"},
    {"name": "賢者之杖", "atk": 50, "weight": 2, "type": "staff"}
]

FOODS_DB = [
    {"name": "蘋果",       "price": 15,  "exp": 20},
    {"name": "香蕉",       "price": 20,  "exp": 25},
    {"name": "草莓",       "price": 25,  "exp": 30},
    {"name": "葡萄",       "price": 30,  "exp": 35},
    {"name": "西瓜",       "price": 35,  "exp": 40},
    {"name": "烤蘿蔔",     "price": 40,  "exp": 45},
    {"name": "高麗菜沙拉", "price": 45,  "exp": 50},
    {"name": "烤玉米",     "price": 50,  "exp": 55},
    {"name": "南瓜派",     "price": 60,  "exp": 60},
    {"name": "炸茄子",     "price": 70,  "exp": 65},
    {"name": "麥香麵包",   "price": 80,  "exp": 70},
    {"name": "飯糰",       "price": 90,  "exp": 75},
    {"name": "炒葵花子",   "price": 100, "exp": 80},
    {"name": "花草茶",     "price": 110, "exp": 85},
    {"name": "特級辣肉丸", "price": 120, "exp": 90},
    {"name": "藍莓蛋糕",   "price": 135, "exp": 95},
    {"name": "櫻桃布丁",   "price": 150, "exp": 100},
    {"name": "水蜜桃凍",   "price": 165, "exp": 105},
    {"name": "鮮檸檬汁",   "price": 180, "exp": 110},
    {"name": "哈密瓜聖代", "price": 200, "exp": 120}
]

PETS_DB = [
    {"name": "柴犬",     "price": 100,  "atk": 4,  "req_exp": 50},
    {"name": "波斯貓",   "price": 150,  "atk": 5,  "req_exp": 55},
    {"name": "迷你豬",   "price": 200,  "atk": 6,  "req_exp": 60},
    {"name": "綠史萊姆", "price": 250,  "atk": 7,  "req_exp": 65},
    {"name": "小精靈",   "price": 300,  "atk": 8,  "req_exp": 70},
    {"name": "風鈴鳥",   "price": 350,  "atk": 9,  "req_exp": 75},
    {"name": "企鵝",     "price": 400,  "atk": 10, "req_exp": 80},
    {"name": "草泥馬",   "price": 450,  "atk": 11, "req_exp": 85},
    {"name": "熊貓",     "price": 500,  "atk": 12, "req_exp": 90},
    {"name": "雷電鼠",   "price": 600,  "atk": 14, "req_exp": 100},
    {"name": "夜貓鷹",   "price": 700,  "atk": 15, "req_exp": 110},
    {"name": "岩石怪",   "price": 800,  "atk": 17, "req_exp": 120},
    {"name": "太陽花精", "price": 900,  "atk": 18, "req_exp": 130},
    {"name": "幽靈水母", "price": 1000, "atk": 20, "req_exp": 140},
    {"name": "冰霜狼",   "price": 1100, "atk": 22, "req_exp": 150},
    {"name": "機械狗",   "price": 1200, "atk": 23, "req_exp": 160},
    {"name": "彩虹鹿",   "price": 1300, "atk": 24, "req_exp": 170},
    {"name": "小火龍",   "price": 1400, "atk": 26, "req_exp": 180},
    {"name": "羽蛇獸",   "price": 1450, "atk": 27, "req_exp": 190},
    {"name": "九尾狐",   "price": 1500, "atk": 28, "req_exp": 200}
]

MONSTER_TYPES = [
    {"name": "綠史萊姆",   "hp": 90,  "atk": 5,  "speed": 1.5, "color": (46, 204, 113)},
    {"name": "野怪哥布林", "hp": 135, "atk": 8,  "speed": 1.8, "color": (230, 126, 34)},
    {"name": "骷髏弓箭手", "hp": 120, "atk": 10, "speed": 2.0, "color": (236, 240, 241)},
    {"name": "吸血蝙蝠",   "hp": 80,  "atk": 7,  "speed": 2.8, "color": (155, 89, 182)},
    {"name": "劇毒蜘蛛",   "hp": 150, "atk": 10, "speed": 1.6, "color": (142, 68, 173)},
    {"name": "瘋狂野豬",   "hp": 210, "atk": 13, "speed": 2.2, "color": (211, 84, 0)},
    {"name": "地牢幽靈",   "hp": 110, "atk": 15, "speed": 2.4, "color": (52, 152, 219)},
    {"name": "岩石守衛",   "hp": 330, "atk": 9,  "speed": 1.0, "color": (127, 140, 141)},
    {"name": "蜥蜴人戰士", "hp": 240, "atk": 15, "speed": 2.1, "color": (39, 174, 96)},
    {"name": "黑狂狼",     "hp": 195, "atk": 17, "speed": 2.6, "color": (44, 62, 80)},
    {"name": "黑暗騎士",   "hp": 360, "atk": 18, "speed": 1.7, "color": (52, 73, 94)},
    {"name": "泥偶巨人",   "hp": 420, "atk": 14, "speed": 1.1, "color": (180, 130, 90)},
    {"name": "地獄咒術師", "hp": 180, "atk": 22, "speed": 1.9, "color": (192, 57, 43)},
    {"name": "沙漠毒蠍",   "hp": 225, "atk": 16, "speed": 2.3, "color": (241, 196, 15)},
    {"name": "鋼鐵石像鬼", "hp": 390, "atk": 20, "speed": 1.4, "color": (149, 165, 166)},
    {"name": "食人花精",   "hp": 270, "atk": 18, "speed": 1.3, "color": (30, 132, 73)},
    {"name": "熔岩怪物",   "hp": 450, "atk": 24, "speed": 1.5, "color": (231, 76, 60)},
    {"name": "虛空影魔",   "hp": 255, "atk": 26, "speed": 2.7, "color": (22, 160, 133)},
    {"name": "死靈法師",   "hp": 300, "atk": 28, "speed": 1.8, "color": (142, 68, 173)},
    {"name": "龍人近衛兵", "hp": 540, "atk": 30, "speed": 2.0, "color": (192, 57, 43)}
]

ALL_VOCABULARY = [
    {"id": i, "jp": jp, "romaji": rm, "zh": zh} for i, (jp, rm, zh) in enumerate([
        ("わたし", "watashi", "我"), ("ねこ", "neko", "貓"), ("いぬ", "inu", "狗"),
        ("たべる", "taberu", "吃"), ("のむ", "nomu", "喝"), ("ほん", "hon", "書"),
        ("やま", "yama", "山"), ("かわ", "kawa", "河川"), ("くるま", "kuruma", "車子"),
        ("さくら", "sakura", "櫻花"), ("みず", "mizu", "水"), ("ひ", "hi", "火"),
        ("き", "ki", "樹木"), ("そら", "sora", "天空"), ("うみ", "umi", "大海"),
        ("はな", "hana", "花朵"), ("あめ", "ame", "雨水"), ("ゆき", "yuki", "白雪"),
        ("かぜ", "kaze", "微風"), ("つき", "tsuki", "月亮"), ("ともだち", "tomodachi", "朋友"),
        ("せんせい", "sensei", "老師"), ("がくせい", "gakusei", "學生"), ("がっこう", "gakkou", "學校"),
        ("いえ", "ie", "家"), ("でんしゃ", "densha", "電車"), ("えき", "eki", "車站"),
        ("さかな", "sakana", "魚"), ("にく", "niku", "肉"), ("やさい", "yasai", "蔬菜")
    ], start=1)
]

# ==========================================
# 3. 程序化像素畫布生成器
# ==========================================
def draw_pixel_hero(job):
    surf = pygame.Surface((36, 36), pygame.SRCALPHA)
    if job == "戰士":
        pygame.draw.rect(surf, (140, 145, 155), (8, 12, 20, 18), border_radius=4)
        pygame.draw.rect(surf, (180, 185, 195), (6, 4, 24, 16), border_radius=5)
        pygame.draw.rect(surf, (20, 20, 25), (10, 10, 16, 4))
        pygame.draw.polygon(surf, COLOR_RED, [(18, 4), (12, -2), (18, 0)])
    elif job == "法師":
        pygame.draw.polygon(surf, COLOR_PURPLE, [(18, 6), (4, 32), (32, 32)])
        pygame.draw.ellipse(surf, (110, 50, 160), (2, 12, 32, 8))
        pygame.draw.polygon(surf, (130, 60, 180), [(18, 0), (8, 14), (28, 14)])
        pygame.draw.circle(surf, COLOR_GOLD, (18, 8), 3)
    else:
        pygame.draw.polygon(surf, COLOR_GREEN, [(18, 2), (4, 32), (32, 32)])
        pygame.draw.rect(surf, (135, 85, 45), (10, 14, 16, 14))
        pygame.draw.rect(surf, (30, 40, 30), (8, 10, 20, 4))
    return surf

def draw_pixel_monster(idx, is_boss=False):
    size = 64 if is_boss else 36
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    scale = size / 36.0
    if idx == 0:
        pygame.draw.ellipse(surf, COLOR_GREEN, (int(4*scale), int(8*scale), int(28*scale), int(24*scale)))
        pygame.draw.ellipse(surf, (200, 255, 200), (int(8*scale), int(10*scale), int(10*scale), int(8*scale)))
    elif idx == 1:
        pygame.draw.rect(surf, (39, 174, 96), (int(8*scale), int(8*scale), int(20*scale), int(22*scale)), border_radius=4)
        pygame.draw.polygon(surf, (39, 174, 96), [(int(8*scale), int(12*scale)), (0, int(6*scale)), (int(8*scale), int(18*scale))])
        pygame.draw.polygon(surf, (39, 174, 96), [(int(28*scale), int(12*scale)), (int(36*scale), int(6*scale)), (int(28*scale), int(18*scale))])
    elif idx == 2:
        pygame.draw.rect(surf, (236, 240, 241), (int(8*scale), int(4*scale), int(20*scale), int(18*scale)), border_radius=5)
        pygame.draw.circle(surf, (20, 20, 20), (int(13*scale), int(12*scale)), int(3*scale))
        pygame.draw.circle(surf, (20, 20, 20), (int(23*scale), int(12*scale)), int(3*scale))
    else:
        c = [(211,84,0), (52,152,219), (127,140,141), (39,174,96), (44,62,80), (52,73,94), (180,130,90), (192,57,43), (241,196,15), (149,165,166)][idx % 10]
        pygame.draw.rect(surf, c, (int(6*scale), int(6*scale), int(24*scale), int(24*scale)), border_radius=6)
        pygame.draw.circle(surf, COLOR_RED, (int(12*scale), int(14*scale)), int(3*scale))
        pygame.draw.circle(surf, COLOR_RED, (int(24*scale), int(14*scale)), int(3*scale))

    if is_boss:
        pygame.draw.polygon(surf, COLOR_GOLD, [(16, 12), (24, 0), (32, 12), (40, 0), (48, 12)])
        pygame.draw.circle(surf, COLOR_RED, (32, 6), 3)
    return surf

def draw_pixel_food(name):
    surf = pygame.Surface((28, 28), pygame.SRCALPHA)
    idx = [f["name"] for f in FOODS_DB].index(name) if name in [f["name"] for f in FOODS_DB] else 0
    if idx == 0:
        pygame.draw.circle(surf, COLOR_RED, (14, 16), 10)
        pygame.draw.rect(surf, (100, 50, 20), (13, 2, 3, 6))
    elif idx == 1:
        pygame.draw.arc(surf, COLOR_GOLD, (4, 4, 20, 20), 0.2, 2.2, 6)
    elif idx == 2:
        pygame.draw.polygon(surf, COLOR_RED, [(8, 8), (20, 8), (14, 24)])
        pygame.draw.polygon(surf, COLOR_GREEN, [(10, 8), (14, 4), (18, 8)])
    elif idx == 4:
        pygame.draw.ellipse(surf, COLOR_GREEN, (3, 6, 22, 16))
        pygame.draw.line(surf, (20, 80, 30), (6, 8), (20, 18), 2)
    elif idx == 8:
        pygame.draw.polygon(surf, (230, 126, 34), [(6, 22), (22, 22), (14, 6)])
        pygame.draw.circle(surf, COLOR_WHITE, (14, 14), 3)
    elif idx == 11:
        pygame.draw.polygon(surf, COLOR_WHITE, [(14, 4), (4, 22), (24, 22)])
        pygame.draw.rect(surf, (20, 20, 20), (10, 16, 8, 6))
    elif idx == 19:
        pygame.draw.polygon(surf, (100, 200, 255), [(8, 14), (20, 14), (14, 26)])
        pygame.draw.circle(surf, COLOR_WHITE, (14, 10), 6)
        pygame.draw.circle(surf, COLOR_RED, (14, 5), 3)
    else:
        c = [COLOR_RED, COLOR_GOLD, COLOR_GREEN, COLOR_PURPLE, COLOR_ORANGE][idx % 5]
        pygame.draw.circle(surf, c, (14, 15), 9)
        pygame.draw.rect(surf, COLOR_WHITE, (12, 6, 4, 4))
    return surf

def draw_pixel_pet(name, stage=1):
    size = 24 + (stage - 1) * 8
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    idx = [p["name"] for p in PETS_DB].index(name) if name in [p["name"] for p in PETS_DB] else 0
    c = [(225, 155, 60), (240, 240, 245), (250, 180, 180), COLOR_GREEN, (155, 89, 182), (52, 152, 219), (241, 196, 15), (127, 140, 141), (230, 126, 34)][idx % 9]
    pygame.draw.ellipse(surf, c, (2, 4, size-4, size-8))
    pygame.draw.circle(surf, COLOR_WHITE, (size//3, size//3), 2 + stage)
    pygame.draw.circle(surf, COLOR_WHITE, (size*2//3, size//3), 2 + stage)
    pygame.draw.circle(surf, (20, 20, 20), (size//3, size//3), 1 + stage//2)
    pygame.draw.circle(surf, (20, 20, 20), (size*2//3, size//3), 1 + stage//2)

    if stage == 1:
        pygame.draw.circle(surf, (255, 200, 200), (size//4, size//2), 2)
        pygame.draw.circle(surf, (255, 200, 200), (size*3//4, size//2), 2)
    elif stage == 2:
        pygame.draw.polygon(surf, COLOR_GOLD, [(size//2 - 4, 2), (size//2, -3), (size//2 + 4, 2)])
        pygame.draw.rect(surf, (60, 60, 70), (4, size//2, size-8, 4))
    elif stage == 3:
        pygame.draw.circle(surf, COLOR_GOLD, (size//2, size//2), size//2 + 2, width=1)
        pygame.draw.polygon(surf, COLOR_GOLD, [(size//2 - 6, 2), (size//2, -5), (size//2 + 6, 2)])
        pygame.draw.polygon(surf, COLOR_BLUE, [(0, size//3), (-4, size//4), (4, size//2)])
        pygame.draw.polygon(surf, COLOR_BLUE, [(size, size//3), (size+4, size//4), (size-4, size//2)])
    return surf

def draw_pixel_chest(is_opened=False):
    surf = pygame.Surface((34, 34), pygame.SRCALPHA)
    if not is_opened:
        pygame.draw.rect(surf, (139, 90, 43), (2, 8, 30, 22), border_radius=4)
        pygame.draw.rect(surf, COLOR_GOLD, (2, 8, 30, 22), width=2, border_radius=4)
        pygame.draw.rect(surf, (200, 200, 200), (13, 15, 8, 8), border_radius=2)
        pygame.draw.circle(surf, COLOR_RED, (17, 19), 2)
    else:
        pygame.draw.rect(surf, (80, 50, 20), (2, 14, 30, 16), border_radius=3)
        pygame.draw.polygon(surf, (110, 70, 30), [(2, 14), (32, 14), (28, 4), (6, 4)])
    return surf

def draw_pixel_health_pack():
    surf = pygame.Surface((24, 24), pygame.SRCALPHA)
    pygame.draw.rect(surf, COLOR_WHITE, (2, 2, 20, 20), border_radius=4)
    pygame.draw.rect(surf, COLOR_RED, (4, 4, 16, 16), width=1, border_radius=3)
    pygame.draw.rect(surf, COLOR_RED, (10, 5, 4, 14))
    pygame.draw.rect(surf, COLOR_RED, (5, 10, 14, 4))
    return surf

def draw_pixel_weapon(w_name):
    surf = pygame.Surface((32, 32), pygame.SRCALPHA)
    idx = [w["name"] for w in WEAPONS_DB].index(w_name) if w_name in [w["name"] for w in WEAPONS_DB] else 0
    w_type = WEAPONS_DB[idx]["type"]
    if w_type == "sword":
        pygame.draw.line(surf, COLOR_WHITE, (6, 26), (26, 6), 4)
        pygame.draw.line(surf, COLOR_GOLD, (4, 28), (10, 22), 5)
    elif w_type == "light":
        pygame.draw.line(surf, COLOR_RED, (6, 26), (26, 6), 5)
        pygame.draw.line(surf, COLOR_WHITE, (8, 24), (24, 8), 2)
    elif w_type == "staff":
        pygame.draw.line(surf, (139, 69, 19), (6, 26), (20, 12), 4)
        pygame.draw.circle(surf, COLOR_GOLD, (24, 8), 6)
    elif w_type == "bow":
        pygame.draw.arc(surf, COLOR_GREEN, (4, 4, 24, 24), 0.5, 2.5, 3)
        pygame.draw.line(surf, COLOR_WHITE, (8, 6), (22, 24), 1)
    elif w_type == "gun":
        pygame.draw.rect(surf, (50, 50, 60), (6, 12, 20, 8), border_radius=2)
        pygame.draw.rect(surf, (80, 50, 30), (8, 20, 5, 8))
    elif w_type == "fish":
        pygame.draw.ellipse(surf, (52, 152, 219), (4, 8, 22, 14))
        pygame.draw.polygon(surf, COLOR_WHITE, [(24, 15), (30, 8), (30, 22)])
    else:
        pygame.draw.line(surf, COLOR_WHITE, (6, 26), (14, 18), 4)
        pygame.draw.line(surf, COLOR_GREEN, (14, 18), (26, 6), 5)
    return surf

def draw_pixel_lobby_building(b_type):
    if b_type == "door":
        surf = pygame.Surface((100, 80), pygame.SRCALPHA)
        pygame.draw.rect(surf, (80, 85, 95), (0, 0, 100, 80), border_radius=10)
        pygame.draw.rect(surf, COLOR_GOLD, (0, 0, 100, 80), width=3, border_radius=10)
        pygame.draw.circle(surf, (40, 120, 220), (50, 40), 30)
        pygame.draw.circle(surf, COLOR_WHITE, (50, 40), 18, width=2)
        return surf
    elif b_type == "shop":
        surf = pygame.Surface((120, 90), pygame.SRCALPHA)
        pygame.draw.rect(surf, (140, 70, 90), (0, 25, 120, 65), border_radius=6)
        pygame.draw.rect(surf, (50, 50, 60), (70, 5, 30, 20), border_radius=3)
        pygame.draw.circle(surf, (240, 200, 160), (35, 12), 10)
        pygame.draw.rect(surf, COLOR_RED, (25, 2, 20, 8), border_radius=3)
        return surf
    elif b_type == "pethouse":
        surf = pygame.Surface((120, 100), pygame.SRCALPHA)
        pygame.draw.polygon(surf, COLOR_PURPLE, [(60, 0), (5, 45), (115, 45)])
        pygame.draw.rect(surf, (80, 55, 90), (15, 45, 90, 50), border_radius=4)
        pygame.draw.circle(surf, COLOR_WHITE, (60, 70), 12)
        return surf
    elif b_type == "vocab":
        surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(surf, (90, 50, 30), (0, 0, 100, 100), border_radius=6)
        pygame.draw.rect(surf, COLOR_GOLD, (10, 20, 80, 12))
        pygame.draw.rect(surf, COLOR_PURPLE, (20, 50, 60, 35), border_radius=4)
        return surf
    else:
        surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(surf, (160, 90, 40), (0, 20, 100, 75), border_radius=8)
        pygame.draw.rect(surf, (80, 85, 95), (0, 20, 100, 75), width=4, border_radius=8)
        pygame.draw.line(surf, COLOR_GOLD, (25, 40), (75, 75), 4)
        pygame.draw.line(surf, COLOR_GOLD, (75, 40), (25, 75), 4)
        return surf

SURF_DOOR     = draw_pixel_lobby_building("door")
SURF_SHOP     = draw_pixel_lobby_building("shop")
SURF_PETHOUSE = draw_pixel_lobby_building("pethouse")
SURF_VOCAB    = draw_pixel_lobby_building("vocab")
SURF_CHEST    = draw_pixel_lobby_building("chest")

# ==========================================
# 4. 手機虛擬控制與互動 UI
# ==========================================
class VirtualJoystick:
    def __init__(self, x, y, radius):
        self.base_rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.center = pygame.math.Vector2(x, y)
        self.stick = pygame.math.Vector2(x, y)
        self.radius = radius
        self.active_touch_id = None
        self.dir = pygame.math.Vector2(0, 0)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.active_touch_id is None:
                if self.base_rect.collidepoint(event.pos):
                    self.active_touch_id = "MOUSE"
                    self.update_stick(event.pos)
            elif event.type == pygame.MOUSEMOTION and self.active_touch_id == "MOUSE":
                self.update_stick(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and self.active_touch_id == "MOUSE":
                self.reset()
            elif event.type == pygame.FINGERDOWN and self.active_touch_id is None:
                pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
                if self.base_rect.collidepoint(pos):
                    self.active_touch_id = event.finger_id
                    self.update_stick(pos)
            elif event.type == pygame.FINGERMOTION and self.active_touch_id == event.finger_id:
                pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
                self.update_stick(pos)
            elif event.type == pygame.FINGERUP and self.active_touch_id == event.finger_id:
                self.reset()

    def update_stick(self, pos):
        self.stick = pygame.math.Vector2(pos)
        dist = self.stick.distance_to(self.center)
        if dist > self.radius:
            self.stick = self.center + (self.stick - self.center).normalize() * self.radius
        self.dir = (self.stick - self.center) / self.radius

    def reset(self):
        self.active_touch_id = None
        self.stick = pygame.math.Vector2(self.center)
        self.dir = pygame.math.Vector2(0, 0)

    def draw(self, surface):
        pygame.draw.circle(surface, (80, 90, 110), (int(self.center.x), int(self.center.y)), self.radius, 3)
        pygame.draw.circle(surface, (180, 190, 210), (int(self.stick.x), int(self.stick.y)), self.radius // 3)

class VirtualActionButton:
    def __init__(self, x, y, radius, text, color=COLOR_GOLD):
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.center = (x, y)
        self.radius = radius
        self.text = text
        self.color = color
        self.is_pressed = False
        self.just_pressed = False
        self.active_touch_id = None

    def update(self, events):
        self.just_pressed = False
        for event in events:
            pos = None
            touch_id = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos, touch_id = event.pos, "MOUSE"
            elif event.type == pygame.FINGERDOWN:
                pos, touch_id = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT), event.finger_id
            
            if pos and self.rect.collidepoint(pos) and self.active_touch_id is None:
                self.active_touch_id = touch_id
                self.is_pressed = True
                self.just_pressed = True

            elif (event.type == pygame.MOUSEBUTTONUP and self.active_touch_id == "MOUSE") or \
                 (event.type == pygame.FINGERUP and self.active_touch_id == getattr(event, 'finger_id', None)):
                self.is_pressed = False
                self.active_touch_id = None

    def draw(self, surface):
        col = (255, 255, 255) if self.is_pressed else self.color
        pygame.draw.circle(surface, col, self.center, self.radius)
        pygame.draw.circle(surface, COLOR_WHITE, self.center, self.radius, 3)
        txt = font_md.render(self.text, True, COLOR_BG_DARK)
        surface.blit(txt, txt.get_rect(center=self.center))

class Button:
    def __init__(self, x, y, w, h, text, color=COLOR_PANEL, hover_color=COLOR_BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface):
        m_pos = pygame.mouse.get_pos()
        col = self.hover_color if self.rect.collidepoint(m_pos) else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_WHITE, self.rect, width=1, border_radius=6)
        txt = font_md.render(self.text, True, COLOR_WHITE)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
                return True
            elif event.type == pygame.FINGERDOWN:
                pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
                if self.rect.collidepoint(pos):
                    return True
        return False

# ==========================================
# 5. 實體類別定義
# ==========================================
class Player:
    def __init__(self, name="勇者", job="戰士"):
        self.name = name; self.job = job
        self.level = 1; self.exp = 0; self.gold = 500
        self.hp = 100; self.max_hp = 100
        self.shield = 50; self.max_shield = 50
        self.attack = 15; self.skin = "預設皮膚"
        self.weapons = ["破舊短劍"]
        self.equipped_weapon = "破舊短劍"
        self.current_floor = 1
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 36, 36)
        self.apply_job_stats()

    def apply_job_stats(self):
        if self.job == "戰士":
            self.max_hp = 160; self.max_shield = 60; self.attack = 18; self.speed = 4.5
        elif self.job == "法師":
            self.max_hp = 90;  self.max_shield = 40; self.attack = 28; self.speed = 3.8
        elif self.job == "弓箭手":
            self.max_hp = 110; self.max_shield = 50; self.attack = 20; self.speed = 5.2
        self.hp = self.max_hp; self.shield = self.max_shield

    def get_total_attack(self):
        w_info = next((w for w in WEAPONS_DB if w["name"] == self.equipped_weapon), {"atk": 5})
        return self.attack + w_info["atk"]

    def add_exp(self, amount):
        self.exp += amount
        needed = self.level * 50
        if self.exp >= needed:
            self.exp -= needed; self.level += 1
            self.max_hp += 20; self.hp = self.max_hp
            self.shield = self.max_shield; self.attack += 4
            return True
        return False

    def to_dict(self):
        d = self.__dict__.copy()
        if "rect" in d: del d["rect"]
        return d

class Pet:
    def __init__(self, name, x=300, y=300):
        self.name = name; self.exp = 0; self.stage = 1
        self.x = x; self.y = y
        self.target_x = x; self.target_y = y
        self.speed = 2.0
        self.attack_cooldown = 0
        pet_info = next((p for p in PETS_DB if p["name"] == name), PETS_DB[0])
        self.base_atk = pet_info["atk"]
        self.req_exp = pet_info["req_exp"]

    def get_current_attack(self):
        return self.base_atk + (self.stage - 1) * 8

    def follow_target(self, tx, ty):
        dist = math.hypot(tx - self.x, ty - self.y)
        if dist > 45:
            angle = math.atan2(ty - self.y, tx - self.x)
            self.x += math.cos(angle) * (self.speed * 1.5)
            self.y += math.sin(angle) * (self.speed * 1.5)

    def update_ai(self):
        if math.hypot(self.target_x - self.x, self.target_y - self.y) < 10:
            if random.random() < 0.02:
                self.target_x = random.randint(100, SCREEN_WIDTH - 100)
                self.target_y = random.randint(150, SCREEN_HEIGHT - 100)
        else:
            angle = math.atan2(self.target_y - self.y, self.target_x - self.x)
            self.x += math.cos(angle) * self.speed
            self.y += math.sin(angle) * self.speed

    def feed(self, added_exp):
        self.exp += added_exp
        if self.exp >= self.req_exp and self.stage < 3:
            self.exp -= self.req_exp
            self.stage += 1
            self.req_exp = int(self.req_exp * 1.5)
            return True
        return False

    def get_stage_str(self):
        return {1: "幼年體(小)", 2: "成長體(中)", 3: "完全體(大)"}[self.stage]

    def to_dict(self):
        return {"name": self.name, "exp": self.exp, "stage": self.stage, "req_exp": self.req_exp}

class Bullet:
    def __init__(self, x, y, target_x, target_y, damage, color=COLOR_GOLD):
        self.rect = pygame.Rect(x, y, 10, 10)
        angle = math.atan2(target_y - y, target_x - x)
        self.vx = math.cos(angle) * 10; self.vy = math.sin(angle) * 10
        self.damage = damage
        self.color = color

    def update(self):
        self.rect.x += self.vx; self.rect.y += self.vy

    def draw(self, surface, cam_x, cam_y):
        sp = (self.rect.x - cam_x, self.rect.y - cam_y)
        pygame.draw.circle(surface, self.color, sp, 5)

class Monster:
    def __init__(self, x, y, m_type_idx, floor, is_boss=False):
        size = 64 if is_boss else 36
        m_info = MONSTER_TYPES[m_type_idx]
        self.rect = pygame.Rect(x, y, size, size)
        self.type_idx = m_type_idx
        self.name = f"👑 {m_info['name']} BOSS" if is_boss else m_info['name']
        floor_mult = 1.0 + (floor - 1) * 0.2
        self.hp = int(m_info['hp'] * (4 if is_boss else 1) * floor_mult)
        self.max_hp = self.hp
        self.attack = int(m_info['atk'] * (1.5 if is_boss else 1) * floor_mult)
        self.speed = m_info['speed']
        self.is_boss = is_boss

    def move_towards(self, px, py):
        angle = math.atan2(py - self.rect.centery, px - self.rect.centerx)
        self.rect.x += math.cos(angle) * self.speed
        self.rect.y += math.sin(angle) * self.speed

    def draw(self, surface, cam_x, cam_y):
        sp = (self.rect.x - cam_x, self.rect.y - cam_y)
        m_surf = draw_pixel_monster(self.type_idx, self.is_boss)
        surface.blit(m_surf, sp)
        if not self.is_boss:
            rate = max(0, self.hp / self.max_hp)
            pygame.draw.rect(surface, (40, 0, 0), (sp[0], sp[1] - 8, 36, 5))
            pygame.draw.rect(surface, COLOR_GREEN, (sp[0], sp[1] - 8, int(36 * rate), 5))

class GroundWeapon:
    def __init__(self, x, y, name):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.name = name

    def draw(self, surface, cam_x, cam_y):
        sp = (self.rect.x - cam_x, self.rect.y - cam_y)
        pygame.draw.circle(surface, COLOR_GOLD, (sp[0]+14, sp[1]+14), 18, width=1)
        screen.blit(draw_pixel_weapon(self.name), sp)

class HealthPack:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)

    def draw(self, surface, cam_x, cam_y):
        sp = (self.rect.x - cam_x, self.rect.y - cam_y)
        pygame.draw.circle(surface, COLOR_GREEN, (sp[0]+12, sp[1]+12), 16, width=1)
        screen.blit(draw_pixel_health_pack(), sp)

class Chest:
    def __init__(self, x, y, word_data):
        self.rect = pygame.Rect(x, y, 34, 34)
        self.word = word_data; self.is_opened = False

    def draw(self, surface, cam_x, cam_y):
        sp = (self.rect.x - cam_x, self.rect.y - cam_y)
        screen.blit(draw_pixel_chest(self.is_opened), sp)

# ==========================================
# 6. 核心遊戲引擎
# ==========================================
class GameEngine:
    def __init__(self):
        self.player = Player()
        self.favorite_ids = []
        self.learned_ids = []
        
        self.pets = [Pet("柴犬")]
        self.active_pet_idx = 0
        self.inventory_foods = {f["name"]: 2 for f in FOODS_DB}

        self.state = "LOBBY"
        self.stage_words = []; self.stage_chests = []; self.stage_monsters = []; self.bullets = []
        self.ground_weapons = []; self.health_packs = []
        self.current_boss = None
        
        self.current_wave = 1
        self.max_waves = 3
        self.boss_spawned = False
        self.boss_defeated = False

        self.current_quiz_chest = None; self.quiz_options = []
        self.info_msg = "歡迎！左側搖桿移動，右側按鈕互動。"

        self.countdown_timer = 0
        self.btn_global_back = Button(850, 15, 150, 40, "⬅️ 返回", COLOR_RED)

        # 虛擬觸控控制器
        self.joystick = VirtualJoystick(120, SCREEN_HEIGHT - 120, 75)
        self.btn_action = VirtualActionButton(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120, 45, "互動", COLOR_GOLD)
        self.btn_secondary = VirtualActionButton(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 220, 38, "出戰/切換", COLOR_PURPLE)

        # 建築物座標
        self.rect_door     = pygame.Rect(460, 70, 100, 80)
        self.rect_shop     = pygame.Rect(800, 90, 120, 90)
        self.rect_pethouse = pygame.Rect(800, 480, 120, 100)
        self.rect_vocab    = pygame.Rect(100, 90, 100, 100)
        self.rect_chest    = pygame.Rect(100, 480, 100, 100)

    def get_active_pet(self):
        if self.pets and 0 <= self.active_pet_idx < len(self.pets):
            return self.pets[self.active_pet_idx]
        return None

    def prepare_stage(self):
        unlearned = [w for w in ALL_VOCABULARY if w["id"] not in self.learned_ids]
        if len(unlearned) < 20: 
            self.stage_words = random.sample(ALL_VOCABULARY, min(20, len(ALL_VOCABULARY)))
        else: 
            self.stage_words = random.sample(unlearned, 20)
        for w in self.stage_words:
            if w["id"] not in self.learned_ids: 
                self.learned_ids.append(w["id"])
        self.state = "LEARN_STAGE"

    def spawn_wave(self, wave_num):
        self.stage_monsters = []
        m_count = 6 + self.player.current_floor * 2
        for _ in range(m_count):
            mx = random.randint(80, WORLD_WIDTH - 80)
            my = random.randint(80, WORLD_HEIGHT - 80)
            m_idx = min(self.player.current_floor - 1 + random.randint(0, 2), 19)
            self.stage_monsters.append(Monster(mx, my, m_idx, self.player.current_floor, is_boss=False))
        self.info_msg = f"⚔️ 第 {wave_num} / {self.max_waves} 波怪物來襲！"

    def init_dungeon(self):
        self.stage_chests = []
        random.shuffle(self.stage_words)
        idx = 0
        for r in range(4):
            for c in range(5):
                if idx < 20:
                    cx = int(80 + c * (WORLD_WIDTH - 160) / 4 + random.randint(-20, 20))
                    cy = int(80 + r * (WORLD_HEIGHT - 160) / 3 + random.randint(-20, 20))
                    self.stage_chests.append(Chest(cx, cy, self.stage_words[idx]))
                    idx += 1

        self.current_wave = 1
        self.spawn_wave(self.current_wave)

        self.current_boss = None
        self.boss_spawned = False
        self.boss_defeated = False

        self.player.rect.center = (WORLD_WIDTH//2, WORLD_HEIGHT//2)
        pet = self.get_active_pet()
        if pet: pet.x = self.player.rect.x + 30; pet.y = self.player.rect.y + 30

        self.bullets = []; self.ground_weapons = []; self.health_packs = []
        self.countdown_timer = 180
        self.state = "DUNGEON"

    async def run(self):
        running = True
        while running:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: running = False

            # 更新虛擬搖桿與按鈕
            self.joystick.update(events)
            self.btn_action.update(events)
            self.btn_secondary.update(events)

            screen.fill(COLOR_BG_DARK)

            if self.state == "LOBBY":
                self.handle_lobby(events)
            elif self.state == "LEARN_STAGE":
                self.handle_learn_stage(events)
            elif self.state == "DUNGEON":
                self.handle_dungeon(events)
            elif self.state == "QUIZ":
                self.handle_quiz(events)
            elif self.state == "PET_HOUSE":
                self.handle_pet_house(events)
            elif self.state == "SHOP":
                self.handle_shop(events)
            elif self.state == "VOCAB_BANK":
                self.handle_vocab_bank(events)
            elif self.state == "BACKPACK":
                self.handle_backpack(events)

            # 觸控 UI 覆蓋渲染
            if self.state in ["LOBBY", "DUNGEON", "PET_HOUSE"]:
                self.joystick.draw(screen)
                self.btn_action.draw(screen)
                if self.state in ["LOBBY", "PET_HOUSE"]:
                    self.btn_secondary.draw(screen)

            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()
        sys.exit()

    # ---------------- 1. 大廳 ----------------
    def handle_lobby(self, events):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]: dx -= self.player.speed
        if keys[pygame.K_d]: dx += self.player.speed
        if keys[pygame.K_w]: dy -= self.player.speed
        if keys[pygame.K_s]: dy += self.player.speed

        dx += self.joystick.dir.x * self.player.speed
        dy += self.joystick.dir.y * self.player.speed

        self.player.rect.x += dx; self.player.rect.y += dy
        self.player.rect.clamp_ip(pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))

        pet = self.get_active_pet()
        if pet: pet.follow_target(self.player.rect.centerx, self.player.rect.centery)

        screen.fill((45, 32, 28))
        for x in range(0, SCREEN_WIDTH, 64):
            pygame.draw.line(screen, (35, 22, 18), (x, 0), (x, SCREEN_HEIGHT), 2)
        pygame.draw.rect(screen, (150, 40, 40), (220, 180, 584, 360), border_radius=12)

        screen.blit(SURF_DOOR, self.rect_door)
        screen.blit(SURF_SHOP, self.rect_shop)
        screen.blit(SURF_PETHOUSE, self.rect_pethouse)
        screen.blit(SURF_VOCAB, self.rect_vocab)
        screen.blit(SURF_CHEST, self.rect_chest)

        def draw_label(text, rect, color=COLOR_GOLD):
            t_surf = font_sm.render(text, True, color)
            bg_rect = pygame.Rect(rect.centerx - t_surf.get_width()//2 - 6, rect.bottom + 4, t_surf.get_width() + 12, 22)
            pygame.draw.rect(screen, (20, 20, 25), bg_rect, border_radius=4)
            pygame.draw.rect(screen, color, bg_rect, width=1, border_radius=4)
            screen.blit(t_surf, (rect.centerx - t_surf.get_width()//2, rect.bottom + 6))

        draw_label("【 迷宮傳送門 】", self.rect_door, COLOR_GOLD)
        draw_label("【 補給商店 】", self.rect_shop, COLOR_RED)
        draw_label("【 寵物小屋 】", self.rect_pethouse, COLOR_PURPLE)
        draw_label("【 魔法單字庫 】", self.rect_vocab, COLOR_BLUE)
        draw_label("【 裝備軍火箱 】", self.rect_chest, COLOR_GREEN)

        screen.blit(draw_pixel_hero(self.player.job), self.player.rect)
        if pet:
            screen.blit(draw_pixel_pet(pet.name, pet.stage), (pet.x - 14, pet.y - 14))

        prompt_txt = None
        is_interact = keys[pygame.K_e] or self.btn_action.just_pressed

        if self.player.rect.colliderect(self.rect_door):
            prompt_txt = "點擊 [互動] 進入迷宮"
            if is_interact: self.prepare_stage()
        elif self.player.rect.colliderect(self.rect_shop):
            prompt_txt = "點擊 [互動] 進入商店"
            if is_interact: self.state = "SHOP"
        elif self.player.rect.colliderect(self.rect_pethouse):
            prompt_txt = "點擊 [互動] 進入寵物小屋"
            if is_interact: self.state = "PET_HOUSE"
        elif self.player.rect.colliderect(self.rect_vocab):
            prompt_txt = "點擊 [互動] 查看單字庫"
            if is_interact: self.state = "VOCAB_BANK"
        elif self.player.rect.colliderect(self.rect_chest):
            prompt_txt = "點擊 [互動] 開啟裝備背包"
            if is_interact: self.state = "BACKPACK"

        if prompt_txt:
            pygame.draw.rect(screen, (0, 0, 0, 180), (self.player.rect.x - 40, self.player.rect.y - 40, 180, 30), border_radius=6)
            screen.blit(font_sm.render(prompt_txt, True, COLOR_GOLD), (self.player.rect.x - 35, self.player.rect.y - 35))

        if self.btn_secondary.just_pressed:
            jobs = ["戰士", "法師", "弓箭手"]
            self.player.job = jobs[(jobs.index(self.player.job) + 1) % 3]
            self.player.apply_job_stats()
            self.info_msg = f"職業切換為【{self.player.job}】！"

        pet_str = f"出戰: {pet.name}(Lv.{pet.stage})" if pet else "無出戰寵物"
        info_txt = f"【{self.player.name}】Lv.{self.player.level} {self.player.job} | {pet_str} | 💰 {self.player.gold}"
        screen.blit(font_md.render(info_txt, True, COLOR_WHITE), (20, 20))
        screen.blit(font_md.render(self.info_msg, True, COLOR_GOLD), (50, SCREEN_HEIGHT - 35))

    # ---------------- 2. 寵物小屋 ----------------
    def handle_pet_house(self, events):
        keys = pygame.key.get_pressed()
        dx = self.joystick.dir.x * self.player.speed
        dy = self.joystick.dir.y * self.player.speed
        self.player.rect.x += dx; self.player.rect.y += dy
        self.player.rect.clamp_ip(pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))

        screen.fill((60, 45, 65))
        screen.blit(font_lg.render("🐾 寵物小屋 - 靠近點擊 [互動] 餵食 / [出戰] 設為出戰", True, COLOR_GOLD), (30, 20))
        self.btn_global_back.draw(screen)

        near_pet_idx = None
        for i, p in enumerate(self.pets):
            p.update_ai()
            pet_rect = pygame.Rect(p.x, p.y, 32, 32)
            screen.blit(draw_pixel_pet(p.name, p.stage), (p.x, p.y))
            is_active = (i == self.active_pet_idx)
            tag = "★出戰中" if is_active else ""
            screen.blit(font_sm.render(f"{p.name} ({p.get_stage_str()[:3]}) {tag}", True, COLOR_GOLD if is_active else COLOR_WHITE), (p.x - 15, p.y - 18))

            if self.player.rect.colliderect(pet_rect):
                near_pet_idx = i

        screen.blit(draw_pixel_hero(self.player.job), self.player.rect)

        if near_pet_idx is not None:
            p = self.pets[near_pet_idx]
            if keys[pygame.K_SPACE] or self.btn_secondary.just_pressed:
                self.active_pet_idx = near_pet_idx
                self.info_msg = f"🐾 【{p.name}】已設為出戰寵物！"
            elif keys[pygame.K_e] or self.btn_action.just_pressed:
                avail_food = next((k for k, v in self.inventory_foods.items() if v > 0), None)
                if avail_food:
                    self.inventory_foods[avail_food] -= 1
                    food_info = next(f for f in FOODS_DB if f["name"] == avail_food)
                    if p.feed(food_info["exp"]):
                        self.info_msg = f"🎉 寵物【{p.name}】成功進化為【{p.get_stage_str()}】！"
                    else:
                        self.info_msg = f"🍖 餵食了【{avail_food}】(+{food_info['exp']} EXP)！"
                else: 
                    self.info_msg = "❌ 庫存沒有食物，請去商店購買！"

        screen.blit(font_md.render(self.info_msg, True, COLOR_GOLD), (30, SCREEN_HEIGHT - 35))
        if self.btn_global_back.is_clicked(events): self.state = "LOBBY"

    # ---------------- 3. 補給商店 ----------------
    def handle_shop(self, events):
        screen.fill(COLOR_PANEL)
        screen.blit(font_lg.render("🛒 補給商店 (💰 金幣: " + str(self.player.gold) + ")", True, COLOR_GOLD), (30, 20))
        self.btn_global_back.draw(screen)

        screen.blit(font_md.render("🍎 購買食物:", True, COLOR_WHITE), (30, 70))
        food_btns = []
        for i, f_info in enumerate(FOODS_DB):
            bx = 30 + (i % 5) * 190; by = 105 + (i // 5) * 45
            screen.blit(draw_pixel_food(f_info["name"]), (bx, by + 6))
            b = Button(bx + 32, by, 145, 38, f"{f_info['name']} 💰{f_info['price']}", COLOR_GREEN)
            b.draw(screen); food_btns.append((b, f_info))

        screen.blit(font_md.render("🐾 購買寵物:", True, COLOR_WHITE), (30, 310))
        pet_buy_btns = []
        for i, p_info in enumerate(PETS_DB):
            bx = 30 + (i % 5) * 190; by = 345 + (i // 5) * 45
            screen.blit(draw_pixel_pet(p_info["name"]), (bx, by + 6))
            b = Button(bx + 32, by, 145, 38, f"{p_info['name']} 💰{p_info['price']}", COLOR_PURPLE)
            b.draw(screen); pet_buy_btns.append((b, p_info))

        screen.blit(font_md.render(self.info_msg, True, COLOR_GOLD), (30, 580))

        if self.btn_global_back.is_clicked(events): self.state = "LOBBY"
        for b, f_info in food_btns:
            if b.is_clicked(events):
                if self.player.gold >= f_info["price"]:
                    self.player.gold -= f_info["price"]
                    self.inventory_foods[f_info["name"]] = self.inventory_foods.get(f_info["name"], 0) + 1
                    self.info_msg = f"🛒 購買了【{f_info['name']}】！"
                else: self.info_msg = f"❌ 金幣不足！"
        for b, p_info in pet_buy_btns:
            if b.is_clicked(events):
                if self.player.gold >= p_info["price"]:
                    self.player.gold -= p_info["price"]
                    self.pets.append(Pet(p_info["name"]))
                    self.info_msg = f"🛒 成功購買強力寵物【{p_info['name']}】！"
                else: self.info_msg = f"❌ 金幣不足！"

    # ---------------- 4. 裝備背包 ----------------
    def handle_backpack(self, events):
        screen.fill(COLOR_PANEL)
        screen.blit(font_lg.render("🧰 裝備軍火背包 - 選擇出戰武器", True, COLOR_GOLD), (30, 20))
        self.btn_global_back.draw(screen)

        screen.blit(font_md.render(f"目前裝備: 【{self.player.equipped_weapon}】", True, COLOR_WHITE), (30, 70))

        w_btns = []
        for i, w_name in enumerate(self.player.weapons):
            bx = 30 + (i % 4) * 230; by = 120 + (i // 4) * 60
            screen.blit(draw_pixel_weapon(w_name), (bx, by + 10))
            is_eq = (w_name == self.player.equipped_weapon)
            w_info = next((w for w in WEAPONS_DB if w["name"] == w_name), {"atk": 5})
            b = Button(bx + 32, by, 180, 45, f"{w_name} (+{w_info['atk']})", COLOR_GOLD if is_eq else COLOR_BLUE)
            b.draw(screen); w_btns.append((b, w_name))

        if self.btn_global_back.is_clicked(events): self.state = "LOBBY"
        for b, w_name in w_btns:
            if b.is_clicked(events):
                self.player.equipped_weapon = w_name
                self.info_msg = f"⚔️ 已裝備【{w_name}】！"

    # ---------------- 5. 迷宮戰鬥 ----------------
    def handle_dungeon(self, events):
        cam_x = max(0, min(self.player.rect.centerx - SCREEN_WIDTH // 2, WORLD_WIDTH - SCREEN_WIDTH))
        cam_y = max(0, min(self.player.rect.centery - SCREEN_HEIGHT // 2, WORLD_HEIGHT - SCREEN_HEIGHT))

        pet = self.get_active_pet()

        if self.countdown_timer > 0:
            self.countdown_timer -= 1
        else:
            dx = self.joystick.dir.x * self.player.speed
            dy = self.joystick.dir.y * self.player.speed
            self.player.rect.x += dx; self.player.rect.y += dy
            self.player.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))

            if pet:
                pet.follow_target(self.player.rect.centerx, self.player.rect.centery)
                pet.attack_cooldown += 1
                if pet.attack_cooldown >= 45:
                    target_enemy = None
                    min_dist = 350
                    all_targets = self.stage_monsters + ([self.current_boss] if self.current_boss else [])
                    for tgt in all_targets:
                        d = math.hypot(tgt.rect.centerx - pet.x, tgt.rect.centery - pet.y)
                        if d < min_dist:
                            min_dist = d
                            target_enemy = tgt
                    if target_enemy:
                        pet.attack_cooldown = 0
                        self.bullets.append(Bullet(pet.x, pet.y, target_enemy.rect.centerx, target_enemy.rect.centery, pet.get_current_attack(), COLOR_PURPLE))

            # 觸控與點擊射擊 (自動過濾虛擬按鍵區域)
            for event in events:
                pos = None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = event.pos
                elif event.type == pygame.FINGERDOWN:
                    pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)

                if pos:
                    if not self.joystick.base_rect.collidepoint(pos) and \
                       not self.btn_action.rect.collidepoint(pos) and \
                       not self.btn_global_back.rect.collidepoint(pos):
                        mx, my = pos
                        if my > 80:
                            self.bullets.append(Bullet(self.player.rect.centerx, self.player.rect.centery, mx + cam_x, my + cam_y, self.player.get_total_attack()))

            for b in self.bullets[:]:
                b.update()
                if not pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT).contains(b.rect):
                    self.bullets.remove(b); continue
                
                if self.current_boss and b.rect.colliderect(self.current_boss.rect):
                    self.current_boss.hp -= b.damage
                    if b in self.bullets: self.bullets.remove(b)
                    if self.current_boss.hp <= 0:
                        self.current_boss = None
                        self.boss_defeated = True
                        self.player.gold += 300
                        self.player.add_exp(150)
                        self.info_msg = "🏆 成功擊敗本層 BOSS！"
                    continue

                for m in self.stage_monsters[:]:
                    if b.rect.colliderect(m.rect):
                        m.hp -= b.damage
                        if b in self.bullets: self.bullets.remove(b)
                        if m.hp <= 0:
                            self.stage_monsters.remove(m)
                            self.player.gold += random.randint(20, 40)
                            self.player.add_exp(25)
                            if random.random() < 0.25:
                                weights = [w["weight"] for w in WEAPONS_DB]
                                chosen_w = random.choices(WEAPONS_DB, weights=weights, k=1)[0]["name"]
                                self.ground_weapons.append(GroundWeapon(m.rect.x, m.rect.y, chosen_w))
                        break

            for gw in self.ground_weapons[:]:
                if self.player.rect.colliderect(gw.rect):
                    if gw.name not in self.player.weapons:
                        self.player.weapons.append(gw.name)
                        self.info_msg = f"🎉 拾獲新神兵【{gw.name}】！已存入背包。"
                    self.ground_weapons.remove(gw)

            for hp_pack in self.health_packs[:]:
                if self.player.rect.colliderect(hp_pack.rect):
                    heal = int(self.player.max_hp * 0.2)
                    self.player.hp = min(self.player.max_hp, self.player.hp + heal)
                    self.info_msg = f"💖 拾取回血包！(+{heal} HP)！"
                    self.health_packs.remove(hp_pack)

            if len(self.stage_monsters) == 0:
                if self.current_wave < self.max_waves:
                    self.current_wave += 1
                    self.spawn_wave(self.current_wave)
                elif not self.boss_spawned and not self.boss_defeated:
                    boss_m_idx = min(self.player.current_floor * 2 - 1, 19)
                    self.current_boss = Monster(WORLD_WIDTH//2, WORLD_HEIGHT//2, boss_m_idx, self.player.current_floor, is_boss=True)
                    self.boss_spawned = True
                    self.info_msg = f"⚠️ 警告！【{self.current_boss.name}】降臨了！"

            if self.current_boss:
                self.current_boss.move_towards(self.player.rect.centerx, self.player.rect.centery)
                if self.current_boss.rect.colliderect(self.player.rect):
                    if self.player.shield > 0: self.player.shield -= 0.6
                    else: self.player.hp -= 0.5

            for m in self.stage_monsters:
                m.move_towards(self.player.rect.centerx, self.player.rect.centery)
                if m.rect.colliderect(self.player.rect):
                    if self.player.shield > 0: self.player.shield -= 0.4
                    else: self.player.hp -= 0.3

            if self.player.hp <= 0:
                self.player.hp = self.player.max_hp; self.player.shield = self.player.max_shield
                self.info_msg = "💀 你在迷宮中戰敗！"
                self.state = "LOBBY"; return

            for chest in self.stage_chests:
                if not chest.is_opened and self.player.rect.colliderect(chest.rect):
                    self.current_quiz_chest = chest
                    correct_zh = chest.word["zh"]
                    wrong_choices = [w["zh"] for w in ALL_VOCABULARY if w["zh"] != correct_zh]
                    opts = random.sample(wrong_choices, min(3, len(wrong_choices))) + [correct_zh]
                    random.shuffle(opts)
                    self.quiz_options = opts
                    self.state = "QUIZ"; break

        # 迷宮繪製
        tile_size = 64
        for x in range(0, SCREEN_WIDTH + tile_size, tile_size):
            for y in range(0, SCREEN_HEIGHT + tile_size, tile_size):
                col = COLOR_DUNGEON_1 if ((x+int(cam_x))//tile_size + (y+int(cam_y))//tile_size) % 2 == 0 else COLOR_DUNGEON_2
                pygame.draw.rect(screen, col, (x - (cam_x % tile_size), y - (cam_y % tile_size), tile_size, tile_size))

        for c in self.stage_chests: c.draw(screen, cam_x, cam_y)
        for gw in self.ground_weapons: gw.draw(screen, cam_x, cam_y)
        for hp_pack in self.health_packs: hp_pack.draw(screen, cam_x, cam_y)
        for m in self.stage_monsters: m.draw(screen, cam_x, cam_y)
        if self.current_boss: self.current_boss.draw(screen, cam_x, cam_y)
        
        if pet:
            screen.blit(draw_pixel_pet(pet.name, pet.stage), (pet.x - cam_x - 14, pet.y - cam_y - 14))
        screen.blit(draw_pixel_hero(self.player.job), (self.player.rect.x - cam_x, self.player.rect.y - cam_y))
        for b in self.bullets: b.draw(screen, cam_x, cam_y)

        # 頂部 HUD
        pygame.draw.rect(screen, (15, 18, 24), (0, 0, SCREEN_WIDTH, 50))
        wave_str = f"第 {self.current_wave}/{self.max_waves} 波" if not self.boss_spawned else "BOSS 決戰"
        screen.blit(font_md.render(f"HP: {int(self.player.hp)}/{self.player.max_hp} | 護盾: {int(self.player.shield)} | 【{wave_str}】 | 💰 {self.player.gold}", True, COLOR_WHITE), (20, 12))
        self.btn_global_back.draw(screen)

        if self.current_boss:
            pygame.draw.rect(screen, (40, 0, 0), (250, 60, 524, 20), border_radius=4)
            b_rate = max(0, self.current_boss.hp / self.current_boss.max_hp)
            pygame.draw.rect(screen, COLOR_RED, (250, 60, int(524 * b_rate), 20), border_radius=4)
            screen.blit(font_sm.render(f"{self.current_boss.name} HP: {int(self.current_boss.hp)}/{self.current_boss.max_hp}", True, COLOR_WHITE), (400, 62))

        if self.countdown_timer > 0:
            sec_left = (self.countdown_timer // 60) + 1
            txt_cd = font_huge.render(f"{sec_left}", True, COLOR_GOLD)
            screen.blit(txt_cd, txt_cd.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

        if len(self.stage_monsters) == 0 and self.boss_defeated and all(c.is_opened for c in self.stage_chests):
            self.player.current_floor += 1
            self.info_msg = f"🎉 成功晉級至第 {self.player.current_floor} 層！"
            self.state = "LOBBY"

        if self.btn_global_back.is_clicked(events): self.state = "LOBBY"

    # ---------------- 6. 單字預習 ----------------
    def handle_learn_stage(self, events):
        screen.fill(COLOR_PANEL)
        screen.blit(font_lg.render(f"📖 第 {self.player.current_floor} 層 - 單字預習 (點擊卡片收藏 ★)", True, COLOR_GOLD), (30, 20))
        btn_start = Button(680, 15, 160, 40, "🚀 出發", COLOR_GREEN)
        btn_start.draw(screen); self.btn_global_back.draw(screen)

        card_rects = []
        for i, w in enumerate(self.stage_words):
            col = i % 4; row = i // 4
            x = 30 + col * 240; y = 75 + row * 120
            is_fav = w["id"] in self.favorite_ids
            box_col = (50, 60, 80) if not is_fav else (75, 65, 30)
            c_rect = pygame.Rect(x, y, 220, 105)
            pygame.draw.rect(screen, box_col, c_rect, border_radius=6)
            pygame.draw.rect(screen, COLOR_GOLD if is_fav else COLOR_GRAY, c_rect, width=1, border_radius=6)
            
            star = "★" if is_fav else "☆"
            screen.blit(font_md.render(f"{star} {w['jp']}", True, COLOR_GOLD if is_fav else COLOR_WHITE), (x+10, y+10))
            screen.blit(font_sm.render(f"({w['romaji']})", True, COLOR_GRAY), (x+10, y+42))
            screen.blit(font_md.render(f"{w['zh']}", True, COLOR_GREEN), (x+10, y+68))
            card_rects.append((c_rect, w))

        if btn_start.is_clicked(events): self.init_dungeon()
        elif self.btn_global_back.is_clicked(events): self.state = "LOBBY"
        
        for event in events:
            pos = None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: pos = event.pos
            elif event.type == pygame.FINGERDOWN: pos = (event.x * SCREEN_WIDTH, event.y * SCREEN_HEIGHT)
            if pos:
                for c_rect, w in card_rects:
                    if c_rect.collidepoint(pos):
                        if w["id"] in self.favorite_ids:
                            self.favorite_ids.remove(w["id"])
                            self.info_msg = f"☆ 取消收藏【{w['jp']}】"
                        else:
                            self.favorite_ids.append(w["id"])
                            self.info_msg = f"★ 已收藏【{w['jp']}】！"

    # ---------------- 7. 寶箱單字問答 ----------------
    def handle_quiz(self, events):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220); overlay.fill((10, 15, 20))
        screen.blit(overlay, (0, 0))

        dialog = pygame.Rect(200, 140, 624, 440)
        pygame.draw.rect(screen, COLOR_PANEL, dialog, border_radius=12)
        pygame.draw.rect(screen, COLOR_GOLD, dialog, width=2, border_radius=12)

        word = self.current_quiz_chest.word
        screen.blit(font_lg.render("📦 寶箱解鎖問答", True, COLOR_GOLD), (dialog.x + 210, dialog.y + 30))
        screen.blit(font_lg.render(f"請問『 {word['jp']} 』({word['romaji']}) 的意思？", True, COLOR_WHITE), (dialog.x + 60, dialog.y + 90))

        btn_opts = []
        for i, opt in enumerate(self.quiz_options):
            bx = dialog.x + 50 + (i % 2) * 270; by = dialog.y + 180 + (i // 2) * 90
            b = Button(bx, by, 250, 60, f"{i+1}. {opt}")
            b.draw(screen); btn_opts.append((b, opt))

        for b, opt in btn_opts:
            if b.is_clicked(events):
                if opt == word["zh"]:
                    g = random.randint(30, 80); self.player.gold += g
                    self.current_quiz_chest.is_opened = True
                    if random.random() < 0.45:
                        self.health_packs.append(HealthPack(self.current_quiz_chest.rect.x, self.current_quiz_chest.rect.y))
                        self.info_msg = f"✨ 答對了！獲得 💰 {g} 金幣與 💖 回血包！"
                    else:
                        self.info_msg = f"✨ 答對了！開啟寶箱獲得 💰 {g} 金幣！"
                else:
                    self.info_msg = f"❌ 答錯了！正確答案是『{word['zh']}』。"
                self.state = "DUNGEON"

    # ---------------- 8. 單字收藏庫 ----------------
    def handle_vocab_bank(self, events):
        screen.fill(COLOR_PANEL)
        screen.blit(font_lg.render("⭐ 單字收藏庫", True, COLOR_GOLD), (30, 20))
        self.btn_global_back.draw(screen)

        fav_words = [w for w in ALL_VOCABULARY if w["id"] in self.favorite_ids]
        if not fav_words: 
            screen.blit(font_md.render("尚無收藏單字！在預習介面點擊單字卡即可收藏。", True, COLOR_WHITE), (50, 120))
        else:
            for i, w in enumerate(fav_words[:14]):
                screen.blit(font_md.render(f"★ [{w['jp']}] ({w['romaji']}) = {w['zh']}", True, COLOR_GOLD), (50, 85 + i * 36))

        if self.btn_global_back.is_clicked(events): self.state = "LOBBY"

# ==========================================
# 7. 啟動進入點 (相容 Pygbag)
# ==========================================
if __name__ == "__main__":
    game = GameEngine()
    asyncio.run(game.run())
