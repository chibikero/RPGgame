import pyxel
import math
import random

print("DEBUG: Script started. Importing modules.")

# --- 定数 ---
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 224
TILE_SIZE = 8
PLAYER_BASE_SPEED = 1.5

# ゲームシーン定義
SCENE_TITLE = 0
SCENE_OPENING = 1
SCENE_MAP = 2
SCENE_BATTLE = 3
SCENE_GAMEOVER = 4
SCENE_VICTORY = 5
SCENE_CLEAR = 6

# マップデータ (0: 通路, 1: 壁, 2: NPC, 3: エンカウント, 4: クリアタイル)
# ★★★ ご提示いただいた新しいMAP_DATA_RAWに差し替え ★★★
MAP_DATA_RAW = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,2,1,0,0,0,1,2,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,3,3,3,1,0,0,0,1,0,0,0,1,0,0,3,0,1,0,0,0,3,3,3,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,3,2,3,1,0,1,0,1,0,1,0,1,0,1,3,0,1,1,1,0,3,2,3,0,1,1,1],
    [1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,3,3,3,1,0,1,0,0,0,1,0,0,0,1,3,0,1,0,0,0,3,3,3,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,3,0,0,0,0,0,0,0,0,0,0,1], # Corrected line 11, removed extra 0
    [1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,3,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1], # Corrected line 20, changed last 1 to 0
    [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1], # Line 22
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1], # Line 23
    [1,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,3,3,3,0,0,0,1,0,0,0,3,3,3,0,0,0,1],
    [1,1,1,0,1,0,1,0,1,1,1,1,1,3,2,3,1,1,1,1,1,1,1,3,2,3,1,1,1,1,1,1,1,3,2,3,1,1,0,1,1,1,0,3,2,3,0,1,1,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,3,3,3,0,0,0,0,0,0,0,3,3,3,0,0,0,1,0,0,0,3,3,3,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1], 
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1],
    [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    # Corrected: Added one more outer wall at the very end
]
# ----------------------------------------------------

MAP_WIDTH_TILES = len(MAP_DATA_RAW[0])
MAP_HEIGHT_TILES = len(MAP_DATA_RAW)
MAP_WIDTH_PX = MAP_WIDTH_TILES * TILE_SIZE
MAP_HEIGHT_PX = MAP_HEIGHT_TILES * TILE_SIZE

# --- Helper Classes ---
class DamageText:
    def __init__(self, text, x, y, color=8, duration=45):
        self.text = str(text); self.x = x; self.y = y
        self.color = color; self.duration = duration
    def update(self):
        self.duration -= 1; self.y -= 0.5
        return self.duration <= 0
    def draw(self):
        pyxel.text(int(self.x), int(self.y), self.text, self.color)

class GameObject:
    def __init__(self, x, y, img_u, img_v, img_w, img_h, colkey=0):
        self.x = float(x); self.y = float(y)
        self.sprite_u, self.sprite_v = img_u, img_v
        self.sprite_w, self.sprite_h = img_w, img_h
        self.colkey = colkey
    def draw(self):
        pyxel.blt(int(self.x), int(self.y), 0, self.sprite_u, self.sprite_v,
                  self.sprite_w, self.sprite_h, self.colkey)

# --- Character Classes ---
class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, TILE_SIZE, TILE_SIZE) # U,V will be set by update_animation
        self.speed = PLAYER_BASE_SPEED; self.is_moving = False
        # ★★★ Player.anim_sprites を setup_assets_programmatically の描画に合わせる ★★★
        self.anim_sprites = {
            "down":  [(0,0), (8,0)],
            "left":  [(0,8), (8,8)],
            "right": [(0,16), (8,16)], # 修正: V座標を16に
            "up":    [(0,24), (8,24)]   # 修正: V座標を24に
        }
        # ★★★ ここまで ★★★
        self.direction = "down"; self.anim_frame_index = 0; self.anim_timer = 0; self.anim_speed = 8
        self.max_hp = 30; self.hp = self.max_hp; self.attack_power = 8
        self.is_hit_flash = 0

    def update_animation(self):
        if self.is_moving:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.anim_frame_index = (self.anim_frame_index + 1) % len(self.anim_sprites[self.direction])
        else: self.anim_frame_index = 0
        cs = self.anim_sprites[self.direction][self.anim_frame_index]
        self.sprite_u, self.sprite_v = cs[0], cs[1]

    def move(self, dx, dy, game_map, game_instance): # game_map is now the Python list
        self.is_moving = (dx != 0 or dy != 0)
        if not self.is_moving: self.update_animation(); return

        if dy > 0: self.direction = "down"
        elif dy < 0: self.direction = "up"
        if dx > 0: self.direction = "right"
        elif dx < 0: self.direction = "left"

        actual_dx, actual_dy = dx, dy
        if dx != 0 and dy != 0: actual_dx /= math.sqrt(2); actual_dy /= math.sqrt(2)

        prev_tile_x = int((self.x + self.sprite_w / 2) // TILE_SIZE)
        prev_tile_y = int((self.y + self.sprite_h / 2) // TILE_SIZE)
        try_x, try_y = self.x + actual_dx, self.y + actual_dy
        coll_offset = 2

        can_move_x = True
        if actual_dx != 0:
            check_x_edge = try_x + (self.sprite_w - 1 - coll_offset if actual_dx > 0 else coll_offset)
            tile_x_to_check = int(check_x_edge // TILE_SIZE)
            tile_y1 = int((self.y + coll_offset) // TILE_SIZE)
            tile_y2 = int((self.y + self.sprite_h - 1 - coll_offset) // TILE_SIZE)
            if not (0 <= tile_x_to_check < MAP_WIDTH_TILES and
                    0 <= tile_y1 < MAP_HEIGHT_TILES and 0 <= tile_y2 < MAP_HEIGHT_TILES and
                    game_map[tile_y1][tile_x_to_check] != 1 and
                    game_map[tile_y2][tile_x_to_check] != 1): can_move_x = False
        if can_move_x: self.x = try_x
        else:
            if actual_dx > 0: self.x = float(tile_x_to_check * TILE_SIZE - self.sprite_w)
            else: self.x = float((tile_x_to_check + 1) * TILE_SIZE)

        can_move_y = True
        if actual_dy != 0:
            check_y_edge = try_y + (self.sprite_h - 1 - coll_offset if actual_dy > 0 else coll_offset)
            tile_y_to_check = int(check_y_edge // TILE_SIZE)
            tile_x1 = int((self.x + coll_offset) // TILE_SIZE)
            tile_x2 = int((self.x + self.sprite_w - 1 - coll_offset) // TILE_SIZE)
            if not (0 <= tile_y_to_check < MAP_HEIGHT_TILES and
                    0 <= tile_x1 < MAP_WIDTH_TILES and 0 <= tile_x2 < MAP_WIDTH_TILES and
                    game_map[tile_y_to_check][tile_x1] != 1 and
                    game_map[tile_y_to_check][tile_x2] != 1): can_move_y = False
        if can_move_y: self.y = try_y
        else:
            if actual_dy > 0: self.y = float(tile_y_to_check * TILE_SIZE - self.sprite_h)
            else: self.y = float((tile_y_to_check + 1) * TILE_SIZE)
            
        self.x = max(0.0, min(self.x, float(MAP_WIDTH_PX - self.sprite_w)))
        self.y = max(0.0, min(self.y, float(MAP_HEIGHT_PX - self.sprite_h)))
        
        current_tile_x = int((self.x + self.sprite_w / 2) // TILE_SIZE)
        current_tile_y = int((self.y + self.sprite_h / 2) // TILE_SIZE)
        if (current_tile_x != prev_tile_x or current_tile_y != prev_tile_y):
             if 0 <= current_tile_y < MAP_HEIGHT_TILES and 0 <= current_tile_x < MAP_WIDTH_TILES:
                tile_type_entered = game_map[current_tile_y][current_tile_x]
                if tile_type_entered == 3 and random.random() < 0.25:
                    game_instance.start_battle()
                elif tile_type_entered == 4:
                    game_instance.game_clear()
        self.update_animation()

    def take_damage(self, amount):
        self.hp -= amount; self.hp = max(0, self.hp)
        self.is_hit_flash = 10; return self.hp <= 0
    def draw_battle_status(self, x, y): # オリジナルはフォントレンダラなし
        if self.is_hit_flash > 0:
            if pyxel.frame_count % 4 < 2: pass
            self.is_hit_flash -= 1
        pyxel.text(x, y, f"PLAYER HP: {self.hp}/{self.max_hp}", 7)

class NPC(GameObject):
    def __init__(self, tile_x, tile_y, message): 
        super().__init__(tile_x * TILE_SIZE, tile_y * TILE_SIZE, 16, 0, TILE_SIZE, TILE_SIZE) # NPC sprite at (16,0)
        self.message = message

class Enemy(GameObject):
    def __init__(self, name, x, y, img_u, img_v, hp, attack):
        super().__init__(x, y, img_u, img_v, TILE_SIZE * 2, TILE_SIZE * 2)
        self.name = name; self.max_hp = hp; self.hp = hp; self.attack_power = attack
        self.is_dead = False; self.is_hit_flash = 0; self.death_animation_timer = 0; self.visible = True
    def take_damage(self, amount):
        self.hp -= amount; self.hp = max(0, self.hp)
        if self.hp <= 0: self.is_dead = True; self.death_animation_timer = 60
        self.is_hit_flash = 10; return self.is_dead
    def attack(self, target_player):
        damage = self.attack_power; target_player.take_damage(damage); return damage
    def update_death_animation(self):
        if self.death_animation_timer > 0:
            self.death_animation_timer -= 1; self.visible = (self.death_animation_timer // 5) % 2 != 0
            if self.death_animation_timer == 0: self.visible = False
            return True
        return False
    def draw(self):
        if not self.visible: return
        super().draw()

# --- Main Game Class ---
class Game:
    def __init__(self):
        print("DEBUG: Game __init__ - Pyxel init call soon.")
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel RPG - Vast Lands", fps=60) # Title updated
        print("DEBUG: Pyxel initialized.")
        
        self.setup_assets_programmatically() 
        print("DEBUG: Assets setup programmatically.")
        
        self.scene = SCENE_TITLE
        
        self.game_map_data = [row[:] for row in MAP_DATA_RAW]
        self.player = Player(TILE_SIZE * 1, TILE_SIZE * 1) 
        self.npcs = []
        self.load_map_objects() 
        print("DEBUG: Map objects loaded from MAP_DATA_RAW.")
        
        self.message_to_display = None; self.message_timer = 0
        self.opening_message_lines = [
            "The Sunstone, source of all light,",
            "has been stolen by the Shadow Lord.",
            "Darkness creeps across the land...",
            "",
            "A hero must venture into the",
            "Cursed Labyrinth to retrieve it.",
            "",
            "You are that hero."
        ]
        self.opening_current_line_block = 0
        self.opening_timer = 0
        self.opening_line_display_time = 150

        self.camera_x = float(self.player.x - SCREEN_WIDTH / 2)
        self.camera_y = float(self.player.y - SCREEN_HEIGHT / 2)
        pyxel.camera(int(self.camera_x), int(self.camera_y)); print("DEBUG: Initial camera set.")
        
        self.current_enemy = None; self.battle_message = ""; self.battle_command_index = 0
        self.battle_turn = "player"; self.battle_sub_scene_timer = 0
        self.game_clear_timer = 0; self.game_clear_phase = 0; self.final_clear_display_timer = 0
        self.damage_texts = []; self.screen_flash_timer = 0
        self.enemies_defeated_count = 0 
        print("DEBUG: Game state variables initialized.")
        print("DEBUG: Starting Pyxel main loop (pyxel.run).")
        pyxel.run(self.update, self.draw)
        print("DEBUG: Pyxel main loop finished.")

    def setup_assets_programmatically(self):
        # オリジナルのpyxel.image(0)のまま
        pyxel.image(0).cls(0)
        # Player Down (0,0), (8,0)
        pyxel.image(0).rect(0,0,8,8,7); pyxel.image(0).pset(3,5,0); pyxel.image(0).pset(4,5,0)
        pyxel.image(0).rect(8,0,8,8,7); pyxel.image(0).pset(2,5,0); pyxel.image(0).pset(5,5,0)
        # Player Left (0,8), (8,8)
        pyxel.image(0).rect(0,8,8,8,7); pyxel.image(0).pset(2,3,0)
        pyxel.image(0).rect(8,8,8,8,7); pyxel.image(0).pset(2,4,0)
        # Player Right (0,16), (8,16) <-- This matches the corrected Player.anim_sprites
        pyxel.image(0).rect(0,16,8,8,7); pyxel.image(0).pset(5,3,0)
        pyxel.image(0).rect(8,16,8,8,7); pyxel.image(0).pset(5,4,0)
        # Player Up (0,24), (8,24) <-- This matches the corrected Player.anim_sprites
        pyxel.image(0).rect(0,24,8,8,7) # Simple up
        pyxel.image(0).rect(8,24,8,8,7) # Simple up alt

        # NPC sprite (U=16, V=0)
        pyxel.image(0).rect(16,0,8,8,10); pyxel.image(0).pset(16+3,3,0); pyxel.image(0).pset(16+4,3,0)
        # Wall tile (U=24, V=0)
        pyxel.image(0).rect(24,0,8,8,5); pyxel.image(0).rectb(24,0,8,8,6)
        # Enemy sprite (U=32, V=0から16x16)
        pyxel.image(0).circ(32+8,0+8,7,11); pyxel.image(0).circ(32+8,0+7,3,3)
        pyxel.image(0).rect(32+5,0+5,2,2,0); pyxel.image(0).rect(32+9,0+5,2,2,0)
        # Clear Tile sprite (U=40, V=0)
        pyxel.image(0).pset(40+4, 0+1, 10); pyxel.image(0).pset(40+3, 0+2, 10); pyxel.image(0).pset(40+5, 0+2, 10)
        pyxel.image(0).line(40+1, 0+3, 40+7, 0+3, 10); pyxel.image(0).pset(40+2, 0+4, 10); pyxel.image(0).pset(40+6, 0+4, 10)
        pyxel.image(0).pset(40+1, 0+5, 10); pyxel.image(0).pset(40+7, 0+5, 10); pyxel.image(0).pset(40+4, 0+6, 10)
        # Big "GAME CLEAR!" letters
        pyxel.image(0).rect(0,32+2,12,2,7); pyxel.image(0).rect(0,32+2,2,10,7); pyxel.image(0).rect(0,32+12,12,2,7); pyxel.image(0).rect(10,32+8,2,4,7); pyxel.image(0).rect(6,32+8,4,2,7) #G
        pyxel.image(0).rect(16+2,32+14,12,2,7); pyxel.image(0).rect(16+2,32+2,2,12,7); pyxel.image(0).rect(16+12,32+2,2,12,7); pyxel.image(0).rect(16+4,32+2,8,2,7); pyxel.image(0).rect(16+4,32+8,8,2,7) #A
        pyxel.image(0).rect(32+1,32+2,2,14,7); pyxel.image(0).rect(32+13,32+2,2,14,7); pyxel.image(0).pset(32+3,32+3,7); pyxel.image(0).pset(32+4,32+4,7); pyxel.image(0).pset(32+5,32+5,7); pyxel.image(0).pset(32+6,32+6,7); pyxel.image(0).pset(32+7,32+7,7); pyxel.image(0).pset(32+8,32+6,7); pyxel.image(0).pset(32+9,32+5,7); pyxel.image(0).pset(32+10,32+4,7); pyxel.image(0).pset(32+11,32+3,7) #M
        pyxel.image(0).rect(48+2,32+2,12,2,7); pyxel.image(0).rect(48+2,32+2,2,14,7); pyxel.image(0).rect(48+2,32+8,10,2,7); pyxel.image(0).rect(48+2,32+14,12,2,7) #E
        pyxel.image(0).rect(80+4,32+2,8,2,7); pyxel.image(0).rect(80+2,32+4,2,10,7); pyxel.image(0).rect(80+4,32+14,8,2,7) #C
        pyxel.image(0).rect(96+2,32+2,2,14,7); pyxel.image(0).rect(96+2,32+14,12,2,7) #L
        pyxel.image(0).rect(112+2,32+2,12,2,7); pyxel.image(0).rect(112+2,32+2,2,14,7); pyxel.image(0).rect(112+2,32+8,10,2,7); pyxel.image(0).rect(112+2,32+14,12,2,7) #E
        pyxel.image(0).rect(128+2,32+14,12,2,7); pyxel.image(0).rect(128+2,32+2,2,12,7); pyxel.image(0).rect(128+12,32+2,2,12,7); pyxel.image(0).rect(128+4,32+2,8,2,7); pyxel.image(0).rect(128+4,32+8,8,2,7) #A
        pyxel.image(0).rect(144+2,32+2,2,14,7); pyxel.image(0).rect(144+2,32+2,10,2,7); pyxel.image(0).rect(144+10,32+3,2,5,7); pyxel.image(0).rect(144+2,32+8,10,2,7); pyxel.image(0).line(144+7,32+10,144+12,32+15,7); pyxel.image(0).line(144+6,32+10,144+11,32+15,7) #R
        pyxel.image(0).rect(160+7,32+2,2,10,7); pyxel.image(0).rect(160+7,32+14,2,2,7) #!

    def load_map_objects(self):
        self.npcs.clear()
        for r_idx, row in enumerate(self.game_map_data):
            for c_idx, tile_type in enumerate(row):
                if tile_type == 2:
                    if r_idx == 1 and c_idx == 38: message = "The path to the Sunstone is long\nand fraught with peril. Good luck."
                    elif r_idx == 4 and c_idx == 44: message = "This maze twists and turns...\nMany have been lost."
                    elif r_idx == 8 and c_idx == 24: message = "Shadows lurk in these halls.\nBe ever vigilant."
                    elif r_idx == 21 and c_idx == 1: message = "A hero! We have awaited your arrival.\nThe kingdom needs you."
                    elif r_idx == 21 and c_idx == 38: message = "The Sunstone... its power is\nthe key to our salvation."
                    elif r_idx == 21 and c_idx == 48: message = "The exit to the south is blocked\nby a powerful guardian, they say."
                    elif r_idx == 32 and c_idx == 37: message = "You are near the end, hero!\nThe Sunstone's power calls to you." # 元のマップデータではこの位置にNPC(2)は無いが、メッセージは用意されている
                    else: message = f"An old traveler ({c_idx},{r_idx})\nBe careful on your journey."
                    self.npcs.append(NPC(c_idx, r_idx, message))
                    self.game_map_data[r_idx][c_idx] = 0

    def start_battle(self):
        self.scene = SCENE_BATTLE
        enemy_x = SCREEN_WIDTH/2-(TILE_SIZE*2)/2; enemy_y = SCREEN_HEIGHT/3-(TILE_SIZE*2)/2
        base_hp=10; base_attack=2; hp_inc=3; atk_inc=0.5
        cur_hp = base_hp+self.enemies_defeated_count*hp_inc
        cur_atk = base_attack+int(self.enemies_defeated_count*atk_inc); cur_atk=max(1,cur_atk)
        enemy_lvl = self.enemies_defeated_count+1
        enemy_u, enemy_v = 32, 0 # Enemy sprite from setup_assets
        enemy_name = f"Maze Spirit Lv.{enemy_lvl}"
        self.current_enemy = Enemy(enemy_name,enemy_x,enemy_y,enemy_u,enemy_v,cur_hp,cur_atk)
        self.battle_message=f"A {self.current_enemy.name} has appeared!"; self.battle_command_index=0
        self.battle_turn="player"; self.damage_texts.clear()
        # pyxel.playm(0, loop=True)

    def end_battle(self, won=False):
        if won:
            self.scene=SCENE_VICTORY; self.battle_message=f"The {self.current_enemy.name} was defeated!"
            self.battle_sub_scene_timer=120; self.enemies_defeated_count+=1
            print(f"DEBUG: Enemies defeated: {self.enemies_defeated_count}")
        else: self.scene=SCENE_MAP
        self.current_enemy=None
        # pyxel.stop()

    def game_clear(self):
        print("DEBUG: Game Clear Reached!")
        self.scene = SCENE_CLEAR
        self.game_clear_phase = 0
        self.game_clear_message_timer = 300
        # pyxel.stop()

    def add_damage_text(self, value, x, y, color=8): self.damage_texts.append(DamageText(value, x, y, color))
    def update_camera_map(self):
        target_cam_x=self.player.x+self.player.sprite_w/2-SCREEN_WIDTH/2
        target_cam_y=self.player.y+self.player.sprite_h/2-SCREEN_HEIGHT/2
        lerp=0.1; self.camera_x+=(target_cam_x-self.camera_x)*lerp; self.camera_y+=(target_cam_y-self.camera_y)*lerp
        self.camera_x=max(0.0,min(self.camera_x,float(MAP_WIDTH_PX-SCREEN_WIDTH)))
        self.camera_y=max(0.0,min(self.camera_y,float(MAP_HEIGHT_PX-SCREEN_HEIGHT)))
        # pyxel.camera() は update_camera_map の最後に移動しました。
        # draw_map_scene の最初で設定するため、ここでの呼び出しは必須ではないかもしれませんが、
        # 他の update 中にカメラ位置を参照する処理がある場合は有効です。
        pyxel.camera(int(self.camera_x), int(self.camera_y))


    def update(self):
        if self.screen_flash_timer > 0: self.screen_flash_timer -= 1
        self.damage_texts = [dt for dt in self.damage_texts if not dt.update()]
        if self.scene == SCENE_TITLE: self.update_title_scene()
        elif self.scene == SCENE_OPENING: self.update_opening_scene()
        elif self.scene == SCENE_MAP: self.update_map()
        elif self.scene == SCENE_BATTLE: self.update_battle()
        elif self.scene == SCENE_GAMEOVER: self.update_gameover()
        elif self.scene == SCENE_VICTORY: self.update_victory()
        elif self.scene == SCENE_CLEAR: self.update_clear_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.scene = SCENE_OPENING
            self.opening_current_line_block = 0
            self.opening_timer = self.opening_line_display_time
            # pyxel.playm(1, loop=True)

    def update_opening_scene(self):
        self.opening_timer -= 1
        pressed_action_key = pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
        if self.opening_timer <= 0 or pressed_action_key:
            lines_in_block = 0; start_idx_for_block_check = self.opening_current_line_block * 3
            # このブロック計算ロジックはオリジナル版のものです
            for i in range(start_idx_for_block_check, len(self.opening_message_lines)):
                lines_in_block += 1
                if self.opening_message_lines[i] == "" or lines_in_block >=3 :
                    if self.opening_message_lines[i] == "" and i+1 < len(self.opening_message_lines) and self.opening_message_lines[i+1] == "": break
                    elif self.opening_message_lines[i] != "" and lines_in_block < 3: continue
                    break
            self.opening_current_line_block +=1
            if start_idx_for_block_check + lines_in_block >= len(self.opening_message_lines): self.scene = SCENE_MAP
            else: self.opening_timer = self.opening_line_display_time

    def update_map(self):
        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()
        if self.message_to_display is None:
            dx, dy = 0.0, 0.0; ps = self.player.speed
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT): dx = -ps
            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT): dx = ps
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP): dy = -ps
            elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN): dy = ps
            self.player.move(dx, dy, self.game_map_data, self)
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                pcx, pcy = self.player.x + self.player.sprite_w / 2, self.player.y + self.player.sprite_h / 2
                for npc in self.npcs:
                    ncx, ncy = npc.x + npc.sprite_w / 2, npc.y + npc.sprite_h / 2
                    if (pcx - ncx)**2 + (pcy - ncy)**2 < (TILE_SIZE * 1.8)**2:
                        self.message_to_display = npc.message; self.message_timer = 240; break
        else:
            self.message_timer -= 1
            if self.message_timer <= 0 or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.message_to_display = None
        self.update_camera_map()

    def update_battle(self):
        if self.current_enemy and self.current_enemy.is_dead:
            if self.current_enemy.update_death_animation(): return
            else: self.end_battle(won=True); return
        if self.battle_turn == "player":
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN): self.battle_command_index = 1 - self.battle_command_index
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                if self.battle_command_index == 0:
                    dmg = self.player.attack_power + random.randint(-1, 2)
                    if self.current_enemy:
                        ed = self.current_enemy.take_damage(dmg)
                        self.add_damage_text(dmg, self.current_enemy.x + self.current_enemy.sprite_w/2 - 4, self.current_enemy.y - 5)
                        self.battle_message = "Player attacks!"; self.screen_flash_timer = 6
                        if ed: self.battle_message = f"{self.current_enemy.name} fainted!"; self.battle_turn = "enemy_defeated_anim"; return
                    self.battle_turn = "enemy_action_delay"; self.battle_sub_scene_timer = 50
                elif self.battle_command_index == 1:
                    if random.random() < 0.6: self.battle_message = "Successfully fled!"; self.battle_sub_scene_timer = 60; self.battle_turn = "player_escaped"
                    else: self.battle_message = "Can't escape!"; self.battle_turn = "enemy_action_delay"; self.battle_sub_scene_timer = 50
        elif self.battle_turn == "enemy_action_delay":
            self.battle_sub_scene_timer -= 1
            if self.battle_sub_scene_timer <= 0: self.battle_turn = "enemy"
        elif self.battle_turn == "enemy":
            if self.current_enemy and not self.current_enemy.is_dead:
                dmg_dealt = self.current_enemy.attack(self.player)
                self.add_damage_text(dmg_dealt, SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT - 75, color=8)
                self.battle_message = f"{self.current_enemy.name} attacks!"; self.screen_flash_timer = 6
                if self.player.hp <= 0: self.scene = SCENE_GAMEOVER; self.battle_message = "You were defeated..."; self.battle_sub_scene_timer = 180; return
            self.battle_turn = "player"
        elif self.battle_turn == "player_escaped":
            self.battle_sub_scene_timer -= 1
            if self.battle_sub_scene_timer <= 0: self.end_battle(won=False)
        elif self.battle_turn == "enemy_defeated_anim": pass

    def update_gameover(self):
        self.battle_sub_scene_timer -= 1
        if self.battle_sub_scene_timer <= 0 or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A): pyxel.quit()

    def update_victory(self):
        self.battle_sub_scene_timer -= 1
        if self.battle_sub_scene_timer <= 0 or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.scene = SCENE_MAP; self.player.hp = self.player.max_hp

    def update_clear_scene(self):
        if self.game_clear_phase == 0:
            self.game_clear_message_timer -= 1
            if self.game_clear_message_timer <= 0 or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.game_clear_phase = 1; self.final_clear_display_timer = 240
        elif self.game_clear_phase == 1:
            self.final_clear_display_timer -= 1
            if self.final_clear_display_timer <= 0 or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                pyxel.quit()

    def draw_title_scene(self):
        pyxel.camera(0,0); pyxel.cls(1)
        title_text = "THE SUNSTONE CURSE"; start_text = "PRESS Z or ENTER TO START"
        title_w = len(title_text)*pyxel.FONT_WIDTH; start_w = len(start_text)*pyxel.FONT_WIDTH
        pyxel.text(SCREEN_WIDTH/2-title_w/2,SCREEN_HEIGHT/2-30,title_text,10); pyxel.text(SCREEN_WIDTH/2-title_w/2+1,SCREEN_HEIGHT/2-30+1,title_text,1)
        if pyxel.frame_count%40<20: pyxel.text(SCREEN_WIDTH/2-start_w/2,SCREEN_HEIGHT/2+20,start_text,7)

    def draw_opening_scene(self):
        pyxel.camera(0,0); pyxel.cls(0); start_y=50; lines_per_block=3; current_y=start_y
        start_idx_for_display=self.opening_current_line_block*lines_per_block; lines_shown_in_block=0
        # この描画ロジックもオリジナル版のものです
        for i in range(start_idx_for_display,len(self.opening_message_lines)):
            if lines_shown_in_block>=lines_per_block and self.opening_message_lines[i-1]=="": break
            if lines_shown_in_block>=5: break
            line_text=self.opening_message_lines[i]
            if line_text: text_w=len(line_text)*pyxel.FONT_WIDTH; pyxel.text(SCREEN_WIDTH/2-text_w/2,current_y,line_text,7)
            current_y+=10; lines_shown_in_block+=1
            if line_text=="" and not (i+1<len(self.opening_message_lines) and self.opening_message_lines[i+1]==""): break
        is_last_block=(start_idx_for_display+lines_shown_in_block>=len(self.opening_message_lines))
        if pyxel.frame_count%30<15:
            continue_text="- PRESS Z TO BEGIN -" if is_last_block else "- PRESS Z TO CONTINUE -"
            continue_w=len(continue_text)*pyxel.FONT_WIDTH; pyxel.text(SCREEN_WIDTH/2-continue_w/2,SCREEN_HEIGHT-20,continue_text,8)

    def draw_map_scene(self):
        pyxel.camera(int(self.camera_x), int(self.camera_y)); pyxel.cls(3)
        stx, sty = max(0, int(self.camera_x // TILE_SIZE)), max(0, int(self.camera_y // TILE_SIZE))
        etx = min(MAP_WIDTH_TILES, stx + (SCREEN_WIDTH // TILE_SIZE) + 2)
        ety = min(MAP_HEIGHT_TILES, sty + (SCREEN_HEIGHT // TILE_SIZE) + 2)
        for r in range(sty, ety):
            for c in range(stx, etx):
                if 0 <= r < MAP_HEIGHT_TILES and 0 <= c < MAP_WIDTH_TILES:
                    tile_type = self.game_map_data[r][c]
                    if tile_type == 1: pyxel.blt(c*TILE_SIZE,r*TILE_SIZE,0,24,0,TILE_SIZE,TILE_SIZE,0) # Wall
                    elif tile_type == 3: pyxel.rect(c*TILE_SIZE,r*TILE_SIZE,TILE_SIZE,TILE_SIZE,12) # Encounter
                    elif tile_type == 4: pyxel.blt(c*TILE_SIZE, r*TILE_SIZE, 0, 40, 0, TILE_SIZE, TILE_SIZE, 0) # Clear
        for npc in self.npcs: npc.draw()
        self.player.draw(); self.draw_message_window_map()

    def draw_battle_scene(self):
        pyxel.camera(0,0); pyxel.cls(2)
        if self.current_enemy:
            if self.current_enemy.is_hit_flash > 0:
                if self.current_enemy.is_hit_flash % 4 < 2: pass
                else:
                    if self.current_enemy.visible: self.current_enemy.draw()
                self.current_enemy.is_hit_flash -= 1
            elif self.current_enemy.visible: self.current_enemy.draw()
            if not self.current_enemy.is_dead:
                e_hp_txt = f"{self.current_enemy.name} HP:{self.current_enemy.hp}/{self.current_enemy.max_hp}"
                txt_w = len(e_hp_txt)*pyxel.FONT_WIDTH; pyxel.text(self.current_enemy.x+self.current_enemy.sprite_w/2-txt_w/2,self.current_enemy.y-10,e_hp_txt,7)
        stat_x,stat_y=10,SCREEN_HEIGHT-60; pyxel.rect(stat_x-3,stat_y-5,110,34,0); pyxel.rectb(stat_x-3,stat_y-5,110,34,7); self.player.draw_battle_status(stat_x,stat_y)
        cmd_x,cmd_y,cmd_w,cmd_h = SCREEN_WIDTH-90,SCREEN_HEIGHT-60,80,40
        pyxel.rect(cmd_x-1,cmd_y-1,cmd_w+2,cmd_h+2,0); pyxel.rectb(cmd_x-1,cmd_y-1,cmd_w+2,cmd_h+2,7)
        cmds=["ATTACK","FLEE"];
        for i,cmd_txt in enumerate(cmds):
            col=7;pre="  "
            if i==self.battle_command_index and self.battle_turn=="player":col=10;pre=">"
            pyxel.text(cmd_x+10,cmd_y+5+i*10,pre+cmd_txt,col)
        msg_x,msg_y,msg_w,msg_h = 10,10,SCREEN_WIDTH-20,40
        pyxel.rect(msg_x,msg_y,msg_w,msg_h,0); pyxel.rectb(msg_x,msg_y,msg_w,msg_h,7)
        txt_w=len(self.battle_message)*pyxel.FONT_WIDTH; pyxel.text(msg_x+(msg_w-txt_w)/2,msg_y+(msg_h-pyxel.FONT_HEIGHT)/2+1,self.battle_message,7)
        for dt in self.damage_texts: dt.draw()

    def draw_gameover_scene(self):
        pyxel.camera(0,0); pyxel.cls(0)
        txt_w=len(self.battle_message)*pyxel.FONT_WIDTH; pyxel.text(SCREEN_WIDTH/2-txt_w/2,SCREEN_HEIGHT/2-4,self.battle_message,8)

    def draw_victory_scene(self):
        self.draw_battle_scene(); pyxel.camera(0,0)
        vic_w,vic_h=160,25; vic_x,vic_y=(SCREEN_WIDTH-vic_w)/2,(SCREEN_HEIGHT-vic_h)/2-30
        pyxel.rect(vic_x,vic_y,vic_w,vic_h,0); pyxel.rectb(vic_x,vic_y,vic_w,vic_h,7)
        txt_w=len(self.battle_message)*pyxel.FONT_WIDTH; pyxel.text(vic_x+(vic_w-txt_w)/2,vic_y+(vic_h-pyxel.FONT_HEIGHT)/2+1,self.battle_message,10)

    def draw_clear_scene(self):
        pyxel.camera(0,0)
        if self.game_clear_phase == 0:
            pyxel.cls(14)
            msg1 = "THE SUNSTONE'S LIGHT RETURNS!"; msg2 = "THE CURSE IS BROKEN."
            msg3 = "PEACE REIGNS ONCE MORE."; msg4 = "(Press Z to Continue)"
            pyxel.text(SCREEN_WIDTH/2-len(msg1)*pyxel.FONT_WIDTH/2,SCREEN_HEIGHT/2-35,msg1,0)
            pyxel.text(SCREEN_WIDTH/2-len(msg2)*pyxel.FONT_WIDTH/2,SCREEN_HEIGHT/2-20,msg2,0)
            pyxel.text(SCREEN_WIDTH/2-len(msg3)*pyxel.FONT_WIDTH/2,SCREEN_HEIGHT/2-5,msg3,0)
            if pyxel.frame_count%30<15: pyxel.text(SCREEN_WIDTH/2-len(msg4)*pyxel.FONT_WIDTH/2,SCREEN_HEIGHT/2+20,msg4,8)
        elif self.game_clear_phase == 1:
            pyxel.cls(10)
            # ★ setup_assets_programmaticallyで定義したスプライト座標を参照
            big_char_sprites = {
                'G': (0, 16), 'A': (16, 16), 'M': (32, 16), 'E': (48, 16),
                'C': (80, 16), 'L': (96, 16), # E is at 112
                'R': (144,16), '!': (160,16),
                ' ': (64, 8) # Assuming a space sprite of width 8px (1 tile) at U=64, V=32
            }
            text_to_draw = "GAME CLEAR!"
            char_sprite_v = 32 # Y in image bank for big letters
            char_sprite_h = 16 # Height of big letter sprites

            total_width_px = sum(big_char_sprites.get(ch, (0,TILE_SIZE))[1] for ch in text_to_draw)
            current_x = SCREEN_WIDTH / 2 - total_width_px / 2
            target_y = SCREEN_HEIGHT / 2 - char_sprite_h / 2

            for char_code in text_to_draw:
                if char_code in big_char_sprites:
                    u, char_w_px = big_char_sprites[char_code]
                    # Assuming all big char sprites are 16px wide in the image bank for blt
                    pyxel.blt(int(current_x), int(target_y), 0, u, char_sprite_v, 16, char_sprite_h, 0)
                    current_x += char_w_px # Advance by the defined character width
                else:
                    current_x += TILE_SIZE # Default space for unknown characters

            exit_msg = "- PRESS Z TO EXIT -"; exit_w = len(exit_msg)*pyxel.FONT_WIDTH
            if pyxel.frame_count%30<15: pyxel.text(SCREEN_WIDTH/2-exit_w/2,SCREEN_HEIGHT-30,exit_msg,8)

    def draw_message_window_map(self):
        if self.message_to_display:
            # オリジナルのカメラ処理
            cam_x,cam_y=int(self.camera_x),int(self.camera_y); pyxel.camera(0,0)
            msg_h,msg_x,msg_y=40,10,SCREEN_HEIGHT-40-10
            pyxel.rect(msg_x,msg_y,SCREEN_WIDTH-20,msg_h,1); pyxel.rectb(msg_x,msg_y,SCREEN_WIDTH-20,msg_h,7)
            lines=self.message_to_display.split('\n');
            for i,line in enumerate(lines): pyxel.text(msg_x+5,msg_y+5+i*10,line,7)
            pyxel.camera(cam_x,cam_y)

    def draw(self):
        if self.scene == SCENE_TITLE: self.draw_title_scene()
        elif self.scene == SCENE_OPENING: self.draw_opening_scene()
        elif self.scene == SCENE_MAP: self.draw_map_scene()
        elif self.scene == SCENE_BATTLE: self.draw_battle_scene()
        elif self.scene == SCENE_GAMEOVER: self.draw_gameover_scene()
        elif self.scene == SCENE_VICTORY: self.draw_victory_scene()
        elif self.scene == SCENE_CLEAR: self.draw_clear_scene()

        if self.screen_flash_timer > 0 and pyxel.frame_count % 4 < 2:
            pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 7)

if __name__ == "__main__":
    print("DEBUG: __main__ block started. Creating Game instance.")
    try:
        Game()
    except Exception as e:
        print(f"ERROR: An exception occurred: {e}")
        import traceback
        traceback.print_exc()
    print("DEBUG: Game instance finished or quit.")