# discord.py を読み込む
from discord import Embed
from discord.ext import commands
# 日付を扱うパッケージを読み込む
from datetime import datetime, date, timedelta
#オプショナル引数を扱う
from typing import Optional
import json

#各種パラメータ
BOT_NAME = "BunjiroBot"
INITIAL_BALANCE = 1000

#各種データ（将来的にはデータベース化）
history = []
account = []


# 接続に必要なオブジェクトを生成
bot = commands.Bot(command_prefix="/")

# 起動時に動作する処理
@bot.event
async def on_ready():
	# 起動したらターミナルにログイン通知が表示される
	print('ログインしました')

# 「/register ytanooka」でytanookaのアカウント作成。
@bot.command()
async def register(ctx,login):
		member = [m for m in account if m["login"] == login]
		if member:
			await ctx.send(login + "は既に登録されてるよ！")
			return False
		account.append({"login":login, "balance":INITIAL_BALANCE})
		history.append({"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "sender":BOT_NAME, "receiver":login, "balance":INITIAL_BALANCE, "comment":"initial distribution"})
		await ctx.send("登録したで！\n" + login + ": " + str(INITIAL_BALANCE))

# 「/give nop 42」でnopに42ポイント送金
@bot.command()
async def give(ctx, receiver, balance, comment: Optional[str] = None):
	sender = ctx.author.name
	sender_a = [m for m in account if m["login"] == sender]
	receiver_a = [m for m in account if m["login"] == receiver]
	if not sender_a:
		await ctx.send("あなたのアカウントは存在しません。")
	elif not receiver_a:
		await ctx.send(receiver + "のアカウントは存在しません。")
	elif sender_a[0]["balance"] < int(balance):
		await ctx.send("残高不足です。現在の残高は"+ str(sender_a[0]['balance']))
	else:
		sender_a[0]["balance"] -= int(balance)
		receiver_a[0]["balance"] += int(balance)
		history.append({"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "sender":sender, "receiver":receiver, "balance":int(balance), "comment":comment})
		await ctx.send(sender + "から" + receiver + "に" + balance + "送金したで！")
		print(account)
		print(history)

# 「/balance ytanooka」で残高表示
@bot.command()
async def balance(ctx,login):
	member = [m for m in account if m["login"] == login]
	if not member:
		await ctx.send(login + "のアカウントは存在しません")
	else:
		await ctx.send(login + ": " + str(member[0]["balance"]))

@bot.command()
async def flow(ctx,login):
	member = [m for m in account if m["login"] == login]
	if not member:
		await ctx.send(login + "のアカウントは存在しません。")
		return False
	f = [f for f in history if f["sender"] == login or f["receiver"] == login]
	str = ""
	for r in f:
		str += r["time"] + " "
		if r["sender"] == login:
			str += str(-1*r["balance"]) + " "
			str += r["receiver"] + " "
			str += r["comment"] + "\n"
		else:
			str += str(r["balance"]) + " "
			str += r["sender"] + " "
			str += r["comment"] + "\n"

if __name__ == "__main__":
	# Botの起動とDiscordサーバーへの接続
	f = open("token", 'r')
	TOKEN = f.readline().split('\n')[0]
	bot.run(TOKEN)
