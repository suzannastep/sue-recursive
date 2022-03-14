# ⚠️ Only modify this file if you know what you're doing!

from bot import TicTacToeBot

def handle_message(runner, channel, message):
    if channel == "init":
        runner.bot = TicTacToeBot({
          "player": message["player"],
          "color": message["color"],
          "turn_time_limit": message["turnTimeLimit"],
          "game_time_limit": message["gameTimeLimit"],
        })
    elif channel == "move":
        return runner.bot.move(message)
