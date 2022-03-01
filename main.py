
import QA
import asyncio
import discord
from discord.ext import commands
import nest_asyncio
import datetime
import json
import os
from urllib import parse, request
import re
import random
import draw
import keep_alive
import math


nest_asyncio.apply()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)


@client.command()
async def aa(ctx):
    await ctx.send('老子直接在你留言區開賭場')


@client.command()
async def af(ctx):
    await ctx.send(
        'https://discord.com/api/oauth2/authorize?client_id=870648282890776597&permissions=8&scope=bot'
    )


@client.command()
async def test(ctx):
    await ctx.send('str(user.id)')


@client.command()
async def QR(ctx, data):
    await ctx.send(
        'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' +
        data)


@client.command()
async def 畫畫(ctx):

    embed = discord.Embed(title=f"大鼻子賭場畫的畫", description=f"")
    embed.set_image(url=random.choice(draw.url))

    await ctx.send(embed=embed)


@client.command()
async def 指令(ctx):
    await ctx.send(
        '!賭 數字,!偷 @人名 !抽獎,!乞討,!快算快答(!cal),!終極密碼(!code) 數字,!頭貼評分 @人名,!打 @人名 ,!give @人名,!開台機率,!吃啥,!排行,!丟炸彈,!抽籤,!痛扁老闆,!QR QRCode的內容\n\n戰鬥系統相關指令(刪檔封測中，你的角色資料隨時會被清空，請自行斟酌)\n!練功\n!status\n!status @人名\n!強化 武器 次數\n!強化 防具 次數\n!決鬥 @人名\n!更新目標\n!單人boss 難度(1~12)\n!bossinfo 難度(1~12)\n!勝率 @人名\n!死亡對決 @人名 (敗者遊戲資料會被全部清除，請慎重使用))'
    )


@client.command()
async def 開賭場網址(ctx):
    await ctx.send(
        '開啟賭場方式 :進入網址 https://replit.com/join/sfwmvlbdki-675bot 按最上面Run，關網頁前按stop'
    )


@client.command()
async def 開台機率(ctx):
    variable = ["🌑", "🌘", "🌗", "🌖", "🌕"]
    await ctx.send(f"{random.choice(variable)}")


@client.command()
async def abc(ctx):
    await ctx.send('我太吵 先閃')


@client.command()
async def 關台(ctx):
    await ctx.send('已離開聊天室。')


@client.command()
async def 痛扁老闆(ctx):
    await ctx.send('代號7414機器人扁了675一頓🤖 🤜 ༼ ͝💧 ͟💥 ͝💧 ༽。')


@client.command()
async def 抽籤(ctx):
    target = random.choice(ctx.guild.members)
    await ctx.send(f" {target.mention}，{ctx.author}抽到了你!")


@client.command()
async def 吃啥(ctx):
    variable = [
        "🍔🍟", "🥟", "🐮🍛", "🍣", "🐮🍜", "🌊♂️🐔🍚", "🍗🍱", "🐮🥩", "🐮🕳", "🔥🍲", "🐷👣🍚"
    ]
    await ctx.send(f"{random.choice(variable)}")


@client.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def 打(ctx, member: discord.Member):
    variable = [
        f"{ctx.author}  打了 {member}一下!👊💥", f"{ctx.author}  踹了 {member}一下!👣💥",
        f"{ctx.author}肛了 {member}一下!ﻝﮞ ̶͞ ✊̶͞ ̶͞ ̶D💦💥"
    ]
    await ctx.send(f"{random.choice(variable)}")


@client.command(aliases=["point"])
async def points(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}的錢╭[◕ ͜🔴◕]👍🏼")
    em.add_field(name="你的錢包", value=wallet_amt)
    #em.add_field(name = "你的保險箱" ,value = bank_amt)
    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 59, commands.BucketType.user)
@commands.cooldown(1, 3, commands.BucketType.channel)
async def 乞討(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(1, 500)

    await ctx.send(f" {ctx.author.name}乞討到{earnings}元💰!一分鐘後可再乞討一次")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def 丟炸彈(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    target = random.choice(ctx.guild.members)
    await open_account(target)
    earnings = random.randrange(1, 5)
    await ctx.send(
        f"{ctx.author} 花費五元丟出了炸彈💣! 💥炸掉 {target} {earnings}元!，10秒後可再丟一次")
    if target == user:
        await ctx.send(f"@{ctx.author}炸到自己，炸彈解除༼ ◕ ͟🔴◕ ༽! ")
        return
    else:
        users[str(user.id)]["wallet"] -= 5
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        users[str(target.id)]["wallet"] -= earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)


@client.command()
@commands.cooldown(1, 3, commands.BucketType.channel)
async def 賭(ctx, amount):
    await open_account(ctx.author)
    users = await get_bank_data()

    user = ctx.author

    amount = int(amount)
    roll = random.randrange(100)
    earnings = amount
    if amount < 0:
        await ctx.send(f"@{ctx.author}不能賭負的!༼ ◕ ͟🔴◕ ༽! ")
        return
    if amount > users[str(user.id)]["wallet"]:
        await ctx.send(f"@{ctx.author}你錢不夠༼ ◕ ͟🔴◕ ༽! ")
        return
    elif roll < 45:
        await ctx.send(f"{ctx.author} 骰到 {roll}(<45)) 並輸掉 {earnings} 元")
        users[str(user.id)]["wallet"] -= earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    if 99 > roll > 45:
        await ctx.send(
            f"{ctx.author}骰到 {roll} (>45)並贏得 {2*earnings} 元!!╭[◕ ͜🔴◕]👍")
        users[str(user.id)]["wallet"] += earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    if roll > 99:
        await ctx.send(
            f" {ctx.author} 骰到{roll} 並贏得大獎 {2.5*earnings} 元!!╭[◕ ͜🔴◕]👍🏼╭[◕ ͜🔴◕]👍🏼╭[◕ ͜🔴◕]👍"
        )
        users[str(user.id)]["wallet"] += (1.5) * earnings
    with open("mainbank.json", "w") as f:
        json.dump(users, f)


@client.command()
@commands.cooldown(1, 3, commands.BucketType.channel)
async def 偷(ctx, member: discord.Member):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    await open_account(member)
    roll = random.randrange(100)
    earnings = random.randrange(1, 100)
    variable = ["💎", "🍌", "👙", "🍔", "🧀", "👟"]

    if roll > 49:
        await ctx.send(
            f"{ctx.author}想偷 {member}🤚...，偷錢成功! 從{member}身上偷到{random.choice(variable)}價值{earnings}元!"
        )
        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        if 1 > users[str(member.id)]["wallet"]:
            users[str(member.id)]["wallet"] -= 0
        else:
            users[str(member.id)]["wallet"] -= earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    elif 20 < roll < 49:
        await ctx.send(
            f"{ctx.author}想偷 {member}🤚...，可是被{member}告而被反拿{earnings}元!")
        users[str(user.id)]["wallet"] -= earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        users[str(member.id)]["wallet"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    elif 20 > roll:
        await ctx.send(
            f"{ctx.author}想偷 {member}🤚...，可是被{member}打而自己被搶走{earnings}元!")
        users[str(user.id)]["wallet"] -= earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        users[str(member.id)]["wallet"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)


@client.command(aliases=["baavatar"])
async def 頭貼評分(ctx, member: discord.Member):
    amount = random.randrange(0, 100)
    embed = discord.Embed(title=f"這張頭貼的評分為......{amount}分!!╭[◕ ͜🔴◕]👍🏼 ",
                          description=f"{member}的頭貼")
    embed.set_image(url=member.avatar_url)

    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 59, commands.BucketType.user)
async def 抽獎(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    roll = random.randrange(100)
    rand1 = [
        " ʕ◕ ͜⚫◕ʔ", "💥🔫༼ ◕ ͟👃🏿◕ ༽🖕🏿", "༼ ◔╭ܫ╮◔ ༽", "༼ᗜ◕ ͜🐽◕ᗜ༽",
        "㊗️🏴󠁧󠁢󠁥󠁮󠁧󠁿🀄️💯祝你期中100", "₁₂₃₄₅₆₇₈₉¹²³⁴⁵⁶⁷⁸⁹小型字體"
    ]
    rand2 = [
        "╙╨༼ ◕ ͟🔴◕༽╨╜",
        "༼ ( ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞ ͟͟͞⊙ ͟🔴 ͟͟͞ ͟༽ ͟͟͞ ͟͟͞ ͟͟͞⊙",
        " [̲̅$̲̅(̲̅◕ ͟🔴◕)̲̅$̲̅]", "o͡͡͡╮༼ ◔╭ܫ╮◔ ༽╭o͡͡͡",
        "╭◕ ͟🔴◕╮ﻝﮞ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜ ͡ ͜⦿💦包莖675",
        "ጿ ኈ ቼ ዽ ጿ ኈ ቼ ዽ ኈ ቼ ዽ ጿ ኈ ቼ ዽ ጿ ኈ ቼ跳街舞", "﷽特殊符號",
        "┖\\\◔ ͟◔\\\┓┏/◔ ͟◔/┛67舞"
    ]
    rand3 = ["🉑🈶🉑🈚️", "╭[◕ ͟🔴◕]👎", "🆆🆃🅵", "╭ ͝◕ ͟🔴 ͝◕╮生氣五"]
    rand4 = [
        "🎰╭[◕ ͜🔴◕]👍🏼🎰大鼻子賭場",
        "╭[◕ ͜🔴◕]👍🏼╭[◕ ͜🔶◕]👍🏼╭[◕ ͜🔔◕]👍🏼╭[◕ ͜❎◕]👍🏼╭[◕ ͜🔵◕]👍🏼╭[◕ ͜🌀◕]👍🏼╭[◕ ͜💜◕]👍🏼彩虹675",
        "⎝⧹╲⎝⧹༼ ﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞo.◕ ͜🔴◕ ༽oﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞﱞ.⧸⎠╱⧸⎠ l 激光675"
    ]
    if roll < 50:
        await ctx.send(
            f"{ctx.author} 抽到{random.choice(rand1)} 並贏得 250 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 250
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        return
    elif 50 <= roll < 75:
        await ctx.send(
            f"{ctx.author} 抽到{random.choice(rand2)} 並贏得 500 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 500
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        return
    elif 96 > roll >= 75:
        await ctx.send(
            f"{ctx.author} 抽到{random.choice(rand3)} 並贏得 0 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 0
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        return
    elif 96 >= roll:
        await ctx.send(
            f"{ctx.author} 抽到{random.choice(rand4)} 並贏得 大獎 2000 元!，一分鐘後可再抽一次")
        users[str(user.id)]["wallet"] += 2000
        with open("mainbank.json", "w") as f:
            json.dump(users, f)


@client.command(aliases=["lb"])
async def 排行(ctx, x=7):
    await open_account(ctx.author)
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f" 金錢排行榜{x} ",
                       description="╭[◕ ͜🔴◕]👍🏼",
                       color=discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


@client.command(aliases=["lb2"])
async def level(ctx, x=7):
    user = ctx.author
    users = await get_character_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["level"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f" 等級排行榜{x} ",
                       description="╭[◕ ͜🔴◕]👍🏼",
                       color=discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


@client.command()
async def give(ctx, member: discord.Member, amount):
    await open_account(ctx.author)
    await open_account(member)
    users = await get_bank_data()
    user = ctx.author
    amount = int(amount)
    await open_account(ctx.author)
    await open_account(member)
    earnings = amount
    if amount > users[str(user.id)]["wallet"]:
        await ctx.send(f"@{ctx.author}你錢不夠༼ ◕ ͟🔴◕ ༽! ")
        return
    if amount < 0:
        await ctx.send(f"@{ctx.author}不能给負的!༼ ◕ ͟🔴◕ ༽! ")
        return
    else:
        await ctx.send(f"{ctx.author}  給了 {member} {earnings}元!╭[◕ ͜🔴◕]👍🏼")
        users[str(user.id)]["wallet"] -= earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        users[str(member.id)]["wallet"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)


@client.command(aliases=["快算快答"])
@commands.cooldown(1, 59, commands.BucketType.channel)
async def cal(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    a = random.randrange(1, 99)
    b = random.randrange(1, 99)
    aa = int(a + b)

    ans = aa

    with open("cal2.json", "w") as f:
        data = ans
        json.dump(data, f)
    await ctx.send(f"聊天室快算快答!{a}+{b}，輸入!c 數字搶答!(EX:!c 30)╭[◕ ͜🔴◕]👍🏼")


@client.command()
async def c(ctx, amount):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    amount = int(amount)
    with open("cal2.json", "r") as f:
        data = json.load(f)
        data = int(data)
    if amount == data:
        with open("cal2.json", "w") as f:
            new = 1438797864
            json.dump(new, f)
        await ctx.send(
            f"答案為{amount}，{ctx.author}第一個算出答案並贏得1000元!╭[◕ ͜🔴◕]👍，一分鐘後可算下一題")
        users[str(user.id)]["wallet"] += 1000
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    else:
        with open("cal2.json", "w") as f:
            new1 = data
            json.dump(new1, f)

#def question():
ques1 = (QA.QA1)     
ques2 = (QA.QA2)     
ques3 = (QA.QA3)     
ques4 = (QA.QA4)     
ques5 = (QA.QA5)     
 #return ques1,ques2,ques3,ques4,ques5
@client.command(aliases=["問答"])
@commands.cooldown(1, 59, commands.BucketType.channel)
async def QA(ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        ans = random.randrange(1,6)
        if ans ==1:
         await ctx.send(
                f"{random.choice(ques1)},輸入!a 選項搶答!(EX:!a 3)╭[◕ ͜🔴◕]👍🏼  ")
        if ans ==2:
         await ctx.send(
                f"{random.choice(ques2)},輸入!a 選項搶答!(EX:!a 3)╭[◕ ͜🔴◕]👍🏼  ")         
        if ans ==3:
         await ctx.send(
                f"{random.choice(ques3)},輸入!a 選項搶答!(EX:!a 3)╭[◕ ͜🔴◕]👍🏼  ")
        if ans ==4:
         await ctx.send(
                f"{random.choice(ques4)},輸入!a 選項搶答!(EX:!a 3)╭[◕ ͜🔴◕]👍🏼 ")      
        if ans ==5:                    
         await ctx.send(
                f"{random.choice(ques5)},輸入!a 選項搶答!(EX:!a 3)╭[◕ ͜🔴◕]👍🏼  ")      
        with open("cal.json", "w") as f:
            data = ans
            json.dump(data, f)

@client.command()
async def a(ctx, amount):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    amount = int(amount)
    with open("cal.json", "r") as f:
        data = json.load(f)
        data = int(data)
    if amount == data:
        with open("cal.json", "w") as f:
            new = 1438797864
            json.dump(new, f)
        await ctx.send(
            f"答案為{amount}，{ctx.author}第一個答出答案並贏得1000元!╭[◕ ͜🔴◕]👍，一分鐘後可答下一題")
        users[str(user.id)]["wallet"] += 1000
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
        ques1 = random.choice(QA.QA1)     
        ques2 = random.choice(QA.QA2)     
        ques3 = random.choice(QA.QA3)     
        ques4 = random.choice(QA.QA4)     
        ques5 = random.choice(QA.QA5) 
    else:
        with open("cal.json", "w") as f:
            new1 = data
            json.dump(new1, f)

@client.command(aliases=["code"])
async def 終極密碼(ctx, amount):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    amount = int(amount)
    with open("pass.json", "r") as f:
        ans = json.load(f)
        ans = int(ans)
    if amount == ans:
        with open("pass.json", "w") as f:
            new = random.randrange(1, 99)
            json.dump(new, f)
        await ctx.send(f"答案為{amount}，{ctx.author}第一個猜中答案並贏得15元!╭[◕ ͜🔴◕]👍")
        users[str(user.id)]["wallet"] += 10
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    elif amount < ans:
        await ctx.send(f"答{ctx.author}花費2元猜了{amount}...再高一點!")
        users[str(user.id)]["wallet"] -= 2
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    elif amount > ans:
        await ctx.send(f"答{ctx.author}花費2元猜了{amount}...再低一點!")
        users[str(user.id)]["wallet"] -= 2
        with open("mainbank.json", "w") as f:
            json.dump(users, f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def create_character(user):

    users = await get_character_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["level"] = 1
        users[str(user.id)]["hp"] = 100
        users[str(user.id)]["atk"] = 10
        users[str(user.id)]["def"] = 3
        users[str(user.id)]["lucky"] = 30
        users[str(user.id)]["currExp"] = 0
        users[str(user.id)]["money"] = 0
        users[str(user.id)]["canRebirth"] = "0"
        users[str(user.id)]["RebirthTimes"] = 0

    with open("character.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users


async def get_character_data():
    with open("character.json", "r") as f:
        users = json.load(f)
    return users


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@commands.cooldown(1, 3, commands.BucketType.channel)
async def 練功(ctx):
    await create_character(ctx.author)
    user = ctx.author
    users = await get_character_data()
    earnings = random.randrange(20, 50)
    earningMoney = random.randrange(35, 80)
    users[str(user.id)]["currExp"] += earnings
    users[str(user.id)]["money"] += earningMoney
    if users[str(user.id)]["currExp"] >= 200:
        users[str(user.id)]["currExp"] -= 200
        users[str(user.id)]["level"] += 1
        users[str(user.id)]["atk"] += random.randrange(3, 7)
        users[str(user.id)]["def"] += random.randrange(2, 4)
        users[str(user.id)]["hp"] += random.randrange(23, 42)
        await ctx.send(
            f"{ctx.author.name}打怪練功獲得 {earnings} 經驗值、{earningMoney} 金幣，並且升了一級💰!各種能力都得到了提升，15秒後可再練功一次"
        )
    else:
        await ctx.send(
            f"{ctx.author.name}打怪練功獲得{earnings}經驗值、{earningMoney} 金幣💰，距離升級還有{200-users[str(user.id)]['currExp']}經驗值!15秒後可再練功一次"
        )
    with open("character.json", "w") as f:
        json.dump(users, f)


#@client.command()
#@commands.cooldown(1, 15, commands.BucketType.user)
#@commands.cooldown(1, 3, commands.BucketType.channel)
#async def 練功(ctx):
#await create_character(ctx.author)
#user = ctx.author
#users = await get_character_data()
#earnings = random.randrange(20, 50)
#earningMoney = random.randrange(35, 80)
#users[str(user.id)]["currExp"] += earnings
#users[str(user.id)]["money"] += earningMoney

#levelUP = await checkLevelUp(user, users)
#if levelUP:
# await ctx.send(
#    f"{ctx.author.name}打怪練功獲得 {earnings} 經驗值、{earningMoney} 金幣，並且升了一級💰!各種能力都得到了提升，15秒後可再練功一次"
#)
#else:
# await ctx.send(
# f"{ctx.author.name}打怪練功獲得{earnings}經驗值、{earningMoney} 金幣💰，距離升級還有{200-users[str(user.id)]['currExp']}經驗值!15秒後可再練功一次"
# )


@client.command()
async def status(ctx, member: discord.Member = None):
    await create_character(ctx.author)
    user = ""
    if member is None:
        user = ctx.author
    else:
        user = member
    users = await get_character_data()

    level = users[str(user.id)]["level"]
    hp = users[str(user.id)]["hp"]
    atk = users[str(user.id)]["atk"]
    yourdef = users[str(user.id)]["def"]
    currExp = users[str(user.id)]["currExp"]
    money = users[str(user.id)]["money"]

    lucky = users[str(user.id)]["lucky"]
    levelUpBuff = 1
    if "levelUpBuff" in users[str(user.id)]:
        levelUpBuff = users[str(user.id)]["levelUpBuff"]
    else:
        canRebirth = "無法進行"
    canRebirth = ""
    if "canRebirth" in users[str(user.id)]:
        if users[str(user.id)]["canRebirth"] == "1":
            canRebirth = "可進行"
        else:
            canRebirth = "無法進行"
    else:
        canRebirth = "無法進行"

    em = discord.Embed(title=f"{user.name}的角色資訊╭[◕ ͜🔴◕]👍🏼")
    em.add_field(name="等級 🔥", value=level)
    em.add_field(name="血量 ❤️", value=hp)
    em.add_field(name="攻擊力 ⚔️", value=atk)
    em.add_field(name="防禦力 🛡", value=yourdef)
    em.add_field(name="經驗值 📊", value=currExp)
    em.add_field(name="金錢 💰", value=money)
    em.add_field(name="幸運值 ", value=lucky)
    em.add_field(name="升級能力加成 ", value=str(int((levelUpBuff - 1) * 100)) + "%")
    em.add_field(name="轉生 ", value=canRebirth)
    #em.add_field(name = "你的保險箱" ,value = bank_amt)
    await ctx.send(embed=em)


@client.command()
async def 強化(ctx, item, times=1):
    originTimes = times
    if not (item == "武器" or item == "防具"):
        return
    await create_character(ctx.author)
    user = ctx.author
    users = await get_character_data()
    if users[str(user.id)]["money"] < 200 * times:
        await ctx.send(f'{ctx.author}金幣不足以強化 {times} 次，每次強化需消耗200金幣')
        return
    hp = users[str(user.id)]["hp"]
    atk = users[str(user.id)]["atk"]
    yourdef = users[str(user.id)]["def"]
    successCount = 0
    while times > 0:
        success = random.randrange(1, 100) > 40
        users[str(user.id)]["money"] -= 150
        if success:
            successCount += 1
            if item == "武器":
                atkup = random.randrange(4, 7)
                users[str(user.id)]["atk"] += atkup
                #await ctx.send(f'{ctx.author}消耗150金幣強化成功，攻擊力從 {atk} 上升到 {atk + atkup}')
            if item == "防具":
                defup = random.randrange(2, 6)
                hpup = random.randrange(23, 36)
                users[str(user.id)]["def"] += defup
                users[str(user.id)]["hp"] += hpup
                #await ctx.send(f'{ctx.author}消耗150金幣強化成功，防禦力從 {yourdef} 上升到 {yourdef + defup}，血量從 {hp} 上升到 {hp + hpup}')
        times -= 1
    if item == "武器":
        await ctx.send(
            f'{ctx.author}強化 {originTimes} 次，成功 {successCount} 次，攻擊力從 {atk} 上升到 {users[str(user.id)]["atk"]}'
        )
    else:
        await ctx.send(
            f'{ctx.author}強化 {originTimes} 次，成功 {successCount} 次，防禦力從 {yourdef} 上升到 {users[str(user.id)]["def"]}，血量從 {hp} 上升到 {users[str(user.id)]["hp"]}'
        )
    with open("character.json", "w") as f:
        json.dump(users, f)


@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
@commands.cooldown(1, 3, commands.BucketType.channel)
async def 決鬥(ctx, member: discord.Member):
    if ctx.author.id == member.id:
        await ctx.send("請勿自己與自己決鬥")
        return
    await battle(ctx, ctx.author, member)


@client.command()
async def 更新目標(ctx):
    await ctx.send(
        "目前計畫更新內容:\n1.Boss戰（單人已完成）：可單人或組隊參加，失敗需扣除金錢，組隊挑戰獎勵平分\n2.死亡對決(已完成)：和決鬥類似，差別是敗者的角色會直接被永久刪除，勝者則會獲得一顆「7414 統粉之魂」\n3.轉生(已完成)：需擁有「7414 統粉之魂」才可進行，轉生後角色會被重置回初始狀態，但是之後會成長得更快速，例如別人升級+50HP，5攻擊，3防禦，你可能+120HP，12攻擊，10防禦，另外這也是唯一一個提昇幸運值的方法(幸運值影響在戰鬥中使用技能的機率，未轉生者一律為30)"
    )


#確認升級function
async def checkLevelUp(user, users):
    extraBuff = 1
    c = users[str(user.id)]
    levelUp = True  #True代表有升級,可以print一些訊息提醒user能力提升了
    if "levelUpBuff" in c:
        extraBuff = c["levelUpBuff"]
    while c["currExp"] >= 200:
        levelUp = True
        c["currExp"] -= 200
        c["hp"] += math.ceil(random.randrange(23, 42) * extraBuff)
        c["atk"] += math.ceil(random.randrange(3, 7) * extraBuff)
        c["def"] += math.ceil(random.randrange(2, 4) * extraBuff)
        c["level"] += 1
    with open("character.json", "w") as f:
        json.dump(users, f)
    return levelUp


#user1 傳入 ctx.author,user2是被tag的,可參考give方法
async def battle(ctx, user1, user2):
    await create_character(user1)
    await create_character(user2)
    users = await get_character_data()
    c1 = users[str(user1.id)]
    c2 = users[str(user2.id)]
    c1hp = c1["hp"]
    #根據戰鬥力差距決定勝利後獲得多少經驗,但最少還是給30
    c1power = c1["atk"] * c1["def"]  #c1的戰鬥力
    c2power = c2["atk"] * c2["def"]  #c2的戰鬥力
    c1def = c1["def"]
    c1lucky = c1["lucky"] * c2["level"] / c1["level"]  #等級高的人幸運值調低,讓弱勢方也有機會翻盤
    #幸運事件列表,前四個觸發機率23.75%,亞統事件機率5%
    #["灑毒,對手失去當前生命30%","吸血,吸取對手15%最大生命","爆擊,傷害翻倍","暈過去了，醒來後精神飽滿，血量恢復30%","極稀有事件：亞洲統神叫對方去死一死，對手直接死亡"]
    c2hp = c2["hp"]
    c2def = c2["def"]
    c2lucky = c2["lucky"] * c1["level"] / c2["level"]  #等級低的人幸運值調高,讓弱勢方也有機會翻盤
    resultStr = ""
    c1dmg = c1["atk"] * (100 / (100 + c2def))  #傷害減免採用LOL,防禦100就減傷50%
    c2dmg = c2["atk"] * (100 / (100 + c1def))
    godtoneFlag = False  #亞統事件是否觸發
    c1AtkFlag = c1["level"] > c2["level"]  #等級高者先攻
    while c1hp > 0 and c2hp > 0:
        c1isLucky = c1lucky > random.randrange(1, 100)  #如果某方運氣好,觸發特殊事件協助他
        c2isLucky = c2lucky > random.randrange(1, 100)
        if c1AtkFlag:
            dmgshift = random.randrange(
                int(c1dmg * -0.1) - 5,
                int(c1dmg * 0.1) + 5)
            if c1isLucky:
                event = random.randrange(1, 100)
                if event > 95:
                    resultStr += f"亞洲統神顯靈怒噴對方去死一死，{user2} 直接當場死亡,勝利者是 {user1}!"
                    godtoneFlag = True
                    c2hp = 0
                    break

                if event > 95 - 23.75:
                    resultStr += f"{user1} 打一打昏過去了，醒來後精神飽滿，恢復30%血量!\n"
                    c1hp += c1["hp"] * 0.3
                elif event > 95 - 23.75 * 2:
                    resultStr += f"{user1} 邊打爐石邊吃完晚餐吃飽喝足，全身都是力量，爆擊造成{int(c1dmg * 2)}傷害!\n"
                    c2hp -= c1dmg * 2
                elif event > 95 - 23.75 * 3:
                    resultStr += f"{user1} 好像會吸血，怎麼都打不死，吸取 {user2} 15%最大生命!\n"
                    c1hp += c2["hp"] * 0.15
                    c2hp -= c2["hp"] * 0.15
                else:
                    resultStr += f"{user1} 放了個屁，臭啊臭啊 {user2} 失去30%當前生命!\n"
                    c2hp *= 0.7
            else:
                c2hp -= (c1dmg + dmgshift)
                resultStr += f"{user1}攻擊， {user2} 受到 {int(c1dmg + dmgshift)} 點傷害!\n"
        else:
            dmgshift = random.randrange(
                int(c2dmg * -0.1) - 5,
                int(c2dmg * 0.1) + 5)
            if c2isLucky:
                event = random.randrange(1, 100)
                if event > 95:
                    resultStr += f"亞洲統神顯靈怒噴對方去死一死，{user1} 直接當場死亡,勝利者是 {user2}!"
                    godtoneFlag = True
                    c1hp = 0
                    break

                if event > 95 - 23.75:
                    resultStr += f"{user2} 打一打昏過去了，醒來後精神飽滿，恢復30%血量!\n"
                    c2hp += c2["hp"] * 0.3
                elif event > 95 - 23.75 * 2:
                    resultStr += f"{user2} 邊打爐石邊吃完晚餐吃飽喝足，全身都是力量，爆擊造成{int(c2dmg * 2)}傷害!\n"
                    c1hp -= c2dmg * 2
                elif event > 95 - 23.75 * 3:
                    resultStr += f"{user2} 好像會吸血，怎麼都打不死，吸取 {user1} 15%最大生命!\n"
                    c2hp += c1["hp"] * 0.15
                    c1hp -= c1["hp"] * 0.15
                else:
                    resultStr += f"{user2} 放了個屁，臭啊臭啊 {user1} 失去30%當前生命!\n"
                    c1hp *= 0.7
            else:
                c1hp -= (c2dmg + dmgshift)
                resultStr += f"{user2}攻擊， {user1} 受到 {int(c2dmg + dmgshift)} 點傷害!\n"

        c1AtkFlag = not c1AtkFlag
    if c1hp <= 0 and not godtoneFlag:
        resultStr += f"{user1}戰敗!\n"
        getExp = int(random.randrange(30, 52) * c1power / c2power)
        users[str(user2.id)]["currExp"] += getExp
        if users[str(user2.id)]["currExp"] > 100:
            users[str(user2.id)]["currExp"] -= 100
            users[str(user2.id)]["level"] += 1
            users[str(user2.id)]["atk"] += random.randrange(3, 7)
            users[str(user2.id)]["def"] += random.randrange(2, 4)
            users[str(user2.id)]["hp"] += random.randrange(23, 42)
        resultStr += f"{user2}獲得 {getExp} 經驗值!,20秒後可在決鬥一次!"
    if c2hp <= 0 and not godtoneFlag:
        resultStr += f"{user2}戰敗!\n"
        getExp = int(random.randrange(30, 52) * c2power / c1power)
        users[str(user1.id)]["currExp"] += getExp
        if users[str(user1.id)]["currExp"] > 100:
            users[str(user1.id)]["currExp"] -= 100
            users[str(user1.id)]["level"] += 1
            users[str(user1.id)]["atk"] += random.randrange(3, 7)
            users[str(user1.id)]["def"] += random.randrange(2, 4)
            users[str(user1.id)]["hp"] += random.randrange(23, 42)
        resultStr += f"{user1}獲得 {getExp} 經驗值!,20秒後可在決鬥一次!"
    with open("character.json", "w") as f:
        json.dump(users, f)
    await ctx.send(resultStr)


@client.command()
async def 組隊boss(ctx, level=1):
    data = 0
    with open("bossfight.json", "r") as f:
        data = json.load(f)
    if data["hasBoss"] == "1":
        await ctx.send("現在已有一場開啟中的Boss戰，請輸入 !go 加入此次遠征")
    else:

        BossObj = await getBossObj(str(level))
        await showBossInfo(ctx, BossObj)
        await ctx.send("開啟一場全新的Boss戰，請輸入 !go 加入此次遠征")
        data["hasBoss"] = "1"
        data["BossLevel"] = str(level)
    with open("bossfight.json", "w") as f:
        json.dump(data, f)


@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)
@commands.cooldown(1, 3, commands.BucketType.channel)
async def 單人boss(ctx, level=1):
    bossObj = await getBossObj(str(level))
    bossObj["originHP"] = bossObj["hp"]
    await battleWithBoss(ctx, ctx.author, bossObj)


@client.command()
async def 五秒(ctx):
    await asyncio.sleep(5)
    await ctx.send("5秒了")


async def battleWithBoss(ctx, player, bossObj):
    #製作挑戰者物件,boss物件,戰前公告
    await create_character(player)
    users = await get_character_data()
    playerObj = users[str(player.id)]
    playerObj["originHP"] = playerObj["hp"]
    await ctx.send(
        f"{player}，戰鬥力{playerObj['atk'] * playerObj['def']}，開始挑戰戰鬥力 {bossObj['atk'] * bossObj['def']} 的{bossObj['name']}"
    )
    playerOriginHP = playerObj["hp"]
    playerOriginATK = playerObj["atk"]
    playerOriginDEF = playerObj["def"]
    #正式開打
    playerAtkFlag = playerObj["level"] > bossObj["level"]
    while playerObj["hp"] > 0 and bossObj["hp"] > 0:
        if playerAtkFlag:
            await doAttack(playerObj, bossObj, player,
                           bossObj["name"])  #參數1對參數2發起攻擊,會直接削減物件血量,注意資料回寫
        else:
            await doAttack(bossObj, playerObj, bossObj["name"], player)
        playerAtkFlag = not playerAtkFlag
    if playerObj["hp"] > 0:
        #挑戰贏了,發獎勵
        playerObj["money"] += bossObj["giveMoney"]
        playerObj["currExp"] += bossObj["giveExp"]
        await ctx.send(
            f"{player} 戰勝了Boss! 獲得 {bossObj['giveMoney']} 金錢和 {bossObj['giveExp']} 經驗值，10 分鐘後可再次挑戰"
        )
    else:
        #挑戰失敗,懲罰
        playerObj["money"] = int(playerObj["money"] * 0.5)
        await ctx.send(
            f"{player} 戰敗! 付出 {playerObj['money']} 元療傷才保住小命，10 分鐘後可再次挑戰")
    #打完之後要把挑戰者各項屬性寫回去,在戰鬥中會有buff debuff 要還原
    playerObj["hp"] = playerOriginHP
    playerObj["atk"] = playerOriginATK
    playerObj["def"] = playerOriginDEF
    playerObj.pop("skill", None)
    playerObj.pop("originHP", None)
    await checkLevelUp(ctx.author, users)
    with open("character.json", "w") as f:
        json.dump(users, f)


async def doAttack(atkObj,
                   atkedObj,
                   atkObjName,
                   atkedObjName,
                   canUseSkill=True):
    #function說明
    #參數1:發起攻擊的物件,必須擁有atk def lucky這些屬性
    #參數2:受到攻擊的物件,必須擁有atk def lucky這些屬性
    #參數3:發起攻擊的物件的名字
    #參數4:受到攻擊的物件的名字
    #參數5:這場戰鬥是否可使用技能,預設可用,但死亡決鬥記得改成0,不用技能
    #return value:這次攻擊的結果(str)
    resStr = ""
    skillToBoss = [
        "爆擊，雙倍傷害", "臭王發威放個屁，減少 Boss 30% 當前生命", "收到欠款五萬心情好，攻擊防禦上升15%"
    ]  #打Boss的時候給玩家用的技能
    if not "skill" in atkObj:
        atkObj["skill"] = skillToBoss

    atkIsLucky = atkObj["lucky"] / (
        atkObj["lucky"] + atkedObj["lucky"]) * 100 > random.randrange(0, 100)
    if not canUseSkill:
        atkIsLucky = False
    if atkIsLucky:
        #使用技能
        skillName = ""
        if len(atkObj["skill"]) == 1:
            skillName = atkObj["skill"][0]
        else:
            skillName = atkObj["skill"][random.randrange(
                0, len(atkObj["skill"]))]
        resStr += await doSkill(atkObj, atkedObj, atkObjName, atkedObjName,
                                skillName)
    else:
        #使用普攻
        dmg = int(atkObj["atk"] * (100 / (100 + atkedObj["def"])))
        dmgshift = random.randrange(min(int(dmg * -0.1), -5),
                                    min(int(dmg * 0.1), 5))
        dmg += dmgshift
        dmg = max(dmg, random.randrange(4, 10))
        atkedObj["hp"] -= dmg
        resStr += f"{atkObjName} 對 {atkedObjName} 造成 {dmg} 傷害"
    #print(resStr) #有需要可以print戰鬥過程出來看
    return resStr


async def doSkill(atkObj, atkedObj, atkObjName, atkedObjName, skillName):
    #function說明
    #參數1:使用技能的物件,必須擁有atk def lucky這些屬性,還要有skill
    #參數2:受到攻擊的物件,必須擁有atk def lucky這些屬性
    #參數3:使用技能的物件的名字
    #參數4:受到攻擊的物件的名字
    #參數5:使用的技能名
    #return value:這次技能的結果(str)
    resuleStr = ""
    dmg = int(atkObj["atk"] * (100 / (100 + atkedObj["def"])))
    dmgshift = random.randrange(min(int(dmg * -0.1), -5),
                                min(int(dmg * 0.1), 5))
    dmg += dmgshift
    dmg = max(dmg, 10)
    skills = [
        "爆擊，雙倍傷害", "臭王發威放個屁，減少 Boss 30% 當前生命", "收到欠款五萬心情好，攻擊防禦上升15%", "汪汪",
        "喵喵", "斷掉啦 Glasses", "你不會更新你要先講", "全台灣每個法官都會判你有罪", "我兒子有病",
        "你去找個會玩的來看", "賴皮大法-這場不算啦", "滑倒", "滑到摔死", "QRQ", "只會鼻地", "222222",
        "我這一刀下去你會死", "利五炭及某", "空幹"
    ]  #這個陣列放所有技能
    if skillName == skills[0]:
        atkedObj["hp"] -= dmg * 2
        resuleStr += f"{atkObjName} 爆擊，造成 {dmg * 2} 傷害"
    elif skillName == skills[1]:
        atkedObj["hp"] *= 0.7
        resuleStr += f"{atkObjName} 使出「臭啊」，臭王放屁，{atkedObjName} 失去 30% 當前生命"
    elif skillName == skills[2]:
        atkObj["atk"] *= 1.15
        atkObj["def"] *= 1.15
        resuleStr += f"{atkObjName} 收到欠款五萬，心情愉悅，攻擊力和防禦力上升15%"
    elif skillName == skills[3]:  #汪汪
        atkedObj["hp"] -= dmg * 1.2
        resuleStr += f"{atkObjName} 使出汪汪強化攻擊，造成 {int(dmg*1.2)} 傷害"
    elif skillName == skills[4]:  #喵喵
        atkedObj["hp"] -= dmg * 1.4
        resuleStr += f"{atkObjName} 使出喵喵強化攻擊，造成 {int(dmg*1.4)} 傷害"
    elif skillName == skills[5]:  #斷掉啦
        atkedObj["hp"] -= atkedObj["originHP"] * 0.2
        resuleStr += f"{atkObjName} 不小心把 Glasses 弄斷啦，玻璃碎片噴到你，造成20%最大生命傷害"
    elif skillName == skills[6]:  #不會更新
        atkedObj["def"] *= 0.6
        resuleStr += f"{atkObjName} 怒噴你不會更新，{atkedObjName} 也要睡啦，防禦降低 40%"
    elif skillName == skills[7]:  #判你有罪
        atkedObj["atk"] *= 0.7
        resuleStr += f"{atkObjName} 判你有罪，使 {atkedObjName} 攻擊力降低 30%"
    elif skillName == skills[8]:  #兒子有病
        atkedObj["def"] *= 0.6
        atkedObj["atk"] *= 0.6
        resuleStr += f"{atkObjName} 說他們兒子有病，導致 {atkedObjName} 自尊心受創，攻擊力和防禦力降低40%"
    elif skillName == skills[9]:  #找個會玩的
        atkedObj["hp"] -= dmg * 2.5
        resuleStr += f"{atkObjName} 叫你找個會玩的，但是你找不到，趁機造成 {int(dmg*2.5)} 傷害"
    elif skillName == skills[10]:  #賴皮大法
        atkObj["hp"] = atkObj["originHP"]
        resuleStr += f"{atkObjName} 使出終極賴皮大法，這局不算，生命值全滿"
    elif skillName == skills[11]:  #滑倒
        atkedObj["hp"] -= dmg * 2.8
        resuleStr += f"{atkObjName} 釋放出些許油，不小心摔了一小跤，造成 {int(dmg*2.8)} 傷害"
    elif skillName == skills[12]:  #滑到摔死
        atkedObj["hp"] -= dmg * 3.0
        resuleStr += f"{atkObjName} 噴出大量的油，直接摔死，造成 {int(dmg*3.0)} 傷害"
    elif skillName == skills[13]:  #QRQ
        atkedObj["hp"] -= dmg * 3.3
        resuleStr += f"{atkObjName} 酒桶連招QRQ，一套帶走，趁機造成 {int(dmg*3.3)} 傷害"
    elif skillName == skills[12]:  #只會鼻地
        atkedObj["hp"] -= dmg * 3.5
        resuleStr += f"{atkObjName} 嘿你就繼續不回家，我就無情BD恭喜，造成 {int(dmg*3.5)} 傷害"
    elif skillName == skills[12]:  #222222
        atkedObj["hp"] -= dmg * 3.8
        resuleStr += f"{atkObjName} 左下社交，拜訪家園222222，造成 {int(dmg*3.8)} 傷害"
    elif skillName == skills[12]:  #我這一刀下去你會死
        atkedObj["hp"] -= dmg * 3.8
        resuleStr += f"{atkObjName} 丁皇出征，直接不生，造成 {int(dmg*3.8)} 傷害"
    elif skillName == skills[12]:  #利五炭及某
        atkedObj["hp"] -= dmg * 4.0
        resuleStr += f"{atkObjName} 我問你一句話就好，你有賺錢嗎，造成 {int(dmg*4.0)} 傷害"
    elif skillName == skills[12]:  #空幹
        atkedObj["hp"] -= dmg * 4.0
        resuleStr += f"{atkObjName} ，， {int(dmg*4.0)} 傷害"
    return resuleStr


@client.command()
async def go(ctx):
    await create_character(ctx.author)
    user = ctx.author
    data = 0
    with open("bossfight.json", "r") as f:
        data = json.load(f)
    if data["hasBoss"] != "1":
        await ctx.send(f"現在沒有Boss戰，請輸入「!組隊Boss」開啟一場")
        return
    if str(user.id) in data["member"]:
        await ctx.send(f"{user} 已加入此次遠征,請勿重複加入")
    else:
        data["member"].append(str(user.id))
        await ctx.send(f"{user} 成功加入此次遠征")
    with open("bossfight.json", "w") as f:
        json.dump(data, f)


@client.command()
async def bossinfo(ctx, level=1):
    BossObj = await getBossObj(str(level))
    await showBossInfo(ctx, BossObj)


async def getBossObj(level):
    data = None
    with open("boss.json", "r") as f:
        data = json.load(f)
    data = data[level]
    return data


@client.command()
async def 勝率(ctx, member: discord.Member):
    await create_character(ctx.author)
    await create_character(member)
    users = await get_character_data()
    winrate = await winRate(users[str(ctx.author.id)], users[str(member.id)])
    await ctx.send(f"{ctx.author} 對上 {member} 的勝率為 {round(winrate * 100, 1)} %"
                   )


async def winRate(obj1, obj2):
    #回傳obj1與obj2對決的勝率

    return obj1["atk"] * obj1["def"] * obj1["hp"] / (
        obj1["atk"] * obj1["def"] * obj1["hp"] +
        obj2["atk"] * obj2["def"] * obj2["hp"])


@client.command()
async def 轉生(ctx):
    await create_character(ctx.author)
    users = await get_character_data()
    canR = await canRebirth(users[str(ctx.author.id)])
    if canR:
        await ctx.send(f"{ctx.author} 你符合轉生資格，請慎重確認後輸入「!我確定要轉生」進行轉生")
    else:
        await ctx.send(f"{ctx.author} 不符合轉生資格，請與他人進行死亡對決取得轉生必需道具")


async def canRebirth(obj):
    #回傳obj是否可轉生
    return "canRebirth" in obj and obj["canRebirth"] == "1"


@client.command()
async def 我確定要轉生(ctx):
    await create_character(ctx.author)
    users = await get_character_data()
    playerObj = users[str(ctx.author.id)]
    canR = await canRebirth(playerObj)
    if not canR:
        await ctx.send(f"{ctx.author} 不符合轉生資格，請與他人進行死亡對決取得轉生必需道具")
        return
    playerObj["level"] = 1
    playerObj["hp"] = 100
    playerObj["atk"] = 10
    playerObj["def"] = 3
    playerObj["lucky"] = playerObj["lucky"] + random.randrange(7, 12)
    playerObj["currExp"] = 0
    playerObj["money"] = 0
    playerObj["canRebirth"] = "0"
    RebirthTimes = 0
    levelUpBuff = 1
    if "RebirthTimes" in playerObj:
        RebirthTimes = playerObj["RebirthTimes"]
    if "levelUpBuff" in playerObj:
        levelUpBuff = playerObj["levelUpBuff"]
    playerObj["RebirthTimes"] = RebirthTimes + 1
    playerObj["levelUpBuff"] = levelUpBuff + round(
        random.randrange(7, 14) / 100, 2)
    playerObj["levelUpBuff"] = round(playerObj["levelUpBuff"], 2)
    with open("character.json", "w") as f:
        json.dump(users, f)
    await ctx.send(
        f"{ctx.author} 轉生第 {playerObj['RebirthTimes']} 次成功!，角色資料被重置為初始狀態，幸運值上升到 {playerObj['lucky']} ，擁有 {int(playerObj['levelUpBuff'] * 100)} % 的升級能力加成!"
    )


@client.command()
async def 死亡對決(ctx, member: discord.Member):
    await create_character(ctx.author)
    await create_character(member)
    users = await get_character_data()
    checkTarget = await haveDeathFight(member)  #判斷你的目標是否正在進行另一場死亡對決
    checkHost = await haveDeathFight(ctx.author)  #判斷你是否正在進行另一場死亡對決
    if checkHost:
        await ctx.send(f"{ctx.author} 你已經發起一場死亡對決，或有人正在挑戰你，請稍後再試")
        return

    if checkTarget:
        await ctx.send(f"{member} 正在進行另一場死亡對決，請稍後再試")
        return

    tagID = f'<@{member.id}>'
    await ctx.send(
        f"{tagID} ，{ctx.author} 對你發起死亡對決，敗者的角色將被永久刪除，請輸入「!接受」 或等待 1 分鐘後自動取消本次對決(建議輸入「!勝率 @人名」先查看勝率)"
    )
    data = {}
    with open("deathFight.json", "r") as f:
        data = json.load(f)
    data[str(ctx.author.id)] = {
        "host": str(ctx.author.id),
        "target": str(member.id),
        "YesNo": "0"
    }
    with open("deathFight.json", "w") as f:
        json.dump(data, f)
    await asyncio.sleep(60)  #60秒後自動清除此次死亡戰鬥
    await clearDeathFight(ctx.author)


async def deathBattle(ctx, player1, player2):
    await create_character(player1)
    await create_character(player2)
    users = await get_character_data()
    playerObj1 = users[str(player1.id)]
    playerOriginHP1 = playerObj1["hp"]
    playerObj2 = users[str(player2.id)]
    playerOriginHP2 = playerObj2["hp"]
    resultStr = ""
    #正式開打
    player1AtkFlag = playerObj1["level"] > playerObj2["level"]
    while playerObj1["hp"] > 0 and playerObj2["hp"] > 0:
        if player1AtkFlag:
            resultStr += await doAttack(playerObj1, playerObj2, player1,
                                        player2,
                                        False)  #參數1對參數2發起攻擊,會直接削減物件血量,注意資料回寫
            resultStr += "\n"
        else:
            resultStr += await doAttack(playerObj2, playerObj1, player2,
                                        player1, False)
            resultStr += "\n"
        player1AtkFlag = not player1AtkFlag
    await ctx.send(resultStr)
    if playerObj1["hp"] > 0:
        #player1贏了,發獎勵,寫回血量資料,清除player2資料
        playerObj1["canRebirth"] = "1"
        playerObj1["hp"] = playerOriginHP1
        await ctx.send(
            f"{player1} 在死亡決鬥中勝出! 獲得一個「7414 統粉之魂」，可進行轉生。{player2} 不幸落敗，角色資料遭到清除!"
        )
        playerObj2["level"] = 1
        playerObj2["hp"] = 100
        playerObj2["atk"] = 10
        playerObj2["def"] = 3
        playerObj2["lucky"] = 30
        playerObj2["currExp"] = 0
        playerObj2["money"] = 0
        playerObj2["canRebirth"] = "0"
        playerObj2["levelUpBuff"] = 1
        playerObj2["RebirthTimes"] = 0
    else:
        #player2贏了,發獎勵,寫回血量資料,清除player1資料
        playerObj2["canRebirth"] = "1"
        playerObj2["hp"] = playerOriginHP2
        await ctx.send(
            f"{player2} 在死亡決鬥中勝出! 獲得一個「7414 統粉之魂」，可進行轉生。{player1} 不幸落敗，角色資料遭到清除!"
        )
        playerObj1["level"] = 1
        playerObj1["hp"] = 100
        playerObj1["atk"] = 10
        playerObj1["def"] = 3
        playerObj1["lucky"] = 30
        playerObj1["currExp"] = 0
        playerObj1["money"] = 0
        playerObj1["canRebirth"] = "0"
        playerObj1["levelUpBuff"] = 1
        playerObj1["RebirthTimes"] = 0
    playerObj1.pop("skill", None)
    playerObj2.pop("skill", None)

    with open("character.json", "w") as f:
        json.dump(users, f)


async def clearDeathFight(user):
    data = {}
    with open("deathFight.json", "r") as f:
        data = json.load(f)
    data.pop(str(user.id), None)
    with open("deathFight.json", "w") as f:
        json.dump(data, f)


@client.command()
async def 接受(ctx):
    await create_character(ctx.author)
    data = {}
    inDeathFight = await haveDeathFight(ctx.author)
    if not inDeathFight:
        await ctx.send(f"目前沒有人對 {ctx.author} 發起死亡對決")
        return
    DeathFightHostEvent = await getFightEvent(ctx.author)
    with open("deathFight.json", "r") as f:
        data = json.load(f)
    DeathFightHostEvent["YesNo"] = "1"
    await ctx.send(
        f"{'<@'+DeathFightHostEvent['target']+'>'}接受了 {'<@'+DeathFightHostEvent['host']+'>'} 發起的死亡對決!，決鬥將在5秒後開始，各位請準備觀賞!"
    )

    with open("deathFight.json", "w") as f:
        json.dump(data, f)
    await asyncio.sleep(5)
    player1 = await client.fetch_user(int(DeathFightHostEvent['host']))
    player2 = await client.fetch_user(int(DeathFightHostEvent['target']))
    await clearDeathFight(player1)  #一旦接受就清除由player1發起的死亡對局事件
    await deathBattle(ctx, player1, player2)


@client.command()
async def 測試ID(ctx):
    player1 = await client.fetch_user(481058718138630155)
    print(player1)


async def getFightEvent(target):
    #根據target的ID 找出死亡決鬥事件物件,如果target沒被挑戰,回傳None
    await create_character(target)
    result = None
    data = {}
    with open("deathFight.json", "r") as f:
        data = json.load(f)
    for host in data:
        if data[host]["target"] == str(target.id):
            result = data[host]
            break
    return result


async def haveDeathFight(user):
    #判斷user是否身處一場死亡對決中(發起者 or 被挑戰者都算),是的話傳回True
    await create_character(user)
    data = None
    result = False
    with open("deathFight.json", "r") as f:
        data = json.load(f)
    for host in data:
        if data[host]["target"] == str(user.id) or data[host]["host"] == str(
                user.id):
            result = True
            break
    return result


async def showBossInfo(ctx, BossObj):
    em = discord.Embed(title=f"Boss資訊╭[◕ ͜🔴◕]👍🏼")
    em.add_field(name="名稱", value=BossObj["name"])
    em.add_field(name="等級 🔥", value=BossObj["level"])
    em.add_field(name="血量 ❤️", value=BossObj["hp"])
    em.add_field(name="攻擊力 ⚔️", value=BossObj["atk"])
    em.add_field(name="防禦力 🛡", value=BossObj["def"])
    em.add_field(name="獎勵經驗值 📊", value=BossObj["giveExp"])
    em.add_field(name="獎勵金錢 💰", value=BossObj["giveMoney"])
    #em.add_field(name = "你的保險箱" ,value = bank_amt)
    await ctx.send(embed=em)


keep_alive.keep_alive()
client.run(token)
