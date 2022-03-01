token = "NjE5MDgzNjg1MDAxNDI4OTky.XXDEnA.a_3YCs03wREl2050GAaUEmSLJmg"

import discord
from discord.ext import commands
import nest_asyncio
import datetime
import json
import os
from urllib import parse, request
import re
import random
import keep_alive

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
async def 指令(ctx):
    await ctx.send(
        '!賭 數字,!偷 @人名 !抽獎,!乞討,!快算快答(!cal),!終極密碼(!code) 數字,!頭貼評分 @人名,!打 @人名 ,!give @人名,!開台機率,!吃啥,!排行,!丟炸彈,!抽籤,!痛扁老闆,!QR QRCode的內容\n\n戰鬥系統相關指令(刪檔封測中，你的角色資料隨時會被清空，請自行評估)\n!練功\n!status\n!強化 武器\n!強化 防具\n!決鬥 @人名\n!更新目標'
    )


@client.command()
async def 開賭場網址(ctx):
    await ctx.send(
        '開賭場網址 : https://replit.com/join/sfwmvlbdki-675bot 按最上面Run，關網頁前按stop')


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

    earnings = random.randrange(1, 1000)

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
    earnings = random.randrange(1, 10)
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

    with open("cal.json", "w") as f:
        data = ans
        json.dump(data, f)
    await ctx.send(f"聊天室快算快答!{a}+{b}，輸入!a 數字搶答!(EX:!a 30)╭[◕ ͜🔴◕]👍🏼")


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
            f"答案為{amount}，{ctx.author}第一個算出答案並贏得10元!╭[◕ ͜🔴◕]👍，一分鐘後可算下一題")
        users[str(user.id)]["wallet"] += 10
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
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
    earnings = random.randrange(10, 37)
    earningMoney = random.randrange(21, 69)
    users[str(user.id)]["currExp"] += earnings
    users[str(user.id)]["money"] += earningMoney

    levelUP = await checkLevelUp(user, users)
    if levelUP:
        await ctx.send(
            f"{ctx.author.name}打怪練功獲得 {earnings} 經驗值、{earningMoney} 金幣，並且升了一級💰!各種能力都得到了提升，15秒後可再練功一次"
        )
    else:
        await ctx.send(
            f"{ctx.author.name}打怪練功獲得{earnings}經驗值、{earningMoney} 金幣💰，距離升級還有{100-users[str(user.id)]['currExp']}經驗值!15秒後可再練功一次"
        )


@client.command()
async def status(ctx):
    await create_character(ctx.author)
    user = ctx.author
    users = await get_character_data()

    level = users[str(user.id)]["level"]
    hp = users[str(user.id)]["hp"]
    atk = users[str(user.id)]["atk"]
    yourdef = users[str(user.id)]["def"]
    currExp = users[str(user.id)]["currExp"]
    money = users[str(user.id)]["money"]

    em = discord.Embed(title=f"{ctx.author.name}的角色資訊╭[◕ ͜🔴◕]👍🏼")
    em.add_field(name="等級 🔥", value=level)
    em.add_field(name="血量 ❤️", value=hp)
    em.add_field(name="攻擊力 ⚔️", value=atk)
    em.add_field(name="防禦力 🛡", value=yourdef)
    em.add_field(name="經驗值 📊", value=currExp)
    em.add_field(name="金錢 💰", value=money)
    #em.add_field(name = "你的保險箱" ,value = bank_amt)
    await ctx.send(embed=em)


@client.command()
async def 強化(ctx, item):
    if not (item == "武器" or item == "防具"):
        return
    await create_character(ctx.author)
    user = ctx.author
    users = await get_character_data()
    hp = users[str(user.id)]["hp"]
    atk = users[str(user.id)]["atk"]
    yourdef = users[str(user.id)]["def"]
    money = users[str(user.id)]["money"]
    success = random.randrange(1, 100) > 40
    if money < 150:
        await ctx.send(f'{ctx.author}金幣不足，每次強化需消耗150金幣')
        return
    users[str(user.id)]["money"] -= 150
    if not success:
        await ctx.send(f'{ctx.author}消耗150金幣強化失敗，角色能力沒有任何改變')
        with open("character.json", "w") as f:
            json.dump(users, f)
        return
    if item == "武器":
        atkup = random.randrange(4, 7)
        users[str(user.id)]["atk"] += atkup
        await ctx.send(f'{ctx.author}消耗150金幣強化成功，攻擊力從 {atk} 上升到 {atk + atkup}')
    if item == "防具":
        defup = random.randrange(2, 6)
        hpup = random.randrange(23, 36)
        users[str(user.id)]["def"] += defup
        users[str(user.id)]["hp"] += hpup
        await ctx.send(
            f'{ctx.author}消耗150金幣強化成功，防禦力從 {yourdef} 上升到 {yourdef + defup}，血量從 {hp} 上升到 {hp + hpup}'
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
        "目前計畫更新內容:\n1.Boss戰：可單人或組隊參加，失敗需扣除金錢，組隊挑戰獎勵平分\n2.死亡對決：和決鬥類似，差別是敗者的角色會直接被永久刪除，勝者則會獲得一顆「7414 統粉之魂」\n3.轉生：需擁有「7414 統粉之魂」才可進行，轉生後角色會被重置回初始狀態，但是之後會成長得更快速，例如別人升級+50HP，5攻擊，3防禦，你可能+120HP，12攻擊，10防禦"
    )


@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
@commands.cooldown(1, 3, commands.BucketType.channel)
async def boss(ctx, level):

    await battle(ctx, ctx.author, str(level), 1)


#確認升級function
async def checkLevelUp(user, users):

    c = users[str(user.id)]
    levelUp = False  #True代表有升級,可以print一些訊息提醒user能力提升了
    while c["currExp"] >= 100:
        levelUp = True
        c["currExp"] -= 100
        c["hp"] += random.randrange(23, 42)
        c["atk"] += random.randrange(3, 7)
        c["def"] += random.randrange(2, 4)
        c["level"] += 1
    with open("character.json", "w") as f:
        json.dump(users, f)
    return levelUp


#user1 傳入 ctx.author,user2是被tag的,可參考give方法
async def battle(ctx, user1, user2, isBossFight=0):
    #isBossFight = 0代表和玩家戰鬥,1代表是和boss戰鬥,預設是0
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
        showBossInfo(ctx,BossObj)
        await ctx.send("開啟一場全新的Boss戰，請輸入 !go 加入此次遠征")
        data["hasBoss"] = "1"
        data["BossLevel"] = str(level)
    with open("bossfight.json", "w") as f:
        json.dump(data, f)


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


async def getBossObj(level):
    data = 0
    with open("boss.json", "r") as f:
        data = json.load(f)
    data = data[level]
    return data


async def showBossInfo(ctx,BossObj):
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


#keep_alive.keep_alive()
#client.run(token)
