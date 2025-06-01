# Importing Libraries
import random as rnd
from discord import ApplicationContext

# Importing Custom Modules
from utils.initialize import embedMaker, printLog, getAdminIDs
from utils.embed_color import ErrorEmbedColor, ProcessEmbedColor
from utils import ServerLog
from database.DBConnector import DBConnector

db_connection = DBConnector()

# =======[ 기본 명령어 ]=================================================

def helpCommand(ctx: ApplicationContext):
    """도움말 명령어
    
    Args:
        ctx (discord.ApplicationContext): 명령어 실행 환경

    Returns:
        discord.ApplicationContext.respond: 명령어 목록 Embed 출력 
    
    """
    printLog(ctx, "명령어")

    embed = embedMaker(":memo:ㅤ|ㅤCOMMAND LIST ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ")
    embed.add_field(name="ㅤ\nㅤ미니게임 명령어", value="ㅤ`/동전`, ㅤ`/주사위`ㅤ", inline=False)
    embed.add_field(name="ㅤ\nㅤ계정 명령어", value="ㅤ`/가입`, ㅤ`/프로필`, ㅤ`/닉변`, ㅤ`/출석체크`, ㅤ`/출석정보`ㅤ", inline=False)
    embed.add_field(name="ㅤ\nㅤ콘텐츠 명령어", value="ㅤ`/지원금`, ㅤ`/도박`, ㅤ`/슬롯머신`,ㅤ`/러시안룰렛`,ㅤ`/낚시` ", inline=False)
    embed.add_field(name="ㅤ\nㅤ\nㅤ추가 예정", value="ㅤ`/코인`, ㅤ`/모험`, ㅤ`/도전과제`", inline=False)
    # embed.add_field(name="ㅤ\n", value="- **장비 명령어** \nㅤ`/장비목록`, ㅤ`/장비정보`, ㅤ`/장비판매`, ㅤ`/강화`,\nㅤ`/파괴방지강화`, ㅤ`/강화정보`, ㅤ`/장비랭킹`", inline=False)
    # embed.add_field(name="ㅤ\n", value="- **코인 명령어** \nㅤ`/코인명령어`, ㅤ`/코인시세`, ㅤ`/보유코인`,\nㅤ`/코인매수`, ㅤ`/코인매도`", inline=False)

    embed.add_field(name="ㅤ\nㅤ**명령어의 상세 도움말을 확인하려면 아래 명령어를 입력하세요.ㅤ**", value="ㅤ\nㅤ→ㅤ`/명령어 [해당 명령어]`\nㅤ", inline=False)

    return ctx.respond("", embed=embed, ephemeral=True)

def helpDetailedCommand(ctx: ApplicationContext, command: str):
    """상세 도움말 명령어
    
    Args:
        ctx (discord.ApplicationContext): 명령어 실행 환경
        command: 명령어 이름
    
    Returns:
        discord.ApplicationContext.respond: 명령어 상세 도움말 Embed 출력

    """
    printLog(ctx, f"명령어 {command}")
    embed = None

    try: 
        if command == "명령어":
            embed = embedMaker(":coin:ㅤ|ㅤCOMMAND")
            embed.add_field(name="ㅤ\nㅤ명령어 정보를 확인합니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/명령어 [명령어]`ㅤ\nㅤ", inline=False)

        elif command == "동전":
            embed = embedMaker(":coin:ㅤ|ㅤCOIN")
            embed.add_field(name="ㅤ\nㅤ동전을 던진 결과 [앞, 뒤] 를 확인합니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/동전`ㅤ\nㅤ", inline=False)

        elif command == "주사위":
            embed = embedMaker(":game_die:ㅤ|ㅤDICE")
            embed.add_field(name="ㅤ\nㅤ주사위를 굴린 결과 [1 ~ 6] 를 확인합니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/주사위`ㅤ\nㅤ", inline=False)

        elif command == "가입":
            embed = embedMaker(":pencil:ㅤ|ㅤREGISTER")
            embed.add_field(name="ㅤ\nㅤShomBot 이용을 위한 유저 정보를 등록합니다.ㅤ\nㅤ유저 정보는 서버 기준으로 저장됩니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/가입`ㅤ\nㅤ", inline=False)

        elif command == "프로필":
            embed = embedMaker(":globe_with_meridians:ㅤ|ㅤPROFILE")
            embed.add_field(name="ㅤ\nㅤ해당 서버의 유저 정보를 확인합니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/프로필`ㅤ\nㅤ", inline=False)

        elif command == "닉변":
            embed = embedMaker(":pencil2:ㅤ|ㅤNICKNAME")
            embed.add_field(name="ㅤ\nㅤ해당 서버의 유저 닉네임을 변경합니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/닉변 [변경할 닉네임]`ㅤ\nㅤ", inline=False)

        elif command == "출석체크":
            embed = embedMaker(":calendar:ㅤ|ㅤATTENDANCE")
            embed.add_field(name="ㅤ\nㅤ매일 1번 출석체크하여 보상을 획득합니다.ㅤ\nㅤ출석체크 정보는 서버 기준으로 저장됩니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/출석체크`ㅤ\nㅤ", inline=False)

        elif command == "출석정보":
            embed = embedMaker(":calendar:ㅤ|ㅤATTENDANCE INFO")
            embed.add_field(name="ㅤ\nㅤ출석체크 현황을 확인합니다.ㅤ\nㅤ출석체크 정보는 서버 기준으로 저장됩니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/출석정보`ㅤ\nㅤ", inline=False)

        elif command == "도박":
            embed = embedMaker(":slot_machine:ㅤ|ㅤGAMBLE")
            embed.add_field(name="ㅤ\nㅤ위험도에 따른 도박을 진행합니다.ㅤ\nㅤ도박 확률 및 보상은 아래와 같습니다.ㅤ", value="", inline=False)
            embed.add_field(name="ㅤ\nㅤ**도박 확률**", value="ㅤ\nㅤㅤ**저위험:** 50%, **중위험:** 30%, **고위험:** 20%ㅤ", inline=False)
            embed.add_field(name="ㅤ\nㅤ**승리 보상**", value="ㅤ\nㅤㅤ**저위험:** 2.0x, **중위험:** 4.0x, **고위험:** 6.0xㅤ", inline=False)
            embed.add_field(name="ㅤ", value="ㅤ사용법:ㅤ `/도박 [위험도] [판돈]`ㅤ\nㅤ", inline=False)

        elif command == "슬롯머신":
            embed = embedMaker(":slot_machine:ㅤ|ㅤSLOT")
            embed.add_field(name="ㅤ\nㅤ슬롯머신을 돌려 같은 심볼이 3개 나왔을 때 보상을 획득합니다.ㅤ\nㅤ슬롯머신 보상은 아래와 같습니다.ㅤ", value="", inline=False)
            embed.add_field(name="ㅤ\nㅤ**슬롯머신 보상**", value="ㅤ\nㅤㅤ**:cherries: : 5x, ㅤㅤ:lemon: : 9x, ㅤ:tangerine: : 17x, ㅤㅤ:watermelon: : 40x,**\nㅤㅤ**:grapes: : 55x, ㅤ:black_joker: : 80x, ㅤ:seven: : 777x, ㅤ:gem: : 1000x**ㅤ", inline=False)
            embed.add_field(name="ㅤ", value="ㅤ사용법:ㅤ `/슬롯머신 [판돈]`ㅤ\nㅤ", inline=False)

        elif command == "지원금":
            embed = embedMaker(":moneybag:ㅤ|ㅤSUBSIDY")
            embed.add_field(name="ㅤ\nㅤ콘텐츠 이용을 위한 지원금을 받습니다.ㅤ\nㅤ보유 포인트가 적을 수록 더 많이 받습니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/지원금`ㅤ\nㅤ", inline=False)

        elif command == "러시안룰렛":
            embed = embedMaker(":gun:ㅤ|ㅤRUSSIAN ROULETTE ㅤ ㅤ ㅤ ㅤ")
            embed.add_field(name="ㅤ\nㅤ혼자만의 러시안룰렛 게임을 진행합니다.ㅤ\nㅤ생존 시 보유 소지금이 2배가 됩니다.ㅤ\nㅤ사망 시 소지금 및 경험치를 모두 잃습니다.ㅤ", value="ㅤ\nㅤ사용법:ㅤ `/러시안룰렛`ㅤ\nㅤ", inline=False)

        elif command == "낚시":
            embed = embedMaker(":fishing_pole_and_fish:ㅤ|ㅤFISHING ㅤ ㅤ ㅤ ㅤ")
            embed.add_field(name="ㅤ\nㅤ낚시를 진행하여 포인트를 획득합니다.ㅤ\nㅤ낚시 보상은 레벨에 비례하여 증가합니다.ㅤ", value="", inline=False)
            embed.add_field(name="ㅤ", value="ㅤ사용법:ㅤ `/낚시` \nㅤ", inline=False)

        else:
            embed = embedMaker(":question:ㅤ|ㅤUNKNOWN COMMAND ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
            embed.add_field(name="ㅤ\nㅤ해당 명령어에 대한 정보를 찾을 수 없습니다.ㅤ\nㅤ", value="", inline=False)

    except Exception as e:
        embed = embedMaker(":warning:ㅤ|ㅤERROR OCCURED ㅤ ㅤ ㅤ ㅤ", ErrorEmbedColor)
        embed.add_field(name="ㅤ\nㅤ명령어 상세 도움말을 출력하는 도중 오류가 발생했습니다.ㅤ", value=f"ㅤ\nㅤ`{e}`\nㅤ", inline=False)

    return ctx.respond("", embed=embed, ephemeral=True)

def coinCommand(ctx: ApplicationContext):
    """동전 명령어
    
    Args:
        ctx (discord.ApplicationContext): 명령어 실행 환경
        
    Returns:
        discord.ApplicationContext.respond: 동전 결과 Embed 출력

    """
    printLog(ctx, "동전")
    embed = embedMaker(":coin:ㅤ|ㅤCOIN ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ")

    if rnd.choice([True, False]):
        embed.add_field(name="ㅤ\nㅤ동전을 던졌더니 '__앞면__' 이 나왔습니다.\nㅤ", value="\n", inline=False)

    else:
        embed.add_field(name="ㅤ\nㅤ동전을 던졌더니 '__뒷면__' 이 나왔습니다.\nㅤ", value="\n", inline=False)

    return ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)

def diceCommand(ctx: ApplicationContext):
    """주사위 명령어

    Args:
        ctx (discord.ApplicationContext): 명령어 실행 환경

    Returns:
        discord.ApplicationContext.respond: 주사위 결과 Embed 출력

    """
    printLog(ctx, "주사위")
    embed = embedMaker(":game_die:ㅤ|ㅤDICE ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ㅤ ")

    val = rnd.choice([1, 2, 3, 4, 5, 6])

    if val == 1:

        embed.add_field(name=f"ㅤ\nㅤ주사위를 굴려서 나온 눈금ㅤ:ㅤ:one:\nㅤ", value="", inline=False)

    elif val == 2:

        embed.add_field(name=f"ㅤ\nㅤ주사위를 굴려서 나온 눈금ㅤ:ㅤ:two:\nㅤ", value="", inline=False)

    elif val == 3:

        embed.add_field(name=f"ㅤ\nㅤ주사위를 굴려서 나온 눈금ㅤ:ㅤ:three:\nㅤ", value="", inline=False)

    elif val == 4:

        embed.add_field(name=f"ㅤ\nㅤ주사위를 굴려서 나온 눈금ㅤ:ㅤ:four:\nㅤ", value="", inline=False)

    elif val == 5:

        embed.add_field(name=f"ㅤ\nㅤ주사위를 굴려서 나온 눈금ㅤ:ㅤ:five:\nㅤ", value="", inline=False)

    else:

        embed.add_field(name=f"ㅤ\nㅤ주사위를 굴려서 나온 눈금ㅤ:ㅤ:six:\nㅤ", value="", inline=False)

    return ctx.respond(f"||<@!{ctx.user.id}>||", embed=embed, ephemeral=False)

# =======[ 유지보수 명령어 ]==============================================

def saveCommand(ctx: ApplicationContext):
    """데이터 저장 명령어
    
    Args:
        ctx (discord.ApplicationContext): 명령어 실행 환경
        
    Returns:
        discord.ApplicationContext.respond: 데이터 저장 결과 Embed 출력

    """
    printLog(ctx, "saveData")

    if int(ctx.author.id) in getAdminIDs():
        db_connection.forceCommitDB()

        embed = embedMaker(":floppy_disk:ㅤ|ㅤMR ㅤ ㅤ", ProcessEmbedColor)
        embed.add_field(name="ㅤ\n유저 정보 저장됨.", value="", inline=False)

    else:
        ServerLog.printErrorLog("Command.BasicCommand: Save Failed. Incorrect Verified ID")

        embed = embedMaker(":warning:ㅤ|ㅤMR ㅤ ㅤ", ErrorEmbedColor)
        embed.add_field(name="ㅤ\n권한이 없습니다.", value="", inline=False)

    return ctx.respond(f"", embed=embed, ephemeral=True)
