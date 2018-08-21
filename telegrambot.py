import random
import time
from pprint import pprint

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
#KeyboarInterrupt

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

import joke
bot = telepot.Bot('666966463:AAG7z2dG__ocBhBkSaOt07a9R0_CtMPfJTk')

cardList=[["項鍊","戒指"],["手機","平板"],["玻璃杯","馬克杯"],["沙發","板凳"],["充電線","延長線"]
        ,["蛋餅","漢堡"],["瑪莎拉蒂","藍寶堅尼"],["便條紙","A4紙"],["耳環","髮夾"],["Iphon6","Iphone5"]
        ,["拖鞋","布鞋"],["雨傘","雨衣"],["外向","內向"],["躲避球","橄欖球"],["照相機","攝影機"]
        ,["辣椒","芥末"],["端午節","中秋節"],["高麗菜","花椰菜"],["雞絲飯","雞肉飯"],["海豹","海豚"]
        ,["蝴蝶","蜜蜂"],["牛奶","豆漿"],["鍵盤","滑鼠"],["學士","碩士"],["滑板車","腳踏車"]
        ,["塑膠袋","垃圾袋"],["拉麵","泡麵"],["手指頭","腳指頭"],["樹葉","樹枝"],["海王星","冥王星"]
        ,["地球","火星"],[" 牙齒","牙套"],["牛","羊"],["天使","惡魔"],["公車","汽車"]
        ,["超級市場" ,"傳統市場"],["醫生","護士"],["冷氣","暖氣"],["飲料","啤酒"],["口香糖","薄荷糖"]
        ,["瓜子","花生"],["高鐵","地鐵"],["鯊魚","鱷魚"],["貓咪","小狗"],["裙子","熱褲"]
        ,["國民黨","民進黨"],["氣球","泡泡"],["內地人","台灣人"],["陰廟","佛壇"],["真菌","細菌"]]
class Player():
    def __init__(self,name,id):
        self.name=name
        self.id=id
        self.card=""
        self.undercover=False
        self.owner=False
        self.voteRight=True
        self.beenVoted=0
        self.hintRight=True
        self.hasreport=[]
        self.bereport = 0
    def setVoteRight(self):
        self.voteRight = not self.voteRight and self.voteRight
    def setCard(self,card):
        self.card=card
    def setUndercover(self):
        self.undercover=True
    def setowner(self):
        self.owner=True
    def isUndercover(self):
        return self.undercover
    def isowner(self):
        return self.owner
    def getId(self):
        return self.id
    def getCard(self):
        return self.card
    def getName(self):
        return self.name
    def canVote(self):
        return self.voteRight
    def plusVoted(self):
        self.beenVoted+=1
    def getBeenVoted(self):
        return self.beenVoted
    def setBeenVoted(self,Num):
        self.beenVoted=Num
    def canHint(self):
        return self.hintRight
    def setHintRight(self):
        self.hintRight = not self.hintRight and self.hintRight
#是owner嗎?
def isowner(msg,username):
    if players[username].isowner():
        return True
    else:
        return False
#you out!
def deleteplayer(chatID,username):
    global howManyPlayer
    global howmanyundercover
    usernamedata.remove(username)
    howManyPlayer = howManyPlayer - 1
    if players[username].isUndercover():
        howmanyundercover = howmanyundercover - 1
        bot.sendMessage(chatId, '抓到臥底了喔!')
    if players[username].isowner():
        Index = random.choice(usernamedata)
        players[Index].setowner()
        bot.sendMessage(chatId, "owner88了喔,"+str(Index)+'變owner')
    del players[username]
    HintRound = True
#printoutcome and reset
def resetHintRight():
    for username in usernamedata:
        Player = players[username]
        Player.setHintRight()
def resetVotedRight():
    for username in usernamedata:
        votePlayer = players[username]
        votePlayer.setVoteRight()
def printCurrentHint(msg,chatId):
    String = ''
    global thisRoundHints
    for hint in thisRoundHints:
        String = String +' '+ players[username]+'的提示:'+msg['text']
    bot.sendMessage(chatID,'大家給的提示:\n'+String)
    
def Hint(chatId):
    global UnHintedPlayers
    if HintStart == False:
        global players
        for player in players:
            UnHintedPlayers.append(player.getName())
        HintStart = True
    global thisRoundHints
    global Hints
    if HintRound:
        if (players[username].canHint()): ###先判斷有沒有重複提示
            if msg['text'] not in Hints: ###判斷是否為已用過的提示
                Hints.append(msg['text'])
                players[username].setHintRight()
                printCurrentHint(msg,chatId)
                UnHintedPlayers.remove(username)
            else:
                bot.sendMessage(chatId,str(player.getName())+'此提示已用過')
        else:
            bot.sendMessage(chatId,str(player.getName())+'重複提示，請遵守規則')
    else: bot.sendMessage(chatId,"嘖嘖，現在還不是給提示環節啦")
    if len(UnHintedPlayers) == 0:
        bot.sendMessage(chatId,'可以開始投票啦~')
        HintStart = False
        thisRoundHints = []
        resetVotedRight()
        HintRound = False

def printOutcome(chatId):
    global howManyPlayer
    global howmanyundercover
    if howmanyundercover == 0:
        bot.sendMessage(chatId, '臥底都被抓到啦!!')
    elif howmanyundercover < (howManyPlayer - howmanyundercover):
        survive = ''
        for i in range(len(usernamedata)):
            if players[usernamedata[i]].isUndercover():
                pass
            else:
                survive = survive + ' ' + str(usernamedata[i])
        bot.sendMessage(chatId, '正義勝利啦!!')
        bot.sendMessage(chatId, '存活:'+survive)
    elif howmanyundercover >= (howManyPlayer - howmanyundercover):
        bot.sendMessage(chatId, '平民這樣也可以輸?!')
    printunder = ''
    for i in range(len(undercover)):
        printunder = printunder + ' ' + str(undercover[i])
    bot.sendMessage(chatId, '臥底有:'+printunder)
    bot.sendMessage(chatId, "owner 輸入/newgame 開始新遊戲")
    exit()
#產生新遊戲
def newgame(msg):####
    global canjoin
    global canNewgame
    chatId =msg['chat']['id'] 
    bot.sendMessage(chatId,'New game starts!')
    canjoin = True
    canNewgame = False
'''def newgame(msg):
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    global howManyPlayer
    global howmanyundercover
    if len(players) != 0 :
        if username not in usernamedata:
            bot.sendMessage(chatId, "已建立新局,輸/join就好了喔")
        elif isowner(msg,username):
            del usernamedata[:]
            del undercover[:]
            players.clear()
            howManyPlayer = 0
            howmanyundercover = 0
            canjoin = True
            bot.sendMessage(chatId, "已經開始新的遊戲！ 用 /join 加入並用 /start 開始遊戲")
        else:
            bot.sendMessage(chatId,"想幹嘛?")
    else:
        bot.sendMessage(chatId, "已經開始新的遊戲！ 用 /join 加入並用 /start 開始遊戲")'''
#加入遊戲 建構玩家加入玩家列表
'''def join(msg):
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    if username in players:
        bot.sendMessage(chatId, '你加過了,87')
    else:
        global howManyPlayer 
        howManyPlayer += 1
        player = Player(str(msg['from']['first_name'])+str(msg['from']['last_name']),msg['from']['id'])
        if len(players) == 0:
            player.setowner()
        players[username] = player
        usernamedata.append(username)
        String = str(msg['from']['first_name'])+" 已加入遊戲"
        bot.sendMessage(chatId, String)
        String = "現在有"+str(howManyPlayer)+"位玩家"+',owner開始請/start'
        bot.sendMessage(chatId,String)
#開始遊戲 決定誰是臥底 發卡'''
'''def start(msg):
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    if username not in usernamedata:
        bot.sendMessage(chatId, "要先輸/join喔")
    elif not isowner(msg,username):
        bot.sendMessage(chatId,"你誰啊")
    elif len(players) < 2:
        bot.sendMessage(chatId,"在等等吧~~這樣不好玩")
    elif canjoin == False:
        bot.sendMessage(chatId,"開始了喔")
    else:
        randomUndercover()
        assignCard(players)
        sendCardMesaage(players)
        bot.sendMessage(chatId,"遊戲開始!")
        canjoin = False
        HintRound = True
        bot.sendMessage(chatId,'現在請大家說出自己的提示')
        #go(chatId)'''
def WhosMole(msg):###呼叫遊戲
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    global howManyPlayer
    global howmanyundercover
    global usernamedata
    global undercover
    global players
    global canStart
    if len(players) != 0 :
        if canStart and username == usernamedata[0]:###判斷是否能開始遊戲
            bot.sendMessage(chatId, 'Hi!', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/start"), KeyboardButton(text="/gameRule")]]
                                ))
        else: 
            if canjoin and username not in usernamedata:###判斷是否能加入遊戲
                bot.sendMessage(chatId, 'Welcome to Who\'s mole game', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/join"), KeyboardButton(text="/gameRule")]]))
            elif isowner(msg,username)and canNewgame:###判斷使否為owner且是否能開始遊戲(在建立newgame到start之間不能再newgame)
                del usernamedata[:]
                del undercover[:]
                players.clear()
                howManyPlayer = 0
                howmanyundercover = 0
                bot.sendMessage(chatId, 'Welcome to Who\'s mole game', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/newgame"), KeyboardButton(text="/gameRule")]]
                                ))
                setOwner(msg)###因為owner不用再輸入一次/join，所以在這建立所需資訊
            else:###遊戲已啟動後，呼叫WhosMole只會有gameRule的選項
                bot.sendMessage(chatId, 'Hi!',reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/gameRule")]]))
    elif len(players) == 0:
        bot.sendMessage(chatId, 'Welcome to Who\'s mole game', reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(text="/newgame"), KeyboardButton(text="/gameRule")]]
                        ))
        setOwner(msg)###因為owner不用再輸入一次/join，所以在這建立所需資訊

def setOwner(msg):###owner建立資訊的地方
    username = '@' + msg['from']['username']
    global howManyPlayer
    global players
    global usernamedata
    howManyPlayer += 1
    player = Player(str(msg['from']['first_name']),msg['from']['id'])    
    player.setowner()
    players[username] = player
    usernamedata.append(username)
    print('usernamedata:',usernamedata)
    print('players:',players)

def join(msg):###一般玩家加入遊戲的function，玩家數超過4位時，便可以啟動/start
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    if username in players:
        bot.sendMessage(chatId, '你加過了,87')
    else:
        global howManyPlayer
        howManyPlayer += 1
        player = Player(str(msg['from']['first_name']),msg['from']['id'])        
        players[username] = player
        usernamedata.append(username)
        String = str(msg['from']['first_name'])+" 已加入遊戲"
        bot.sendMessage(chatId, String)
        String = "現在有"+str(howManyPlayer)+"位玩家"
        bot.sendMessage(chatId,String)
        if len(usernamedata) >= 4:###玩家數超過4位時，便可以啟動/start
            global canStart
            String = "已達遊戲最低人數,owner可以輸入「WhosMole」來開始遊戲!"
            bot.sendMessage(chatId,String)
            canStart = True
        print(usernamedata)
        
def start(msg):####start啟動後，不能再join、start;但可以newgame
    global canStart
    global HintRound
    global canNewgame
    chatId=msg['chat']['id']
    username = '@' + msg['from']['username']
    global canjoin
    if username not in usernamedata:
        bot.sendMessage(chatId, "要先輸'WhosMole'或'/join'喔")
    elif not isowner(msg,username):
        bot.sendMessage(chatId,"你誰啊")
    elif len(players) < 4:
        bot.sendMessage(chatId,"在等等吧~~這樣不好玩")
    elif canjoin == False:
        bot.sendMessage(chatId,"開始了喔")
    else:
        randomUndercover()
        assignCard(players)
        sendCardMesaage(players)
        bot.sendMessage(chatId,"遊戲開始!")
        ####start啟動後，不能再join、start;但可以newgame
        canjoin = False
        HintRound = True
        canNewgame = True
        canStart = False
        bot.sendMessage(chatId,'現在請大家說出自己的提示')
        #go(chatId)
def gameRule(msg):###遊戲規則講解
    chatId = msg['chat']['id']
    bot.sendMessage(chatId,'【誰是臥底-遊戲規則】\n'
                    +'此遊戲會將參加者分為兩隊，並且BOT會各自私訊題目\n'
        +'在不公布答案的條件下，參加者輪流提示自己的題目\n'
        +'並判斷究竟自己是臥底方還是平民方，在投票時將敵方投票出局。\n'
        +'若自己是臥底，努力生存到臥底方人數和平民方人數一樣時便能獲勝;\n'
        +'如果是平民方，將全數臥底方投票出局便能獲勝。')  
     
#指令控制中心
def handle(msg):
    global chatId
    global canNewgame
    chatId = msg['from']['id']
    pprint(msg)
    username = '@' + msg['from']['username']
    massage = msg['text'].split(' ')
    if( massage[0]=='WhosMoleGame'):####修正
        WhosMole(msg)
        print("hi")
    if not canjoin and (username not in players):
        pass
    else:
        if( massage[0]=="/join"):
            join(msg)
        elif( massage[0]=='/newgame'and canNewgame):
            newgame(msg)
        elif( massage[0]=='/start'):
            start(msg)
        elif( massage[0]=='/help'):
            help(msg)
        elif ( massage[0]=='/hint'):
            Hint(msg['chat']['id'])
        #elif(len(massage)==2 and massage[0]=='/vote' ):
        # ↑↑ 上面的elif是原本的程式碼,因為要嘗試讓def haha運行,所以改成下面的程式
        elif( massage[0]=='/haha' ):
            targetName=massage[0]
            showVoteButton(msg,username,targetName)
            
            #vote(msg['chat']['id'],username,targetName)
            # ↑↑ 原本def vote的資料
        elif(len(massage)==2 and massage[0]=='/report' ):
            targetName = massage [1]
            report(msg,msg['chat']['id'],targetName,username)
        elif ('/笑話' in msg['text']):
            Data = joke.main(msg)
            bot.sendMessage(msg['chat']['id'],random.choice(Data))
        elif( massage[0]=='/voteStatus'):
            printVote(msg['chat']['id'])
        elif( massage[0]=='haha'):
            bot.sendMessage(msg['chat']['id'],"笑屁")
        elif( massage[0]=='你可以滾了'):
            bot.sendMessage(msg['chat']['id'],"http://i.imgur.com/rAVzont.jpg")
        elif( massage[0]=='傻眼'):
            bot.sendMessage(msg['chat']['id'],"https://i.imgur.com/iU6V8Ja.png")
        elif(massage[0]=='@WhoIsUndercoverBot'):
            bot.sendMessage(msg['chat']['id'],"幹嘛（‘·д·）")
        elif(massage[0]=='問號'):
            bot.sendMessage(msg['chat']['id'],"http://i.imgur.com/friaaLF.jpg")
        elif(massage[0]=="test"):
            printOutcome(msg['chat']['id'])
        elif(massage[0]=="/gameRule"):
            gameRule(msg)
def checkName(String):
    if(String in usernamedata):
        return True
    else:
        return False
#發卡
def assignCard(players):
    cardList1 = random.choice(cardList)
    for player in players:
        if players[player].isUndercover():
            players[player].setCard(cardList1[0])
        else :
            players[player].setCard(cardList1[1])
#隨機抽臥底
def randomUndercover():
    global howManyPlayer
    global howmanyundercover
    howmanyundercover = howManyPlayer // 4
    Index = random.sample(usernamedata,howmanyundercover)
    for i in range(len(Index)):
        players[Index[i]].setUndercover()
        undercover.append(Index[i])
#傳送
def sendCardMesaage(players):
    for player in players:
        bot.sendMessage(players[player].getId(),players[player].getCard())
def status(msg):
    global howManyPlayer
    chatId=msg['chat']['id']
    String = "現在有"+str(howManyPlayer)+"位玩家"
    bot.sendMessage(chatId,String)
    allplayer = ''
    for player in players:
        allplayer = allplayer +' '+ player
    bot.sendMessage(chatId,'玩家有:'+ allplayer)
#    String = "臥底是"+str(undercover.getName())
#    bot.sendMessage(chatId,String)
def help(msg):
    chatId=msg['chat']['id']
    bot.sendMessage(chatId,"/newgame 重新遊戲")
    bot.sendMessage(chatId,"/start 開始遊戲")
    bot.sendMessage(chatId,"/join 加入遊戲")

def on_callback_query(msg):
    global usernamedata
    global chatId
    global isButtonTime
    global button
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    if(query_data in usernamedata):
        vote(chatId,("@"+str(msg['from']['username'])),query_data)
    elif(query_data == "結束投票"):
        global message_with_inline_keyboard
        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            print("idf",msg_idf)
            bot.editMessageText(msg_idf, printVote())
        else:
            bot.answerCallbackQuery(query_id, text='No previous message to edit')
    bot.answerCallbackQuery(query_id, text='投票囉')

def resetVotedNumber():
    for username in usernamedata:
        votePlayer = players[username]
        votePlayer.setBeenVoted(0)

def vote(chatId,username,VotedUsername):
    # ↑↑ def vote沒動
    print('vote這裡')
    
    global canvote
    if canvote :
        if(players[username].canVote()):
   
            players[VotedUsername].plusVoted()
        else:
            bot.sendMessage(chatId,"投票過了87")
        
        players[username].setVoteRight()
    elif HintRound == True:
        Str = ''
        global UnHintedPlayers
        for player in UnHintedPlayers:
            Str = Str+ '' +player
        bot.sendMessage(chatId,"提示環節還未結束啊啊\n"+Str+'快點提示!')

    else:
        bot.sendMessage(chatId,"嘖嘖，現在不能投阿")
     

def showVoteButton(msg,username,targetName):
    pprint(msg)
    global usernamedata
    global keyboards
    global players
    global message_with_inline_keyboard
    print('我是haha')
    if(len(keyboards)>0):
        del keyboards[:]
    for username in usernamedata:
        keyboards.append([InlineKeyboardButton(text=(players[username].getName()), callback_data=username)])
    keyboards.append([InlineKeyboardButton(text="結束投票", callback_data="結束投票")])
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard = keyboards)
    message_with_inline_keyboard = bot.sendMessage(chat_id, "現在開始投票", reply_markup = keyboard)
    print('我是XDXDXDXD')
    
def printVote():
    String=""
    global canvote
    if canvote :
        for username in usernamedata:
            votePlayer = players[username]
            String=String + votePlayer.getName() + "被投了" + str(votePlayer.getBeenVoted()) + "票" + "\r\n"
        return String
    else:
         bot.sendMessage(chatId,'還沒投呢!')
         
         
         
'''def printUsername(chatId):
    String=""
    for username in usernamedata:
        votePlayer = players[username]
        String=String + votePlayer.getName() + ":" + username + "\r\n"
    bot.sendMessage(chatId,String)'''

def checkWhoisMaxVoted():
    maxVotePlayer = players[username[0]]
    for username in usernamedata:
        votePlayer = players[username]
        if(votePlayer.getBeenVoted() > maxVotePlayer.getBeenVoted()):
            maxVotePlayer=username
    return maxVotePlayer
'''def timer(chatId,n,sec):  
    
    每n秒執行一次
    
    while True:
        if sec == 0 :
            break
        bot.sendMessage(chatId,str(sec))
        sec -= 1
        time.sleep(n)'''

def deletereport(msg,chatId,targetName):
    global howManyPlayer
    global howmanyundercover
    deleteplayer(chatId,targetName)
    bot.sendMessage(chatId,targetName + "你太壞了掰掰囉")
    if howmanyundercover == 0:
        bot.sendMessage(chatId,"沒臥底了")
        newgame(msg)
def deleterecord(username):
    for I in players[username].hasreport:
	    players[I].bereport -= 1
def report(msg,chatId,targetName,username):
    if username not in usernamedata:
        bot.sendMessage(chatId,"乾～你又沒玩檢舉屁喔")
    elif targetName not in usernamedata:
        bot.sendMessage(chatId,"此人不在遊戲內！！87")
    
    elif targetName in players[username].hasreport:
        bot.sendMessage(chatId,"你要讓他死嗎？")
    
    else:
        players[username].hasreport.append(targetName)
        players[targetName].bereport += 1
        bot.sendMessage(chatId,targetName + "被檢舉了")
        if players[targetName].bereport >= howManyPlayer//2:
            # deleteplayer(chatId,targetName)
            deleterecord(targetName)
            deletereport(msg,chatId,targetName)
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()#等候輸入
message_with_inline_keyboard=None
keyboards=[]
chatId=0
players = {} #@username player
Hints = []
usernamedata = []
howManyPlayer = 0
howmanyundercover = 0
undercover = []
canjoin = True
HintRound = False
canvote = True
isButtonTime = True
canNewgame = True
thisRoundHints = {}
UnHintedPlayers = []
while 1:
    time.sleep(1)