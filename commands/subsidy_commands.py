# Importing Libraries
from datetime import date, timedelta
import time as t
from discord import ApplicationContext

# Importing Custom Modules
from utils.initialize import embedMaker, coolDownEmbed, printLog, formattedPoint
from utils.embed_color import ErrorEmbedColor
from domain.user.user_service import UserService
from domain.user.user_model import User
from domain.subsidy.subsidy_service import UserSubsidyService
from domain.subsidy.subsidy_model import UserSubsidy

userService = UserService()
subsidyService = UserSubsidyService()

# 지원금 쿨타임 상수
COOLDOWN_TIME = 600

async def subsidyCommand(ctx: ApplicationContext) -> ApplicationContext.respond:
    """지원금 명령어
    
    Args:
        ctx: 명령어 실행 환경
         
    Returns:
        ApplicationContext.respond: 지원금 결과 Embed 출력
    
    """
    printLog(ctx, "지원금")

    id, guild = ctx.author.id, ctx.guild.id

    if not userService.isUserExist(id, guild):
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤSUBSIDY ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False), ephemeral=True)
    
    user = userService.getUserInfo(id, guild)
    userNo = user.user_num
    subsidyData = None
    currTime = int(t.time())
    subsidyStack = 0
    prevTime = 0

    # 지원금을 한번도 안받았을 경우
    if not subsidyService.subsidyDataExists(userNo):
        subsidyData = await subsidyService.addUserSubsidyData(userNo)
        
        # subsidyService.updateUserSubsidyData(userNo, currTime, 1)

        subsidyStack = 0

    # 지원금을 한번이라도 받았을 경우
    else:
        subsidyData = subsidyService.getUserSubsidyData(userNo)
        subsidyStack = subsidyData.user_subsidy_cnt
        prevTime = subsidyData.user_subsidy_time

        print(f"지원금 스택: {subsidyStack}")

    # 쿨타임 체크 로직
    coolDownData = coolDownEmbed(currTime, prevTime, "지원금")
    if coolDownData[0]:
        return await ctx.respond(f"", embed=coolDownData[1], ephemeral=True)
    
    userPoint = user.user_point    
    subsidyStack += 1
    rewardPoint = subsidyService.receiveSubsidyReward(userPoint)

    userService.addUserPoint(id, guild, rewardPoint)

    embed = embedMaker(":moneybag:ㅤ|ㅤSUBSIDY ㅤ ㅤ ㅤ")
    embed.add_field(name="ㅤ\nㅤ지원금을 성공적으로 받았습니다.ㅤ", value=f"", inline=False)
    embed.add_field(name=f"ㅤ\nㅤ지원금ㅤ", value=f"ㅤㅤ**포인트ㅤ**:ㅤ`+ {formattedPoint(rewardPoint)} p`ㅤ\nㅤ", inline=False)

    # 쿨타임 적용 로직
    subsidyService.updateUserSubsidyData(userNo, currTime + COOLDOWN_TIME, subsidyStack)
    return await ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)
    