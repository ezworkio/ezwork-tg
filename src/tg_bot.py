import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from models import session, TgAccounts
from rabbit_client import RabbitMQReceiver
from settings import load_config

logging.basicConfig(level=logging.INFO)

config = load_config()
rabbit = RabbitMQReceiver(config.RMQPARAMS)
rabbit.connect()


def start_handler(update, context):
    tg_accounts = session.query(TgAccounts).filter_by(
        telegram_user_id=update.effective_chat.id
    ).first()

    if tg_accounts:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Оповещения с лендинга уже идут к тебе, так что не беспокойся ;)"
        )
    else:
        tg_account = TgAccounts(telegram_user_id=update.effective_chat.id)
        session.add(tg_account)
        session.commit()

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Привет! Теперь ты будешь получать заявки с лендинга EZWork"
        )


def notificator(context):
    rabbit_get = rabbit.get()

    logging.log(msg=rabbit_get, level=logging.INFO)

    if rabbit_get is not None:
        data = rabbit_get['data']
        method_frame = rabbit_get['method_frame']
        if data:
            if data['service'] == 'tg':
                if data['action'] == 'landing_form':
                    rabbit.channel.basic_ack(delivery_tag=method_frame.delivery_tag)

                    for id, telegram_user_id in session.query(TgAccounts.id, TgAccounts.telegram_user_id):

                        context.bot.send_message(
                            telegram_user_id,
                            'Новая заявка на регистрацию\r\nИмя: ' + str(data['data']['name']) + '\r\nНомер телефона: ' + str(data['data']['phone'])
                        )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я не понимаю этой команды"
    )


tg_updater = Updater('1296686925:AAGiODRgjvXswNf91eOH88QYLKjF1FrHtA0')
tg_updater.dispatcher.job_queue.run_repeating(notificator, interval=1, first=0)
tg_updater.dispatcher.add_handler(CommandHandler('start', start_handler))
unknown_handler = MessageHandler(Filters.command, unknown)
tg_updater.dispatcher.add_handler(unknown_handler)
tg_updater.start_polling()
tg_updater.idle()
