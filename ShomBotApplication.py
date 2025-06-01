# Importing Libraries

import discord
from discord.commands import Option
import os
from dotenv import load_dotenv
import asyncio
from discord import ApplicationContext

# Importing Custom Modules

from utils import ServerLog
from commands.basic_commands import saveCommand, helpCommand, helpDetailedCommand, coinCommand, diceCommand
from commands.user_commands import registerCommand, profileCommand, changeNicknameCommand
from commands.attendance_commands import attendanceCommand, attendanceInfoCommand
from commands.gamble_commands import gambleCommand, slotCommand
from commands.subsidy_commands import subsidyCommand
from commands.russian_commands import russianRouletteCommand
from commands.fish_commands import fishBefore, fishAfter

load_dotenv()
token = str(os.getenv('TOKEN'))
version = str(os.getenv('VERSION'))
versionDetail = str(os.getenv('VERSION_DETAIL'))

bot = discord.Bot()

# ShomBot Test Server ID
verifiedServer = [770208551401684992]

@bot.event
async def on_ready():
    gameMessage = "'/명령어'"
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(gameMessage))
    print('ㅤ')   
    ServerLog.printInfoLog("=================================================================")
    ServerLog.printInfoLog("")
    ServerLog.printInfoLog(f"\tShomBot Online")
    ServerLog.printInfoLog(f"\tBot ID: {str(bot.user.id)}")
    ServerLog.printInfoLog(f"\tBot Version: {versionDetail}")
    ServerLog.printInfoLog(f"\tGameMessage: {gameMessage}")
    ServerLog.printInfoLog("")
    ServerLog.printInfoLog("\tWaiting for Request..")
    ServerLog.printInfoLog("")
    ServerLog.printInfoLog("=================================================================")

# =======[ 각종 버튼 정보 ]=================================================


# =======[ 유지보수 명령어 ]=================================================

@bot.slash_command(name="savedata", guild_ids=verifiedServer, description="[Admin Command] 모든 유저 정보 저장(실험적)")
async def savedata(ctx: ApplicationContext):
    return await saveCommand(ctx)

# =======[ 기본 명령어 ]====================================================

@bot.slash_command(name="명령어", description="명령어 목록을 확인합니다.")
async def 명령어(ctx: ApplicationContext, 명령어: Option(str, "명령어 입력, 빈칸 입력시 전체 명령어 조회") = "전체"): # type: ignore
    
    if 명령어 == "전체":
        return await helpCommand(ctx)

    else:
        return await helpDetailedCommand(ctx, 명령어)

@bot.slash_command(name="동전", description="동전을 던져 결과를 확인합니다.")
async def 동전(ctx: ApplicationContext):
    return await coinCommand(ctx)

@bot.slash_command(name="주사위", description="주사위를 굴려 결과를 확인합니다.")
async def 주사위(ctx: ApplicationContext):
    return await diceCommand(ctx)

# =======[ 계정 명령어 ]====================================================

@bot.slash_command(name="가입", description="숌봇 서비스 이용을 위한 가입을 진행합니다.")
async def 가입(ctx: ApplicationContext):
    return await registerCommand(ctx)

@bot.slash_command(name="프로필", description="프로필을 확인합니다.")
async def 프로필(ctx: ApplicationContext):
    return await profileCommand(ctx)

@bot.slash_command(name="닉변", description="숌봇 서비스에서의 닉네임을 변경합니다.")
async def 닉변(ctx: ApplicationContext, 변경할닉네임: Option(str, "변경할 닉네임 입력(공백 불가)")): # type: ignore
    return await changeNicknameCommand(ctx, 변경할닉네임)

# =======[ 출결 명령어 ]====================================================

@bot.slash_command(name="출석체크", description="출석체크를 진행합니다.")
async def 출석체크(ctx: ApplicationContext):
    return await attendanceCommand(ctx)

@bot.slash_command(name="출석정보", description="출석정보를 확인합니다.")
async def 출석정보(ctx: ApplicationContext):
    return await attendanceInfoCommand(ctx)

# =======[ 도박 명령어 ]====================================================

@bot.slash_command(name="도박", description="도박을 진행합니다.")
async def 도박(ctx: ApplicationContext, 위험도: Option(str, "위험도 입력", choices=["저위험", "중위험", "고위험"]), 판돈: Option(int, "판돈 입력")): # type: ignore
    return await gambleCommand(ctx, 위험도, int(판돈))

@bot.slash_command(name="슬롯머신", description="슬롯머신을 진행합니다.")
async def 슬롯머신(ctx: ApplicationContext, 판돈: Option(int, "판돈 입력")): # type: ignore
    
    slotResult = await slotCommand(ctx, 판돈)

    if slotResult[0]:
        await ctx.defer() # 응답 대기 상태로 전환

        await ctx.respond(f"||<@!{ctx.user.id}>||", embed=slotResult[1], ephemeral=False)
        await asyncio.sleep(2)

        return await ctx.interaction.edit_original_response(embed=slotResult[2])

    else:
        return await ctx.respond(f"", embed=slotResult[1], ephemeral=True)

# =======[ 낚시 명령어 ]====================================================

@bot.slash_command(name="낚시", description="낚시를 진행합니다.") # type: ignore
async def 낚시(ctx: ApplicationContext):
    
    fishData = await fishBefore(ctx)

    if fishData[0]:
        await ctx.defer()

        await ctx.respond(f"||<@!{ctx.user.id}>||", embed=fishData[2][0], ephemeral=False)

        for i in range(3):
            await asyncio.sleep(fishData[1] / 4)
            await ctx.interaction.edit_original_response(embed=fishData[2][i+1])            

        await asyncio.sleep(fishData[1] / 4)

        fishResult = await fishAfter(ctx)
        if fishResult[0]:
            
            return await ctx.interaction.edit_original_response(embed=fishResult[1])

        else:
            return await ctx.interaction.edit_original_response(embed=fishResult[1])
        
    else:
        return await ctx.respond(f"", embed=fishData[2], ephemeral=True)



# =======[ 지원금 명령어 ]==================================================

@bot.slash_command(name="지원금", description="서비스 이용을 위한 지원금을 받습니다.")
async def 지원금(ctx: ApplicationContext):
    return await subsidyCommand(ctx)

# =======[ 러시안룰렛 명령어 ]==============================================

@bot.slash_command(name="러시안룰렛", description="모든 것을 걸고 운명을 시험합니다.")
async def 러시안룰렛(ctx: ApplicationContext):
    return await russianRouletteCommand(ctx)

# =======[ 봇 실행 ]========================================================

try:
    bot.run(token) # run the bot with the token

except discord.errors.Forbidden as e:
    print("Forbidden Error Occured: ", e)