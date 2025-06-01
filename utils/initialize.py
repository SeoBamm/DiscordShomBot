# Importing libraries
import discord
import os
import ast
from dotenv import load_dotenv

# Importing Custom Modules
from utils.ServerLog import *
from utils.embed_color import DefaultEmbedColor, CoolDownEmbedColor

# =======[ 기본 설정 ]===================================================

load_dotenv()
token = str(os.getenv('TOKEN'))
version = str(os.getenv('VERSION'))
versionDetail = str(os.getenv('VERSION_DETAIL'))
icon_url = str(os.getenv('ICON_URL'))

def getToken() -> str:
    """Token 반환 함수
    
    Returns:
        str: Token 문자열

    """
    return token

def getVersion() -> str:
    """Version 반환 함수

    Returns:
        str: Version 문자열

    """
    return version

def getVersionDetail() -> str:
    """Version 상세 정보 반환 함수

    Returns:
        str: Version 상세 정보 문자열

    """
    return versionDetail

def getIconURL() -> str:
    """Icon URL 반환 함수

    Returns:
        str: Icon URL 문자열

    """
    return icon_url

def getAdminIDs() -> list[int]:
    """Admin IDs 반환 함수

    Returns:
        list[int]: Admin IDs 리스트

    """
    admin_ids = os.getenv("ADMIN_IDS", "")

    # 문자열을 튜플로 변환한 후, 리스트로 변환
    return list(ast.literal_eval(admin_ids))

def getDBconfig() -> dict:
    """DB 정보 반환 함수

    Returns:
        dict: DB 정보 딕셔너리
    """
    db_config = {
        "HOST": os.getenv("DB_HOST"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "DATABASE": os.getenv("DB_DATABASE"),
        "RAISE_ON_WARNINGS": os.getenv("DB_RAISE_ON_WARNINGS") == 'True',
        "DB_COMMIT_THRESHOLD": int(os.getenv("DB_COMMIT_THRESHOLD")),
        "DB_PING_INTERVAL": int(os.getenv("DB_PING_INTERVAL"))
    }
    return db_config

# =======[ Embed 생성기 ]================================================

def embedMaker(title: str, color: int=DefaultEmbedColor) -> discord.Embed:
    """Embed 생성기

    Args:
        title: Embed의 제목
        color: Embed의 색상

    Returns:
        discord.Embed: Embed 객체

    """
    embed = discord.Embed(title=title, description="", color=color)
    # embed.set_footer(text=f"ShomBot ㅤv {version} \nPowered By seobamm", icon_url=icon_url)
    embed.set_footer(text=f"ShomBot ㅤv {version} \nPowered By seobamm")

    return embed

def coolDownEmbed(currTime: int, userTime: int, command: str) -> tuple[bool, discord.Embed]:
    """CoolDown 상태 및 Embed 출력 함수

    Args:
        currTime: 현재 시간
        userTime: 명령어 재사용 가능 시간
        command: 명령어 이름

    Returns:
        tuple[bool, discord.Embed]: CoolDown 상태 및 Embed 객체

    """
    if currTime >= userTime:

        return False, 0

    else:
        embed = embedMaker(":clock3:ㅤ|ㅤCOOLDOWN ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", CoolDownEmbedColor)

        gap = userTime - currTime

        if gap >= 3600:
            hour = gap // 3600
            minute = (gap % 3600) // 60
            second = (gap % 3600) % 60
            embed.add_field(name=f"ㅤ\n`{command}` 명령어가 재사용 대기 중입니다.ㅤ", value=f"`해당 명령어의 재사용 대기시간 : {hour}시간 {minute}분 {second}초`ㅤ\nㅤ", inline=False)

        elif gap >= 60:
            minute = gap // 60
            second = gap % 60
            embed.add_field(name=f"ㅤ\n`{command}` 명령어가 재사용 대기 중입니다.ㅤ", value=f"`해당 명령어의 재사용 대기시간 : {minute}분 {second}초`ㅤ\nㅤ", inline=False)
        
        else:
            embed.add_field(name=f"ㅤ\n`{command}` 명령어가 재사용 대기 중입니다.ㅤ", value=f"`해당 명령어의 재사용 대기시간 : {gap}초`ㅤ\nㅤ", inline=False)
        
        embed.set_footer(text=f"ShomBot ㅤv {version} \nPowered By seobamm")

        return True, embed
    
def inProgressEmbed(isInprogress: int, command: str) -> tuple[bool, discord.Embed]:
    """InProgress 상태 및 Embed 출력 함수

    Args:
        isInprogress: 진행 중 여부 (0: False, 1: True)
        command: 명령어 이름

    Returns:
        tuple[bool, discord.Embed]: InProgress 상태 및 Embed 객체

    """
    if isInprogress == 0:
        return False, 0

    else:
        embed = embedMaker(":hourglass:ㅤ|ㅤIN PROGRESS ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ", CoolDownEmbedColor)

        embed.add_field(name=f"ㅤ\n`{command}` 명령어를 수행 중입니다.ㅤ", value=f"`수행이 완료될 때까지 잠시 기다려 주세요.`ㅤ\nㅤ", inline=False)
        
        embed.set_footer(text=f"ShomBot ㅤv {version} \nPowered By seobamm")

        return True, embed    
  
# =======[ ServerLog 생성기 ]============================================

def printLog(ctx: discord.ApplicationContext, command: str) -> None:
    """ServerLog 출력 함수

    Args:
        ctx: 명령어 실행 환경
        command: 명령어 이름

    Returns:
        None

    """
    printInfoLog(f"ShomBotApplication: [{ctx.guild.name}({ctx.guild.id})] {ctx.user.name}({ctx.user.id}) >> /{command}")

# =======[ 기타 포매팅 함수 ]==============================================

def formattedPoint(point: int) -> str:
    """포인트 포매팅 함수
    
    Args:
        point: 포인트
        
    Returns:
        str: 포인트 포매팅 결과물 문자열

    """
    return "{:,}".format(int(point))

def getLevelInfo(exp: int) -> tuple[int, int, float]:
    """레벨 정보 반환 함수
    
    Args:
        exp: 경험치량
        
    Returns:
        tuple[int, int, float]: 레벨, 경험치량, 백분율

    """
    level = exp >> 10  # 1024로 나눈 몫 (레벨)
    currExp = exp & 1023  # 1024로 나눈 나머지 (현재 경험치)
    percentage = currExp / 1024 * 100  # 1024로 나눈 나머지를 백분율 변환
    return level, currExp, percentage

def getExpBar(percentage: float) -> str:
    """경험치 바 반환 함수

    Args:
        percentage: 경험치 백분율

    Returns:
        str: 경험치 바 문자열
    """
    bar_length = 10  # 경험치 바 길이
    filled_blocks = int(percentage / (100 / bar_length))  # 🔵 개수
    empty_blocks = bar_length - filled_blocks  # ▬ 개수
    
    bar = ":blue_square:" * filled_blocks + ":white_large_square:" * empty_blocks  # 경험치 바 생성
    return f"{bar}ㅤ [ {percentage:.2f}%] "


