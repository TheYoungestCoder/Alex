from os import environ
import disnake
from disnake.ext import commands

ci = disnake.CommandInteraction
bot = commands.Bot()


def get_op(ctx: disnake.Member | disnake.Guild):
    for role in ctx.roles:
        if role.name == "op":
            return role


@bot.slash_command()
async def kick(inter: ci, target: disnake.Member):
    await target.kick()
    await inter.response.send_message(
        f"Kicked {target.mention}: Kicked by an operator")


@bot.slash_command()
async def ban(inter: ci, target: disnake.Member):
    await target.ban()
    await inter.response.send_message(
        f"Banned {target.mention}: Banned by an operator")


@bot.slash_command()
async def op(inter: ci, target: disnake.Member):
    msg = f"Nothing changed. The player already is an operator"
    if get_op(target) is None:
        msg = f"Made {target.mention} a server operator"
        await target.add_roles(get_op(inter.guild))
    await inter.response.send_message(msg)


@bot.slash_command()
async def deop(inter: ci, target: disnake.Member):
    msg = "Nothing changed. The player is not an operator"
    if op := get_op(target):
        await target.remove_roles(op)
        msg = f"Made {target.mention} no longer a server operator"
    await inter.response.send_message(msg)


@bot.slash_command()
async def tag(inter: ci,
              target: disnake.Member,
              command: commands.option_enum(["add", "remove", "list"]),
              role: disnake.Role = None):
    msg = f"{target.mention} has "
    if command == "add":
        msg = f"{target.mention} already has this tag"
        if role not in target.roles:
            await target.add_roles(role)
            msg = f"Added tag {role.mention} to {target.mention}"
    elif command == "remove":
        msg = f"{target.mention} does not have this tag"
        if role in target.roles:
            await target.add_roles(role)
            msg = f"Removed tag {role.mention} from {target.mention}"
    elif roles := target.roles:
        msg = f"{target.mention} has {len(roles)} tags: {', '.join(role.mention for role in roles)}"
    await inter.response.send_message(msg)


@bot.slash_command()
async def advance(inter: ci, target: disnake.Member, advancement: str):
    embed = disnake.Embed()
    embed.add_field(
        "⁢", f"{target.mention} has made the advancement [[{advancement}]](https://example.com)⁢\n⁢\n")
    await inter.response.send_message("⁢", embed=embed)


@bot.slash_command()
async def locate(inter: ci, target: disnake.Member):
    msg = f"There is no voice channel with member {target.mention}"
    if voice := target.voice:
        msg = f"{target.mention} is in {voice.channel.mention}"
    await inter.response.send_message(msg)


async def teleport(inter: ci, target: disnake.VoiceChannel):
    msg = f"Teleported {inter.author.mention} to {target.mention}"
    try:
        await inter.author.move_to(target)
    except:
        msg = f"Teleportation failed. You must be in a voice channel"
    await inter.response.send_message(msg)
bot.slash_command()(teleport)
bot.slash_command(name="tp")(teleport)

bot.run(environ["BOT_TOKEN"])
