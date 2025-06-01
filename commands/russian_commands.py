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
from domain.russian.russian_service import UserRussianService
from domain.russian.russian_model import UserRussian

userService = UserService()
russianService = UserRussianService()

# 러시안 룰렛 쿨타임 상수
COOLDOWN_TIME = 1200

async def russianRouletteCommand(ctx: ApplicationContext) -> ApplicationContext.respond:
    """러시안룰렛 명령어
    
    Args:
        ctx: 명령어 실행 환경
        
    Returns:
        ApplicationContext.respond: 러시안룰렛 결과 Embed 출력
    
    """
    printLog(ctx, "러시안룰렛")

    id, guild = ctx.author.id, ctx.guild.id

    if not userService.isUserExist(id, guild):
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤRUSSIAN ROULETTEㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False), ephemeral=True)
    
    user = userService.getUserInfo(id, guild)
    userNo = user.user_num
    russianData = None
    currTime = int(t.time())
    russianStack = 0
    russianDead = 0
    prevTime = 0

    # 러시안룰렛을 한번도 안했을 경우
    if not russianService.russianDataExists(userNo):
        russianData = await russianService.addUserRussianData(userNo)
        
        # russianService.updateUserRussianData(userNo, currTime, 1)

        russianStack = 0
        russianDead = 0

    # 러시안룰렛을 한번이라도 했을 경우
    else:
        russianData = russianService.getUserRussianData(userNo)
        russianStack = russianData.user_russian_cnt
        russianDead = russianData.user_russian_dead
        prevTime = russianData.user_russian_time

        print(f"러시안룰렛 스택: {russianStack}")

    # 쿨타임 체크 로직
    coolDownData = coolDownEmbed(currTime, prevTime, "러시안룰렛")
    if coolDownData[0]:
        return await ctx.respond(f"", embed=coolDownData[1], ephemeral=True)
    
    point = user.user_point
    # 유저의 소지금이 10,000 포인트 미만일 경우
    if point < 10000:
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤRUSSIAN ROULETTEㅤ ㅤ ㅤ", ErrorEmbedColor)
                                    .add_field(name="ㅤ\nㅤ소지금이 10,000 포인트 이상이어야 합니다.ㅤ\nㅤ", value=""
                                    , inline=False), ephemeral=True)
    
    exp = user.user_exp
    russianStack += 1
    russianReward = russianService.receiveRussianReward(point, exp)
    embed = None

    if russianReward[0]:

        rewardExp = int(russianReward[1])
        rewardPoint = russianReward[2]

        userService.addUserPoint(id, guild, rewardPoint)
        userService.addUserExperience(id, guild, rewardExp)

        embed = embedMaker(":zany_face:ㅤ|ㅤRUSSIAN ROULETTEㅤ ㅤ ㅤ")
        embed.add_field(name="ㅤ\nㅤ생존 !ㅤ", value=f"", inline=False)
        embed.add_field(name=f"ㅤ\nㅤ생존 보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)

    else:

        userService.setUserPoint(id, guild, 0)
        userService.setUserExperience(id, guild, 0)
        
        russianDead += 1 
        russianService.updateUserRussianDead(userNo, russianDead)

        embed = embedMaker(":skull:ㅤ|ㅤRUSSIAN ROULETTEㅤ ㅤ ㅤ")
        embed.add_field(name=f"ㅤ\nㅤ사망 !ㅤ\nㅤ", value=f"ㅤㅤ**포인트, 경험치 초기화!**ㅤ\nㅤ", inline=False)

    # 쿨타임 적용 로직
    russianService.updateUserRussianData(userNo, currTime + COOLDOWN_TIME, russianStack)
    return await ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)

    