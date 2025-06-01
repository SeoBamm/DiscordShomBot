# Importing Libraries
from datetime import datetime
import time as t
import random as rnd
from discord import ApplicationContext

# Importing Custom Modules
from utils.initialize import embedMaker, coolDownEmbed, printLog, formattedPoint
from utils.embed_color import ErrorEmbedColor
from domain.user.user_service import UserService
from domain.user.user_model import User
from domain.gamble.gamble_service import UserGambleService
from domain.gamble.gamble_model import UserGamble

userService = UserService()
gambleService = UserGambleService()

# 도박, 슬롯머신 쿨타임 상수
COOLDOWN_TIME = 10

async def gambleCommand(ctx: ApplicationContext, gambleTier: str, point: int) -> ApplicationContext.respond:
    """도박 명령어
    
    Args:
        ctx: 명령어 실행 환경
        gambleTier: 위험도(저, 중, 고)
        point: 판돈돈
        
    Returns:
        ApplicationContext.respond: 도박 결과 Embed 출력
    
    """
    if gambleTier == "저위험":
        tier = 0
    elif gambleTier == "중위험":
        tier = 1
    elif gambleTier == "고위험":
        tier = 2

    tierStr = ["저위험", "중위험", "고위험"]
    printLog(ctx, f"도박 {gambleTier} {point}")

    id, guild = ctx.author.id, ctx.guild.id

    if not userService.isUserExist(id, guild):
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤGAMBLE ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False), ephemeral=True)
    
    user = userService.getUserInfo(id, guild)
    userNo = user.user_num
    gambleData = None
    currTime = int(t.time())
    gambleStack = 0
    prevTime = 0

    # 도박을 한번도 안했을 경우
    if not gambleService.gambleDataExists(userNo):
        gambleData = await gambleService.addUserGambleData(userNo)
        
        # gambleService.updateUserGambleData(userNo, currTime, 1)

        gambleStack = 0

    # 도박을 한번이라도 했을 경우
    else:
        gambleData = gambleService.getUserGambleData(userNo)
        gambleStack = gambleData.user_gamble_cnt
        prevTime = gambleData.user_gamble_time

        # gambleService.updateUserGambleData(userNo, currTime, gambleStack)

        print(f"도박횟수: {gambleStack}")

    # 쿨타임 체크 로직
    coolDownData = coolDownEmbed(currTime, prevTime, "도박")
    if coolDownData[0]:
        return await ctx.respond(f"", embed=coolDownData[1], ephemeral=True)

    # 유저가 보유 포인트의 90%를 초과하여 판돈에 걸었을 경우 체크 로직
    userPoint = user.user_point
    if point > userPoint * 0.9:
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤGAMBLE ㅤ ㅤ ㅤ", ErrorEmbedColor)
                                    .add_field(name="ㅤ\nㅤ판돈은 보유 포인트의 90%를 초과할 수 없습니다.ㅤ\n", value="", inline=False)
                                    .add_field(name=f"ㅤ\nㅤ배팅 가능 최대 금액 : `{formattedPoint(int(userPoint * 0.9))} p`ㅤ\nㅤ", value="", inline=False)
                                    , ephemeral=True)
    
    # 유저가 10,000 포인트 미만을 판돈에 걸었을 경우 체크 로직
    elif point < 10000:
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤGAMBLE ㅤ ㅤ ㅤ", ErrorEmbedColor)
                                    .add_field(name="ㅤ\nㅤ판돈은 10,000 포인트 이상이어야 합니다.ㅤ\nㅤ", value="", inline=False)
                                    , ephemeral=True)

    gambleStack += 1
    gambleResult = gambleService.receiveGambleReward(point, tier)
    embed = None

    if gambleResult[0]:

        rewardExp = int(gambleResult[1])
        rewardPoint = int(gambleResult[2])

        userService.addUserPoint(id, guild, rewardPoint)
        userService.addUserExperience(id, guild, rewardExp)

        embed = embedMaker(":star2:ㅤ|ㅤGAMBLE ㅤ ㅤ ㅤ ㅤ ㅤ")
        embed.add_field(name=f"ㅤ\nㅤ{gambleTier}도 도박 승리 !", value=f"", inline=False)
        embed.add_field(name=f"ㅤ\nㅤ승리 보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

    else:

        rewardExp = int(gambleResult[1])
        rewardPoint = int(gambleResult[2])

        userService.subtractUserPoint(id, guild, rewardPoint)
        userService.addUserExperience(id, guild, rewardExp)

        embed = embedMaker(":thunder_cloud_rain:ㅤ|ㅤGAMBLE ㅤ ㅤ ㅤ ㅤ ㅤ")
        embed.add_field(name=f"ㅤ\nㅤ{gambleTier}도 도박 패배..", value=f"", inline=False)
        embed.add_field(name=f"ㅤ\nㅤ패배 보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`- {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

    # 쿨타임 적용 로직
    gambleService.updateUserGambleData(userNo, currTime + COOLDOWN_TIME, gambleStack)
    return await ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)


async def slotCommand(ctx: ApplicationContext, point: int) -> tuple:
    """슬롯머신 명령어
    
    Args:
        ctx: 명령어 실행 환경
        point: 판돈
        
    Returns:
        tuple: 게임여부, Embed(슬롯머신 대기 Embed), Embed(슬롯머신 결과 Embed) 
    
    """
    printLog(ctx, f"슬롯머신 {point}")

    id, guild = ctx.author.id, ctx.guild.id

    if not userService.isUserExist(id, guild):
        return False, embedMaker(":x:ㅤ|ㅤSLOT ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False), None
    
    user = userService.getUserInfo(id, guild)
    userNo = user.user_num
    gambleData = None
    currTime = int(t.time())
    gambleStack = 0
    prevTime = 0

    # 도박을 한번도 안했을 경우
    if not gambleService.gambleDataExists(userNo):
        gambleData = await gambleService.addUserGambleData(userNo)
        
        # gambleService.updateUserGambleData(userNo, currTime, 1)

        gambleStack = 0

    # 도박을 한번이라도 했을 경우
    else:
        gambleData = gambleService.getUserGambleData(userNo)
        gambleStack = gambleData.user_gamble_cnt
        prevTime = gambleData.user_gamble_time
        gambleStack = gambleData.user_gamble_cnt

        # gambleService.updateUserGambleData(userNo, currTime, gambleStack)

        print(f"도박횟수: {gambleStack}")

    # 쿨타임 체크 로직
    coolDownData = coolDownEmbed(currTime, prevTime, "슬롯머신")
    if coolDownData[0]:
        return False, coolDownData[1]

    # 유저가 보유 포인트의 90%를 초과하여 판돈에 걸었을 경우 체크 로직
    userPoint = user.user_point
    if point > userPoint * 0.9:
        return False, embedMaker(":x:ㅤ|ㅤSLOT ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ판돈은 보유 포인트의 90%를 초과할 수 없습니다.ㅤ\n", value="", inline=False).add_field(name=f"ㅤ\nㅤ배팅 가능 최대 금액 : `{formattedPoint(int(userPoint * 0.9))} p`ㅤ\nㅤ", value="", inline=False), None
    
    # 유저가 10,000 포인트 미만을 판돈에 걸었을 경우 체크 로직
    elif point < 10000:
        return False, embedMaker(":x:ㅤ|ㅤSLOT ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ판돈은 10,000 포인트 이상이어야 합니다.ㅤ\nㅤ", value="", inline=False), None
    
    gambleStack += 1
    slotResult = gambleService.receiveSlotReward(point)

    result = slotResult[0]
    resultArray = slotResult[1]
    print(f"슬롯머신 결과: {resultArray}")
    resultSlot = gambleService.showSlotResult(resultArray)
    rewardExp = int(slotResult[2])
    rewardPoint = slotResult[3]
    
    startEmbed = embedMaker(":slot_machine:ㅤ|ㅤSLOT ㅤ ㅤ ㅤ ㅤ ㅤ")
    startEmbed.add_field(name=f"ㅤ\nㅤ슬롯머신을 돌리는 중..ㅤ\nㅤ\nㅤ『ㅤ:question:ㅤ:question:ㅤ:question:ㅤ』ㅤ", value=f"", inline=False)
    startEmbed.add_field(name=f"ㅤ\nㅤ판돈", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`{formattedPoint(point)} p`\nㅤ\nㅤ", inline=False)

    resultEmbed = None

    # 슬롯머신을 돌렸지만 아무것도 안나왔을 경우
    if result == -1:
        userService.subtractUserPoint(id, guild, rewardPoint)
        userService.addUserExperience(id, guild, rewardExp)

        resultEmbed = embedMaker(":thunder_cloud_rain:ㅤ|ㅤSLOT ㅤ ㅤ ㅤ")
        resultEmbed.add_field(name=f"ㅤ\nㅤ슬롯머신 결과 \nㅤ\nㅤ{resultSlot} ㅤ>>ㅤ 꽝..ㅤ", value=f"", inline=False)
        resultEmbed.add_field(name=f"ㅤ\nㅤ패배 보상", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`- {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)
        
    # 슬롯머신을 돌렸을 때 성공했을 경우
    else:
        userService.addUserPoint(id, guild, rewardPoint)
        userService.addUserExperience(id, guild, rewardExp)

        resultEmbed = embedMaker(":star2:ㅤ|ㅤSLOT ㅤ ㅤ ㅤ")
        resultEmbed.add_field(name=f"ㅤ\nㅤ슬롯머신 결과 \nㅤ\nㅤ{resultSlot} ㅤ>>ㅤ 승리 !ㅤ", value=f"", inline=False)
        resultEmbed.add_field(name=f"ㅤ\nㅤ승리 보상", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)


    # 쿨타임 적용 로직
    gambleService.updateUserGambleData(userNo, currTime + COOLDOWN_TIME, gambleStack)
    return True, startEmbed, resultEmbed




    
    

        
