from bangtal import *

startscene=Scene('','images/시작.png')
title=Object('images/제목.png')
title.locate(startscene,100,50)
title.setScale(2)
title.show()

timer=Timer(0.1)
endtimer=Timer(5)


startBtn=Object('images/시작버튼.png')
startBtn.locate(startscene,850,50)
startBtn.setScale(0.7)
startBtn.show()

scene1=Scene('룸1','images/배경-1.png')

door1=Object('images/문-오른쪽-닫힘.png')
door1.locate(scene1,800,380)
door1.show()
door1.closed=True

key=Object('images/열쇠.png')
key.locate(scene1,600,150)
key.setScale(0.2)
key.show()

jack=Object('images/호박.png')
jack.locate(scene1,550,150)
jack.setScale(0.05)
jack.show()

scene2=Scene('룸2','images/배경-2.png')

door2=Object('images/문-왼쪽-열림.png')
door2.locate(scene2,320,270)
door2.show()


door3=Object('images/문-오른쪽-닫힘.png')
door3.locate(scene2,800,380)
door3.show()

keypad=Object('images/키패드.png')
keypad.locate(scene2,950,520)
keypad.show()

switch=Object('images/스위치.png')
switch.locate(scene2,930,500)
switch.show()

password=Object('images/암호.png')
password.setScale(0.4)
password.locate(scene2,600,100)

badscene=Scene('','images/badend.png')

cellar=Object('images/지하실.png')
cellar.setScale(0.4)
cellar.locate(scene2,300,100)

#sound를 써보려 하였으나 play함수 사용시 missing positional argument python 'loop'라는 문구의 오류가 나와 재생이 불가합니다.
#opensound=Sound("sounds/열림.wav")
#closesound=Sound("sounds/닫힘.wav")

def startBtn_onMouseAction(x,y,action):
    scene1.enter()
    showMessage('여긴 어디지...')
startBtn.onMouseAction=startBtn_onMouseAction

def door1_onMouseAction(x,y,action):
    if door1.closed:
        if key.inHand():
            door1.setImage('images/문-오른쪽-열림.png')
            showMessage('문 틈새로 어두운 방이 보인다.')
            door1.closed=False
        else:
            showMessage('열리지 않는다...')
    else:
        scene2.enter()
door1.onMouseAction=door1_onMouseAction

def key_onMouseAction(x,y,action):
    key.pick()
key.onMouseAction=key_onMouseAction

jack.moved=False
jack.direct=''
scene2.entered=False
def jack_onMouseAction(x,y,action):
    if jack.moved==False:
        if action==MouseAction.DRAG_LEFT:
            jack.locate(scene1,450,150)
            jack.direct='좌'
        elif action==MouseAction.DRAG_RIGHT:
            jack.locate(scene1,650,150)
            jack.direct='우'
        jack.moved=True
    else:
        if jack.direct=='좌':
            if action==MouseAction.DRAG_RIGHT:
                jack.locate(scene1,550,150)
        elif jack.direct=='좌':
            if action==MouseAction.DRAG_LEFT:
                jack.locate(scene1,550,150)
        jack.moved=False

jack.onMouseAction=jack_onMouseAction


door2.locked=False
door2.clicked=0
def door2_onMouseAction(x,y,action):
    if door2.locked:
        door2.clicked+=1
        if door2.clicked==1:
            showMessage('조금만 더 두드리면 열릴것 같다')
        if door2.clicked==5:
            door2.locked=False
            door2.setImage('images/문-왼쪽-열림.png')
    else:
        scene1.enter()
        scene2.entered=True

door2.onMouseAction=door2_onMouseAction

lighted=True
n=0
def onTimeoutAction():
    global n,lighted
    lighted=not lighted
    if lighted:
        scene2.setLight(1)
        password.hide()
        cellar.hide()
    else:
        scene2.setLight(0.2)
        password.show()
        cellar.show()
    if n<=3:
        n+=1
        timer.set(0.1)
        timer.start()
timer.onTimeout=onTimeoutAction

def onendTimeoutAction():
    endGame()
endtimer.onTimeout=onendTimeoutAction

door3.closed=True
door3.locked=True
door3.clicked=False
def door3_onMouseAction(x,y,action):
    if door3.locked:
        showMessage('문이 잠겨있다.')
        if door3.clicked==False:
            timer.start()
            door3.clicked=True
            door2.locked=True
            door2.setImage('images/문-왼쪽-닫힘.png')
    elif door3.closed:
        door3.setImage('images/문-오른쪽-열림.png')
        door3.closed=False
    else:
        if key.inHand()==False and jack.moved==False:
            startscene.enter()
            showMessage('True-end')
            title.hide()
            startBtn.hide()
            endtimer.start()
        else:
            badscene.enter()
            showMessage('bad-end:모든것을 제자리에 되돌려라')
            endtimer.start()
door3.onMouseAction=door3_onMouseAction

def door3_onKeypad():
    door3.locked=False
door3.onKeypad=door3_onKeypad

def keypad_onMouseAction(x,y,action):
    showKeypad('312',door3)
keypad.onMouseAction=keypad_onMouseAction

def switch_onMouseAction(x,y,action):
    global lighted
    lighted=not lighted
    if lighted:
        scene2.setLight(1)
        password.hide()
        cellar.hide()
    else:
        scene2.setLight(0.25)
        password.show()
        cellar.show()
switch.onMouseAction=switch_onMouseAction

def cellar_onMouseAction(x,y,action):
    startscene.enter()
    showMessage('hidden-end:찝찝한 탈출')
    title.hide()
    startBtn.hide()
    endtimer.start()
cellar.onMouseAction=cellar_onMouseAction
startGame(startscene)