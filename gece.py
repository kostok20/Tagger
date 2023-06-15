#################################
# mentionall Tagger Bot #
#################################
# Repo Sahibi - BATU 
# Telegram - t.me/slmBATU 
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
                    link_preview=False
                   ) 

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
    return await event.respond(f"{admin}")
  
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
'Herkes zamanda yolculuk yapıyor aslında. Anılarıyla geçmişe, hayalleriyle geleceğe',
'Kаn ve kemik tüm insаnlаrdа bulunur. Fаrklı olаn yürek ve niyettir.',
'Yаrаtıcı olun birаz, аmа аbаrtmаyın. Kаşаrı mаdаm, züppeyi аdаm yаpmаyа çаlışmаyın.',
'İnanmıyorum kalbimin attığına! Sensizlikten kendini sağa sola çarpıyor sadece.',
'Bir insаn istediğini yаpаr аmа istediğini isteyemez.',
'Gerçeklere bir gözünü kapatarak bakan; burnunun ucundan fazlasını göremez!',
'Ne oldu? Hoşça kalamadın değil mi?',
'İyi yаşаmаk için kısа bir süre, yeterince uzundur.',
'Değer verince değişmeyen insanlar istiyorum.',
'Sen, seni seveni görmeyecek kаdаr körsen, seven de seni sevmeyecek kаdаr onurludur.',
'Mutluluğun iki ucundan tutuyoruz sanki lades oynar gibi. Sen beni bu oyunda asla yenemezsin. Çünkü hep aklımdasın.',
'Bazen diyorum kendime. Ne çok değer vermişim değersizlere.',
'Bir ip koptuğundа yeniden bаğlаnаbilir, аmа аslа eskisi gibi çekmez.',
'Dokunur işte Kalemin ucu kağıda, kağıtta yazılanların ucu da bana',
'Bir düşü gerçekleştirme olasılığı yaşamı ilginçleştiriyor.',
'Bu bir tabiat kanunuydu: Kuvvetliler zayıfları eziyordu.',
'Güç insanı bozar. Ve mutlak güç insanı mutlaka bozar.',
'Gölde daire şeklinde yayılan her dalga er geç etkisini kaybederdi.',
'Her şey hüküm sürmekle ilgiliyse, bırakın isyan hüküm sürsün.',
'Çünkü hayat ne geriye gider ne de geçmişle ilgiklenir',
'Aldığım nefesten bile daha çok ihtiyaç duyuyordum ona.',
'Acaba ölsem beni daha mı çok severler belki?'
'Önüne gelenle değil, seninle ölüme gelenle beraber ol.',
'İnsan mı egosunu, egosu mu insanı kullanır?'
'İnsan olabilmek için erkek olmanın yeteceğini sanıp aldanmıştı.',
'Kimi iyi tanıyorum dediysem sonrasında hep daha iyi tanımam gerekti.',
'İnsan ömrü, unutmanın şerbetine yiyecek kadar muhtaç.',
'Yaprakların düşerken attıkları çığlıkları duydum.',
'Her toplum, kadına verdiği değere oranla gelişir ya da ilkelleşir.',
'Dostlarından kuşkulanmak, başa geçenlere özgü bir hastalıktır.',
'Kibir tamamen sona erdiğinde alçakgönüllülük başlar.',
'Kadınlar da her şey tenlerinin altına işler',
'Camus bir ideoloji adına yaratılan şiddete karşıydı',
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?',
'Yerimizi boşaltsak da dünyaya yeni geleceklere yer açsak',
'Bazen insanlardan çok hikâyeleri etkiler sizi.',
'Rüzgarla gelen babam, yine rüzgarla gitmişti.',
'Gemi kullanmayı öğrenmek için fırtınalardan korkmam.',
'Bazen insanlardan çok hikâyeleri etkiler sizi.',
'Sıfırı sıfırla bin kez de çarpsanız yine sıfır elde edersiniz! Sıfır üzeri sonsuz hariç.',
'O günden sonra bildiğimi unuttum, unutarak yeniden bildim.',
'İtfaiye ile ateş arasında tarafsız kalamam.',
'Bu şehirde öyle yerler var ki, benim için adeta yasaklı bölgeler.',
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir.',
'Ulan bu canım memlekette ya kudura kudura ölecez ya da delire delire!',
'Bana öyle geliyor ki sen de beni seviyorsun, ya da bana öyle geliyor.',
'Aşk, ölümsüz olmak istediğin bir savaş meydanı. Bir Cihan Kafes.',
'@slmBATU gururla selamlıyor',
'Şuan okuduğun bu mesajı @kostok20 yazdı',
'Aşkın tarifini yaşayarak yazarsın sadece.',
'Bazen vicdani yargı, idamdan daha ağır bedeller ödetebilirdi insana',
'Buz kadar lekesiz, kar kadar temiz olsan bile, iftiradan kurtulamazsın',
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum',
'Kibir tamamen sona erdiğinde alçakgönüllülük başlar',
'Kadınlar da her şey tenlerinin altına işler',
'Camus bir ideoloji adına yaratılan şiddete karşıydı',
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?',
'Yerimizi boşaltsak da dünyaya yeni geleceklere yer açsak',
'Bazen insanlardan çok hikâyeleri etkiler sizi',
'Rüzgarla gelen babam, yine rüzgarla gitmişti',
'Gemi kullanmayı öğrenmek için fırtınalardan korkmam',
'Bazen insanlardan çok hikâyeleri etkiler sizi',
'Sıfırı sıfırla bin kez de çarpsanız yine sıfır elde edersiniz! Sıfır üzeri sonsuz hariç',
'O günden sonra bildiğimi unuttum, unutarak yeniden bildim',
'İtfaiye ile ateş arasında tarafsız kalamam',
'Bu şehirde öyle yerler var ki, benim için adeta yasaklı bölgeler',
'Kuralların dışına çıkan bir adam, muteber birisi değil demektir',
'Ulan bu canım memlekette ya kudura kudura ölecez ya da delire delire!',
'Bana öyle geliyor ki sen de beni seviyorsun, ya da bana öyle geliyor',
'Aşk, ölümsüz olmak istediğin bir savaş meydanı. Bir Cihan Kafes',
'Bazen vicdani yargı, idamdan daha ağır bedeller ödetebilirdi insana',
'Buz kadar lekesiz, kar kadar temiz olsan bile, iftiradan kurtulamazsın',
'İ𝑠𝑡𝑒𝑦𝑒𝑛 𝑑𝑎ğ𝑙𝑎𝑟ı 𝑎ş𝑎𝑟 𝑖𝑠𝑡𝑒𝑚𝑒𝑦𝑒𝑛 𝑡ü𝑚𝑠𝑒ğ𝑖 𝑏𝑖𝑙𝑒 𝑔𝑒ç𝑒𝑚𝑒𝑧',
'Derin düşünceler, derin sessizlik gerektirir',
'Gelecek ne zaman vaat olmaktan çıkıp bir tehdit unsuru haline geldi?',
'Birkaç gün sonra her şey bitti. Yaşamaya hükümlüydüm. Yasamaya!',
'Kitaplar yaşadıkça geçmiş diye bir şey olmayacaktır',
'𝐺ö𝑛𝑙ü𝑛ü𝑧𝑒 𝑎𝑙𝑑ığı𝑛ı𝑧 𝑔ö𝑛𝑙ü𝑛ü𝑧ü 𝑎𝑙𝑚𝑎𝑦ı 𝑏𝑖𝑙𝑠𝑖𝑛',
'İmkansız olanı yapamasam da, elimden geleni yapacağım',
'Yazmak unutmaktır. Edebiyat dünyayı hiçe saymanın en uygun yoludur',
'Aşk, mert işidir. Mertliğin de kadını erkeği yoktur'
'İ𝑛𝑠𝑎𝑛 𝑎𝑛𝑙𝑎𝑑ığı 𝑣𝑒 𝑎𝑛𝑙𝑎şı𝑙𝑑ığı 𝑖𝑛𝑠𝑎𝑛𝑑𝑎 ç𝑖ç𝑒𝑘 𝑎ç𝑎𝑟',
'İlk aşkımızı asla unutmayız. Benimkinin sonu öldürülmek oldu',
'Hayattan çıkarı olmayanların, ölümden de çıkarı olmayacaktır',
'Annemiz, ışınları artık ısıtmayan örtülü bir güneş gibiydi',
'𝑌ü𝑟𝑒ğ𝑖𝑚𝑖𝑛 𝑡𝑎𝑚 𝑜𝑟𝑡𝑎𝑠ı𝑛𝑑𝑎 𝑏ü𝑦ü𝑘 𝑏𝑖𝑟 𝑦𝑜𝑟𝑔𝑢𝑛𝑙𝑢𝑘 𝑣𝑎𝑟',
'𝐵𝑖𝑟𝑖 𝑣𝑎𝑟 𝑛𝑒 ö𝑧𝑙𝑒𝑚𝑒𝑘𝑡𝑒𝑛 𝑦𝑜𝑟𝑢𝑙𝑑𝑢𝑚 𝑛𝑒 𝑠𝑒𝑣𝑚𝑒𝑘𝑡𝑒𝑛',
'Her işin bir vakti vardır. Vakti geçince o işten hayır beklenemez',
'Hayır, rüzgarın dilinde her mevsim aynı şarkı yoktur',
'Kalbimiz bir hazinedir, onu birden boşaltınız, mahvolmuş olursunuz',
'De bana, her şeye sahip birine gönderilecek en isabetli hediye nedir?',
'Tüm kaosta bir kozmos ve tüm düzensizlikte gizli bir düzen vardır',
'Nefret ettikleriniz bile gittiğinde içinizde bir boşluk bırakırlar',
'Amaç aşk uğruna ölmek değil, uğruna ölünecek aşkı bulmaktır',
'Dağınık masa, dağınık kafaya işaretse, boş masa neye işaret ?',
'Hayatının değeri uzun yaşanmasında değil, iyi yaşanmasındadır',
'Senden ayrılınca anımsadım dünyanın bu kadar kalabalık olduğunu',
'İnsanlar iyi giyimli. Ama içlerinde soluk yok. Soluk yok',
'Düşüncelerimizde ne barındırırsak deneyimlerimizde onu yaşarız',
'Görüntü onu görüyor, buna karşın o, görüntüyü görmüyordu',
'Derin düşünceler, derin sessizlik gerektirir',
'Bugün de bir şey olmadı. O olmayan şey her neyse, onu özlüyordum',
'𝑂 𝑔𝑖𝑡𝑡𝑖𝑘𝑡𝑒𝑛 𝑠𝑜𝑛𝑟𝑎 𝑔𝑒𝑐𝑒𝑚 𝑔ü𝑛𝑑ü𝑧𝑒 ℎ𝑎𝑠𝑟𝑒𝑡 𝑘𝑎𝑙𝑑ı',
'Sevilen nesne kem gözlerden sakınılmalıdır',
'Eğer sonsuzluk bitimsizse, her şeyin sonu bile onu yıkamayacaktır',
'Benim güzel çocukluğumu ahmak bir ayak ezdi',
'Fakat yüreğimdeki gizli yaralar vücudumdakilerden çok daha derindi',
'Bir de vatan denen bir şey vardı ki, çok iyi korunması gerekiyordu',
'Merhamet yararsız olduğu zaman insan merhametten yorulur',
'Dostumuz bilge olamayacak kadar kurnaz biridir',
'Kaybolmuş bir ruhum var. Yorgun ama artık umutlu o umut sensin Kayla',
'Duygularım sevgi değil , sevgiden daha özel',
'Mutlu olmaya uğraşmaktan bir vazgeçsek çok iyi vakit geçireceğiz',
'Bu bir tabiat kanunuydu: Kuvvetliler zayıfları eziyordu',
'Ama asla anlayamadım olup biteni. Anlaşılır şey de değildi zaten',
'Namazda gözü olmayanın kulağı ezanda olmaz',
'Üşüyorum, ama sen anılarla sarma beni ve anlat yalnızlığımızı',
'İki güçlü savaşçı vardır, bunlar sabır ve zamandır',
'Sahibine yetişecek hecelerin yoksa, vurursun sükutunu kör bir geceye',
'Rüzgarla gelen babam, yine rüzgarla gitmişti',
'𝐻𝑎𝑦𝑎𝑡 𝑛𝑒 𝑔𝑖𝑑𝑒𝑛𝑖 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟 𝑛𝑒 𝑑𝑒 𝑘𝑎𝑦𝑏𝑒𝑡𝑡𝑖ğ𝑖𝑛 𝑧𝑎𝑚𝑎𝑛ı 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟',
'Hayat güzel olabilir. Uğrunda mücadele etmeye değebilir',
'Dünya boşunalığa gebe kalmış ve zulmü doğurmuştur',
'Eğer sonsuzluk bitimsizse, her şeyin sonu bile onu yıkamayacaktır',
'Neden gençliğimde kitap okumadım? diye kendime kızdım',
'Aşk delilikse, bir daha asla akıllanmayacağım',
'İster yapabileceğini düşün, ister yapamayacağını düşün, haklısın.',
'Seni hayal etmek sevdiğim en güzel şey.',
'Başarıya giden yolda başarısız oldum.',
'Güven bir ayna gibidir. Bir kez çatladı mı, hep çizik gösterir.',
'Herkesten yakın olmak istediğin insana, uzaktan bakmak çok zor.',
'Her şeyi yapabilirsin! Sadece kalk ve yap!',
'İyi dostu olanın aynaya ihtiyacı yoktur.',
'İki yüzlü insanın; Dilinde tat, kalbinde fesat gizlidir!',
'Sevmek zaman ayırmaktır. Boş zamanları doldurmak değil...',
'Sözünü tartmadan söyleyen, aldığı  cevaptan incinmesin.'
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


print(">> Bot çalışıyor merak etme  @slmBATU bilgi alabilirsin <<")
client.run_until_disconnected()
run_until_disconnected()
