# Importing Libraries
from discord import ApplicationContext

# Importing Custom Modules
from utils.initialize import embedMaker, printLog, getLevelInfo, formattedPoint, getExpBar
from utils.embed_color import ErrorEmbedColor
from domain.user.user_service import UserService
from domain.user.user_model import User

service = UserService()

async def registerCommand(ctx: ApplicationContext) -> ApplicationContext.respond:
    """가입 명령어
    
    Args:
        ctx: 명령어 실행 환경
        
    Returns:
        ApplicationContext.respond: 가입 결과 Embed 출력
    
    """
    printLog(ctx, "가입")

    response = await service.addUser(ctx.author.id, ctx.guild.id, ctx.author.display_name)

    if response == 1:
        embed = embedMaker(":white_check_mark:ㅤ|ㅤREGISTER ㅤ ㅤ")
        embed.add_field(name="ㅤ\nㅤ가입이 완료되었습니다.ㅤ", value="ㅤ\nㅤ`/프로필` 명령어로 프로필을 확인하세요.ㅤ\nㅤ", inline=False)

    elif response == 2:
        embed = embedMaker(":x:ㅤ|ㅤREGISTER ㅤ ㅤ", ErrorEmbedColor)
        embed.add_field(name="ㅤ\nㅤ가입 과정에서 오류 발생.ㅤ", value="ㅤ\nㅤ관리자에게 문의하세요.ㅤ\nㅤ", inline=False)

    else:
        embed = embedMaker(":warning:ㅤ|ㅤREGISTER ㅤ ㅤ")
        embed.add_field(name="ㅤ\nㅤ이미 가입된 유저입니다.ㅤ", value="ㅤ\nㅤ`/프로필` 명령어로 프로필을 확인하세요.ㅤ\nㅤ", inline=False)

    return await ctx.respond(f"", embed=embed, ephemeral=True)

def profileCommand(ctx: ApplicationContext) -> ApplicationContext.respond:
    """프로필 명령어
    
    Args:
        ctx: 명령어 실행 환경
        
    Returns:
        ApplicationContext.respond: 프로필 Embed 출력
    
    """
    printLog(ctx, "프로필")
    
    id, guild = ctx.author.id, ctx.guild.id

    user = service.getUserInfo(id, guild)
    embed = None

    if user is None:
        embed = embedMaker(":x:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
        embed.add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False)

    else:
        name = user.user_name
        point = user.user_point
        level, exp, percent = getLevelInfo(user.user_exp)
        embed = embedMaker(":globe_with_meridians:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ")
        embed.add_field(name=f"ㅤ\nㅤ' {name} 'ㅤ 님의 프로필ㅤ", value="", inline=False)
        embed.add_field(name=f"ㅤ\nㅤ레벨, 경험치ㅤ: ㅤ{level} Lv, ㅤ{exp} exp / 1024 ㅤ\nㅤ{getExpBar(percent)}", value="", inline=False)
        embed.add_field(name=f"ㅤ\nㅤ보유 포인트ㅤ: ㅤ`{formattedPoint(point)} p`ㅤ\nㅤ", value=f"", inline=False)

    return ctx.respond(f"", embed=embed, ephemeral=False)

def changeNicknameCommand(ctx: ApplicationContext, newName: str) -> ApplicationContext.respond:
    """닉네임 변경 명령어
    
    Args:
        ctx: 명령어 실행 환경
        
    Returns:
        ApplicationContext.respond: 닉네임 변경 결과 Embed 출력
    
    """
    printLog(ctx, f"닉변 {newName}")

    id, guild = ctx.author.id, ctx.guild.id
    embed = None

    if service.isUserExist(id, guild):

        user = service.getUserInfo(id, guild)
        prevName = user.user_name

        if " " in newName:
            embed = embedMaker(":x:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
            embed.add_field(name="ㅤ\nㅤ닉네임에는 공백이 포함될 수 없습니다.\nㅤ", value="", inline=False)
    
        elif ":" in newName or "<" in newName or "_" in newName or "`" in newName or "@" in newName or "*" in newName or "|" in newName:
            embed = embedMaker(":x:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
            embed.add_field(name="ㅤ\nㅤ닉네임에는 일부 특수문자가 포함될 수 없습니다.\nㅤ", value="", inline=False)

        elif len(newName) > 20:
            embed = embedMaker(":x:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
            embed.add_field(name="ㅤ\nㅤ닉네임의 길이는 20자를 초과할 수 없습니다.\nㅤ", value="", inline=False)

        elif newName == prevName:
            embed = embedMaker(":x:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
            embed.add_field(name="ㅤ\nㅤ기존 닉네임과 동일합니다.\nㅤ", value="", inline=False)

        else:
            if service.updateUserName(id, guild, newName):
                embed = embedMaker(":white_check_mark:ㅤ|ㅤPROFILE ㅤ ㅤ")
                embed.add_field(name="ㅤ\nㅤ닉네임 변경이 완료되었습니다.ㅤ", value="", inline=False)
                embed.add_field(name=f"ㅤ\nㅤ변경 전 닉네임ㅤ: ㅤ`{prevName}`", value="", inline=False)
                embed.add_field(name=f"ㅤ\nㅤ변경 후 닉네임ㅤ: ㅤ`{newName}`", value="ㅤ", inline=False)

                return ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)

            else:
                embed = embedMaker(":x:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
                embed.add_field(name="ㅤ\nㅤ닉네임 변경 과정에서 오류 발생.ㅤ", value="ㅤ\nㅤ관리자에게 문의하세요.ㅤ\nㅤ", inline=False)

    else:
        embed = embedMaker(":x:ㅤ|ㅤPROFILE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
        embed.add_field(name="ㅤ\nㅤ가입된 유저가 아닙니다.ㅤ", value="ㅤ\nㅤ`/가입` 명령어로 가입하세요.ㅤ\nㅤ", inline=False)

    return ctx.respond(f"", embed=embed, ephemeral=True)
