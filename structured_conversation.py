import asyncio
from datetime import datetime, timedelta
import random
from telethon import TelegramClient, events

# ==== Налаштування акаунтів ====
accounts = [
    {
        "api_id": "24937877",
        "api_hash": "ea965beea8cbd30bdede9cd833e153df",
        "phone": "+79886102536",
        "session": "session_evelina",
        "name": "Евелина",
        "responses_to_messages": {
            "И да до конца дня жду все переводы на кошелёк": ["Ок"],
            "Кинул матч. Если у кого-то будут вопросы пишите": ["Ок"],
        },
    },
    {
        "api_id": "21939330",
        "api_hash": "7219726c15f087c480715cd868fe0a66",
        "phone": "+79899314493",
        "session": "session_jenya",
        "name": "Женя",
        "responses_to_messages": {
            "Ребята. Готовимся есть инсайд. Жду фитбек по готовности": ["Я готов"],
            "И да до конца дня жду все переводы на кошелёк": ["Будет сделано бос"],
        },
    },
    {
        "api_id": "29854499",
        "api_hash": "7d96f558a03187ad9834debedb8b2f71",
        "phone": "+79827280996",
        "session": "session_iryna",
        "name": "Ірина",
        "responses_to_messages": {
            "Всем привет": ["Добрый день"],
        },
    },
    {
        "api_id": "21993796",
        "api_hash": "ed9bbff90ea57864f307cc56f238d4f3",
        "phone": "+79363168089",
        "session": "session_matvey",
        "name": "Матвій",
        "responses_to_messages": {
            "Всем привет": ["О есть что-то для нас?"],
        },
    },
    {
        "api_id": "13623212",
        "api_hash": "298ac6a2c639573f64a898c9997ac214",
        "phone": "+79178691992",
        "session": "session_vanya",
        "name": "Ваня",
        "responses_to_messages": {
            "Привет": ["👋"],
            "Ребята. Готовимся есть инсайд. Жду фитбек по готовности": ["+"],
        },
    },
    {
        "api_id": "22135148",
        "api_hash": "29a7d449bd1f1cd3dba69357f9122c76",
        "phone": "+79378670599",
        "session": "session_katya",
        "name": "Катя",
        "responses_to_messages": {
            "Привет": ["Хаюшки"],
            "Ребята. Готовимся есть инсайд. Жду фитбек по готовности": ["Я думаю все готовы уже давно"],
        },
    },
]

# ==== ID чата ====
chat_id = -1002495997895

async def run_accounts(accounts, chat_id):
    clients = []
    last_responded = {}

    for account in accounts:
        client = TelegramClient(account["session"], account["api_id"], account["api_hash"])
        await client.start(phone=account["phone"])
        print(f"✅ Аккаунт {account['name']} авторизован!")
        clients.append((account, client))

    async def handle_incoming_messages(client, account):
        @client.on(events.NewMessage(chats=chat_id))
        async def handle_message(event):
            sender = await event.get_sender()
            if sender.is_self:
                return

            message_text = event.message.text.strip()
            user_key = (sender.id, account["name"])

            print(f"📩 Получено сообщение: {message_text} от {sender.id}")

            for key_phrases, responses in account["responses_to_messages"].items():
                if any(phrase.lower() in message_text.lower() for phrase in (key_phrases if isinstance(key_phrases, tuple) else [key_phrases])):
                    response = random.choice(responses)
                    await asyncio.sleep(random.randint(35, 120))
                    await event.reply(response)
                    print(f"💬 {account['name']} ответил: {response}")
                    last_responded[user_key] = datetime.now()
                    return

            print(f"📩 Неожиданное сообщение: {message_text}")

    tasks = []
    for account, client in clients:
        tasks.append(asyncio.create_task(handle_incoming_messages(client, account)))

    await asyncio.gather(*[client.run_until_disconnected() for _, client in clients], *tasks)

# ==== Главная функция ====
async def main():
    await run_accounts(accounts, chat_id)

if __name__ == "__main__":
    asyncio.run(main())
