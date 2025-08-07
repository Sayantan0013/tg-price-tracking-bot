from argparse import ArgumentParser
import pycountry
from telegram import BotCommand, MenuButtonCommands

def get_country_name(alpha2_code):
    country = pycountry.countries.get(alpha_2=alpha2_code.upper())
    return country.name if country else None

def get_country_list():
    return [country.alpha_2.lower() for country in pycountry.countries]

async def set_commands(application):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help info"),
        BotCommand("region", "set your region")
    ]
    await application.bot.set_my_commands(commands)
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

# def parse_args():
