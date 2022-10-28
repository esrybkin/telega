from random import randint
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

CNT_CANDY = 2021
MAX_CANDY_STEP = 28
MIN_CANDY_STEP = 0
PLAYERS_NAMES = {
    1: 'Компьютер',
    2: 'update.effective_user.first_name'
}


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Количество конфет всего: {CNT_CANDY}')
    await update.message.reply_text(f'За один ход можно взять не более {MAX_CANDY_STEP} конфет')
    await update.message.reply_text(f'Первый ход определяет жребий')
    await update.message.reply_text(f'Выигрывает тот, кто последним заберет все конфеты!')
    await update.message.reply_text(f'Для хода необходимо написать команду /h и число конфет')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # log_command(update, context)
    await update.message.reply_text(f'/rules\n/start\n/help\n')


def get_first_move_player() -> int:
    return randint(1, 2)


def valid_cnt_candy(cnt: int) -> bool:
    if MIN_CANDY_STEP <= cnt <= MAX_CANDY_STEP:
        return True
    else:
        return False


def valid_type_value_cnt_candy(cnt: str) -> bool:
    if cnt.isdigit():
        return True
    else:
        return False


def valid_value_cnt_candy(cnt: int, full_cnt: int, players_candies: dict) -> bool:
    if (full_cnt - (players_candies[1] + players_candies[2])) < cnt:
        return False
    else:
        return True


def get_remainder(players_candies: dict, full_cnt: int) -> int:
    return full_cnt - (players_candies[1] + players_candies[2])


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    cnt_candy_players: dict = {
        1: 0,
        2: 0
    }

    id_player: int = get_first_move_player()
    if id_player == 1:
        await update.message.reply_text(f'Первым ходит {PLAYERS_NAMES[1]}!')
    else:
        await update.message.reply_text(f'Первый ход ваш, {update.effective_user.first_name}!')



    while (cnt_candy_players[1] + cnt_candy_players[2]) < CNT_CANDY:
        if id_player == 1:
            # current_cnt_candy = ((CNT_CANDY - cnt_candy_players[1] - cnt_candy_players[2]) % MAX_CANDY_STEP) + 1
            current_cnt_candy = randint(1, 29)
            cnt_candy_players[id_player] += int(current_cnt_candy)
            await update.message.reply_text(f'Компьютер берёт {current_cnt_candy}')
            await update.message.reply_text(f"Осталось конфет: {get_remainder(cnt_candy_players, CNT_CANDY)}")
            id_player += 1
            continue
        else:
            await update.message.reply_text(f"{update.effective_user.first_name}, Ваш ход. Сколько берём конфет? -> ")
            # await update.message.reply_text(update.message.text)
            msg = update.message.text
            cnt = msg.split()
            current_cnt_candy = cnt[1]

            if not valid_type_value_cnt_candy(current_cnt_candy) or not valid_cnt_candy(int(current_cnt_candy)):
                await update.message.reply_text(f"Допустимое число конфет [{MIN_CANDY_STEP} , {MAX_CANDY_STEP}]")
                continue

            if not valid_value_cnt_candy(int(current_cnt_candy), CNT_CANDY, cnt_candy_players):
                await update.message.reply_text(f"{update.effective_user.first_name}, Вы не можете взять больше конфет, чем осталось")
                continue

            cnt_candy_players[id_player] += int(current_cnt_candy)
            await update.message.reply_text(f"Осталось конфет: {get_remainder(cnt_candy_players, CNT_CANDY)}")
            id_player -= 1
            continue

        id_player = 1 if id_player == 2 else 2

    await update.message.reply_text(f"Победу одержал {PLAYERS_NAMES[1 if id_player == 2 else 2]}")