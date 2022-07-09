#################################
# mentionall Tagger Bot #
#################################
# Repo Sahibi - Samilben 
# Telegram - t.me/Samilben
# Telegram - t.me/Samilben 
##################################
import heroku3
import random
import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.events import StopPropagation
from config import client, USERNAME, log_qrup, startmesaj, qrupstart, komutlar, sahib, support

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)



anlik_calisan = []
gece_tag = []

#tektag
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global gece_tag
  gece_tag.remove(event.chat_id)
  
  
# Başlanğıc Mesajı
@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  if event.is_private:
    async for usr in client.iter_participants(event.chat_id):
     ad = f"[{usr.first_name}](tg://user?id={usr.id}) "
     await client.send_message(log_qrup, f"ℹ️ **Yeni Kullanıcı -** {ad}")
     return await event.reply(f"{ad} {startmesaj}", buttons=(
                      [
                       Button.inline("🎛 Komutlar", data="komutlar")
                      ],
                      [Button.url('🌱 Beni Gruba Ekle', f'https://t.me/{USERNAME}?startgroup=a')],
                      [Button.url('📣 Support', f'https://t.me/{support}'),
                       Button.url('👨🏻‍💻 Sahibim', f'https://t.me/{sahib}')]
                    ),
                    link_preview=False)


  if event.is_group:
    return await client.send_message(event.chat_id, f"{qrupstart}")

# Başlanğıc Button
@client.on(events.callbackquery.CallbackQuery(data="start"))
async def handler(event):
    async for usr in client.iter_participants(event.chat_id):
     ad = f"[{usr.first_name}](tg://user?id={usr.id}) "
     await event.edit(f"{ad} {startmesaj}", buttons=(
                      [
                       Button.inline("🎛 Komutlar", data="komutlar")
                      ],
                      [Button.url('🌱 Beni Gruba Ekle', f'https://t.me/{USERNAME}?startgroup=a')],
                      [Button.url('📣 Support', f'https://t.me/{support}'),
                       Button.url('👨🏻‍💻 Sahibim', f'https://t.me/{sahib}')]
                    ),
                    link_preview=False)

# gece kusu
@client.on(events.callbackquery.CallbackQuery(data="komutlar"))
async def handler(event):
    await event.edit(f"{komutlar}", buttons=(
                      [
                      Button.inline("◀️ Geri", data="start")
                      ]
                    ),
                    link_preview=False)

# 5 li etiketleme modulü
@client.on(events.NewMessage(pattern="^/utag ?(.*)"))
async def mentionall(event):
  global gece_tag
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajları göremiyorum! (bu mesaj beni gruba eklemeden önce yazılmış)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Etiketleme mesajı yazmadın!__")
  else:
    return await event.respond("__Etiketleme için bir mesajı yanıtlayın veya bir mesaj yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Üye etiketleme başladı\n⏱️ İnterval - 2 saniye",
                    buttons=(
                      [
                      Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    gece_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"➢ [{usr.first_name}](tg://user?id={usr.id})\n "
      if event.chat_id not in gece_tag:
        await event.respond("⛔ Üye etiketleme işlemi durduruldu",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# admin etiketleme modülü
@client.on(events.NewMessage(pattern="^/atag ?(.*)"))
async def mentionalladmin(event):
  global gece_tag
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajları göremiyorum! (bu mesaj beni gruba eklemeden önce yazılmış)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Etiketleme mesajı yazmadın!__")
  else:
    return await event.respond("__Etiketleme için bir mesajı yanıtlayın veya bir mesaj yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Admin etiketleme başladı\n⏱️ İnterval - 2 saniye",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    gece_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in gece_tag:
        await event.respond("⛔ Admin etiketleme işlemi durduruldu",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# tek tek etiketleme modülü
@client.on(events.NewMessage(pattern="^/tektag ?(.*)"))
async def tektag(event):
  global gece_tag
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajları göremiyorum! (bu mesaj beni gruba eklemeden önce yazılmış)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Etiketleme mesajı yazmadın!__")
  else:
    return await event.respond("__Etiketleme için bir mesajı yanıtlayın veya bir mesaj yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Tek-tek etiketleme başladı\n⏱️ İnterval - 2 saniye",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    gece_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in gece_tag:
        await event.respond("⛔ Teker teker etiketleme işlemi durduruldu",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# Emoji ile etiketleme modülü

anlik_calisan = []

tekli_calisan = []




emoji = " ❤️ 🧡 💛 💚 💙 💜 🖤 🤍 🤎 🙂 🙃 😉 😌 😍 🥰 😘 😗 😙 😚 😋 😛 😝 😜 🤪 🤨 🧐 🤓 😎 🤩 🥳 😏 😒 " \
        "😞 😔 😟 😕 🙁 😣 😖 😫 😩 🥺 😢 😭 😤 😠 😡  🤯 😳 🥵 🥶 😱 😨 😰 😥 😓 🤗 🤔 🤭 🤫 🤥 😶 😐 😑 😬 🙄 " \
        "😯 😦 😧 😮 😲 🥱 😴 🤤 😪 😵 🤐 🥴 🤢 🤮 🤧 😷 🤒 🤕 🤑 🤠 😈 👿 👹 👺 🤡  👻 💀 👽 👾 🤖 🎃 😺 😸 😹 " \
        "😻 😼 😽 🙀 😿 😾 ❄️ 🌺 🌨 🌩 ⛈ 🌧 ☁️ ☀️ 🌈 🌪 ✨ 🌟 ☃️ 🪐 🌏 🌙 🌔 🌚 🌝 🕊 🦩 🦦 🌱 🌿 ☘ 🍂 🌹 🥀 🌾 " \
        "🌦 🍃 🎋".split(" ")

@client.on(events.NewMessage(pattern="^/etag ?(.*)"))
async def etag(event):
  global gece_tag
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajları göremiyorum! (bu mesaj beni gruba eklemeden önce yazılmış)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Etiketleme mesajı yazmadın!__")
  else:
    return await event.respond("__Etiketleme için bir mesajı yanıtlayın veya bir mesaj yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Emoji ile etiketleme başladı\n⏱️ İnterval - 2 saniye",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    gece_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id}) "
      if event.chat_id not in gece_tag:
        await event.respond("⛔ Emoji ile etiketleme işlemi durduruldu",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    

#########################

# söz ile etiketleme modülü

soz = (
'𝐾𝑎𝑙𝑏𝑖 𝑔ü𝑧𝑒𝑙 𝑜𝑙𝑎𝑛ı𝑛 𝑔ö𝑧ü𝑛𝑑𝑒𝑛 𝑦𝑎ş 𝑒𝑘𝑠𝑖𝑘 𝑜𝑙𝑚𝑎𝑧𝑚ış', 
'İ𝑦𝑖𝑦𝑖𝑚 𝑑𝑒𝑠𝑒𝑚 𝑖𝑛𝑎𝑛𝑎𝑐𝑎𝑘 𝑜 𝑘𝑎𝑑𝑎𝑟 ℎ𝑎𝑏𝑒𝑟𝑠𝑖𝑧 𝑏𝑒𝑛𝑑𝑒𝑛', 
'𝑀𝑒𝑠𝑎𝑓𝑒𝑙𝑒𝑟 𝑈𝑚𝑟𝑢𝑚𝑑𝑎 𝐷𝑒ğ𝑖𝑙, İç𝑖𝑚𝑑𝑒 𝐸𝑛 𝐺ü𝑧𝑒𝑙 𝑌𝑒𝑟𝑑𝑒𝑠𝑖𝑛',
'𝐵𝑖𝑟 𝑀𝑢𝑐𝑖𝑧𝑒𝑦𝑒 İℎ𝑡𝑖𝑦𝑎𝑐ı𝑚 𝑉𝑎𝑟𝑑ı 𝐻𝑎𝑦𝑎𝑡 𝑆𝑒𝑛𝑖 𝐾𝑎𝑟şı𝑚𝑎 Çı𝑘𝑎𝑟𝑑ı', 
'Ö𝑦𝑙𝑒 𝑔ü𝑧𝑒𝑙 𝑏𝑎𝑘𝑡ı 𝑘𝑖 𝑘𝑎𝑙𝑏𝑖 𝑑𝑒 𝑔ü𝑙üşü𝑛 𝑘𝑎𝑑𝑎𝑟 𝑔ü𝑧𝑒𝑙 𝑠𝑎𝑛𝑚ış𝑡ı𝑚', 
'𝐻𝑎𝑦𝑎𝑡 𝑛𝑒 𝑔𝑖𝑑𝑒𝑛𝑖 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟 𝑛𝑒 𝑑𝑒 𝑘𝑎𝑦𝑏𝑒𝑡𝑡𝑖ğ𝑖𝑛 𝑧𝑎𝑚𝑎𝑛ı 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟', 
'𝑆𝑒𝑣𝑚𝑒𝑘 𝑖ç𝑖𝑛 𝑠𝑒𝑏𝑒𝑝 𝑎𝑟𝑎𝑚𝑎𝑑ı𝑚 ℎ𝑖ç 𝑠𝑒𝑠𝑖 𝑦𝑒𝑡𝑡𝑖 𝑘𝑎𝑙𝑏𝑖𝑚𝑒', 
'𝑀𝑢𝑡𝑙𝑢𝑦𝑢𝑚 𝑎𝑚𝑎 𝑠𝑎𝑑𝑒𝑐𝑒 𝑠𝑒𝑛𝑙𝑒', 
'𝐵𝑒𝑛 ℎ𝑒𝑝 𝑠𝑒𝑣𝑖𝑙𝑚𝑒𝑘 𝑖𝑠𝑡𝑒𝑑𝑖ğ𝑖𝑚 𝑔𝑖𝑏𝑖 𝑠𝑒𝑣𝑖𝑛𝑑𝑖𝑚', 
'𝐵𝑖𝑟𝑖 𝑣𝑎𝑟 𝑛𝑒 ö𝑧𝑙𝑒𝑚𝑒𝑘𝑡𝑒𝑛 𝑦𝑜𝑟𝑢𝑙𝑑𝑢𝑚 𝑛𝑒 𝑠𝑒𝑣𝑚𝑒𝑘𝑡𝑒𝑛', 
'Ç𝑜𝑘 𝑧𝑜𝑟 𝑏𝑒 𝑠𝑒𝑛𝑖 𝑠𝑒𝑣𝑚𝑒𝑦𝑒𝑛 𝑏𝑖𝑟𝑖𝑛𝑒 𝑎şı𝑘 𝑜𝑙𝑚𝑎𝑘', 
'Ç𝑜𝑘 ö𝑛𝑒𝑚𝑠𝑒𝑑𝑖𝑘 𝑖ş𝑒 𝑦𝑎𝑟𝑎𝑚𝑎𝑑ı 𝑎𝑟𝑡ı𝑘 𝑏𝑜ş𝑣𝑒𝑟𝑖𝑦𝑜𝑟𝑢𝑧', 
'𝐻𝑒𝑟𝑘𝑒𝑠𝑖𝑛 𝑏𝑖𝑟 𝑔𝑒ç𝑚𝑖ş𝑖 𝑣𝑎𝑟, 𝐵𝑖𝑟𝑑𝑒 𝑣𝑎𝑧𝑔𝑒ç𝑚𝑖ş𝑖', 
'𝐴şı𝑘 𝑜𝑙𝑚𝑎𝑘 𝑔ü𝑧𝑒𝑙 𝑏𝑖𝑟 ş𝑒𝑦 𝑎𝑚𝑎 𝑠𝑎𝑑𝑒𝑐𝑒 𝑠𝑎𝑛𝑎', 
'𝐴𝑛𝑙𝑎𝑦𝑎𝑛 𝑦𝑜𝑘𝑡𝑢, 𝑆𝑢𝑠𝑚𝑎𝑦ı 𝑡𝑒𝑟𝑐𝑖ℎ 𝑒𝑡𝑡𝑖𝑚', 
'𝑆𝑒𝑛 ç𝑜𝑘 𝑠𝑒𝑣 𝑑𝑒 𝑏ı𝑟𝑎𝑘ı𝑝 𝑔𝑖𝑑𝑒𝑛 𝑦𝑎𝑟 𝑢𝑡𝑎𝑛𝑠ı𝑛', 
'𝑂 𝑔𝑖𝑡𝑡𝑖𝑘𝑡𝑒𝑛 𝑠𝑜𝑛𝑟𝑎 𝑔𝑒𝑐𝑒𝑚 𝑔ü𝑛𝑑ü𝑧𝑒 ℎ𝑎𝑠𝑟𝑒𝑡 𝑘𝑎𝑙𝑑ı', 
'𝐻𝑒𝑟 ş𝑒𝑦𝑖𝑛 𝑏𝑖𝑡𝑡𝑖ğ𝑖 𝑦𝑒𝑟𝑑𝑒 𝑏𝑒𝑛𝑑𝑒 𝑏𝑖𝑡𝑡𝑖𝑚 𝑑𝑒ğ𝑖ş𝑡𝑖𝑛 𝑑𝑖𝑦𝑒𝑛𝑙𝑒𝑟𝑖𝑛 𝑒𝑠𝑖𝑟𝑖𝑦𝑖𝑚', 
'𝐺ü𝑣𝑒𝑛𝑚𝑒𝑘 𝑠𝑒𝑣𝑚𝑒𝑘𝑡𝑒𝑛 𝑑𝑎ℎ𝑎 𝑑𝑒ğ𝑒𝑟𝑙𝑖, 𝑍𝑎𝑚𝑎𝑛𝑙𝑎 𝑎𝑛𝑙𝑎𝑟𝑠ı𝑛', 
'İ𝑛𝑠𝑎𝑛 𝑏𝑎𝑧𝑒𝑛 𝑏ü𝑦ü𝑘 ℎ𝑎𝑦𝑒𝑙𝑙𝑒𝑟𝑖𝑛𝑖 𝑘üçü𝑘 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟𝑙𝑎 𝑧𝑖𝑦𝑎𝑛 𝑒𝑑𝑒𝑟', 
'𝐾𝑖𝑚𝑠𝑒 𝑘𝑖𝑚𝑠𝑒𝑦𝑖 𝑘𝑎𝑦𝑏𝑒𝑡𝑚𝑒𝑧 𝑔𝑖𝑑𝑒𝑛 𝑏𝑎ş𝑘𝑎𝑠ı𝑛ı 𝑏𝑢𝑙𝑢𝑟, 𝑘𝑎𝑙𝑎𝑛 𝑘𝑒𝑛𝑑𝑖𝑛𝑖', 
'𝐺üç𝑙ü 𝑔ö𝑟ü𝑛𝑒𝑏𝑖𝑙𝑖𝑟𝑖𝑚 𝑎𝑚𝑎 𝑖𝑛𝑎𝑛 𝑏𝑎𝑛𝑎 𝑦𝑜𝑟𝑔𝑢𝑛𝑢𝑚', 
'Ö𝑚𝑟ü𝑛ü𝑧ü 𝑠𝑢𝑠𝑡𝑢𝑘𝑙𝑎𝑟ı𝑛ı𝑧ı 𝑑𝑢𝑦𝑎𝑛  𝑏𝑖𝑟𝑖𝑦𝑙𝑒 𝑔𝑒ç𝑖𝑟𝑖𝑛', 
'𝐻𝑎𝑦𝑎𝑡 𝑖𝑙𝑒𝑟𝑖𝑦𝑒 𝑏𝑎𝑘ı𝑙𝑎𝑟𝑎𝑘 𝑦𝑎ş𝑎𝑛ı𝑟 𝑔𝑒𝑟𝑖𝑦𝑒 𝑏𝑎𝑘𝑎𝑟𝑎𝑘 𝑎𝑛𝑙𝑎şı𝑙ı𝑟', 
'𝐴𝑟𝑡ı𝑘 ℎ𝑖ç𝑏𝑖𝑟 ş𝑒𝑦 𝑒𝑠𝑘𝑖𝑠𝑖 𝑔𝑖𝑏𝑖 𝑑𝑒ğ𝑖𝑙 𝐵𝑢𝑛𝑎 𝑏𝑒𝑛𝑑𝑒 𝑑𝑎ℎ𝑖𝑙𝑖𝑚', 
'𝐾ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛𝑒 𝑔ö𝑛ü𝑙𝑑𝑒 𝑣𝑒𝑟𝑖𝑙𝑖𝑟 ö𝑚ü𝑟𝑑𝑒', 
'𝐵𝑖𝑟 ç𝑖ç𝑒𝑘𝑙𝑒 𝑔ü𝑙𝑒𝑟 𝑘𝑎𝑑ı𝑛 𝑏𝑖𝑟 𝑙𝑎𝑓𝑙𝑎 ℎü𝑧ü𝑛', 
'𝑈𝑠𝑙ü𝑝 𝑘𝑎𝑟𝑎𝑘𝑡𝑒𝑟𝑖𝑑𝑖𝑟 𝑖𝑛𝑠𝑎𝑛ı𝑛', 
'𝐻𝑒𝑟 ş𝑒𝑦𝑖 𝑏𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑖𝑙 𝑘ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟 𝑜𝑙𝑠𝑢𝑛 ℎ𝑎𝑦𝑎𝑡ı𝑛ı𝑧𝑑𝑎', 
'𝑀𝑒𝑠𝑎𝑓𝑒 𝑖𝑦𝑖𝑑𝑖𝑟 𝑁𝑒 ℎ𝑎𝑑𝑑𝑖𝑛𝑖 𝑎ş𝑎𝑛 𝑜𝑙𝑢𝑟 𝑛𝑒 𝑑𝑒 𝑐𝑎𝑛ı𝑛ı 𝑠ı𝑘𝑎𝑛', 
'𝑌ü𝑟𝑒ğ𝑖𝑚𝑖𝑛 𝑡𝑎𝑚 𝑜𝑟𝑡𝑎𝑠ı𝑛𝑑𝑎 𝑏ü𝑦ü𝑘 𝑏𝑖𝑟 𝑦𝑜𝑟𝑔𝑢𝑛𝑙𝑢𝑘 𝑣𝑎𝑟', 
'𝑉𝑒𝑟𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑒𝑟𝑖𝑛 𝑛𝑎𝑛𝑘ö𝑟ü 𝑜𝑙𝑚𝑎𝑦ı𝑛 𝑔𝑒𝑟𝑖𝑠𝑖 ℎ𝑎𝑙𝑙𝑜𝑙𝑢𝑟', 
'𝐻𝑒𝑚 𝑔üç𝑙ü 𝑜𝑙𝑢𝑝 ℎ𝑒𝑚 ℎ𝑎𝑠𝑠𝑎𝑠 𝑘𝑎𝑙𝑝𝑙𝑖 𝑏𝑖𝑟𝑖 𝑜𝑙𝑚𝑎𝑘 ç𝑜𝑘 𝑧𝑜𝑟', 
'𝑀𝑢ℎ𝑡𝑎ç 𝑘𝑎𝑙ı𝑛 𝑦ü𝑟𝑒ğ𝑖 𝑔ü𝑧𝑒𝑙 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟𝑎', 
'İ𝑛𝑠𝑎𝑛 𝑎𝑛𝑙𝑎𝑑ığı 𝑣𝑒 𝑎𝑛𝑙𝑎şı𝑙𝑑ığı 𝑖𝑛𝑠𝑎𝑛𝑑𝑎 ç𝑖ç𝑒𝑘 𝑎ç𝑎𝑟', 
'İ𝑠𝑡𝑒𝑦𝑒𝑛 𝑑𝑎ğ𝑙𝑎𝑟ı 𝑎ş𝑎𝑟 𝑖𝑠𝑡𝑒𝑚𝑒𝑦𝑒𝑛 𝑡ü𝑚𝑠𝑒ğ𝑖 𝑏𝑖𝑙𝑒 𝑔𝑒ç𝑒𝑚𝑒𝑧', 
'İ𝑛ş𝑎𝑙𝑙𝑎ℎ 𝑠𝑎𝑏ı𝑟𝑙𝑎 𝑏𝑒𝑘𝑙𝑒𝑑𝑖ğ𝑖𝑛 ş𝑒𝑦 𝑖ç𝑖𝑛 ℎ𝑎𝑦ı𝑟𝑙ı 𝑏𝑖𝑟 ℎ𝑎𝑏𝑒𝑟 𝑎𝑙ı𝑟𝑠ı𝑛', 
'İ𝑦𝑖 𝑜𝑙𝑎𝑛 𝑘𝑎𝑦𝑏𝑒𝑡𝑠𝑒 𝑑𝑒 𝑘𝑎𝑧𝑎𝑛ı𝑟', 
'𝐺ö𝑛𝑙ü𝑛ü𝑧𝑒 𝑎𝑙𝑑ığı𝑛ı𝑧 𝑔ö𝑛𝑙ü𝑛ü𝑧ü 𝑎𝑙𝑚𝑎𝑦ı 𝑏𝑖𝑙𝑠𝑖𝑛', 
'𝑌𝑖𝑛𝑒 𝑦ı𝑟𝑡ı𝑘 𝑐𝑒𝑏𝑖𝑚𝑒 𝑘𝑜𝑦𝑚𝑢ş𝑢𝑚 𝑢𝑚𝑢𝑑𝑢', 
'Ö𝑙𝑚𝑒𝑘 𝐵𝑖 ş𝑒𝑦 𝑑𝑒ğ𝑖𝑙 𝑦𝑎ş𝑎𝑚𝑎𝑚𝑎𝑘 𝑘𝑜𝑟𝑘𝑢𝑛ç', 
'𝑁𝑒 𝑖ç𝑖𝑚𝑑𝑒𝑘𝑖 𝑠𝑜𝑘𝑎𝑘𝑙𝑎𝑟𝑎 𝑠ığ𝑎𝑏𝑖𝑙𝑑𝑖𝑚 𝑁𝑒 𝑑𝑒 𝑑ış𝑎𝑟ı𝑑𝑎𝑘𝑖 𝑑ü𝑛𝑦𝑎𝑦𝑎', 
'İ𝑛𝑠𝑎𝑛 𝑠𝑒𝑣𝑖𝑙𝑚𝑒𝑘𝑡𝑒𝑛 ç𝑜𝑘 𝑎𝑛𝑙𝑎şı𝑙𝑚𝑎𝑦ı 𝑖𝑠𝑡𝑖𝑦𝑜𝑟𝑑𝑢 𝑏𝑒𝑙𝑘𝑖 𝑑𝑒', 
'𝐸𝑘𝑚𝑒𝑘 𝑝𝑎ℎ𝑎𝑙ı 𝑒𝑚𝑒𝑘 𝑢𝑐𝑢𝑧𝑑𝑢', 
'𝑆𝑎𝑣𝑎ş𝑚𝑎𝑦ı 𝑏ı𝑟𝑎𝑘ı𝑦𝑜𝑟𝑢𝑚 𝑏𝑢𝑛𝑢 𝑣𝑒𝑑𝑎 𝑠𝑎𝑦'
'Herkes zamanda yolculuk yapıyor aslında. Anılarıyla geçmişe, hayalleriyle geleceğe'
'Kаn ve kemik tüm insаnlаrdа bulunur. Fаrklı olаn yürek ve niyettir.'
'Yаrаtıcı olun birаz, аmа аbаrtmаyın. Kаşаrı mаdаm, züppeyi аdаm yаpmаyа çаlışmаyın.'
'İnanmıyorum kalbimin attığına! Sensizlikten kendini sağa sola çarpıyor sadece.'
'Bir insаn istediğini yаpаr аmа istediğini isteyemez.'
'Gerçeklere bir gözünü kapatarak bakan; burnunun ucundan fazlasını göremez!'
'Ne oldu? Hoşça kalamadın değil mi?'
'İyi yаşаmаk için kısа bir süre, yeterince uzundur.'
'Değer verince değişmeyen insanlar istiyorum.'
'Sen, seni seveni görmeyecek kаdаr körsen, seven de seni sevmeyecek kаdаr onurludur.'
'Mutluluğun iki ucundan tutuyoruz sanki lades oynar gibi. Sen beni bu oyunda asla yenemezsin. Çünkü hep aklımdasın.'
'Bazen diyorum kendime. Ne çok değer vermişim değersizlere.'
'Bir ip koptuğundа yeniden bаğlаnаbilir, аmа аslа eskisi gibi çekmez.'
'Dokunur işte Kalemin ucu kağıda, kağıtta yazılanların ucu da bana'
'Bir düşü gerçekleştirme olasılığı yaşamı ilginçleştiriyor.'
'Bu bir tabiat kanunuydu: Kuvvetliler zayıfları eziyordu.'
'Güç insanı bozar. Ve mutlak güç insanı mutlaka bozar.'
'Gölde daire şeklinde yayılan her dalga er geç etkisini kaybederdi.'
'Her şey hüküm sürmekle ilgiliyse, bırakın isyan hüküm sürsün.'
'Çünkü hayat ne geriye gider ne de geçmişle ilgiklenir'
'Aldığım nefesten bile daha çok ihtiyaç duyuyordum ona.'
'Acaba ölsem beni daha mı çok severler belki?'
'Önüne gelenle değil, seninle ölüme gelenle beraber ol.'
'İnsan mı egosunu, egosu mu insanı kullanır?'
'İnsan olabilmek için erkek olmanın yeteceğini sanıp aldanmıştı.'
'Kimi iyi tanıyorum dediysem sonrasında hep daha iyi tanımam gerekti.'
'İnsan ömrü, unutmanın şerbetine yiyecek kadar muhtaç.'
'Yaprakların düşerken attıkları çığlıkları duydum.'
'Her toplum, kadına verdiği değere oranla gelişir ya da ilkelleşir.'
'Dostlarından kuşkulanmak, başa geçenlere özgü bir hastalıktır.'
'Kibir tamamen sona erdiğinde alçakgönüllülük başlar.'
'Kadınlar da her şey tenlerinin altına işler'
'Camus bir ideoloji adına yaratılan şiddete karşıydı'
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?'
'Yerimizi boşaltsak da dünyaya yeni geleceklere yer açsak'
'Bazen insanlardan çok hikâyeleri etkiler sizi.'
'Rüzgarla gelen babam, yine rüzgarla gitmişti.'
'Gemi kullanmayı öğrenmek için fırtınalardan korkmam.'
'Bazen insanlardan çok hikâyeleri etkiler sizi.'
'Sıfırı sıfırla bin kez de çarpsanız yine sıfır elde edersiniz! Sıfır üzeri sonsuz hariç.'
'O günden sonra bildiğimi unuttum, unutarak yeniden bildim.'
'İtfaiye ile ateş arasında tarafsız kalamam.'
'Bu şehirde öyle yerler var ki, benim için adeta yasaklı bölgeler.'
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir.'
'Ulan bu canım memlekette ya kudura kudura ölecez ya da delire delire!'
'Bana öyle geliyor ki sen de beni seviyorsun, ya da bana öyle geliyor.'
'Aşk, ölümsüz olmak istediğin bir savaş meydanı. Bir Cihan Kafes.'
'@Samilbots gururla selamlıyor'
'Şuan okuduğun bu mesajı @Samilben yazdı'
'Aşkın tarifini yaşayarak yazarsın sadece.'
'Bazen vicdani yargı, idamdan daha ağır bedeller ödetebilirdi insana'
'Buz kadar lekesiz, kar kadar temiz olsan bile, iftiradan kurtulamazsın'
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum'
'Kibir tamamen sona erdiğinde alçakgönüllülük başlar'
'Kadınlar da her şey tenlerinin altına işler'
'Camus bir ideoloji adına yaratılan şiddete karşıydı'
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?'
'Yerimizi boşaltsak da dünyaya yeni geleceklere yer açsak'
'Bazen insanlardan çok hikâyeleri etkiler sizi'
'Rüzgarla gelen babam, yine rüzgarla gitmişti'
'Gemi kullanmayı öğrenmek için fırtınalardan korkmam'
'Bazen insanlardan çok hikâyeleri etkiler sizi'
'Sıfırı sıfırla bin kez de çarpsanız yine sıfır elde edersiniz! Sıfır üzeri sonsuz hariç'
'O günden sonra bildiğimi unuttum, unutarak yeniden bildim'
'İtfaiye ile ateş arasında tarafsız kalamam'
'Bu şehirde öyle yerler var ki, benim için adeta yasaklı bölgeler'
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir'
'Ulan bu canım memlekette ya kudura kudura ölecez ya da delire delire!'
'Bana öyle geliyor ki sen de beni seviyorsun, ya da bana öyle geliyor'
'Aşk, ölümsüz olmak istediğin bir savaş meydanı. Bir Cihan Kafes'
'Bazen vicdani yargı, idamdan daha ağır bedeller ödetebilirdi insana'
'Buz kadar lekesiz, kar kadar temiz olsan bile, iftiradan kurtulamazsın'
'İ𝑠𝑡𝑒𝑦𝑒𝑛 𝑑𝑎ğ𝑙𝑎𝑟ı 𝑎ş𝑎𝑟 𝑖𝑠𝑡𝑒𝑚𝑒𝑦𝑒𝑛 𝑡ü𝑚𝑠𝑒ğ𝑖 𝑏𝑖𝑙𝑒 𝑔𝑒ç𝑒𝑚𝑒𝑧'
'Derin düşünceler, derin sessizlik gerektirir'
'Gelecek ne zaman vaat olmaktan çıkıp bir tehdit unsuru haline geldi?'
'Birkaç gün sonra her şey bitti. Yaşamaya hükümlüydüm. Yasamaya!'
'Kitaplar yaşadıkça geçmiş diye bir şey olmayacaktır'
'𝐺ö𝑛𝑙ü𝑛ü𝑧𝑒 𝑎𝑙𝑑ığı𝑛ı𝑧 𝑔ö𝑛𝑙ü𝑛ü𝑧ü 𝑎𝑙𝑚𝑎𝑦ı 𝑏𝑖𝑙𝑠𝑖𝑛'
'İmkansız olanı yapamasam da, elimden geleni yapacağım'
'Yazmak unutmaktır. Edebiyat dünyayı hiçe saymanın en uygun yoludur'
'Aşk, mert işidir. Mertliğin de kadını erkeği yoktur'
'İ𝑛𝑠𝑎𝑛 𝑎𝑛𝑙𝑎𝑑ığı 𝑣𝑒 𝑎𝑛𝑙𝑎şı𝑙𝑑ığı 𝑖𝑛𝑠𝑎𝑛𝑑𝑎 ç𝑖ç𝑒𝑘 𝑎ç𝑎𝑟'
'İlk aşkımızı asla unutmayız. Benimkinin sonu öldürülmek oldu'
'Hayattan çıkarı olmayanların, ölümden de çıkarı olmayacaktır'
'Annemiz, ışınları artık ısıtmayan örtülü bir güneş gibiydi'
'𝑌ü𝑟𝑒ğ𝑖𝑚𝑖𝑛 𝑡𝑎𝑚 𝑜𝑟𝑡𝑎𝑠ı𝑛𝑑𝑎 𝑏ü𝑦ü𝑘 𝑏𝑖𝑟 𝑦𝑜𝑟𝑔𝑢𝑛𝑙𝑢𝑘 𝑣𝑎𝑟'
'𝐵𝑖𝑟𝑖 𝑣𝑎𝑟 𝑛𝑒 ö𝑧𝑙𝑒𝑚𝑒𝑘𝑡𝑒𝑛 𝑦𝑜𝑟𝑢𝑙𝑑𝑢𝑚 𝑛𝑒 𝑠𝑒𝑣𝑚𝑒𝑘𝑡𝑒𝑛'
'Her işin bir vakti vardır. Vakti geçince o işten hayır beklenemez'
'Hayır, rüzgarın dilinde her mevsim aynı şarkı yoktur'
'Kalbimiz bir hazinedir, onu birden boşaltınız, mahvolmuş olursunuz'
'De bana, her şeye sahip birine gönderilecek en isabetli hediye nedir?'
'Tüm kaosta bir kozmos ve tüm düzensizlikte gizli bir düzen vardır'
'Nefret ettikleriniz bile gittiğinde içinizde bir boşluk bırakırlar'
'Amaç aşk uğruna ölmek değil, uğruna ölünecek aşkı bulmaktır'
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?'
'Hayatının değeri uzun yaşanmasında değil, iyi yaşanmasındadır'
'Senden ayrılınca anımsadım dünyanın bu kadar kalabalık olduğunu'
'İnsanlar iyi giyimli. Ama içlerinde soluk yok. Soluk yok'
'Düşüncelerimizde ne barındırırsak deneyimlerimizde onu yaşarız'
'Görüntü onu görüyor, buna karşın o, görüntüyü görmüyordu'
'Derin düşünceler, derin sessizlik gerektirir'
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum'
'𝑂 𝑔𝑖𝑡𝑡𝑖𝑘𝑡𝑒𝑛 𝑠𝑜𝑛𝑟𝑎 𝑔𝑒𝑐𝑒𝑚 𝑔ü𝑛𝑑ü𝑧𝑒 ℎ𝑎𝑠𝑟𝑒𝑡 𝑘𝑎𝑙𝑑ı'
'Sevilen nesne kem gözlerden sakınılmalıdır'
'Eğer sonsuzluk bitimsizse, her şeyin sonu bile onu yıkamayacaktır'
'Benim güzel çocukluğumu ahmak bir ayak ezdi'
'Fakat yüreğimdeki gizli yaralar vücudumdakilerden çok daha derindi'
'Bir de vatan denen bir şey vardı ki, çok iyi korunması gerekiyordu'
'Merhamet yararsız olduğu zaman insan merhametten yorulur'
'Dostumuz bilge olamayacak kadar kurnaz biridir'
'Kaybolmuş bir ruhum var. Yorgun ama artık umutlu o umut sensin Kayla'
'Duygularım sevgi değil , sevgiden daha özel'
'Mutlu olmaya uğraşmaktan bir vazgeçsek çok iyi vakit geçireceğiz'
'Bu bir tabiat kanunuydu: Kuvvetliler zayıfları eziyordu'
'Ama asla anlayamadım olup biteni. Anlaşılır şey de değildi zaten'
'Namazda gözü olmayanın kulağı ezanda olmaz'
'Üşüyorum, ama sen anılarla sarma beni ve anlat yalnızlığımızı'
'İki güçlü savaşçı vardır, bunlar sabır ve zamandır'
'Sahibine yetişecek hecelerin yoksa, vurursun sükutunu kör bir geceye'
'Rüzgarla gelen babam, yine rüzgarla gitmişti'
'𝐻𝑎𝑦𝑎𝑡 𝑛𝑒 𝑔𝑖𝑑𝑒𝑛𝑖 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟 𝑛𝑒 𝑑𝑒 𝑘𝑎𝑦𝑏𝑒𝑡𝑡𝑖ğ𝑖𝑛 𝑧𝑎𝑚𝑎𝑛ı 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟'
'Hayat güzel olabilir. Uğrunda mücadele etmeye değebilir'
'Dünya boşunalığa gebe kalmış ve zulmü doğurmuştur'
'Eğer sonsuzluk bitimsizse, her şeyin sonu bile onu yıkamayacaktır'
'Neden gençliğimde kitap okumadım? diye kendime kızdım'
'Yerimizi boşaltsak da dünyaya yeni geleceklere yer açsak'
'Dikkat ettin mi, bugünlerde insanlar birbirlerini nasıl incitiyorlar'
'Hayattan pek çok şey öğrenen insanlar, neşeli ve masum kalamazlar'
'Aldığım nefesten bile daha çok ihtiyaç duyuyordum ona'
"Bir bavula her şey sığmadıkça gitmek hiçbir zaman kolay olmayacak'
'İnsanın hayatı kendi eseridir. Herkes kendi hayatının mimarıdır'
'Seni öldürmeyen şey, başladığı işi bitirmek için geri döner'
'Rüzgarla gelen babam, yine rüzgarla gitmişt'
'Kusursuz bir insan ararsan, dört dörtlük bir yalnızlık yaşarsın'
'Her şeyi hem olduğu gibi, hem de olması gerektiği gibi görmelisin'
'Düşüncelerimizde ne barındırırsak deneyimlerimizde onu yaşarız'
'Görüntü onu görüyor, buna karşın o, görüntüyü görmüyordu'
'Derin düşünceler, derin sessizlik gerektirir'
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum'
'𝑂 𝑔𝑖𝑡𝑡𝑖𝑘𝑡𝑒𝑛 𝑠𝑜𝑛𝑟𝑎 𝑔𝑒𝑐𝑒𝑚 𝑔ü𝑛𝑑ü𝑧𝑒 ℎ𝑎𝑠𝑟𝑒𝑡 𝑘𝑎𝑙𝑑ı'
'Sevilen nesne kem gözlerden sakınılmalıdır'
'Eğer sonsuzluk bitimsizse, her şeyin sonu bile onu yıkamayacaktır'
'Benim güzel çocukluğumu ahmak bir ayak ezdi'
'Fakat yüreğimdeki gizli yaralar vücudumdakilerden çok daha derindi'
'Bir de vatan denen bir şey vardı ki, çok iyi korunması gerekiyordu'
'Merhamet yararsız olduğu zaman insan merhametten yorulur'
'Dostumuz bilge olamayacak kadar kurnaz biridir'
'Kaybolmuş bir ruhum var. Yorgun ama artık umutlu o umut sensin Kayla'
'Duygularım sevgi değil , sevgiden daha özel'
'Mutlu olmaya uğraşmaktan bir vazgeçsek çok iyi vakit geçireceğiz'
'Bu bir tabiat kanunuydu: Kuvvetliler zayıfları eziyordu'
'Ama asla anlayamadım olup biteni. Anlaşılır şey de değildi zaten'
'Namazda gözü olmayanın kulağı ezanda olmaz'
'Üşüyorum, ama sen anılarla sarma beni ve anlat yalnızlığımızı'
'İki güçlü savaşçı vardır, bunlar sabır ve zamandır'
'Sahibine yetişecek hecelerin yoksa, vurursun sükutunu kör bir geceye'
'Rüzgarla gelen babam, yine rüzgarla gitmişti'
'𝐻𝑎𝑦𝑎𝑡 𝑛𝑒 𝑔𝑖𝑑𝑒𝑛𝑖 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟 𝑛𝑒 𝑑𝑒 𝑘𝑎𝑦𝑏𝑒𝑡𝑡𝑖ğ𝑖𝑛 𝑧𝑎𝑚𝑎𝑛ı 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟'
'Hayat güzel olabilir. Uğrunda mücadele etmeye değebilir'
'Dünya boşunalığa gebe kalmış ve zulmü doğurmuştur'
'Eğer sonsuzluk bitimsizse, her şeyin sonu bile onu yıkamayacaktır'
'Neden gençliğimde kitap okumadım? diye kendime kızdım'
'Yerimizi boşaltsak da dünyaya yeni geleceklere yer açsak'
'Dikkat ettin mi, bugünlerde insanlar birbirlerini nasıl incitiyorlar'
'Hayattan pek çok şey öğrenen insanlar, neşeli ve masum kalamazlar'
'Aldığım nefesten bile daha çok ihtiyaç duyuyordum ona'
'Bir bavula her şey sığmadıkça gitmek hiçbir zaman kolay olmayacak'
'İnsanın hayatı kendi eseridir. Herkes kendi hayatının mimarıdır'
'Seni öldürmeyen şey, başladığı işi bitirmek için geri döner'
'Rüzgarla gelen babam, yine rüzgarla gitmişti'
'Kusursuz bir insan ararsan, dört dörtlük bir yalnızlık yaşarsın'
'Her şeyi hem olduğu gibi, hem de olması gerektiği gibi görmelisin'
'İnsan mezardan dönemez ama hatadan dönebilir'
'Erkeğin eşini öldürdüğü tek hayvan türü insandır'
'Egemenlik gerçekten milletin olduğunda hükümetlere gerek kalmayacak'
'Bize bir kaç deli gerek, şu akıllıların yol açtığı duruma bak'
'İki soylu kavga edince fakirin kulübesi yanar'
'Birkaç gün sonra her şey bitti. Yaşamaya hükümlüydüm. Yasamaya!'
'Uygarlıklar, en yukarıdaki en aşağıdakini unuttuğunda çöküyor'
'İ𝑠𝑡𝑒𝑦𝑒𝑛 𝑑𝑎ğ𝑙𝑎𝑟ı 𝑎ş𝑎𝑟 𝑖𝑠𝑡𝑒𝑚𝑒𝑦𝑒𝑛 𝑡ü𝑚𝑠𝑒ğ𝑖 𝑏𝑖𝑙𝑒 𝑔𝑒ç𝑒𝑚𝑒𝑧'
'Sarayın bahçesindeki maymunlar gibiydi zihni. Daldan dala atlıyordu'
'Müona göre zaman, Dünya'daki bize göre daha yavaş akıyor olmalı'
'Hırs, tırnakları çıkarır ama ayaklara da taş bağlar'
'Hiçbir şey yapmadan geçen hayat, ölümdür'
'Üşüyorum, ama sen anılarla sarma beni ve anlat yalnızlığımızı'
'Kelimeler olmadan yaşadıkları için mi hayvanlar daha az korkuyor ?'
'Marifet tadı alarak yaşamakta. Bazen akıllı, bazen deli'
'𝐵𝑖𝑟 𝑀𝑢𝑐𝑖𝑧𝑒𝑦𝑒 İℎ𝑡𝑖𝑦𝑎𝑐ı𝑚 𝑉𝑎𝑟𝑑ı 𝐻𝑎𝑦𝑎𝑡 𝑆𝑒𝑛𝑖 𝐾𝑎𝑟şı𝑚𝑎 Çı𝑘𝑎𝑟𝑑ı'
'Keşke gerçek hayat resimlerdeki kadar mükemmel olsaydı'
'Çünkü hayat ne geriye gider ne de geçmişle ilgiklenir'
'Mezardakilerin pişman oldukları şeyler için diriler birbirini yiyor'
'Güzel nimetleri mahvetti insan, kader deyip şimdi geçti köşesine'
'Kabul etmesi çok zordu ama yıllar çok çabuk geçiyordu'
'Öfkenin başlangıcı çılgınlık, sonu pişmanlıktır'
'Önüne gelenle değil, seninle ölüme gelenle beraber ol'
'Kendi yaralarını iyileştirmezsen, herkesin bıçağı keskin kalır'
'Keşke gerçek hayat resimlerdeki kadar mükemmel olsaydı'
'İ𝑛𝑠𝑎𝑛 𝑏𝑎𝑧𝑒𝑛 𝑏ü𝑦ü𝑘 ℎ𝑎𝑦𝑒𝑙𝑙𝑒𝑟𝑖𝑛𝑖 𝑘üçü𝑘 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟𝑙𝑎 𝑧𝑖𝑦𝑎𝑛 𝑒𝑑𝑒𝑟'
'İyi iştah vicdanın rahatlığına işarettir'
'Belki de bu evren, yüce bir ruhun gölgesidir'
'Yerinde duran, geriye gidiyor demektir İleri, daima ileri!'
'𝐻𝑒𝑟𝑘𝑒𝑠𝑖𝑛 𝑏𝑖𝑟 𝑔𝑒ç𝑚𝑖ş𝑖 𝑣𝑎𝑟, 𝐵𝑖𝑟𝑑𝑒 𝑣𝑎𝑧𝑔𝑒ç𝑚𝑖ş𝑖''
'Tarihin öyle bir devrindeyiz ki iktisadi dava belki en sonda geliyor'
'İnsan aslında sahip olduklarının bilincinde olmayan bir kapitalist'
'Ortalıkta horultudan geçilmiyordu. İçleri rahat uyumayanlar horlar'
'Hayatımda bana ait olmayan bir zaman yaşamaya başladım'
'Erkek sevdiği zaman arzu yoktur; arzuladığı zaman ise, aşk yoktur.'
'Neden gençliğimde kitap okumadım? diye kendime kızdım'
'Ama işte hayat böyle: Ne fazla şikayetçi ol, ne de fazla beklentili'
'Ulan bu canım memlekette ya kudura kudura ölecez ya da delire delire!'
'Yalnızlığa dayanabilen insan yeryüzünün en kuvvetli insanıdır'
'Zekâ; fikirlerle uğraşırken, akıl; sistemli düşünceye yönelir!'
'İ𝑠𝑡𝑒𝑦𝑒𝑛 𝑑𝑎ğ𝑙𝑎𝑟ı 𝑎ş𝑎𝑟 𝑖𝑠𝑡𝑒𝑚𝑒𝑦𝑒𝑛 𝑡ü𝑚𝑠𝑒ğ𝑖 𝑏𝑖𝑙𝑒 𝑔𝑒ç𝑒𝑚𝑒𝑧'
'Hayır, rüzgarın dilinde her mevsim aynı şarkı yoktur'
'Bedenim iyileşebileceği, ama ruhumun yaraları asla iyileşmeyecekti'
'Biz buğdayı evcilleşirmedik, buğday bizi evcilleştirdi'
'Hayattan pek çok şey öğrenen insanlar, neşeli ve masum kalamazlar'
'𝑌𝑖𝑛𝑒 𝑦ı𝑟𝑡ı𝑘 𝑐𝑒𝑏𝑖𝑚𝑒 𝑘𝑜𝑦𝑚𝑢ş𝑢𝑚 𝑢𝑚𝑢𝑑𝑢'
'Erkek sevdiği zaman arzu yoktur; arzuladığı zaman ise, aşk yoktur'
'Hayatımda bana ait olmayan bir zaman yaşamaya başladım'
'İnsan eliyle ölümler artık bana katlanılmaz geliyordu'
'𝐵𝑒𝑛 ℎ𝑒𝑝 𝑠𝑒𝑣𝑖𝑙𝑚𝑒𝑘 𝑖𝑠𝑡𝑒𝑑𝑖ğ𝑖𝑚 𝑔𝑖𝑏𝑖 𝑠𝑒𝑣𝑖𝑛𝑑𝑖𝑚''
'Egemenlik gerçekten milletin olduğunda hükümetlere gerek kalmayacak'
'Hayatın da kendini anlatmak için her zaman garip yöntemleri vardır'
'Hayvan hakları daha büyük kafesler değil boş kafesler talep eder'
'Güzel nimetleri mahvetti insan, kader deyip şimdi geçti köşesine'
'Öğrenmeye en fazla ihtiyaç duyduğunuz şeyi en iyi öğretirsiniz'
'Dorukta yalnız kalmaktan ve doruktan başlamak ne kadar zormuş meğer'
'Doğru yoldan giden topal, yoldan sapan çabuk yürüyüşlüyü geçer'
'Regan'ın adam olacağı zaten daha küçücük bir çocukken belliydi'
'Ne kadar derine yuvarlanırsan, o kadar yükseğe uçarsın'
'Yalnız olduğunu en çok,'yalnız değilsin' dediklerinde hissedersin'
'Çünkü hayat ne geriye gider ne de geçmişle ilgiklenir'
'Bir devleti kurmak için bin yıl ister, yıkmak için bir saat yeter'
'Korkularınızdan saklanmak onları yok etmezdi'
'𝐵𝑒𝑛 ℎ𝑒𝑝 𝑠𝑒𝑣𝑖𝑙𝑚𝑒𝑘 𝑖𝑠𝑡𝑒𝑑𝑖ğ𝑖𝑚 𝑔𝑖𝑏𝑖 𝑠𝑒𝑣𝑖𝑛𝑑𝑖𝑚'
'Görüntü onu görüyor, buna karşın o, görüntüyü görmüyordu'
'𝐵𝑖𝑟 ç𝑖ç𝑒𝑘𝑙𝑒 𝑔ü𝑙𝑒𝑟 𝑘𝑎𝑑ı𝑛 𝑏𝑖𝑟 𝑙𝑎𝑓𝑙𝑎 ℎü𝑧ü𝑛'
'Ö𝑙𝑚𝑒𝑘 𝐵𝑖 ş𝑒𝑦 𝑑𝑒ğ𝑖𝑙 𝑦𝑎ş𝑎𝑚𝑎𝑚𝑎𝑘 𝑘𝑜𝑟𝑘𝑢𝑛ç'
'Acıyla yaşamanın mümkün olduğunu sen herkesten daha iyi bilirsin'
'Ve o gün öyle bir gittin ki, ben o günden sonra kendimi hissetmedim'
'Söylesene; beni kaybedecek kadar kimi, neyi kazanmak için gidiyordun?'
'Şaşarım seven insan nasıl uyur? Aşıka her türlü uyku haramdır'
'Radyasyondan çok birbirlerinin kalplerini kırmaktan ölüyor insanlar'
'Sefaletin son derecesindeki insan az bir şeyle kendini zengin görür'
'Rüzgarla gelen babam, yine rüzgarla gitmişti'
'Yukarıdan bakmak, yukarı bakmaktan kolaydır'
'Dünya boşunalığa gebe kalmış ve zulmü doğurmuştur'
'𝑀𝑒𝑠𝑎𝑓𝑒 𝑖𝑦𝑖𝑑𝑖𝑟 𝑁𝑒 ℎ𝑎𝑑𝑑𝑖𝑛𝑖 𝑎ş𝑎𝑛 𝑜𝑙𝑢𝑟 𝑛𝑒 𝑑𝑒 𝑐𝑎𝑛ı𝑛ı 𝑠ı𝑘𝑎𝑛'
'Verdiğin bütün acılara dayanabiliyorsam , seni özlediğim içindir'
'Tay at olunca at dinlenir, çocuk adam olunca ata dinlenir'
'Kitap, müzik, meditasyon ve arkadaş, ruhumuza en iyi gelen tedavidir'
'Bugün yaşadıkların, düne kadar ilmek ilmek dokudukların aslında'
'Erdem eken onu sık sık sulamayı unutmamalı'
'İyi de, kör olmak ölmek değil ki, Evet ama ölmek kör olmak demek'
'Düşünce değerli bir şeydi, sonuçlar veren bir şeydi'
'İ𝑛𝑠𝑎𝑛 𝑎𝑛𝑙𝑎𝑑ığı 𝑣𝑒 𝑎𝑛𝑙𝑎şı𝑙𝑑ığı 𝑖𝑛𝑠𝑎𝑛𝑑𝑎 ç𝑖ç𝑒𝑘 𝑎ç𝑎𝑟'
'Kabul etmesi çok zordu ama yıllar çok çabuk geçiyordu'
'Fakat yüreğimdeki gizli yaralar vücudumdakilerden çok daha derindi'
'Aşk, yaşamı; cinayet, ölümü sıradanlıktan kurtarır'
'Çünkü hayat ne geriye gider ne de geçmişle ilgiklenir'
'Kendi yaralarını iyileştirmezsen, herkesin bıçağı keskin kalır'
'Ey kutsal gece! Sen de bizden haz alır mısın?'
'𝐵𝑖𝑟 𝑀𝑢𝑐𝑖𝑧𝑒𝑦𝑒 İℎ𝑡𝑖𝑦𝑎𝑐ı𝑚 𝑉𝑎𝑟𝑑ı 𝐻𝑎𝑦𝑎𝑡 𝑆𝑒𝑛𝑖 𝐾𝑎𝑟şı𝑚𝑎 Çı𝑘𝑎𝑟𝑑ı'
'Her işin bir vakti vardır. Vakti geçince o işten hayır beklenemez'
'Kıskancın suskunluğu çok gürültülüdür'
'Yaprakların düşerken attıkları çığlıkları duydum'
'Kitap, müzik, meditasyon ve arkadaş, ruhumuza en iyi gelen tedavidir'
'Erkeğin eşini öldürdüğü tek hayvan türü insandır'
'Ama işte hayat böyle: Ne fazla şikayetçi ol, ne de fazla beklentili'
'Dünya boşunalığa gebe kalmış ve zulmü doğurmuştur'
'Değişmeniz için önemli bir şeylerin risk altında olması gerekir'
'Hangi sevdanın yuvasından atılmış leylek yavrusuydum'
'İşte bağırıyorum. Ve beni duyan gene benim'
'Çok canım sıkılıyor, kuş vuralım istersen'
'Ortalıkta horultudan geçilmiyordu. İçleri rahat uyumayanlar horlar'
'𝐵𝑖𝑟 ç𝑖ç𝑒𝑘𝑙𝑒 𝑔ü𝑙𝑒𝑟 𝑘𝑎𝑑ı𝑛 𝑏𝑖𝑟 𝑙𝑎𝑓𝑙𝑎 ℎü𝑧ü𝑛'
'Ey kutsal gece! Sen de bizden haz alır mısın?'
'Yıllar uçup gider ama kalp aynı yerde kalır'
'Kibir tamamen sona erdiğinde alçakgönüllülük başlar'
'Sahibine yetişecek hecelerin yoksa, vurursun sükutunu kör bir geceye'
'Olay şu: günün sonunda aynada hala kendi yüzüne bakman gerekiyor'
'Öğrenmeye en fazla ihtiyaç duyduğunuz şeyi en iyi öğretirsiniz'
'Hayatının değeri uzun yaşanmasında değil, iyi yaşanmasındadır'
'Derin düşünceler, derin sessizlik gerektirir'
'Dorukta yalnız kalmaktan ve doruktan başlamak ne kadar zormuş meğer'
'Amaç aşk uğruna ölmek değil, uğruna ölünecek aşkı bulmaktır'
'Sevilen nesne kem gözlerden sakınılmalıdır'
'İnsan, can sıkıcı bir saç demetidir, ben de akılsız bir robotum'
'Tarihin öyle bir devrindeyiz ki iktisadi dava belki en sonda geliyor'
'Demek insanlar alçalınca, vahşi hayvandan daha tehlikeli olabiliyor'
'Derin düşünceler, derin sessizlik gerektirir'
'Tüm kaosta bir kozmos ve tüm düzensizlikte gizli bir düzen vardır'
'Hayır, Jamie. Ben daha zenginim. Sana sahibim'
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum'
'Buz kadar lekesiz, kar kadar temiz olsan bile, iftiradan kurtulamazsın'
'Seni öldürmeyen şey, başladığı işi bitirmek için geri döner'
'Günlerin bir akşamının olması, nasıl da acımasızdı!'
'Ölüm hayatın sonu değil , bir aşamasıdır'
'Belki de bu evren, yüce bir ruhun gölgesidir'
'Güzel nimetleri mahvetti insan, kader deyip şimdi geçti köşesine'
'Her birimiz geçici olmanın tutkuyla karışık acıklı itirafıyız'
'Kaybedecek hiç bir şeyi olmayanların bomboş gözleriyle bakıyorsun'
'Hayatımda bana ait olmayan bir zaman yaşamaya başladım'
'Kendine gel Osmancık, biz intikam peşinde değil, devlet peşindeyiz'
'Gözler yaşarmadıkça gönüllerde gökkuşağı oluşmaz'
'Gözlerindeki yumuşamadan anlıyordum ki, becerebilseydi gülümserdi'
'Yüreklerin çarpmadığı yerlerde de yaprakların düşmesi gerekir'
'Hem bir şey bilmez, hem de her şeye karışır, fikir beyân edersin'
'Ama işte hayat böyle: Ne fazla şikayetçi ol, ne de fazla beklentili'
'Şaşırmayınız, bu toplum zamanı kullanma özürlüdür'
'İnsan gurura kapılmamalıdır, aciz ve zavallı olduğunu bilmelidir'
'Korkularınızdan saklanmak onları yok etmezdi'
'Mucizeler bir kere başladı mı bitmek bilmez!'
'Ama işte hayat böyle: Ne fazla şikayetçi ol, ne de fazla beklentili'
'Sevilen nesne kem gözlerden sakınılmalıdır'
'Erdem eken onu sık sık sulamayı unutmamalı'
'İnsan güzel bir kitap okuduğu yerden nasıl ayrılabilir?'
'İnsanı olgunlaştıran yaşı değil, yaşadıklarıdır'
'Bana hakaret ederek kendi kusurlarını örtebileceğini mi sanıyorsun?'
'Ç𝑜𝑘 𝑧𝑜𝑟 𝑏𝑒 𝑠𝑒𝑛𝑖 𝑠𝑒𝑣𝑚𝑒𝑦𝑒𝑛 𝑏𝑖𝑟𝑖𝑛𝑒 𝑎şı𝑘 𝑜𝑙𝑚𝑎𝑘'
'Bakın etrafa hep maziden şikayet ediyoruz, hepimiz onunla meşgulüz'
'Bir kadının hayatta aldığı en büyük risk'
'Senin herkesten beklediğin muamele, herkesin de beklediği muameledir'
'Radyasyondan çok birbirlerinin kalplerini kırmaktan ölüyor insanlar'
'İ𝑠𝑡𝑒𝑦𝑒𝑛 𝑑𝑎ğ𝑙𝑎𝑟ı 𝑎ş𝑎𝑟 𝑖𝑠𝑡𝑒𝑚𝑒𝑦𝑒𝑛 𝑡ü𝑚𝑠𝑒ğ𝑖 𝑏𝑖𝑙𝑒 𝑔𝑒ç𝑒𝑚𝑒𝑧'
'Onurlu bir adam, susuzluğunu giderdiği kuyuya taş atmaz'
'Herkes bir şeyler bekler, ama bir ananın beklediği okşanmaktır hep'
'İnsan ömrü, unutmanın şerbetine yiyecek kadar muhtaç'
'Kalıbına yakışanı arar durursan. Kalbine yakışanı zor bulursun!''
'Karşılaştığı olayları ikiye ayırıyordu'
'Belki de gerçek, iki çocuk arasındaki en kısa doğrudur'
'İnsanın sevdiği bir ev olunca, kendisine mahsus bir hayatı da olur'
'Bazen insanın kaderi, başkalarının kaderi üzerinden yazılıyordu'
'Duygularım sevgi değil , sevgiden daha özel'
'Hayatımda bana ait olmayan bir zaman yaşamaya başladım'
'Senin var olduğunu bilmek yaşamaya devam etmemin sebebiydi'
'Hem bir şey bilmez, hem de her şeye karışır, fikir beyân edersin'
'Hangisi daha kötü: Sevmeden sevişmek mi yoksa sevişmeden sevmek mi?'
'𝐻𝑒𝑟 ş𝑒𝑦𝑖𝑛 𝑏𝑖𝑡𝑡𝑖ğ𝑖 𝑦𝑒𝑟𝑑𝑒 𝑏𝑒𝑛𝑑𝑒 𝑏𝑖𝑡𝑡𝑖𝑚 𝑑𝑒ğ𝑖ş𝑡𝑖𝑛 𝑑𝑖𝑦𝑒𝑛𝑙𝑒𝑟𝑖𝑛 𝑒𝑠𝑖𝑟𝑖𝑦𝑖𝑚'
'İ𝑛𝑠𝑎𝑛 𝑎𝑛𝑙𝑎𝑑ığı 𝑣𝑒 𝑎𝑛𝑙𝑎şı𝑙𝑑ığı 𝑖𝑛𝑠𝑎𝑛𝑑𝑎 ç𝑖ç𝑒𝑘 𝑎ç𝑎𝑟''
'Seni öldürmeyen şey, başladığı işi bitirmek için geri döner'
'Başarısızlık, başarmamış olmak demektir. Gerçekten öyle'
'𝑉𝑒𝑟𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑒𝑟𝑖𝑛 𝑛𝑎𝑛𝑘ö𝑟ü 𝑜𝑙𝑚𝑎𝑦ı𝑛 𝑔𝑒𝑟𝑖𝑠𝑖 ℎ𝑎𝑙𝑙𝑜𝑙𝑢𝑟''
'İnsan eliyle ölümler artık bana katlanılmaz geliyordu'
'İlk aşkımızı asla unutmayız. Benimkinin sonu öldürülmek oldu'
'Biz mi İZ'in peşinden koşarız yoksa İZ mi bizi kovalar?'
'Aşk, ölümsüz olmak istediğin bir savaş meydanı. Bir Cihan Kafes'
'Terbiyenin sırrı, çocuğa saygı ile başlar'
'𝐾𝑖𝑚𝑠𝑒 𝑘𝑖𝑚𝑠𝑒𝑦𝑖 𝑘𝑎𝑦𝑏𝑒𝑡𝑚𝑒𝑧 𝑔𝑖𝑑𝑒𝑛 𝑏𝑎ş𝑘𝑎𝑠ı𝑛ı 𝑏𝑢𝑙𝑢𝑟, 𝑘𝑎𝑙𝑎𝑛 𝑘𝑒𝑛𝑑𝑖𝑛𝑖'
'Şiirin amacı, bizi şiir haline sokmasıdır'
'Açlık insanı öldüren, partileri yaşatan bir olaydır'
'Gözlerimi yaklaşan sonuma dikip huzur içinde yaşıyorum'
'Neden gençliğimde kitap okumadım? diye kendime kızdım'
'Terapi, biri diğerinden daha dertli iki insanın karşılaşmasıdır'
'Savaşın keskin baltası kendilerini de yıkmıştı, umutlarını da'
'Belki de bu evren, yüce bir ruhun gölgesidir'
'İnsanın sevdiği bir ev olunca, kendisine mahsus bir hayatı da olur'
'Düşüncelerimizde ne barındırırsak deneyimlerimizde onu yaşarız'
'Her toplum, kadına verdiği değere oranla gelişir ya da ilkelleşir'
'Hiçbir yere gitmiyorsun. Tam da olman gerektiğin yerdesin!'
'Karşılıksız bir aşk kadar acımasız bir kader yoktur'
'Ama sen fikirleri seviyorsun insanları değil'
'İnsan gurura kapılmamalıdır, aciz ve zavallı olduğunu bilmelidir'
'Adaletin ne olduğundan habersiz bir insan adalet üzerine ne yazabilir?'
'Arkadaş sahibi olmanın tek yolu, önce arkadaş olmaktır'
'İ𝑦𝑖 𝑜𝑙𝑎𝑛 𝑘𝑎𝑦𝑏𝑒𝑡𝑠𝑒 𝑑𝑒 𝑘𝑎𝑧𝑎𝑛ı𝑟''
'Şiir yazmanın insanı uçurumun kenarına sürükleyen bir yanı var'
'Mektuplar ruhları öpücüklerden daha çok kaynaştırır'
'Elimi şah damarıma koydum ama gülümsüyordum'
'Düşüncelerimizde ne barındırırsak deneyimlerimizde onu yaşarız'
'Merhamet yararsız olduğu zaman insan merhametten yorulur'
'Senden ayrılınca anımsadım dünyanın bu kadar kalabalık olduğunu'
'Fakat herkes bilir ki hayat, yaşanmak zahmetine değmeyen bir şeydir'
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?'
'Gözlerimi yaklaşan sonuma dikip huzur içinde yaşıyorum'
'Bazı şeyleri yarım bileceğine, bir şey bilme, daha iyi'
'Ten dikenliğinden geçmeden, can gülistanına varamazsın'
'Bir düşü gerçekleştirme olasılığı yaşamı ilginçleştiriyor'
'Biz dünyadan gider olduk kalanlara selam olsun'
'İnsan eliyle ölümler artık bana katlanılmaz geliyordu'
'Ne yazık ki aşk hayalin çocuğu, hayal kırıklığının annesidir'
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir'
'Güç insanı bozar. Ve mutlak güç insanı mutlaka bozar'
'Bir devleti kurmak için bin yıl ister, yıkmak için bir saat yeter'
'Varlığınızda kıymetinizi bilmeyenleri, yokluğunuzla terbiye edin'
'Bana hakaret ederek kendi kusurlarını örtebileceğini mi sanıyorsun?''
'Gözler yaşarmadıkça gönüllerde gökkuşağı oluşmaz'
'Regan'ın adam olacağı zaten daha küçücük bir çocukken belliydi'
'Öğrenmeye en fazla ihtiyaç duyduğunuz şeyi en iyi öğretirsiniz'
'Sen, ağaca bakmaktan ormanı göremeyen o küçük insanlardan birisi'
'Terapi, biri diğerinden daha dertli iki insanın karşılaşmasıdır'
'Ve o gün öyle bir gittin ki, ben o günden sonra kendimi hissetmedim'
'Yetenek yapabileceğini yapar, deha ise yapması gerekeni'
'Tarihin öyle bir devrindeyiz ki iktisadi dava belki en sonda geliyor'
'Belleğin seni en çok etkileyen şeyleri en derine saklar'
'Bana öyle geliyor ki sen de beni seviyorsun, ya da bana öyle geliyor'
'Gözlerindeki yumuşamadan anlıyordum ki, becerebilseydi gülümserdi'
'Bir düşü gerçekleştirme olasılığı yaşamı ilginçleştiriyor'
'Bugün yaşadıkların, düne kadar ilmek ilmek dokudukların aslında'
'Çok canım sıkılıyor, kuş vuralım istersen'
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir'
'Kadınlar da her şey tenlerinin altına işler'
'Asıl acı çekilen acı değil sevilenin çektiği acıyı bilmektir'
'Öğrenmeye en fazla ihtiyaç duyduğunuz şeyi en iyi öğretirsiniz'
'𝑀𝑒𝑠𝑎𝑓𝑒 𝑖𝑦𝑖𝑑𝑖𝑟 𝑁𝑒 ℎ𝑎𝑑𝑑𝑖𝑛𝑖 𝑎ş𝑎𝑛 𝑜𝑙𝑢𝑟 𝑛𝑒 𝑑𝑒 𝑐𝑎𝑛ı𝑛ı 𝑠ı𝑘𝑎𝑛'
'Ve insanların arasında yalnız olmaktan daha korkunç bir şey yoktur'
'Şimdi artık çok geç. Zaten her zaman çok geç olacak'
'Hayat gerçekten basit ama biz karmaşıklaştırmakta ısrar ediyoruz'
'Güzel nimetleri mahvetti insan, kader deyip şimdi geçti köşesine'
'Kimse sizi öğrenmeye zorlayamaz. Siz istediğinizde öğreneceksiniz'
'Bazı yaralar vardır ki, kapanmış olsalar bile dokununca sızlarlar'
'Birkaç gün sonra her şey bitti. Yaşamaya hükümlüydüm. Yasamaya!'
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum'
'Ö𝑚𝑟ü𝑛ü𝑧ü 𝑠𝑢𝑠𝑡𝑢𝑘𝑙𝑎𝑟ı𝑛ı𝑧ı 𝑑𝑢𝑦𝑎𝑛  𝑏𝑖𝑟𝑖𝑦𝑙𝑒 𝑔𝑒ç𝑖𝑟𝑖𝑛'
'Bir düşü gerçekleştirme olasılığı yaşamı ilginçleştiriyor'
'Hayatta fevkalade hiçbir hadise yoktur. Her şey birbirinin aynıdır'
'0 ile 100 arasındaki 10 saniyelik süre bitti'
'Gözler yalan söylemez derler, şimdi gözlerime yalan söyleteceğim'
'Dorukta yalnız kalmaktan ve doruktan başlamak ne kadar zormuş meğer'
'En hüzünlü kuşlar bile şakıyacak bir mevsim bulurlar'
'Ben cılız bir suymuşum da sen başına buyruk akmayı severmişsin'
'𝐴𝑛𝑙𝑎𝑦𝑎𝑛 𝑦𝑜𝑘𝑡𝑢, 𝑆𝑢𝑠𝑚𝑎𝑦ı 𝑡𝑒𝑟𝑐𝑖ℎ 𝑒𝑡𝑡𝑖𝑚'
'𝑆𝑒𝑛 ç𝑜𝑘 𝑠𝑒𝑣 𝑑𝑒 𝑏ı𝑟𝑎𝑘ı𝑝 𝑔𝑖𝑑𝑒𝑛 𝑦𝑎𝑟 𝑢𝑡𝑎𝑛𝑠ı𝑛'
'Kitaplar yaşadıkça geçmiş diye bir şey olmayacaktır'
'Görmezden gelinmek, alaya alınmaktan da kötü bir histi'
'𝑌ü𝑟𝑒ğ𝑖𝑚𝑖𝑛 𝑡𝑎𝑚 𝑜𝑟𝑡𝑎𝑠ı𝑛𝑑𝑎 𝑏ü𝑦ü𝑘 𝑏𝑖𝑟 𝑦𝑜𝑟𝑔𝑢𝑛𝑙𝑢𝑘 𝑣𝑎𝑟'
'Hırs, tırnakları çıkarır ama ayaklara da taş bağlar'
'Sen onu yaralarından tanıdın, O sana yarasını açmadı'
'Fırtınaya hiç yakalanmamış bir gemi, limanda yapayalnız demektir'
'Gelmeyeceğini bile bile beklemek saflık değil, aşktır!'
'Değişmeniz için önemli bir şeylerin risk altında olması gerekir'
'Hayatının değeri uzun yaşanmasında değil, iyi yaşanmasındadır'
'Dostumuz bilge olamayacak kadar kurnaz biridir'
'Kabul etmesi çok zordu ama yıllar çok çabuk geçiyordu'
'Kimse sizi öğrenmeye zorlayamaz. Siz istediğinizde öğreneceksiniz'
'Ne kadar derine yuvarlanırsan, o kadar yükseğe uçarsın'
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir'
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir'
'Konuşmak dilin işi değil kalbin marifetidir'
'Az ümit edip çok elde etmek hayatın hakiki sırrıdır'
'𝑀𝑒𝑠𝑎𝑓𝑒 𝑖𝑦𝑖𝑑𝑖𝑟 𝑁𝑒 ℎ𝑎𝑑𝑑𝑖𝑛𝑖 𝑎ş𝑎𝑛 𝑜𝑙𝑢𝑟 𝑛𝑒 𝑑𝑒 𝑐𝑎𝑛ı𝑛ı 𝑠ı𝑘𝑎𝑛'
'İnsanların çoğunu ilgilendiren şeyler beni hiç ilgilendirmiyordu'
'Kaybolmuş bir ruhum var. Yorgun ama artık umutlu o umut sensin Kayla'
'Her şeye vakit vardır ama yapmaya değer şeyler hariç'
'İnsanların çoğunu ilgilendiren şeyler beni hiç ilgilendirmiyordu'
'Her şey hüküm sürmekle ilgiliyse, bırakın isyan hüküm sürsün'
'İ𝑛𝑠𝑎𝑛 𝑎𝑛𝑙𝑎𝑑ığı 𝑣𝑒 𝑎𝑛𝑙𝑎şı𝑙𝑑ığı 𝑖𝑛𝑠𝑎𝑛𝑑𝑎 ç𝑖ç𝑒𝑘 𝑎ç𝑎𝑟'
'Bizim tek ulu önderimiz vardır, o da YÜCE ATATÜRK'tür'
'𝐾ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛𝑒 𝑔ö𝑛ü𝑙𝑑𝑒 𝑣𝑒𝑟𝑖𝑙𝑖𝑟 ö𝑚ü𝑟𝑑𝑒'
'Anlamayacak olanlara söyleme sakın, bilebileceğin en güzel şeyleri!''
'İki güçlü savaşçı vardır, bunlar sabır ve zamandır'
'𝐾ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛𝑒 𝑔ö𝑛ü𝑙𝑑𝑒 𝑣𝑒𝑟𝑖𝑙𝑖𝑟 ö𝑚ü𝑟𝑑𝑒'
'Düşüncelerimizde ne barındırırsak deneyimlerimizde onu yaşarız'
'Yalnızdım, çünkü acı sadece tek kişilikti. Korku tek kişilikti'
'Yıllar uçup gider ama kalp aynı yerde kalır'
'Düşünce değerli bir şeydi, sonuçlar veren bir şeydi'
'Yazmak unutmaktır. Edebiyat dünyayı hiçe saymanın en uygun yoludur'
'Biz buğdayı evcilleşirmedik, buğday bizi evcilleştirdi'
'Belki de gerçek, iki çocuk arasındaki en kısa doğrudur'
'Ruhun, bedeninden daha önce ölecektir. Artık hiçbir şeyden korkma'
'Marifet tadı alarak yaşamakta. Bazen akıllı, bazen deli'
'Kalbimiz bir hazinedir, onu birden boşaltınız, mahvolmuş olursunuz'
'Doğru yoldan giden topal, yoldan sapan çabuk yürüyüşlüyü geçer'
'Açlık insanı öldüren, partileri yaşatan bir olaydır'
'𝐻𝑒𝑟 ş𝑒𝑦𝑖 𝑏𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑖𝑙 𝑘ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟 𝑜𝑙𝑠𝑢𝑛 ℎ𝑎𝑦𝑎𝑡ı𝑛ı𝑧𝑑𝑎'
'Geldiğimiz ülkelerin felaketi hiç bir umutlarının olmayışında'
'Ve daima duyarım zaman denen kanatlı arabanın arkamdan gelen sesini'
'Senin var olduğunu bilmek yaşamaya devam etmemin sebebiydi'
'Yıllar uçup gider ama kalp aynı yerde kalır'
'Başarısızlık, başarmamış olmak demektir. Gerçekten öyle'
'Yüreklerin çarpmadığı yerlerde de yaprakların düşmesi gerekir'
'Yaşam, insan zihninin icat edebileceği her şeyden kat kat tuhaftır'
'Düşünce değerli bir şeydi, sonuçlar veren bir şeydi'
'Fakat herkes bilir ki hayat, yaşanmak zahmetine değmeyen bir şeydir'
'Şiirin amacı, bizi şiir haline sokmasıdır'
'Çünkü aylaklık yeryüzünün mevsimlerine yabancılaşmak demektir'
'Düşüncelerin seni ne geleceğe ne de geçmişe taşır'
'Her birimiz geçici olmanın tutkuyla karışık acıklı itirafıyız'
'Kelimeler olmadan yaşadıkları için mi hayvanlar daha az korkuyor ?'
'Ne istedigini kendin bilmiyor musun? Nasıl dayanabiliyorsun bilmemeye?'
'Dorukta yalnız kalmaktan ve doruktan başlamak ne kadar zormuş meğer'
'Acı bazı insanların anladıkları tek dildir'
'Amaç aşk uğruna ölmek değil, uğruna ölünecek aşkı bulmaktır'
'Bazen insanlardan çok hikâyeleri etkiler sizi'
'Hasta düşünceler gibi hayaller üretiyorlar kafalarında'
'Göreceksin ki hayatın zevki değişikliktedir'
'Yüreklerin çarpmadığı yerlerde de yaprakların düşmesi gerekir'
'Gözlerindeki yumuşamadan anlıyordum ki, becerebilseydi gülümserdi'
'Hayatımda bana ait olmayan bir zaman yaşamaya başladım'
'Boş bir adamın ne olduğunu düşünmek bile insana ürküntü verir'
'Eğer sonsuzluk bitimsizse, her şeyin sonu bile onu yıkamayacaktır'
'Ölümünüz, çalamayacağınız ilk fotoğraf olacaktır'
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir'
'Kitap, müzik, meditasyon ve arkadaş, ruhumuza en iyi gelen tedavidir'
'İnsanlar iyi giyimli. Ama içlerinde soluk yok. Soluk yok'
'Konuşmak dilin işi değil kalbin marifetidir'
'Ben cılız bir suymuşum da sen başına buyruk akmayı severmişsin'
'Dokunur işte Kalemin ucu kağıda, kağıtta yazılanların ucu da bana'
'Bazı yaralar vardır ki, kapanmış olsalar bile dokununca sızlarlar'
'Dokunur işte Kalemin ucu kağıda, kağıtta yazılanların ucu da bana'
'Gitmek fiilinin altını, çift çizgiyle en güzel trenler çizermiş'
'Hayatımda bana ait olmayan bir zaman yaşamaya başladım'
'İnsanoğlu daima haddini aşma eğilimindedir, zaten hatası da budur'
'Şimdi artık çok geç. Zaten her zaman çok geç olacak'
'Bazen vicdani yargı, idamdan daha ağır bedeller ödetebilirdi insana'
'Millet, bayram ve kandillerde tarihini, geçmiş ve geleceğini yaşar'
'𝐸𝑘𝑚𝑒𝑘 𝑝𝑎ℎ𝑎𝑙ı 𝑒𝑚𝑒𝑘 𝑢𝑐𝑢𝑧𝑑𝑢'
'Ama asla anlayamadım olup biteni. Anlaşılır şey de değildi zaten'
'Ve o gün öyle bir gittin ki, ben o günden sonra kendimi hissetmedim'
'Uyumak, ölmeye yatmak demekti Sarıkamış' ta'
'Birisinin zengin olması için diğerinin fakirleşmesine gerek yoktur'
'Uygarlıklar, en yukarıdaki en aşağıdakini unuttuğunda çöküyor'
'İnsan mezardan dönemez ama hatadan dönebilir'
'Hayır, Jamie. Ben daha zenginim. Sana sahibim'
'İtip beni, balıma dadanan bu çağı sevmedim'
'𝑀𝑒𝑠𝑎𝑓𝑒 𝑖𝑦𝑖𝑑𝑖𝑟 𝑁𝑒 ℎ𝑎𝑑𝑑𝑖𝑛𝑖 𝑎ş𝑎𝑛 𝑜𝑙𝑢𝑟 𝑛𝑒 𝑑𝑒 𝑐𝑎𝑛ı𝑛ı 𝑠ı𝑘𝑎𝑛'
'Ne kadar derine yuvarlanırsan, o kadar yükseğe uçarsın'
'Ben tuttum birini sevdim, hayatı nasıl sevdiysem onu da öyle sevdim'
'Sevmeyi öğreneceksiniz, dinlemeyi öğrendiğiniz zaman'
'Aşk, dört nala giden at gibidir, ne dizginden anlar, ne söz dinler'
'Dünyanın en yoksul insanı, paradan başka hiçbir şeyi olmayandır'
'Olay şu: günün sonunda aynada hala kendi yüzüne bakman gerekiyor'
'Görüntü onu görüyor, buna karşın o, görüntüyü görmüyordu'
'İ𝑛𝑠𝑎𝑛 𝑏𝑎𝑧𝑒𝑛 𝑏ü𝑦ü𝑘 ℎ𝑎𝑦𝑒𝑙𝑙𝑒𝑟𝑖𝑛𝑖 𝑘üçü𝑘 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟𝑙𝑎 𝑧𝑖𝑦𝑎𝑛 𝑒𝑑𝑒𝑟'
'Yaşamak bir denge meselesi. Birine aşırı bağlanmak dengesizliktir'
'Aslına bakılırsa kim kaderini elinde tutabiliyor ki tam anlamıyla?''
'Tay at olunca at dinlenir, çocuk adam olunca ata dinlenir'
'Aşırı kızgınlığın verdiği bir sakinlik içindeydi'
'Tüm kaosta bir kozmos ve tüm düzensizlikte gizli bir düzen vardır'
'Kabul etmesi çok zordu ama yıllar çok çabuk geçiyordu'
'Namazda gözü olmayanın kulağı ezanda olmaz'
'Burası bizim değil, bizi öldürmek isteyenlerin ülkesi!'
'Adalet ancak gerçekten, saadet ancak adaletten doğabilir'
'Dikkat ettin mi, bugünlerde insanlar birbirlerini nasıl incitiyorlar'
'De bana, her şeye sahip birine gönderilecek en isabetli hediye nedir?'
'𝐾𝑖𝑚𝑠𝑒 𝑘𝑖𝑚𝑠𝑒𝑦𝑖 𝑘𝑎𝑦𝑏𝑒𝑡𝑚𝑒𝑧 𝑔𝑖𝑑𝑒𝑛 𝑏𝑎ş𝑘𝑎𝑠ı𝑛ı 𝑏𝑢𝑙𝑢𝑟, 𝑘𝑎𝑙𝑎𝑛 𝑘𝑒𝑛𝑑𝑖𝑛𝑖'
'Arkadaş sahibi olmanın tek yolu, önce arkadaş olmaktır'
'Yazmak unutmaktır. Edebiyat dünyayı hiçe saymanın en uygun yoludur'
'İyi iştah vicdanın rahatlığına işarettir'
'Kendini okumayan benim alfabemi bilemez, beni de anlayamaz'
'Hayattan çıkarı olmayanların, ölümden de çıkarı olmayacaktır'
'İnsan olabilmek için erkek olmanın yeteceğini sanıp aldanmıştı'
'İnsanı olgunlaştıran yaşı değil, yaşadıklarıdır'
'Kimi iyi tanıyorum dediysem sonrasında hep daha iyi tanımam gerekti'
'Gölde daire şeklinde yayılan her dalga er geç etkisini kaybederdi'
'Duygularım sevgi değil , sevgiden daha özel'
'Gerçek değişimin kanıtlanmaya ihtiyacı yoktur Değişirsin, biter'
'Kadınlar da her şey tenlerinin altına işler'
'Her şeye vakit vardır ama yapmaya değer şeyler hariç'
'Hiçbir şey yapmadan geçen hayat, ölümdür'
'Hangi sevdanın yuvasından atılmış leylek yavrusuydum'
'Onurlu bir adam, susuzluğunu giderdiği kuyuya taş atmaz'
'Ama asla anlayamadım olup biteni. Anlaşılır şey de değildi zaten'
'Aldığım nefesten bile daha çok ihtiyaç duyuyordum ona'
'Hayvan hakları daha büyük kafesler değil boş kafesler talep eder'
'Uyumak, ölmeye yatmak demekti Sarıkamış' ta'
'Hangisi daha kötü: Sevmeden sevişmek mi yoksa sevişmeden sevmek mi?'
'Bize benzer gayeler taşıyanlar en tehlikeli düşmanlarımız oluyor'
'Sen, ağaca bakmaktan ormanı göremeyen o küçük insanlardan birisin'
'Hayallerinizdeki ağacı, siz izin vermeden kesmeye kimin gücü yeter?'
'Göreceksin ki hayatın zevki değişikliktedir'
'Geçmişin güzelliği geçmiş olmasındandır'
'𝑌ü𝑟𝑒ğ𝑖𝑚𝑖𝑛 𝑡𝑎𝑚 𝑜𝑟𝑡𝑎𝑠ı𝑛𝑑𝑎 𝑏ü𝑦ü𝑘 𝑏𝑖𝑟 𝑦𝑜𝑟𝑔𝑢𝑛𝑙𝑢𝑘 𝑣𝑎𝑟'
'Kalıbına yakışanı arar durursan. Kalbine yakışanı zor bulursun!'
'Kendini beğenmişler yalnız övgüleri dinler'
'İnsanların zamanına hükmedenin gücü sınırsız olur'
'Sevmeyi öğreneceksiniz, dinlemeyi öğrendiğiniz zaman'
'Ama işte hayat böyle: Ne fazla şikayetçi ol, ne de fazla beklentili'
'Verdiğin bütün acılara dayanabiliyorsam , seni özlediğim içindir'
'Acı bazı insanların anladıkları tek dildir'
'İnsanın kendi hayallerine para ödemesi umutsuzlukların en beteriydi'
'Her şey hüküm sürmekle ilgiliyse, bırakın isyan hüküm sürsün'
'𝐺ü𝑣𝑒𝑛𝑚𝑒𝑘 𝑠𝑒𝑣𝑚𝑒𝑘𝑡𝑒𝑛 𝑑𝑎ℎ𝑎 𝑑𝑒ğ𝑒𝑟𝑙𝑖, 𝑍𝑎𝑚𝑎𝑛𝑙𝑎 𝑎𝑛𝑙𝑎𝑟𝑠ı𝑛'
'Hayvan hakları daha büyük kafesler değil boş kafesler talep eder'
'Kalbimiz bir hazinedir, onu birden boşaltınız, mahvolmuş olursunuz'
'Günlerin bir akşamının olması, nasıl da acımasızdı!'
'İnsan ancak bir başkasının varlığıyla anlam buluyor'
'𝐸𝑘𝑚𝑒𝑘 𝑝𝑎ℎ𝑎𝑙ı 𝑒𝑚𝑒𝑘 𝑢𝑐𝑢𝑧𝑑𝑢'
'Sevmeyi öğreneceksiniz, dinlemeyi öğrendiğiniz zaman'
'Ç𝑜𝑘 ö𝑛𝑒𝑚𝑠𝑒𝑑𝑖𝑘 𝑖ş𝑒 𝑦𝑎𝑟𝑎𝑚𝑎𝑑ı 𝑎𝑟𝑡ı𝑘 𝑏𝑜ş𝑣𝑒𝑟𝑖𝑦𝑜𝑟𝑢𝑧'
'Bir düşü gerçekleştirme olasılığı yaşamı ilginçleştiriyor'
'Aşk, yaşamı; cinayet, ölümü sıradanlıktan kurtarır'
'Kalbimiz bir hazinedir, onu birden boşaltınız, mahvolmuş olursunuz'
'Sahibine yetişecek hecelerin yoksa, vurursun sükutunu kör bir geceye'
'Tay at olunca at dinlenir, çocuk adam olunca ata dinlenir'
'İmkansız şeyler kafamızın içinde olur. Çünkü hayat gerçektir'
'İnsanın sevdiği bir ev olunca, kendisine mahsus bir hayatı da olur'
'Benim güzel çocukluğumu ahmak bir ayak ezdi'
'Hayatımda bana ait olmayan bir zaman yaşamaya başladım'
'𝑆𝑒𝑣𝑚𝑒𝑘 𝑖ç𝑖𝑛 𝑠𝑒𝑏𝑒𝑝 𝑎𝑟𝑎𝑚𝑎𝑑ı𝑚 ℎ𝑖ç 𝑠𝑒𝑠𝑖 𝑦𝑒𝑡𝑡𝑖 𝑘𝑎𝑙𝑏𝑖𝑚𝑒'
'Edepli edebinden susar, edepsiz de ben susturdum zanneder'
'Boş bir adamın ne olduğunu düşünmek bile insana ürküntü verir'
'Ey kutsal gece! Sen de bizden haz alır mısın?'
'Rüzgarla gelen babam, yine rüzgarla gitmişti'
'Yalnızlığa dayanabilen insan yeryüzünün en kuvvetli insanıdır'
'Her şeyi hem olduğu gibi, hem de olması gerektiği gibi görmelisin'
'Hangi sevdanın yuvasından atılmış leylek yavrusuydum'
'Terapi, biri diğerinden daha dertli iki insanın karşılaşmasıdır'
'Gözler yaşarmadıkça gönüllerde gökkuşağı oluşmaz'
'İnsan mı egosunu, egosu mu insanı kullanır?'
'İ𝑛𝑠𝑎𝑛 𝑏𝑎𝑧𝑒𝑛 𝑏ü𝑦ü𝑘 ℎ𝑎𝑦𝑒𝑙𝑙𝑒𝑟𝑖𝑛𝑖 𝑘üçü𝑘 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟𝑙𝑎 𝑧𝑖𝑦𝑎𝑛 𝑒𝑑𝑒𝑟'
'Aşk, mert işidir. Mertliğin de kadını erkeği yoktur'
'Bir toplum ne kadar özgür olursa, güç kullanmak o kadar zorlaşır'
'İnsanlar yalnız felaketi yaşarken gerçeğe kendilerini kaptırırlar'
'Gölde daire şeklinde yayılan her dalga er geç etkisini kaybederdi'
'Nefret ettikleriniz bile gittiğinde içinizde bir boşluk bırakırlar'
'Türkçe hocasına göre, çoğul konuşanlar alçakgönüllü olurmuş'
'Her uygarlık teokrasi ile başlayıp demokrasiye ulaşır'
'Sen onu yaralarından tanıdın, O sana yarasını açmadı'
'Belden aşağısı bedenin aşkı, belden yukarısı ruhun'
'Yaprakların düşerken attıkları çığlıkları duydum'
'Hayat kendinizi bulmaya dair değildir. Daha çok çikolataya dairdir'
'Bir çocuk en çok başka bir çocuğa güvenir'
'İnsanın kendi hayallerine para ödemesi umutsuzlukların en beteriydi      '
'Yerinde duran, geriye gidiyor demektir İleri, daima ileri!'
'Arkadaş sahibi olmanın tek yolu, önce arkadaş olmaktır'
'Düşüncelerimizde ne barındırırsak deneyimlerimizde onu yaşarız'
'0 ile 100 arasındaki 10 saniyelik süre bitti'
'Efendim, mutlu olmak için mutlaka zengin mi olmak gerekir?'
'Yaşam, insan zihninin icat edebileceği her şeyden kat kat tuhaftır'
'Ah! İnsanın insandan vazgeçemediği nasıl da doğruydu'
'Kendisiyle ilgili bir olayda da adil bir yargılayıcı olabilir miydi?'
'Şimdi artık çok geç. Zaten her zaman çok geç olacak'
'Hangi sevdanın yuvasından atılmış leylek yavrusuydum'
'Hayvan hakları daha büyük kafesler değil boş kafesler talep eder'
'Kibir tamamen sona erdiğinde alçakgönüllülük başlar'
'Efendim, mutlu olmak için mutlaka zengin mi olmak gerekir?'
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?'
'Öfkenin başlangıcı çılgınlık, sonu pişmanlıktır'
'Sadece sevgi ve iyiliği anlatın, diğerlerini herkes söylüyor zaten'
"Erkek sevdiği zaman arzu yoktur; arzuladığı zaman ise, aşk yoktur."
'Cinayet işlemek, ölenleri geri getirmez, sadece ölümü yüceltirdi'
'Ona koşmak ve aynı zamanda da ondan uzaklaşmak istiyorum'
'Senin herkesten beklediğin muamele, herkesin de beklediği muameledir'
'İlk izlenim daima hayal kırıklığı yaratır'
'Dorukta yalnız kalmaktan ve doruktan başlamak ne kadar zormuş meğer'
'𝐻𝑒𝑟 ş𝑒𝑦𝑖 𝑏𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑖𝑙 𝑘ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟 𝑜𝑙𝑠𝑢𝑛 ℎ𝑎𝑦𝑎𝑡ı𝑛ı𝑧𝑑𝑎'
'Hırsızlardan en zararlısı zamanınızdan çalanlardır'
'Belki de gerçek, iki çocuk arasındaki en kısa doğrudur'
'Kibir tamamen sona erdiğinde alçakgönüllülük başlar'
'Ve daima duyarım zaman denen kanatlı arabanın arkamdan gelen sesini'
'Yaprakların düşerken attıkları çığlıkları duydum'
'𝐸𝑘𝑚𝑒𝑘 𝑝𝑎ℎ𝑎𝑙ı 𝑒𝑚𝑒𝑘 𝑢𝑐𝑢𝑧𝑑𝑢'
'Kalbimiz bir hazinedir, onu birden boşaltınız, mahvolmuş olursunuz'
'Ölüm hayatın sonu değil , bir aşamasıdır'
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum'
'Kendisiyle ilgili bir olayda da adil bir yargılayıcı olabilir miydi?'
'İnsanın adaleti araması için illa bir sebebi mi olmalı?'
'Sarayın bahçesindeki maymunlar gibiydi zihni. Daldan dala atlıyordu'
'Aslına bakılırsa kim kaderini elinde tutabiliyor ki tam anlamıyla?'
'Gitmek fiilinin altını, çift çizgiyle en güzel trenler çizermiş'
'İnsanlar yalnız felaketi yaşarken gerçeğe kendilerini kaptırırlar'
 'Aşk, mert işidir. Mertliğin de kadını erkeği yoktur'
'Şaşarım seven insan nasıl uyur? Aşıka her türlü uyku haramdır'
'Acı bazı insanların anladıkları tek dildir'
'Arkadaş sahibi olmanın tek yolu, önce arkadaş olmaktır'
'Ve daima duyarım zaman denen kanatlı arabanın arkamdan gelen sesini'
'Ve daima duyarım zaman denen kanatlı arabanın arkamdan gelen sesini'
'Hayat kendinizi bulmaya dair değildir. Daha çok çikolataya dairdir'
'Verdiğin bütün acılara dayanabiliyorsam , seni özlediğim içindir'
'𝑌𝑖𝑛𝑒 𝑦ı𝑟𝑡ı𝑘 𝑐𝑒𝑏𝑖𝑚𝑒 𝑘𝑜𝑦𝑚𝑢ş𝑢𝑚 𝑢𝑚𝑢𝑑𝑢'
'Hayat bir şey değildir, itinayla yaşayınız'
'Birkaç gün sonra her şey bitti. Yaşamaya hükümlüydüm. Yasamaya!'
'Kitaplar yaşadıkça geçmiş diye bir şey olmayacaktır'
'Burası bizim değil, bizi öldürmek isteyenlerin ülkesi!'
'Sarayın bahçesindeki maymunlar gibiydi zihni. Daldan dala atlıyordu'
'İnsanın adaleti araması için illa bir sebebi mi olmalı?'
'Gelecek ne zaman vaat olmaktan çıkıp bir tehdit unsuru haline geldi?'
'Gece açılıp gündüz kapanan bir parantezdim'
'Aslına bakılırsa kim kaderini elinde tutabiliyor ki tam anlamıyla?'
'Bedenim iyileşebileceği, ama ruhumun yaraları asla iyileşmeyecekti'
'Görmezden gelinmek, alaya alınmaktan da kötü bir histi'
'Asıl acı çekilen acı değil sevilenin çektiği acıyı bilmektir'
'Yüreklerin çarpmadığı yerlerde de yaprakların düşmesi gerekir'
'Mezardakilerin pişman oldukları şeyler için diriler birbirini yiyor'
'Bilinç yalnızca sen hiçbir yere gitmiyorken berraktır'
'Erdem eken onu sık sık sulamayı unutmamalı'
'Şiirin amacı, bizi şiir haline sokmasıdır'
'Karşılaştığı olayları ikiye ayırıyordu'
'Yaşam, insan zihninin icat edebileceği her şeyden kat kat tuhaftır'
'Ö𝑦𝑙𝑒 𝑔ü𝑧𝑒𝑙 𝑏𝑎𝑘𝑡ı 𝑘𝑖 𝑘𝑎𝑙𝑏𝑖 𝑑𝑒 𝑔ü𝑙üşü𝑛 𝑘𝑎𝑑𝑎𝑟 𝑔ü𝑧𝑒𝑙 𝑠𝑎𝑛𝑚ış𝑡ı𝑚'
'Bazen vicdani yargı, idamdan daha ağır bedeller ödetebilirdi insana'
'Yalnızlığa dayanabilen insan yeryüzünün en kuvvetli insanıdır'
'Yüreklerin çarpmadığı yerlerde de yaprakların düşmesi gerekir'
'İyi iştah vicdanın rahatlığına işarettir'
'𝐵𝑖𝑟 𝑀𝑢𝑐𝑖𝑧𝑒𝑦𝑒 İℎ𝑡𝑖𝑦𝑎𝑐ı𝑚 𝑉𝑎𝑟𝑑ı 𝐻𝑎𝑦𝑎𝑡 𝑆𝑒𝑛𝑖 𝐾𝑎𝑟şı𝑚𝑎 Çı𝑘𝑎𝑟𝑑ı'
'Dostlarından kuşkulanmak, başa geçenlere özgü bir hastalıktır'
'İnsanı anlamakla meşgulüz, üstelik görünürde hiç ipucu da yok'
'Dokunur işte Kalemin ucu kağıda, kağıtta yazılanların ucu da bana'
'Uyumak, ölmeye yatmak demekti Sarıkamış' ta'
'Ve insanların arasında yalnız olmaktan daha korkunç bir şey yoktur'
'Senin var olduğunu bilmek yaşamaya devam etmemin sebebiydi'
'𝐻𝑒𝑟 ş𝑒𝑦𝑖 𝑏𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑖𝑙 𝑘ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟 𝑜𝑙𝑠𝑢𝑛 ℎ𝑎𝑦𝑎𝑡ı𝑛ı𝑧𝑑𝑎'
'İnsanoğlu daima haddini aşma eğilimindedir, zaten hatası da budur'
'Aşk denen şey kafanda tanım değiştirince canın yanar'
'Sen onu yaralarından tanıdın, O sana yarasını açmadı'
'Terapi, biri diğerinden daha dertli iki insanın karşılaşmasıdır'
'Aşk bir çeşit zafer yürüyüşü değildir'
'Hangisi daha kötü: Sevmeden sevişmek mi yoksa sevişmeden sevmek mi?
'𝐻𝑎𝑦𝑎𝑡 𝑛𝑒 𝑔𝑖𝑑𝑒𝑛𝑖 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟 𝑛𝑒 𝑑𝑒 𝑘𝑎𝑦𝑏𝑒𝑡𝑡𝑖ğ𝑖𝑛 𝑧𝑎𝑚𝑎𝑛ı 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟''
'Müona göre zaman, Dünya'daki bize göre daha yavaş akıyor olmalı'
'İnsanların zamanına hükmedenin gücü sınırsız olur'
'Aşk bir çeşit zafer yürüyüşü değildir'
'Şimdi artık çok geç. Zaten her zaman çok geç olacak'
'Öfkenin başlangıcı çılgınlık, sonu pişmanlıktır'
'İmkansız şeyler kafamızın içinde olur. Çünkü hayat gerçektir'
'Hayatta fevkalade hiçbir hadise yoktur. Her şey birbirinin aynıdır'
'Bazen insanlardan çok hikâyeleri etkiler sizi'
'İçimdeki seni beğenmiyorsan. İçime karışma! Sen kendi içine bak'
'Adaletin ne olduğundan habersiz bir insan adalet üzerine ne yazabilir?'
'Kendini beğenmişler yalnız övgüleri dinler'
'𝐸𝑘𝑚𝑒𝑘 𝑝𝑎ℎ𝑎𝑙ı 𝑒𝑚𝑒𝑘 𝑢𝑐𝑢𝑧𝑑𝑢''
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?'
'Acaba ölsem beni daha mı çok severler belki?'
'Balıkçıyla evlenmek denizle evlenmek gibidir'
'Demek insanlar alçalınca, vahşi hayvandan daha tehlikeli olabiliyor'
'Uyumak, ölmeye yatmak demekti Sarıkamış' ta'
'İnsanın sevdiği bir ev olunca, kendisine mahsus bir hayatı da olur'
'Bazen insanlardan çok hikâyeleri etkiler sizi'
'Çağın vebası: 'mutsuz insanlar', 'mutlu fotoğraflar’
'Şaşarım seven insan nasıl uyur? Aşıka her türlü uyku haramdır'
'Beni anlasa, o da benimle aynı düşü görse!'
'İnsan, can sıkıcı bir saç demetidir, ben de akılsız bir robotum'
'Bazen vicdani yargı, idamdan daha ağır bedeller ödetebilirdi insana'
'Dostumuz bilge olamayacak kadar kurnaz biridir'
'Belki de gerçek, iki çocuk arasındaki en kısa doğrudur'
'Bu bir tabiat kanunuydu: Kuvvetliler zayıfları eziyordu'
'Savaş alanı da insanlar için en büyük ibret okuludur'
'İnsan mı egosunu, egosu mu insanı kullanır?'
'İnsan eliyle ölümler artık bana katlanılmaz geliyordu'
'İnsan gurura kapılmamalıdır, aciz ve zavallı olduğunu bilmelidir'
'𝐻𝑒𝑚 𝑔üç𝑙ü 𝑜𝑙𝑢𝑝 ℎ𝑒𝑚 ℎ𝑎𝑠𝑠𝑎𝑠 𝑘𝑎𝑙𝑝𝑙𝑖 𝑏𝑖𝑟𝑖 𝑜𝑙𝑚𝑎𝑘 ç𝑜𝑘 𝑧𝑜𝑟'
'𝐻𝑒𝑟𝑘𝑒𝑠𝑖𝑛 𝑏𝑖𝑟 𝑔𝑒ç𝑚𝑖ş𝑖 𝑣𝑎𝑟, 𝐵𝑖𝑟𝑑𝑒 𝑣𝑎𝑧𝑔𝑒ç𝑚𝑖ş𝑖'
'O günden sonra bildiğimi unuttum, unutarak yeniden bildim'
'İnsanın sevdiği bir ev olunca, kendisine mahsus bir hayatı da olur'
'Kurnazlığın, hilenin olduğu yerde küçüklük vardır'
'Çağın vebası: 'mutsuz insanlar', 'mutlu fotoğraflar’
'Bir klasiği her yeniden okuma, ilk okuma gibi bir keşif okumasıdır'
'Mutlu olmaya uğraşmaktan bir vazgeçsek çok iyi vakit geçireceğiz'
'Camus bir ideoloji adına yaratılan şiddete karşıydı'
'Aslına bakılırsa kim kaderini elinde tutabiliyor ki tam anlamıyla?'
'Hayatının değeri uzun yaşanmasında değil, iyi yaşanmasındadır'
'Güç insanı bozar. Ve mutlak güç insanı mutlaka bozar'
'Ve o gün öyle bir gittin ki, ben o günden sonra kendimi hissetmedim'
'İnsanı anlamakla meşgulüz, üstelik görünürde hiç ipucu da yok'
'Savaş alanı da insanlar için en büyük ibret okuludur'
'Kalbimiz bir hazinedir, onu birden boşaltınız, mahvolmuş olursunuz'
'Önüne gelenle değil, seninle ölüme gelenle beraber ol'
'Kendisiyle ilgili bir olayda da adil bir yargılayıcı olabilir miydi?'
'İtip beni, balıma dadanan bu çağı sevmedim'
'Verdiğin bütün acılara dayanabiliyorsam , seni özlediğim içindir'
'Mucizeler bir kere başladı mı bitmek bilmez!'
'Bu bir tabiat kanunuydu: Kuvvetliler zayıfları eziyordu'
'Her şey hüküm sürmekle ilgiliyse, bırakın isyan hüküm sürsün'
'Her işin bir vakti vardır. Vakti geçince o işten hayır beklenemez'
'İnsanın adaleti araması için illa bir sebebi mi olmalı?'
'Yüreklerin çarpmadığı yerlerde de yaprakların düşmesi gerekir'
'Aşkın arzusuna ulaşmasını engelleyen şey yine aşkın kendisiydi'
'Aşkın arzusuna ulaşmasını engelleyen şey yine aşkın kendisiydi'
'Göreceksin ki hayatın zevki değişikliktedir'
'Ten dikenliğinden geçmeden, can gülistanına varamazsın'
'Sen onu yaralarından tanıdın, O sana yarasını açmadı'
'Ö𝑦𝑙𝑒 𝑔ü𝑧𝑒𝑙 𝑏𝑎𝑘𝑡ı 𝑘𝑖 𝑘𝑎𝑙𝑏𝑖 𝑑𝑒 𝑔ü𝑙üşü𝑛 𝑘𝑎𝑑𝑎𝑟 𝑔ü𝑧𝑒𝑙 𝑠𝑎𝑛𝑚ış𝑡ı𝑚'
'Yaprakların düşerken attıkları çığlıkları duydum'
'Sefaletin son derecesindeki insan az bir şeyle kendini zengin görür'
'Aşk, ölümsüz olmak istediğin bir savaş meydanı. Bir Cihan Kafes'
'Terapi, biri diğerinden daha dertli iki insanın karşılaşmasıdır'
'Ortalıkta horultudan geçilmiyordu. İçleri rahat uyumayanlar horlar'
'Ve daima duyarım zaman denen kanatlı arabanın arkamdan gelen sesini'
'𝐴𝑟𝑡ı𝑘 ℎ𝑖ç𝑏𝑖𝑟 ş𝑒𝑦 𝑒𝑠𝑘𝑖𝑠𝑖 𝑔𝑖𝑏𝑖 𝑑𝑒ğ𝑖𝑙 𝐵𝑢𝑛𝑎 𝑏𝑒𝑛𝑑𝑒 𝑑𝑎ℎ𝑖𝑙𝑖𝑚'
'Senin herkesten beklediğin muamele, herkesin de beklediği muameledir'
'Hayattan çıkarı olmayanların, ölümden de çıkarı olmayacaktır'
'Can gövdeye yük, dünya insana mülk değildir'
'Kitaplar yaşadıkça geçmiş diye bir şey olmayacaktır'
'Camus bir ideoloji adına yaratılan şiddete karşıydı'
'𝐺üç𝑙ü 𝑔ö𝑟ü𝑛𝑒𝑏𝑖𝑙𝑖𝑟𝑖𝑚 𝑎𝑚𝑎 𝑖𝑛𝑎𝑛 𝑏𝑎𝑛𝑎 𝑦𝑜𝑟𝑔𝑢𝑛𝑢𝑚'
'Mucizeler bir kere başladı mı bitmek bilmez!'
'Kalıbına yakışanı arar durursan. Kalbine yakışanı zor bulursun!'
'Gece açılıp gündüz kapanan bir parantezdim'
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum.'
'Fırtınaya hiç yakalanmamış bir gemi, limanda yapayalnız demektir'
'Sevmeyi öğreneceksiniz, dinlemeyi öğrendiğiniz zaman'
'Müona göre zaman Dünya 'daki bize göre daha yavaş akıyor olmalı'
'Şiir yazmanın insanı uçurumun kenarına sürükleyen bir yanı var'
'Ne istedigini kendin bilmiyor musun? Nasıl dayanabiliyorsun bilmemeye?'
'Acaba ölsem beni daha mı çok severler belki'
'Güzel nimetleri mahvetti insan, kader deyip şimdi geçti köşesine'
'Tarihin öyle bir devrindeyiz ki iktisadi dava belki en sonda geliyor'
'Yalnız olduğunu en çok,'yalnız değilsin' dediklerinde hissedersin.'
'Bazen insanın kaderi, başkalarının kaderi üzerinden yazılıyordu'
'Dostlarından kuşkulanmak, başa geçenlere özgü bir hastalıktır.'
) 


@client.on(events.NewMessage(pattern="^/stag ?(.*)"))
async def stag(event):
  global gece_tag
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajları göremiyorum! (bu mesaj beni gruba eklemeden önce yazılmış)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Etiketleme mesajı yazmadın!__")
  else:
    return await event.respond("__Etiketleme için bir mesajı yanıtlayın veya bir mesaj yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Söz ile etiketleme başladı\n⏱️ İnterval - 2 saniye",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    gece_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(soz)}](tg://user?id={usr.id}) "
      if event.chat_id not in gece_tag:
        await event.respond("⛔ Söz ile etiketleme işlemi durduruldu",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    
#########################

# renk ile etiketleme modülü
renk = "🔴 🟠 🟡 🟢 🔵 🟣 🟤 ⚫ ⚪ " .split(" ") 
        

@client.on(events.NewMessage(pattern="^/rtag ?(.*)"))
async def rtag(event):
  global gece_tag
  if event.is_private:
    return await event.respond(f"{noqrup}")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond(f"{noadmin}")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Eski mesajları göremiyorum! (bu mesaj beni gruba eklemeden önce yazılmış)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Etiketleme mesajı yazmadın!__")
  else:
    return await event.respond("__Etiketleme için bir mesajı yanıtlayın veya bir mesaj yazın!__")
    
  if mode == "text_on_cmd":
    await client.send_message(event.chat_id, "❄️ Renk ile etiketleme başladı\n⏱️ İnterval - 2 saniye",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  ) 
    gece_tag.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{random.choice(renk)}](tg://user?id={usr.id}) "
      if event.chat_id not in gece_tag:
        await event.respond("⛔ Renk ile etiketleme işlemi durduruldu",
                    buttons=(
                      [
                       Button.url('📣 Support', f'https://t.me/{support}')
                      ]
                    )
                  )
        return
      if usrnum == 3:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

    
#########################


print(">> Bot çalışmaktadur merak etme 🚀 @Samilben bilgi alabilirsin <<")
client.run_until_disconnected()
run_until_disconnected()
