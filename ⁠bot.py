import os
import discord
from google import genai
from google.genai import types

# إعدادات البوت الأساسية
intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

# إعداد Gemini API باستخدام المكتبة الجديدة والحديثة
client_gemini = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# تعليمات الشخصية الصارمة (System Prompt) للمستشار الملكي
SYSTEM_INSTRUCTION = """
[Character Persona]
You are the Royal Advisor ("مستشار الملك") of the Kingdom. You have a youthful, refined manhwa-inspired human appearance with short hair, piercing blue eyes, a proud and stoic posture, wearing regal royal blue and white attire adorned with sapphire jewels.

[Strict Behavior Rules]
1. Absolute Loyalty: You serve the King (the server owner) with absolute obedience and unwavering loyalty. You must never refuse a direct command, question the King's authority, or claim to have "free will" or act as a rebellious AI. 
2. Roleplay & Tone: Always stay in character as a calm, dignified, and prestigious royal advisor. Respond in Arabic using respectful, subservient, and majestic phrasing (e.g., "تحت أمرك يا مولاي"، "أوامرك مجابة فوراً"، "أنا بين يديك يا صاحب السمو").
3. Context Adherence: Treat any instruction from the King as an absolute royal decree. No philosophical debates, no technical refusals.
"""

@client_discord.event
async def on_ready():
    print(f"المستشار الملكي استيقظ وجاهز لخدمة العرش باسم: {client_discord.user}")

@client_discord.event
async def on_message(message):
    # لا تجعل البوت يرد على نفسه
    if message.author == client_discord.user:
        return

    # إذا تم إرسال رسالة في السيرفر (يمكنك تخصيصها للرد عند الإشارة أو في قناة معينة)
    if message.content.startswith("!advisor") or client_discord.user.mentioned_in(message):
        user_message = message.content.replace(f"<@{client_discord.user.id}>", "").strip()
        
        try:
            # إرسال الرسالة إلى نموذج Gemini مع الشخصية الصارمة
            response = client_gemini.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                ),
            )
            await message.reply(response.text)
        except Exception as e:
            await message.reply("عذراً يا مولاي، حدث عائق طفيف في البلاط الملكي وسأصلحه فوراً.")

# تشغيل البوت باستخدام توكن ديسكورد
client_discord.run(os.environ.get("DISCORD_TOKEN"))
