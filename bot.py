import discord
import datetime
import os
import dotenv
import growtopia
import aiosqlite
from discord.ext import commands

dotenv.load_dotenv()

class GrowContext(commands.Context):
	_growuser = None

	@property
	def growuser(self):
		return self._growuser

	async def get_growuser(self):
		async with aiosqlite.connect('./db/data.sql') as db:
			self._db = db
			async with db.execute('SELECT * FROM members WHERE id = ?',(self.author.id,)) as cursor:
				data = await cursor.fetchone()
				if data:
					user = growtopia.StaticGrowuser(data,self.author)
					self._growuser = user
					return user

class Cocoinator(commands.Bot):

	async def get_context(self,message,*,cls=GrowContext):
		return await super().get_context(message,cls=cls)

bot = Cocoinator(command_prefix=".",case_insensitive=True, activity=discord.Game(name="with the guild members | .help"),help_command=None,intents=discord.Intents.all(),owner_ids=[477789603403792404,716503311402008577]
)
bot.load_extension('jishaku')
try:
	os.system('clear')
except:
	pass
bot.uptime = datetime.datetime.utcnow()
bot.color = discord.Colour.from_rgb(132, 112, 255)
bot.colour = discord.Colour.from_rgb(132, 112, 255)

extensions = ['utility','shop','profit','levels','guild','growtopia','events']
for i in extensions:
	bot.load_extension('cogs.'+i)

@bot.check
async def check(ctx):
    if await bot.is_owner(ctx.author) or ctx.channel.id == 749168433782063174 or not ctx.guild:
        return True
    return False

@bot.listen()
async def on_ready():
	print('(BOT) Ready to be used')

bot.run(os.getenv('TOKEN'))