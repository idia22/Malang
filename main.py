import pygame
import sys
import pandas as pd
import random
import os
import math

import config

pygame.init()

# ================
# 기본 경로 설정
# ================
# __file__이 없는 환경에서도 동작하도록 안전하게 처리
try:
    base_path = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_path = os.getcwd()
ASSET_PATHS = {
    "logo": os.path.join(base_path, "assets", "logo.png"),
    "guest_button": os.path.join(base_path, "assets", "btn_guest.png"),
    "account_button": os.path.join(base_path, "assets", "btn_account.png"),
    "nav_books": os.path.join(base_path, "assets", "nav_books.png"),
    "nav_home": os.path.join(base_path, "assets", "nav_home.png"),
    "nav_social": os.path.join(base_path, "assets", "nav_social.png"),
    "exit_button": os.path.join(base_path, "assets", "btn_exit.png"),
    "main_menu_bg": os.path.join(base_path, "assets", "main_menu_bg.png"),
    "room_bg": os.path.join(base_path, "assets", "room_bg.png"),
    "social_vs_bg": os.path.join(base_path, "assets", "social_vs_bg.png"),
    "my_room_bg": os.path.join(base_path, "assets", "my_room_bg.png"),
    "ranking_bg": os.path.join(base_path, "assets", "ranking_bg.png"),
    "pick_a_word_bg": os.path.join(base_path, "assets", "pick_a_word_bg.png"),
    "select_the_meaning_bg": os.path.join(base_path, "assets", "select_the_meaning_bg.png"),
    "char_default": os.path.join(base_path, "assets", "char_default.png"),
    "item_shirt": os.path.join(base_path, "assets", "item_shirt.png"),
    "item_pants": os.path.join(base_path, "assets", "item_pants.png"),
    "item_glasses": os.path.join(base_path, "assets", "item_glasses.png"),
    "item_hat": os.path.join(base_path, "assets", "item_hat.png"),
    "quiz_option": os.path.join(base_path, "assets", "quiz_option.png"),
    "toggle_on": os.path.join(base_path, "assets", "toggle_on.png"),
    "toggle_off": os.path.join(base_path, "assets", "toggle_off.png"),
    "theme_light": os.path.join(base_path, "assets", "theme_light.png"),
    "theme_dark": os.path.join(base_path, "assets", "theme_dark.png"),
}

# ================
# 화면 설정
# ================
SCREEN_WIDTH, SCREEN_HEIGHT = 350, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("말랑")

# 색상 및 테마
RED, BLUE = (220, 80, 80), (100, 140, 250)
GREEN_LIGHT, RED_LIGHT = (144, 238, 144), (255, 182, 193)
GRAY = (180, 180, 180)
LIGHT_BLUE_GRAY = (200, 210, 230)
light_theme_colors = {'bg': (255, 255, 255), 'text': (0, 0, 0), 'ui_bg': (230, 230, 230), 'ui_accent': (200, 200, 200), 'bubble_bg': (255, 255, 255), 'border': (200, 200, 200)}
dark_theme_colors = {'bg': (40, 42, 54), 'text': (248, 248, 242), 'ui_bg': (68, 71, 90), 'ui_accent': (98, 114, 164), 'bubble_bg': (68, 71, 90), 'border': (150, 150, 150)}
current_theme, COLORS = "light", light_theme_colors

# 폰트 로딩 (assets 폴더 사용)
try:
    FONT_PATH = os.path.join(base_path, 'assets/NanumBarunGothic.ttf')
    font_large = pygame.font.Font(FONT_PATH, 36)
    font_medium = pygame.font.Font(FONT_PATH, 24)
    font_small = pygame.font.Font(FONT_PATH, 17)
    font_tiny = pygame.font.Font(FONT_PATH, 14)
    font_atomic = pygame.font.Font(FONT_PATH, 10)
except Exception:
    # 경고는 출력하지만 실행은 계속
    try:
        print(f"경고: 폰트 파일을 찾을 수 없습니다: {FONT_PATH}")
    except Exception:
        pass
    font_large, font_medium, font_small, font_tiny = [pygame.font.SysFont(None, size) for size in [48, 32, 24, 18]]

# ======================
# 데이터(문제) 로드
# ======================
try:
    # df = pd.read_csv(os.path.join(base_path,'/Users/joyeonghun/pygamge_Project/vocabulary_spelling_questions.csv'), encoding='utf-8').astype(str).replace('nan', '')
    df = pd.read_csv(os.path.join(base_path, 'data/vocabulary_spelling_questions.csv'), encoding='utf-8').astype(str).replace('nan', '')
    questions_by_level = {i: df[df['단계'] == str(i)].to_dict('records') for i in [1, 2, 3]}
    all_questions = questions_by_level[1] + questions_by_level[2] + questions_by_level[3]
except FileNotFoundError:
    print("오류: 'vocabulary_spelling_questions.csv' 파일을 찾을 수 없습니다.")
    # 파일이 없으면 최소 실행은 되도록 빈 리스트로 대체 (단, 퀴즈 기능은 제한)
    questions_by_level = {1: [], 2: [], 3: []}
    all_questions = []

# 레벨 진행도 저장 및 로드
'''PROGRESS_FILE = "level_unlock.txt"
def save_level_progress(level):
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(level))

def load_level_progress():
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 1

unlocked_level = load_level_progress()'''

DOTORI_FILE = "dotori_count.txt"
dotori_obtained = False  # 도토리 획득 여부 전역 변수로 추가
def save_dotori_count(count):
    global dotori_obtained
    dotori_obtained = True  # 도토리 획득 여부 (필요 시 로직 추가)
    with open(DOTORI_FILE, 'w') as f:
        f.write(str(count))

def load_dotori_count():
    try:
        with open(DOTORI_FILE, 'r') as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

# ================
# 헬퍼 함수
# ================
def get_text_lines(text, font, max_width):
    if not text:
        return []
    words, lines, current_line = text.split(' '), [], ""
    for word in words:
        if font.size(current_line + word)[0] < max_width:
            current_line += word + " "
        else:
            lines.append(current_line.strip()); current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

def draw_text_in_container(lines, font, color, surface, container_rect, align="left"):
    y_offset = 0
    if not color==0:
        pygame.draw.rect(surface, color,container_rect)
    try:
        if lines.isdigit() :
            line_surface = font.render(lines, True, (0,0,0))
            surface.blit(line_surface, line_surface.get_rect(center=container_rect.center))
    except:
        indent = 0
        for i,line in enumerate(lines):
            line_surface = font.render(line, True, (0,0,0))
            line_rect = line_surface.get_rect()
            if i == 0:
                indent = (container_rect.width - line_rect.width) / 2
            if align == "left":
                line_rect.topleft = (container_rect.x+indent, container_rect.y + y_offset)
            elif align == "center":
                line_rect.midtop = (container_rect.centerx, container_rect.y +y_offset)
                
            surface.blit(line_surface, line_rect)

            y_offset += font.get_height()

# ================
# Image-aware Button 클래스
# ================
class Button:
    def __init__(self, rect, text=None, color=None, text_color=None, image_path=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.base_color = color
        self.text_color_override = text_color
        self.image_path = image_path
        self._image = None
        if image_path:
            self._image = self._load_and_scale(image_path)

    def _load_and_scale(self, path):
        try:
            if not os.path.exists(path):
                return None
            img = pygame.image.load(path).convert_alpha()
            w, h = self.rect.width, self.rect.height
            iw, ih = img.get_width(), img.get_height()
            # 비율 유지하여 맞추기
            if ih/iw >= h/w:
                # 이미지가 세로로 긴 경우: 높이에 맞추고 너비는 비율대로
                target_h = h
                target_w = max(1, int(iw / ih * target_h))
            else:
                target_w = w
                target_h = max(1, int(ih / iw * target_w))
            scaled = pygame.transform.smoothscale(img, (target_w, target_h))
            return scaled
        except Exception:
            return None

    def reload_image(self):
        if self.image_path:
            self._image = self._load_and_scale(self.image_path)

    def draw(self, surface):
        # 배경 사각형 (이미지 없을 때의 대체)
        color = self.base_color if self.base_color else COLORS['ui_accent']
        text_color = self.text_color_override if self.text_color_override else COLORS['text']
        if self._image:
            # 이미지가 버튼보다 작다면 가운데 정렬
            img = self._image
            img_rect = img.get_rect(center=self.rect.center)
            surface.blit(img, img_rect)
            # 이미지 위 텍스트 (필요 시)
            if self.text:
                txt = font_tiny.render(self.text, True, text_color)
                surface.blit(txt, txt.get_rect(center=self.rect.center))
        else:
            # 기본 렌더
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            if self.text:
                padding = 8
                target_rect = self.rect.inflate(-padding, -padding)
                current_font = font_small
                text_surface = current_font.render(self.text, True, text_color)
                if text_surface.get_width() > target_rect.width:
                    current_font = font_tiny
                    text_surface = current_font.render(self.text, True, text_color)
                surface.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def transparent_draw(self, surface, border_radius=-1):
        # 디버그용 테두리 표시
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, width=1, border_radius=border_radius)
        color = self.base_color if self.base_color else COLORS['ui_accent']
        text_color = self.text_color_override if self.text_color_override else COLORS['text']
        if self.text:
            txt = font_tiny.render(self.text, True, text_color)
            surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ================
# 퀴즈 로직 상태 변수
# ================
current_level, current_question_index, score = 0, 0, 0
quiz_questions, answer_buttons = [], []
user_answer, correct_answer = None, None
answer_checked = False
current_quiz_mode, total_questions = None, 0

def start_quiz(mode, level=None):
    global scene, current_quiz_mode, current_level, quiz_questions, total_questions, score, user_answer, answer_checked, current_question_index
    scene, current_quiz_mode = "quiz_game", mode
    score, user_answer, answer_checked, current_question_index = 0, None, False, 0
    if mode == "practice" and level and questions_by_level.get(level):
        current_level, total_questions = level, min(15, len(questions_by_level[level]) or 15)
        quiz_questions = random.sample(questions_by_level[level] if questions_by_level[level] else [], total_questions) if questions_by_level[level] else []
    elif mode == "test":
        current_level, total_questions = None, min(20, len(all_questions) or 20)
        quiz_questions = random.sample(all_questions if all_questions else [], total_questions) if all_questions else []
    # 준비
    prepare_current_question()

def prepare_current_question():
    global answer_buttons, correct_answer,how_many_options, context_existence
    
    answer_buttons.clear()
    if not quiz_questions or current_question_index >= len(quiz_questions):
        return
    question = quiz_questions[current_question_index]
    how_many_options = question.get('선택지3')
    context_existence = question.get('보기')
    options = []
    context_text = None

    # 2지선다 예외 처리
    if question.get('보기') and question.get('선택지1') and not question.get('선택지2'):
        options = [question['보기'], question['선택지1']]
        correct_answer = question.get('정답', '')
    else:
        options = [question.get(f'선택지{i}', '') for i in [1,2,3,4] if question.get(f'선택지{i}', '')]
        if question.get('정답', '').isdigit():
            correct_idx = int(question['정답']) - 1
            correct_answer = options[correct_idx] if 0 <= correct_idx < len(options) else ""
        else:
            correct_answer = question.get('정답', '')
        context_text = question.get('보기', None)

    # UI 레이아웃 동적 계산
    side_margin = SCREEN_WIDTH * 0.075
    content_width = SCREEN_WIDTH - (side_margin * 2)
    current_y = 80
    # 문제 텍스트 높이 계산
    question_lines = get_text_lines(question.get('문제', ''), font_medium, content_width)
    q_height = len(question_lines) * font_medium.get_height()
    current_y += q_height + 20

    if context_text:
        context_lines = get_text_lines(context_text, font_small, content_width - 40)
        box_h = len(context_lines) * font_small.get_height() + 20
        current_y +=   50+box_h
    if how_many_options == '':
        current_y = 248
    else:
        current_y = 201
    button_height = 65
    button_gap = 10
    for option in options:
        button_rect = (side_margin, current_y, content_width, button_height)
        # 여기서 이미지 기반 버튼으로 생성 (퀴즈 선택지도 이미지로 대체 가능)
        btn = Button(button_rect, option, image_path=ASSET_PATHS.get("quiz_option"))
        answer_buttons.append(btn)
        current_y += button_height + button_gap

# ================
# 리소스(이미지) 로드 / 기본 대체
# ================
def safe_load_and_scale(path, target_size):
    try:
        if not path or not os.path.exists(path):
            return None
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, target_size)
    except Exception:
        return None

#배경이미지 (있으면 로드)
main_menu_bg = safe_load_and_scale(ASSET_PATHS.get("main_menu_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
social_vs_bg = safe_load_and_scale(ASSET_PATHS.get("social_vs_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
pick_a_word_bg = safe_load_and_scale(ASSET_PATHS.get("pick_a_word_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
select_the_meaning_bg = safe_load_and_scale(ASSET_PATHS.get("select_the_meaning_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
my_room_bg = safe_load_and_scale(ASSET_PATHS.get("my_room_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
char_default_img = safe_load_and_scale(ASSET_PATHS.get("char_default"), (160, 200))

# ================
# 상태 및 버튼 정의 (이미지 경로 지정 가능)
# ================
scene, quiz_bubble_visible = "login", False
scroll_offset_x = 0

# 버튼들 (이미지 경로를 Button 생성자에 넣어두면 바꿀 수 있음)
guest_btn = Button((25, 350, 300, 70), "게스트로 로그인", image_path=ASSET_PATHS.get("guest_button"))
account_btn = Button((25, 440, 300, 60), "계정 로그인 (비활성)", image_path=ASSET_PATHS.get("account_button"))
setting_btn = Button((292, 17, 41, 41), image_path=None)

# 네비게이션 (여덟 개)
x_main = 25
x_gap = 62
nav_buttons = [
    Button((35, 508, 83, 37), image_path=ASSET_PATHS.get("nav_books")),
    Button((133, 508, 83, 37), image_path=ASSET_PATHS.get("nav_home")),
    Button((231, 508, 83, 37), image_path=ASSET_PATHS.get("nav_social")),
    Button((x_main, 640, 50, 50)),
    Button((x_main +x_gap, 640, 49, 49), image_path=ASSET_PATHS.get("nav_books")),
    Button((x_main +2*x_gap, 640, 49, 49), image_path=ASSET_PATHS.get("nav_social")),
    Button((x_main +3*x_gap, 640, 49, 49),image_path=ASSET_PATHS.get("ranking_bg")),
    Button((x_main +4*x_gap, 640, 49, 49), image_path=ASSET_PATHS.get("nav_home")),
]

# 퀴즈 드롭다운(버블) 관련
quiz_btn_rect = nav_buttons[2].rect
bubble_w, bubble_h = 230, 70
bubble_y = quiz_btn_rect.top - bubble_h - 30
bubble_rect = pygame.Rect(quiz_btn_rect.centerx - bubble_w/2, bubble_y, bubble_w, bubble_h)
practice_bubble_btn = Button((bubble_rect.left + 10, bubble_rect.top + 15, 100, 40), "연습 모드", image_path=None)
test_bubble_btn = Button((bubble_rect.right - 110, bubble_rect.top + 15, 100, 40), "테스트 모드", image_path=None)
back_btn = Button((20, 19, 33, 33),image_path=None)
back_btn_settings = Button((20, 19, 33, 33),text='back',image_path=None)
back_btn_my_room = Button((18, 13, 33, 33),image_path=None)

level_buttons = [Button((75, 175 + i*100, 200, 60), f"{i+1}단계") for i in range(3)]
retry_btn, main_menu_btn = Button((40, 450, 130, 50), "다시하기"), Button((180, 450, 130, 50), "메인 메뉴")
exit_quiz_flow_btn = Button((SCREEN_WIDTH - 100, SCREEN_HEIGHT - 60, 80, 40), "나가기", image_path=ASSET_PATHS.get("exit_button"))

# 설정 토글 (이미지로 표시할 토글 경로 사용)
i = 90
bgm_btn = Button((210, 184, 100, 40),'on',(20,93,191),(255,255,255), image_path=ASSET_PATHS.get("toggle_on"))
sfx_btn = Button((210, 184+i, 100, 40),'on',(20,93,191),(255,255,255), image_path=ASSET_PATHS.get("toggle_on"))
theme_btn = Button((210, 184+2*i, 100, 40),"다크 모드 on",COLORS['ui_bg'], image_path=ASSET_PATHS.get("theme_light"))

# 꾸미기 아이템 목록(집 메뉴에 표시)
item_images = [
    ASSET_PATHS.get("item_shirt"),
    ASSET_PATHS.get("item_pants"),
    ASSET_PATHS.get("item_glasses"),
    ASSET_PATHS.get("item_hat"),
]

# =====================================
# 말풍선 퀴즈 뷰용 타원 + 꼬리 그리기 함수 (기존)
# =====================================
def draw_rounded_rect_with_tail(surface, rect, color, border_color, radius, tail_x_center):
    points = []
    tl = (rect.left + radius, rect.top + radius)
    tr = (rect.right - radius, rect.top + radius)
    br = (rect.right - radius, rect.bottom - radius)
    bl = (rect.left + radius, rect.bottom - radius)
    # 각 코너 곡선 근사
    for angle in range(180, 271, 15):
        points.append((tl[0] + radius * math.cos(math.radians(angle)), tl[1] + radius * math.sin(math.radians(angle))))
    for angle in range(270, 361, 15):
        points.append((tr[0] + radius * math.cos(math.radians(angle)), tr[1] + radius * math.sin(math.radians(angle))))
    for angle in range(0, 91, 15):
        points.append((br[0] + radius * math.cos(math.radians(angle)), br[1] + radius * math.sin(math.radians(angle))))
    tail_width, tail_height = 15, 10
    points.extend([(tail_x_center + tail_width, rect.bottom), (tail_x_center, rect.bottom + tail_height), (tail_x_center - tail_width, rect.bottom)])
    for angle in range(90, 181, 15):
        points.append((bl[0] + radius * math.cos(math.radians(angle)), bl[1] + radius * math.sin(math.radians(angle))))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, border_color, points, 2)

def draw_quiz_bubble(surface):
    draw_rounded_rect_with_tail(surface, bubble_rect, COLORS['bubble_bg'], COLORS['border'], 15, quiz_btn_rect.centerx)
    practice_bubble_btn.draw(surface); test_bubble_btn.draw(surface)

# ================
# 메인 루프
# ================
running = True
quiz_bubble_visible = False

# 퀴즈 준비 (만약 start_quiz 호출 없이 들어갔을 때 오류 방지)
if quiz_questions:
    prepare_current_question()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 마우스 휠로 집 화면 아이템 슬라이드 처리
        if scene == "my_room" and event.type == pygame.MOUSEWHEEL:
            # 한 슬롯 너비는 80 (같은 방식으로 하드코딩된 UI를 준수)
            max_scroll = max(0, len(item_images) * 80 - (SCREEN_WIDTH - 40))
            scroll_offset_x = max(min(0, scroll_offset_x + event.y * 30), -max_scroll)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # 로그인 화면
            if scene == "login":
                if guest_btn.is_clicked(pos):
                    scene = "main_menu"
            elif scene == "main_menu":
                if nav_buttons[0].is_clicked(pos):
                    start_quiz(mode="test", level=None)
                elif nav_buttons[1].is_clicked(pos):
                    scene = "my_room"
                elif nav_buttons[2].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[3].is_clicked(pos):
                    scene = "main_menu"
                elif nav_buttons[4].is_clicked(pos):
                    start_quiz(mode="test", level=None)
                elif nav_buttons[5].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[6].is_clicked(pos):
                    scene = "ranking"
                elif nav_buttons[7].is_clicked(pos):
                    scene = "my_room"
                elif setting_btn.is_clicked(pos):
                    scene = "settings"
            # 공통 뒤로가기
            if scene in ["social_vs", "settings", "practice_level_selection", "practice_test_selection", "quiz_results", "ranking"]:
                if back_btn.is_clicked(pos):
                    scene = "main_menu"
            # 연습 레벨 선택
            if scene == "practice_level_selection":
                for i, btn in enumerate(level_buttons):
                    if i + 1 <= unlocked_level and btn.is_clicked(pos):
                        start_quiz(mode="practice", level=i + 1)
                        
            # 퀴즈 진행 중
            elif scene == "quiz_game":
                if nav_buttons[3].is_clicked(pos):
                    scene = "main_menu"
                elif nav_buttons[4].is_clicked(pos):
                    pass
                elif nav_buttons[5].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[6].is_clicked(pos):
                    scene = "ranking"
                elif nav_buttons[7].is_clicked(pos):
                    scene = "my_room"
                
                if back_btn.is_clicked(pos):
                    scene = "main_menu"
                elif not answer_checked:
                    for btn in answer_buttons:
                        if btn.is_clicked(pos):
                            user_answer, answer_checked = btn.text, True
                            if user_answer == correct_answer:
                                score += 1
                            #pygame.time.set_timer(pygame.USEREVENT, 5)
                            current_question_index += 1
                            user_answer = None
                            if current_question_index < total_questions:
                                prepare_current_question()
                                
                            else:
                                scene = "quiz_results"
                            break
                    
            elif scene == "quiz_results":
                if retry_btn.is_clicked(pos):
                    start_quiz(mode=current_quiz_mode, level=current_level)
                    dotori_obtained = False  # 재시작 시 도토리 획득 여부 초기화
                elif main_menu_btn.is_clicked(pos):
                    scene = "main_menu"
                    dotori_obtained = False
            elif scene == "social_vs":
                if nav_buttons[3].is_clicked(pos):
                    scene = "main_menu"
                elif nav_buttons[4].is_clicked(pos):
                    start_quiz(mode="test", level=None)
                elif nav_buttons[5].is_clicked(pos):
                    scene = "social_vs"
                elif nav_buttons[6].is_clicked(pos):
                    scene = "ranking"
                elif nav_buttons[7].is_clicked(pos):
                    scene = "my_room"
            elif scene == "my_room":
                if back_btn_my_room.is_clicked(pos):
                    scene = "main_menu"
            # 설정 화면 테마 토글
            elif scene == "settings":
                '''if theme_btn.is_clicked(pos):
                    current_theme, COLORS = ("dark", dark_theme_colors) if current_theme == "light" else ("light", light_theme_colors)
                    # 테마 버튼 이미지 갱신(이미지 경로로 바꾸고 싶으면 ASSET_PATHS 수정)
                    theme_btn.image_path = ASSET_PATHS.get("theme_dark" if current_theme == "dark" else "theme_light")
                    theme_btn.reload_image()'''
            # 퀴즈/소셜 화면 등에서 '나가기' 버튼 (exit_quiz_flow_btn 사용)
            if scene in ["quiz_menu"]:
                # (이미 exit handlers 있지만 안전하게 처리)
                if exit_quiz_flow_btn.is_clicked(pos):
                    scene = "main_menu"
            # 연습/테스트 bubble 선택
            if quiz_bubble_visible and practice_bubble_btn.is_clicked(pos):
                start_quiz(mode="practice", level=1)
            if quiz_bubble_visible and test_bubble_btn.is_clicked(pos):
                start_quiz(mode="test", level=None)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if scene == "quiz_game":
                answer_checked = False
        # 퀴즈 자동 진행 타이머 이벤트
        if event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            current_question_index += 1
            user_answer, answer_checked = None, False
            if current_question_index < total_questions:
                prepare_current_question()
            else:
                scene = "quiz_results"

    # --- 화면 그리기 ---
    screen.fill(COLORS['bg'])

    if scene == "login":
        # (로고 + 버튼 - 이미지가 있으면 이미지로 표시)
        pygame.draw.circle(screen, COLORS['ui_accent'], (175, 130), 60, 3)
        logo = font_medium.render("로고", True, COLORS['text']); screen.blit(logo, logo.get_rect(center=(175, 130)))
        title = font_large.render("말랑", True, COLORS['text']); screen.blit(title, title.get_rect(center=(175, 230)))
        guest_btn.draw(screen); account_btn.draw(screen)

    elif scene == "main_menu":
        # 배경 이미지 있으면 표시, 없으면 기본
        if main_menu_bg:
            screen.blit(main_menu_bg, (0,0))
        else:
            pygame.draw.rect(screen, COLORS['ui_bg'], (0,0, SCREEN_WIDTH, SCREEN_HEIGHT))
        # 네비 버튼
        for btn in nav_buttons:
            btn.transparent_draw(screen)
        setting_btn.transparent_draw(screen)

    elif scene == "my_room":
        screen.blit(my_room_bg,(0,0))
        back_btn_my_room.transparent_draw(screen)
        rect = pygame.Rect(280, 25, 40, 22)
        draw_text_in_container(f"{load_dotori_count()}", font_tiny, (255,255,255), screen, rect, align="center")
        # (아이템을 클릭했을 때 동작하도록 하려면 여기에 is_clicked 검사 추가 가능)

    elif scene == "social_vs":
        screen.blit(social_vs_bg,(0,0))
        back_btn.transparent_draw(screen)
        for btn in nav_buttons[3:]:
            btn.transparent_draw(screen)
        # 오른쪽 하단 '나가기' 버튼 (이미지/대체)
        #exit_quiz_flow_btn.draw(screen)
    elif scene == "ranking":
        screen.blit(safe_load_and_scale(ASSET_PATHS.get("ranking_bg"), (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        back_btn.transparent_draw(screen)

    elif scene == "settings":
        back_btn_settings.draw(screen)
        title = font_large.render("설정", True, COLORS['text']); screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, 80)))
        for i, label in enumerate(["배경음", "효과음", "테마 색상"]):
            screen.blit(font_medium.render(label, True, COLORS['text']), (40, 190 + i*90))
        # theme_btn 표시: 이미지가 있으면 이미지로
        bgm_btn.draw(screen); sfx_btn.draw(screen); theme_btn.draw(screen)

    elif scene == "practice_test_selection":
        back_btn.draw(screen)
        title = font_large.render("퀴즈 모드 선택", True, COLORS['text']); screen.blit(title, title.get_rect(center=(200, 80)))
        practice_bubble_btn.draw(screen); test_bubble_btn.draw(screen)

    elif scene == "practice_level_selection":
        back_btn.draw(screen)
        title = font_large.render("연습 모드", True, COLORS['text']); screen.blit(title, title.get_rect(center=(175, 90)))
        for i, btn in enumerate(level_buttons):
            if i + 1 > unlocked_level:
                btn.text, btn.base_color = f"{i+1}단계 🔒", GRAY
            else:
                btn.text, btn.base_color = f"{i+1}단계", BLUE
            btn.draw(screen)

    elif scene == "quiz_game":
        if quiz_questions and current_question_index < len(quiz_questions):
            if how_many_options == '' and context_existence == '':
                screen.blit(pick_a_word_bg, (0,0))
                pygame.draw.rect(screen, (255,246,246), (55,90, 240, 30))
                current_y = 130
            elif how_many_options == '':
                screen.blit(pick_a_word_bg, (0,0))
                current_y = 85
                context_y = 140
            else:
                screen.blit(select_the_meaning_bg, (0,0))
                current_y = 85
                context_y = 130
            for btn in nav_buttons[3:]:
                btn.transparent_draw(screen)
            back_btn.transparent_draw(screen)
            a = font_small.render(f"{current_question_index + 1} / {total_questions}", True, COLORS['text'])
            screen.blit(a,a.get_rect(center=(SCREEN_WIDTH/2,35)))
            question = quiz_questions[current_question_index]
            side_margin = SCREEN_WIDTH * 0.1
            content_width = SCREEN_WIDTH - (side_margin * 2)
            

            q_lines = get_text_lines(question.get('문제', ''), font_small, 240)
            q_rect = pygame.Rect(55, current_y, 240, len(q_lines) * font_small.get_height())
            draw_text_in_container(q_lines, font_small, (255,244,244), screen, q_rect,align="left")
            current_y = q_rect.bottom 

            context_text = None
            if not (question.get('보기') and question.get('선택지1') and not question.get('선택지2')):
                context_text = question.get('보기')

            if context_text:
                context_lines = get_text_lines(context_text, font_tiny, content_width - 40)
                box_h = len(context_lines) * font_tiny.get_height() + 20
                box_rect = pygame.Rect(side_margin, context_y, content_width, box_h)
                #pygame.draw.rect(screen, COLORS['ui_bg'],box_rect, border_radius=10)
                draw_text_in_container(context_lines, font_tiny, 0, screen, box_rect.inflate(-20, -20), align="left")

            for btn in answer_buttons:
                original_color = btn.base_color
                if answer_checked:
                    if btn.text == correct_answer:
                        btn.base_color = GREEN_LIGHT
                    elif btn.text == user_answer:
                        btn.base_color = RED_LIGHT
                else:
                    btn.base_color = COLORS['ui_bg']
                btn.transparent_draw(screen)
                btn.base_color = original_color

        #exit_quiz_flow_btn.draw(screen)

    elif scene == "quiz_results":
        title_text = "연습 결과" if current_quiz_mode == "practice" else "테스트 결과"
        title = font_large.render(title_text, True, COLORS['text']); screen.blit(title, title.get_rect(center=(SCREEN_WIDTH/2, 100)))
        score_text = font_medium.render(f"총 {total_questions}문제 중 {score}개를 맞혔습니다!", True, COLORS['text']); screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH/2, 220)))
        unlock_message = ""
        pass_threshold = total_questions * 0.9 if total_questions else 9999
        if current_quiz_mode == "practice" and score >= pass_threshold and current_level < 3 and current_level + 1 > unlocked_level:
            unlocked_level = current_level + 1
            #save_level_progress(unlocked_level)
            unlock_message = "🎉 다음 레벨이 해금되었습니다! 🎉"
        elif current_quiz_mode == "test" and score >= pass_threshold and dotori_obtained == False:
            dotori_earned = random.randint(5, 15)
            total_dotori = load_dotori_count() + dotori_earned
            save_dotori_count(total_dotori)
            unlock_message = f"🎉 통과하여 도토리 {dotori_earned}개를 획득했습니다! 🎉 (총 도토리: {total_dotori}개)"
        msg, color = ("🎉 통과했습니다! 🎉", BLUE) if score >= pass_threshold else ("다시 도전해보세요!", RED)
        result = font_large.render(msg, True, color); screen.blit(result, result.get_rect(center=(SCREEN_WIDTH/2, 300)))
        if unlock_message:
            unlock_msg_render = font_medium.render(unlock_message, True, GREEN_LIGHT)
            screen.blit(unlock_msg_render, unlock_msg_render.get_rect(center=(200, 350)))
        retry_btn.draw(screen); main_menu_btn.draw(screen)

    if quiz_bubble_visible:
        draw_quiz_bubble(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()