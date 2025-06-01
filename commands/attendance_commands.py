# Importing Libraries
from datetime import date, timedelta
import time as t
from discord import ApplicationContext

# Importing Custom Modules
from utils.initialize import embedMaker, printLog, formattedPoint
from utils.embed_color import ErrorEmbedColor
from domain.user.user_service import UserService
from domain.user.user_model import User
from domain.attendance.attendance_service import UserAttendanceService
from domain.attendance.attendance_model import UserAttendance

userService = UserService()
attendanceService = UserAttendanceService()

async def attendanceCommand(ctx: ApplicationContext) -> ApplicationContext.respond:
    """출석체크 명령어
    
    Args:
        ctx: 명령어 실행 환경
        
    Returns:
        ApplicationContext.respond: 출석 결과 Embed 출력
    
    """
    printLog(ctx, "출석체크")

    id, guild = ctx.author.id, ctx.guild.id

    if not userService.isUserExist(id, guild):
        return await ctx.respond(f"||<@!{ctx.user.id}>||", embed=embedMaker(":x:ㅤ|ㅤATTENDANCE ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False), ephemeral=True)

    user = userService.getUserInfo(id, guild)
    userNo = user.user_num
    attendanceData = None
    currDate = date.today()
    attTotal, attStack = 0, 0

    # 출석체크를 한번도 안했을 경우
    if not attendanceService.attendanceDataExists(userNo):
        attendanceData = await attendanceService.addUserAttendanceData(userNo)
        
        attendanceService.updateUserAttendanceData(userNo, currDate, 1, 1)

        attTotal, attStack = 1, 1

    # 출석체크를 한번이라도 했을 경우
    else:
        attendanceData = attendanceService.getUserAttendanceData(userNo)
        attTotal = attendanceData.user_att_total
        attStack = attendanceData.user_att_stack

        print(f"출석일: {currDate}, 연속출석일: {attStack}, 누적출석일: {attTotal}")
    
        # 이미 출석했을 경우 처리 로직
        lastDate = attendanceData.user_att.date()
        if lastDate == currDate:

            return await ctx.respond(f"", embed=embedMaker(":clock3:ㅤ|ㅤATTENDANCE ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ오늘은 이미 출석체크를 완료했습니다.ㅤ\nㅤ", value="", inline=False), ephemeral=True)
        
        # 연속 출석일 끊김유무에 따른 처리 로직
        if lastDate < currDate - timedelta(days=1):
            attTotal += 1
            attStack = 1

        else:
            attTotal += 1
            attStack += 1

        attendanceService.updateUserAttendanceData(userNo, currDate, attTotal, attStack)

    rewardExp, rewardPoint = attendanceService.receiveAttendanceReward(attTotal, attStack)

    # exp, point = user.user_exp, user.user_point
    # resultExp, resultPoint = exp + rewardExp, point + rewardPoint

    userService.addUserPoint(id, guild, rewardPoint)
    userService.addUserExperience(id, guild, rewardExp)

    embed = embedMaker(":calendar:ㅤ|ㅤATTENDANCE ㅤ ㅤ ㅤ ㅤ ㅤ")
    embed.add_field(name=f"ㅤ\nㅤ`{currDate}` 출석체크 완료 !", value=f"", inline=False)
    embed.add_field(name=f"ㅤ\nㅤ출석 보상  ", value=f"ㅤㅤ**포인트ㅤ:**ㅤ`+ {formattedPoint(rewardPoint)} p`\nㅤㅤ**경험치ㅤ:**ㅤ`+ {rewardExp} exp`\nㅤ", inline=False)
    embed.add_field(name=f"ㅤ\nㅤ연속 출석일ㅤ: ㅤ`{attStack}` 일ㅤ\nㅤ누적 출석일ㅤ: ㅤ`{attTotal}` 일ㅤ\nㅤ", value=f"", inline=False)

    return await ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)

async def attendanceInfoCommand(ctx: ApplicationContext) -> ApplicationContext.respond:
    """출석 정보 명령어
    
    Args:
        ctx: 명령어 실행 환경
        
    Returns:
        ApplicationContext.respond: 출석 정보 Embed 출력
    
    """
    printLog(ctx, "출석정보")

    id, guild = ctx.author.id, ctx.guild.id

    if not userService.isUserExist(id, guild):
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤATTENDANCE INFO ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False), ephemeral=True)

    user = userService.getUserInfo(id, guild)
    name = user.user_name
    userNo = user.user_num
    attendanceData = None

    attDate = None

    if not attendanceService.attendanceDataExists(userNo):
        
        return await ctx.respond(f"", embed=embedMaker(":x:ㅤ|ㅤATTENDANCE INFO ㅤ ㅤ ㅤ", ErrorEmbedColor).add_field(name="ㅤ\nㅤ출석체크를 한번도 하지 않았습니다.ㅤ\nㅤ", value="", inline=False), ephemeral=True)

    else:
        attendanceData = attendanceService.getUserAttendanceData(userNo)

    attDate = attendanceData.user_att
    attTotal = attendanceData.user_att_total
    attStack = attendanceData.user_att_stack

    attDate = attDate.date()

    embed = embedMaker(":calendar:ㅤ|ㅤATTENDANCE INFO ㅤ ㅤ ㅤ")
    embed.add_field(name=f"ㅤ\nㅤ' {name} 'ㅤ 님의 출석 정보ㅤ", value=f"", inline=False)
    embed.add_field(name=f"ㅤ\nㅤ최근 출석일ㅤ: ㅤ`{attDate}`ㅤ\nㅤ연속 출석일ㅤ: ㅤ`{attStack}` 일ㅤ\nㅤ누적 출석일ㅤ: ㅤ`{attTotal}` 일ㅤ\nㅤ", value=f"", inline=False)

    return await ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)




        




