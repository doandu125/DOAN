import pygame, random, sys, os, time
from pygame.locals import *

WINDOWWIDTH = 700
WINDOWHEIGHT = 900
TEXTCOLOR = (255, 255, 255)
BACKGROUND_IMAGE = pygame.image.load('nenvutru.png')
FPS = 100
BADDIEMINSIZE = 50
BADDIEMAXSIZE = 100
BADDIEMINSPEED = 10
BADDIEMAXSPEED = 10
ADDNEWBADDIERATE = 16
PLAYERMOVERATE = 7
count = 5
topScore=100

# Hàm kết thúc game
def terminate():
    pygame.quit()
    sys.exit()

# Chờ người chơi nhấn phím
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            # Nhấn phím ESC thì thoát
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # escape quits
                    terminate()
                return # Nhấn phím khác thì chạy game

# Kiểm tra tàu va chạm với ...
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

# Viết một dòng chữ từ tọa độ (x, y)
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Bắt đầu game
pygame.init()
mainClock = pygame.time.Clock() # Khởi tạo đồng hồ
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # Tạo cửa sổ với kích thước (WINDOWWIDTH, WINDOWHEIGHT)
pygame.display.set_caption('aaaaa bbbb cccc') # Đặt tiêu đề cho cửa sổ là 'aaaa....'
pygame.mouse.set_visible(False) # Tắt hiển thị chuột

# Load ảnh cho các sự vật trong game
playerImage = pygame.image.load('tauvutru1.png')
car3 = pygame.image.load('saochoi21.png')
car4 = pygame.image.load('saochoi.png')
playerRect = playerImage.get_rect() # Lấy khung hình chữ nhật bao quanh tàu
baddieImage = pygame.image.load('vienda.png')
sample = [car3, car4, baddieImage]
wallLeft = pygame.image.load('anhnenen.png')
wallRight = pygame.image.load('anhnen2.png')
font = pygame.font.SysFont(None, 42) # Đặt font
drawText('NHAN ENTER DE BAT DAU GAME!', font, windowSurface, (WINDOWWIDTH / 3) - 137, (WINDOWHEIGHT / 3)+80) # Viết chữ đầu game
pygame.display.update() # Hiển thị các nội dung
waitForPlayerToPressKey() # Chờ người chơi nhấn phím
zero = 0

# Ban đầu count=5 tương đương 5 mạng
while (count > 0):
    baddies = []
    score = 0
    # đặt tàu ở giữa màn hình
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0

    ########## BẮT ĐÀU KIỂM TRA CÒN SỐNG ###########
    # trong khi vẫn còn sống 
    while True:
        # tăng điểm theo thời gian chơi
        score += 1

        # lấy các sự kiện xảy ra trong game bằng hàm pygame.event.get()
        for event in pygame.event.get():

            # Các sự kiện gây thoát (đóng cửa sổ, tắt game, tắt máy, crashed...)
            if event.type == QUIT:
                terminate()

            # Các sự kiện nhấn phím
            if event.type == KEYDOWN:
                # phím z - hack chạy lùi
                if event.key == ord('z'):
                    reverseCheat = True
                # phím x - hack chạy chậm
                if event.key == ord('x'):
                    slowCheat = True
                # phím mũi tên trái hoặc phím a - sang trái
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                # mũi tên phải/d
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                # mũi lên lên/w
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                # mũi tên xuống/s
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            # Các sự kiện bỏ nhấn phím
            if event.type == KEYUP:
                # bỏ nhấn z - tắt hack chạy lùi
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                # bỏ nhấn x - tắt hack chạy chậm
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                # bỏ nhấn ESC - thoát
                if event.key == K_ESCAPE:
                    terminate()

                # Bỏ nhấn các phím di chuyển - ngưng di chuyển về hướng tươngứng
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

        # Nếu không đang trong chế độ hack thì tăng chướng ngại vật thêm 1
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        # Nếu số lương chướng ngại vật (baddieAddCounter) đạt ngưỡng ADDNEWBADDIERATE (bằng 16 - khai báo trên đầu)
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0 # thì reset số lượng chướng ngại vật về 0
            baddieSize = 30
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(random.choice(sample), (23, 47)),
                         }
            baddies.append(newBaddie) # rồi thêm một chướng ngại vật mới
            sideLeft = {'rect': pygame.Rect(0, 0, 126, 600),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(wallLeft, (126, 599)),
                        }
            baddies.append(sideLeft) # thêm tường bên trái
            sideRight = {'rect': pygame.Rect(497, 0, 303, 600),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface': pygame.transform.scale(wallRight, (303, 599)),
                         }
            baddies.append(sideRight) # thêm tường bên phải

        # Kiểm tra di chuyển có va chạm tường hay không
        if moveLeft and playerRect.left > 0: # chưa chạm tường trái
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0) # thì cứ đi sang trái
        if moveRight and playerRect.right < WINDOWWIDTH: # phải
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0: # lên
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT: # xuống
            playerRect.move_ip(0, PLAYERMOVERATE)

        # kiểm tra từng chướng ngại vật
        for b in baddies:
            if not reverseCheat and not slowCheat: # nếu không đang trong chế độ hack
                b['rect'].move_ip(0, b['speed']) # thì chướng ngại vật di chuyển bình thường
            elif reverseCheat: # trong chế dộ hack đi lùi
                b['rect'].move_ip(0, -5) # thì chướng ngại vật cũng đi lùi
            elif slowCheat: # trong chế độ hack đi chậm
                b['rect'].move_ip(0, 1) # thì chướng ngại vật cũng đi chậm

        for b in baddies[:]: # kiểm tra từng chướng ngại vật
            if b['rect'].top > WINDOWHEIGHT: # nếu chướng ngại vật đi quá đường biên dưới
                baddies.remove(b) # thì xóa bỏ chướng ngại vật

        # đặt các thông số cho thông tin trong game
        font = pygame.font.SysFont(None, 38)
        windowSurface.blit(BACKGROUND_IMAGE, [0,0])
        drawText('Score: %s' % (score), font, windowSurface, 128, 0) # in điểm
        drawText('Top Score: %s' % (topScore), font, windowSurface, 128, 21) # in điểm cao nhất
        drawText('Rest Life: %s' % (count), font, windowSurface, 128, 41) # in số mạng còn lại

        windowSurface.blit(playerImage, playerRect) # hiển thị ra các thông số

        for b in baddies: # kiểm tra từng chướng ngại vật
            windowSurface.blit(b['surface'], b['rect']) # hiển thị ra từng cái

        pygame.display.update() # reload lại toàn màn hình

        if playerHasHitBaddie(playerRect, baddies): # kiểm tra nếu tàu va chạm chướng ngại vật
            if score > topScore: # điểm hiện tại lớn hơn điểm cao nhất
                topScore = score # thì đặt lại điểm cao nhất
            break

        # định thời gian cho mỗi lần cập nhật (FPS - frame per second)
        # Ở trên định nghĩa FPS = 100 -> giới hạn reload trang ở 100 FPS
        mainClock.tick(FPS) 
    ########## HẾT KIỂM TRA CÒN SỐNG ##########
    # khi chết 
    count = count - 1 # trừ mạng đi 1
    time.sleep(1) # delay 1ms
    font = pygame.font.SysFont(None, 52)
    if (count == 0): # nếu hết mạng
        # Hiển thị game over 
        drawText('Game Over', font, windowSurface, (WINDOWWIDTH / 3)+40, (WINDOWHEIGHT / 3)+70)
        # Nhấn phím bất kỳ để chơi lại
        drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH /3) - 110, (WINDOWHEIGHT / 3) + 95)
        pygame.display.update()
        time.sleep(2) # delay 2ms
        waitForPlayerToPressKey() # chờ người chơi nhấn phím
        count = 3 # từ lần 2 chỉ còn 3 mạng (lần đầu có 5 mạng)

