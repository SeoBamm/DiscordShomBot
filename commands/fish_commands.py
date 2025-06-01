# Importing Libraries
from datetime import date, timedelta
import time as t
import random as rnd
from discord import ApplicationContext

# Importing Custom Modules
from utils.initialize import embedMaker, coolDownEmbed, inProgressEmbed, printLog, formattedPoint, getLevelInfo
from utils.embed_color import DefaultEmbedColor, ErrorEmbedColor
from domain.user.user_service import UserService
from domain.user.user_model import User
from domain.fish.fish_service import UserFishService
from domain.fish.fish_model import UserFish

userService = UserService()
userFishService = UserFishService()

# 낚시 쿨타임 상수
COOLDOWN_TIME = 5

# 낚시 시간 상수
FISH_TIME = 8

# 물고기 종류 상수
FISH_LIST = [
    "정어리",   # Sardine
    "고등어",   # Mackerel
    "멸치",     # Anchovy
    "방어",     # Yellowtail
    "농어",     # Sea bass
    "참치",     # Tuna
    "전갱이",   # Jack mackerel
    "도미",     # Sea bream
    "우럭",     # Rockfish
    "광어",     # Flounder
    "노래미",   # Greenling
    "갈치",     # Hairtail
    "삼치",     # Spanish mackerel
    "참돔",     # Red sea bream
    "붉바리",   # Grouper
    "쥐노래미", # Korean rockfish
    "가자미",   # Flatfish
    "다랑어",   # Bonito
    "대구",     # Cod
    "방석고기"  # John Dory
]

async def fishBefore(ctx: ApplicationContext) -> tuple:
    """낚시 지연 명령어
    
    Args:
        ctx: 명령어 실행 환경

    Returns:
        tuple: 게임여부, 지연 시간, Embed 리스트
    """
    printLog(ctx, "낚시")

    id, guild = ctx.author.id, ctx.guild.id

    if not userService.isUserExist(id, guild):
        return False, 0, embedMaker(":x:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False)
    
    user = userService.getUserInfo(id, guild)
    userNo = user.user_num
    fishData = None
    currTime = int(t.time())
    prevTime = 0

    # 현재 낚시를 하고 있는지 확인
    fishNow = 0

        # 낚시를 한번도 안했을 경우
    if not userFishService.fishDataExists(userNo):
        fishData = await userFishService.addUserFishData(userNo)

        fishNow = 0

    # 낚시를 한번이라도 했을 경우
    else:
        fishData = userFishService.getUserFishData(userNo)
        
        prevTime = fishData.user_fish_time
        fishNow = fishData.user_fish_now

    # 명령어 수행 중 체크 로직
    inProgressData = inProgressEmbed(fishNow, "낚시")
    if inProgressData[0]:
        return False, 0, inProgressData[1]
    
    # 쿨타임 체크 로직
    coolDownData = coolDownEmbed(currTime, prevTime, "낚시")
    if coolDownData[0]:
        return False, 0, coolDownData[1]
    
    # 명령어 수행 중 처리
    fishDelay = int(FISH_TIME * rnd.uniform(0.5, 1.2))
    userFishService.toggleFishNow(userNo)

    embedList = []

    for i in range(4):
        
        dots = (i+1) * "." 
        embedList.append(embedMaker(":fishing_pole_and_fish:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name=f"ㅤ\nㅤ낚시 하는 중{dots}ㅤ\nㅤ", value="", inline=False))


    printLog(ctx, f"낚시 시작, {fishDelay}초 대기")

    return True, fishDelay, embedList


async def fishAfter(ctx: ApplicationContext) -> tuple:
    """낚시 명령어
    
    Args:
        ctx: 명령어 실행 환경
        
    Returns:
        tuple: 게임여부, Embed(낚시 결과 Embed)
    
    """

    try:
        id, guild = ctx.author.id, ctx.guild.id

        user = userService.getUserInfo(id, guild)
        userNo = user.user_num
        currTime = int(t.time())

        fishData = userFishService.getUserFishData(userNo)
        fishStack = fishData.user_fish_cnt
        fishSuccess = fishData.user_fish_success
        fishGreat = fishData.user_fish_great
        fishBoots = fishData.user_fish_boots
        fishBlow = fishData.user_fish_blow
        
        exp = user.user_exp
        userLevel = getLevelInfo(exp)[0]
        fishStack += 1
        
        userFishService.toggleFishNow(userNo)
        embed = None

        # 낚시 결과 확인
        userFishService.toggleFishNow(userNo)
        result, rewardExp, rewardPoint, rewardCode = userFishService.receiveFishReward(userLevel, fishBoots, fishStack)

        fishStack += 1

        # 실패했을 경우
        if result == 0:

            embed = embedMaker(":thunder_cloud_rain:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name="ㅤ\nㅤ낚시 실패 !ㅤ", value="", inline=False)
            embed.add_field(name=f"ㅤ\nㅤ보상  ", value=f"ㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

        # 성공했을 경우
        elif result == 1:

            fishSuccess += 1
            fish = rnd.choice(FISH_LIST)

            embed = embedMaker(":fish:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name=f"ㅤ\nㅤ야생의 `{fish}` 을(를) 잡았습니다 !ㅤ", value="", inline=False)
            embed.add_field(name=f"ㅤ\nㅤ보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

            userService.addUserPoint(id, guild, rewardPoint)

        # 부츠를 낚았을 경우
        elif result == 2:

            fishBoots += 1

            # 부츠를 77번 낚았을 경우
            if rewardCode == 1:

                embed = embedMaker(":boot:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name="ㅤ\nㅤ77번째 부츠로 황금 장화를 낚았습니다 !ㅤ", value="", inline=False)
                embed.add_field(name=f"ㅤ\nㅤ보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

            else:
            
                embed = embedMaker(":boot:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name="ㅤ\nㅤ버려진 장화를 낚았습니다 !ㅤ", value="", inline=False)
                embed.add_field(name=f"ㅤ\nㅤ보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

            userService.addUserPoint(id, guild, rewardPoint)

        # 복어를 낚았을 경우
        elif result == 3:

            fishBlow += 1

            embed = embedMaker(":blowfish:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name="ㅤ\nㅤ이런! 복어를 잡았습니다 !ㅤ", value="", inline=False)
            embed.add_field(name=f"ㅤ\nㅤ보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`- {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

            userService.subtractUserPoint(id, guild, rewardPoint)

        # 월척을 낚았을 경우
        elif result == 4:

            fishGreat += 1
            fish = rnd.choice(FISH_LIST)

            # 첫 낚시부터 월척을 낚았을 경우
            if rewardCode == 1:

                embed = embedMaker(":troical_fish:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name=f"ㅤ\nㅤ엄청나게 커다란 `{fish}` 을(를) 잡았습니다 !ㅤ\nㅤ\nㅤ첫 낚시부터 월척을 낚았습니다 !ㅤㅤ", value="", inline=False)
                embed.add_field(name=f"ㅤ\nㅤ보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

            else:

                embed = embedMaker(":tropical_fish:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", DefaultEmbedColor).add_field(name=f"ㅤ\nㅤ엄청나게 커다란 `{fish}` 을(를) 잡았습니다 !ㅤ", value="", inline=False)
                embed.add_field(name=f"ㅤ\nㅤ보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

            userService.addUserPoint(id, guild, rewardPoint)
        
        userService.addUserExperience(id, guild, rewardExp)

        # 쿨타임 적용 로직
        userFishService.updateUserFishData(userNo, currTime + COOLDOWN_TIME, fishStack, fishSuccess, fishGreat, fishBoots, fishBlow, fishNow=0)
        
        return True, embed

    except Exception as e:
        print(f"Error in fishCommand: {e}")
        return False, embedMaker(":x:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ오류 발생 !", value="", inline=False)










