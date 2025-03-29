
# from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, Filters
# import json
# import os
# from datetime import datetime, timedelta

# # Database
# paid_users = {}
# registrations = {}
# feedbacks = {}
# doctor_appointments = {}

# def load_json(filename):
#     try:
#         if os.path.exists(filename):
#             with open(filename, 'r', encoding='utf-8') as f:
#                 return json.load(f)
#     except Exception as e:
#         print(f"Error loading {filename}: {e}")
#     return {}

# def save_json(filename, data):
#     try:
#         with open(filename, 'w', encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)
#     except Exception as e:
#         print(f"Error saving {filename}: {e}")

# # Load data
# paid_users = load_json('paid_users.json')
# registrations = load_json('registrations.json')
# feedbacks = load_json('feedback.json')
# doctor_appointments = load_json('doctor_appointments.json')

# ADMIN_ID = 7201258445
# CLINIC_LOCATION = (41.311081, 69.240562)
# CLINIC_PHONE = "+998908161706"
# PAYMENT_CARD = "4073420080671617"

# def generate_doctor_slots(days=7):
#     slots = {}
#     today = datetime.now().date()
    
#     for day in range(days):
#         current_date = today + timedelta(days=day)
#         date_str = current_date.strftime("%Y-%m-%d")
        
#         month = {
#             1: 'Yanvar', 2: 'Fevral', 3: 'Mart', 4: 'Aprel',
#             5: 'May', 6: 'Iyun', 7: 'Iyul', 8: 'Avgust',
#             9: 'Sentabr', 10: 'Oktabr', 11: 'Noyabr', 12: 'Dekabr'
#         }[current_date.month]
        
#         slots[date_str] = {
#             'date_display': f"{current_date.day} {month}",
#             'slots': []
#         }
        
#         for hour in range(9, 17, 2):
#             time_slot = f"{hour:02d}:00-{(hour+2):02d}:00"
#             slots[date_str]['slots'].append(time_slot)
    
#     return slots

# DOCTORS = {
#     "Terapevt": {
#         "name": "Doktor Aliev",
#         "info": "20 yillik tajriba, terapiya bo'yicha mutaxassis",
#         "price": "100,000 so'm",
#         "available_slots": generate_doctor_slots(7)
#     },
#     "Kardiolog": {
#         "name": "Doktor Rashidov",
#         "info": "Yurak kasalliklari bo'yicha yetakchi mutaxassis",
#         "price": "150,000 so'm",
#         "available_slots": generate_doctor_slots(7)
#     },
#     "Nevropatolog": {
#         "name": "Doktor Karimova",
#         "info": "Nevrologiya bo'yicha 15 yillik tajriba",
#         "price": "120,000 so'm",
#         "available_slots": generate_doctor_slots(7)
#     },
#     "Pediatr": {
#         "name": "Doktor Usmonova",
#         "info": "Bolalar salomatligi bo'yicha 10 yillik tajriba",
#         "price": "90,000 so'm",
#         "available_slots": generate_doctor_slots(7)
#     }
# }

# def is_admin(user_id):
#     return str(user_id) == str(ADMIN_ID)

# def get_main_menu(user_id):
#     menu = [
#         ["👨‍⚕️ Doktorlarimiz"],  
#         ["🏥 Klinika Haqida", "📞 Aloqa"],
#         ["📝 Fikr Bildirish", "💸 To'lov"],
#         ["📅 Qabulga Yozilish"]
#     ]
    
#     if is_admin(user_id):
#         menu.append(["🛠 Admin Paneli"])
    
#     return ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=False)

# def start(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     user = update.message.from_user
#     welcome_msg = (
#         f"🎉 *Assalomu alaykum, {user.first_name}!* 🎉\n"
#         "ShifoNur klinikasi botiga xush kelibsiz! 🌟\n\n"
#         "🔥 Sog‘ligingizni bizga ishonib topshiring:\n"
#         "👇 Quyidagi tugmalar bilan tanishib, hoziroq boshlang!"
#     )
#     update.message.reply_text(welcome_msg, parse_mode='Markdown', reply_markup=get_main_menu(user.id))

# def show_doctors(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     message = (
#         "👩‍⚕️ *Bizning Professional Doktorlarimiz* 👨‍⚕️\n\n"
#         "Siz uchun eng yaxshi mutaxassislar tayyor:\n"
#     )
#     for specialty, doctor in DOCTORS.items():
#         message += (
#             f"👤 *{doctor['name']}* - {specialty}\n"
#             f"ℹ️ {doctor['info']}\n"
#             f"💰 Narx: {doctor['price']}\n"
#             f"🕒 Dushanba-Juma, 9:00-17:00\n"
#             f"🎯 *Qabulga yozilish uchun avval to‘lov qiling!* 👇\n\n"
#         )
#     keyboard = [
#         [InlineKeyboardButton("💸 Hozir To‘lov Qilish", callback_data="pay_methods")],
#         [InlineKeyboardButton("◀️ Bosh Menyuga", callback_data="back_to_main")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

# def show_available_specialties(update: Update, context: CallbackContext):
#     user_id = str(update.message.from_user.id) if update.message else str(update.callback_query.from_user.id)
    
#     if user_id not in paid_users and not is_admin(user_id):
#         text = (
#             "⚠️ *Qabulga yozilish uchun avval to‘lov qiling!* ⚠️\n\n"
#             "👉 '💸 To‘lov' bo‘limida to‘lov qiling va chekni yuboring.\n"
#             "✅ Admin tasdiqlagach, qabulga yozilish ochiladi!"
#         )
#         if update.message:
#             update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_main_menu(user_id))
#         else:
#             update.callback_query.edit_message_text(text, parse_mode='Markdown')
#         return
    
#     keyboard = [
#         [InlineKeyboardButton(f"👩‍⚕️ {specialty}", callback_data=f"specialty_{specialty}")]
#         for specialty in DOCTORS
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     text = (
#         "📅 *Qabulga Yozilish* 📅\n\n"
#         "🎯 O‘zingizga kerakli mutaxassisni tanlang:"
#     )
    
#     if update.message:
#         update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
#     else:
#         update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# def show_specialty_info(update: Update, context: CallbackContext, specialty: str):
#     query = update.callback_query
#     query.answer()
    
#     doctor = DOCTORS[specialty]
#     keyboard = [
#         [InlineKeyboardButton("📅 Vaqt Tanlash", callback_data=f"dates_{specialty}")],
#         [InlineKeyboardButton("◀️ Bosh Menyuga", callback_data="back_to_main")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     context.bot.send_message(
#         chat_id=query.message.chat_id,
#         text=(
#             f"👤 *{doctor['name']}* - {specialty}\n"
#             f"ℹ️ {doctor['info']}\n"
#             f"💰 Narx: {doctor['price']}\n\n"
#             "🔥 Hozir qabul vaqtini tanlang:"
#         ),
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# def update_doctor_slots():
#     today = datetime.now().date()
    
#     for doctor_name, doctor in DOCTORS.items():
#         for date_str in list(doctor['available_slots'].keys()):
#             slot_date = datetime.strptime(date_str, "%Y-%m-%d").date()
#             if slot_date < today:
#                 del doctor['available_slots'][date_str]
        
#         existing_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in doctor['available_slots'].keys()]
#         latest_date = max(existing_dates) if existing_dates else today - timedelta(days=1)
        
#         for day in range(1, 8):
#             new_date = latest_date + timedelta(days=day)
#             date_str = new_date.strftime("%Y-%m-%d")
            
#             if date_str not in doctor['available_slots'] and new_date.weekday() < 5:
#                 new_slots = generate_doctor_slots(1)
#                 if date_str in new_slots:
#                     doctor['available_slots'][date_str] = new_slots[date_str]

# def show_available_dates(update: Update, context: CallbackContext, specialty: str):
#     query = update.callback_query
#     query.answer()
    
#     update_doctor_slots()
    
#     doctor = DOCTORS[specialty]
#     available_dates = sorted(doctor['available_slots'].keys())[:7]
    
#     keyboard = [
#         [InlineKeyboardButton(
#             f"📅 {doctor['available_slots'][date]['date_display']}", 
#             callback_data=f"times_{specialty}_{date}")]
#         for date in available_dates
#     ]
#     keyboard.append([InlineKeyboardButton("◀️ Orqaga", callback_data=f"specialty_{specialty}")])
    
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     query.message.reply_text(
#         f"👩‍⚕️ *{doctor['name']}*\n\n"
#         "📅 Qabul kunini tanlang:",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# def show_time_slots(update: Update, context: CallbackContext, specialty: str, date: str):
#     query = update.callback_query
#     query.answer()
    
#     doctor = DOCTORS[specialty]
#     if date not in doctor['available_slots']:
#         query.message.reply_text("❌ Bu kunda qabul yo‘q!")
#         return
    
#     time_slots = doctor['available_slots'][date]['slots']
    
#     keyboard = [
#         [InlineKeyboardButton(
#             f"⏰ {slot}", 
#             callback_data=f"confirm_{specialty}_{date}_{slot}")]
#         for slot in time_slots
#     ]
#     keyboard.append([InlineKeyboardButton("◀️ Orqaga", callback_data=f"dates_{specialty}")])
    
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     date_display = doctor['available_slots'][date]['date_display']
#     slots_text = "\n".join(time_slots) if time_slots else "Bo‘sh vaqt yo‘q."
    
#     query.message.reply_text(
#         f"📅 *{date_display} uchun vaqtlar:*\n\n{slots_text}",
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# def confirm_appointment(update: Update, context: CallbackContext, specialty: str, date: str, time_slot: str):
#     query = update.callback_query
#     query.answer()
    
#     user_id = str(query.from_user.id)
    
#     doctor = DOCTORS[specialty]
#     if time_slot in doctor['available_slots'][date]['slots']:
#         doctor['available_slots'][date]['slots'].remove(time_slot)
#     else:
#         query.message.reply_text("❌ Bu vaqt band! Boshqasini tanlang.")
#         return
    
#     context.user_data[user_id] = context.user_data.get(user_id, {})
#     context.user_data[user_id]['pending_appointment'] = {
#         'specialty': specialty,
#         'date': date,
#         'date_display': doctor['available_slots'][date]['date_display'],
#         'time_slot': time_slot,
#         'doctor_name': doctor['name']
#     }
#     context.user_data[user_id]['first_name'] = query.from_user.first_name
#     context.user_data[user_id]['username'] = query.from_user.username or "Noma'lum"
    
#     context.bot.send_message(
#         chat_id=user_id,
#         text=(
#             f"🎉 *Tabriklaymiz, {query.from_user.first_name}!* 🎉\n"
#             f"✅ Qabulingiz tasdiqlandi:\n\n"
#             f"👩‍⚕️ *Doktor:* {doctor['name']}\n"
#             f"📅 *Sana:* {doctor['available_slots'][date]['date_display']}\n"
#             f"⏰ *Vaqt:* {time_slot}\n\n"
#             f"🏥 *Manzil:* Toshkent sh., Mirzo Ulug‘bek ko‘chasi, 45\n"
#             f"📞 *Aloqa:* {CLINIC_PHONE}\n\n"
#             f"🔥 *Eslatma:* Qabulga 10 daqiqa oldin keling!"
#         ),
#         parse_mode='Markdown',
#         reply_markup=get_main_menu(user_id)
#     )
    
#     registrations[user_id] = {
#         'specialty': specialty,
#         'date': date,
#         'date_display': doctor['available_slots'][date]['date_display'],
#         'time_slot': time_slot,
#         'status': 'confirmed',
#         'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'user_info': {
#             'id': int(user_id),
#             'name': context.user_data[user_id].get('first_name', 'Noma‘lum'),
#             'username': context.user_data[user_id].get('username', 'Noma‘lum')
#         }
#     }
#     save_json('registrations.json', registrations)
    
#     if user_id in paid_users:
#         del paid_users[user_id]
#         save_json('paid_users.json', paid_users)
    
#     if user_id in context.user_data:
#         context.user_data[user_id].pop('pending_appointment', None)

# def handle_callback(update: Update, context: CallbackContext):
#     query = update.callback_query
#     if not query:
#         return
#     try:
#         query.answer()
        
#         if query.data == 'back_to_main':
#             context.bot.send_message(
#                 chat_id=query.message.chat_id,
#                 text="🌟 Bosh menyuga xush kelibsiz!",
#                 reply_markup=get_main_menu(query.from_user.id)
#             )
#             return
            
#         elif query.data == 'pay_back':
#             query.message.delete()
#             context.bot.send_message(
#                 chat_id=query.message.chat_id,
#                 text="🌟 Bosh menyuga qaytdingiz!",
#                 reply_markup=get_main_menu(query.from_user.id)
#             )
#             return
            
#         elif query.data == 'pay_methods':
#             show_payment_options(update, context)
#             return
            
#         elif query.data.startswith('pay_'):
#             method = query.data.split('_')[1]
#             if method in ['click', 'payme', 'uzum']:
#                 show_payment_instructions(update, context, method)
#             elif method == 'done':
#                 query.edit_message_text(
#                     "✅ *To‘lov uchun rahmat!* ✅\n"
#                     "📸 Chek skrinshotini shu yerga yuboring.\n"
#                     "⏳ Admin tasdiqlashini kuting...",
#                     parse_mode='Markdown'
#                 )
#             return
            
#         elif query.data.startswith('specialty_'):
#             specialty = query.data.split('_')[1]
#             show_specialty_info(update, context, specialty)
#             return
            
#         elif query.data.startswith('dates_'):
#             specialty = query.data.split('_')[1]
#             show_available_dates(update, context, specialty)
#             return
            
#         elif query.data.startswith('times_'):
#             parts = query.data.split('_')
#             if len(parts) >= 3:
#                 show_time_slots(update, context, parts[1], parts[2])
#             return
            
#         elif query.data.startswith('confirm_'):
#             parts = query.data.split('_')
#             if len(parts) >= 4:
#                 confirm_appointment(update, context, parts[1], parts[2], '_'.join(parts[3:]))
#             return
            
#         query.edit_message_text("⚠️ Noma‘lum buyruq! Menyudan tanlang 👇")
        
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         query.edit_message_text("⚠️ Xatolik yuz berdi! Qaytadan urinib ko‘ring.")

# def about_clinic(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     text = (
#         "🏥 *ShifoNur - Sizning Sog‘ligingiz G‘amxo‘ri!* 🏥\n\n"
#         "💙 Biz oilangiz salomatligi uchun eng yaxshi xizmatni taqdim etamiz!\n\n"
#         "📍 *Manzil:* Toshkent sh., Mirzo Ulug‘bek ko‘chasi, 45\n"
#         "🕒 *Ish vaqti:* Dushanba-Juma, 8:00-18:00\n"
#         f"📞 *Telefon:* {CLINIC_PHONE}\n\n"
#         "🎯 *Foydalanish:* Lokatsiyani oching yoki qo‘ng‘iroq qiling!"
#     )
#     update.message.reply_text(text, parse_mode="Markdown")
#     update.message.reply_location(latitude=CLINIC_LOCATION[0], longitude=CLINIC_LOCATION[1])

# def contact_us(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     text = (
#         "📞 *Biz Bilan Bog‘laning!* 📞\n\n"
#         f"📱 *Telefon:* {CLINIC_PHONE}\n"
#         "✈️ *Telegram:* @ShifoNurClinic\n"
#         "📧 *Email:* info@shifonur.uz\n\n"
#         "🔥 *Aloqa usuli:* Qo‘ng‘iroq qiling yoki Telegramda yozing!"
#     )
#     update.message.reply_text(text, parse_mode="Markdown")

# def show_payment_options(update: Update, context: CallbackContext):
#     if update.message is None and update.callback_query is None:
#         return
#     payment_urls = {
#         'click': f'https://my.click.uz/services/pay?service_id=123&card_number={PAYMENT_CARD}&amount=100000',
#         'payme': f'https://payme.uz/pay?card={PAYMENT_CARD}&amount=100000',
#         'uzum': f'https://uzumbank.uz/pay?card={PAYMENT_CARD}&amount=100000'
#     }
    
#     buttons = [
#         [InlineKeyboardButton(f"💳 Click - {PAYMENT_CARD}", url=payment_urls['click'])],
#         [InlineKeyboardButton(f"💳 Payme - {PAYMENT_CARD}", url=payment_urls['payme'])],
#         [InlineKeyboardButton(f"💳 Uzum - {PAYMENT_CARD}", url=payment_urls['uzum'])],
#         [InlineKeyboardButton("◀️ Bosh Menyuga", callback_data='pay_back')],
#         [InlineKeyboardButton("✅ To‘lov Qildim", callback_data='pay_done')]
#     ]
#     reply_markup = InlineKeyboardMarkup(buttons)
    
#     text = (
#         "💸 *Tez To‘lov - Qabulga Bir Qadam!* 💸\n\n"
#         "🎯 Quyidagi usuldan tanlang:\n"
#         f"💳 *Karta:* `{PAYMENT_CARD}`\n"
#         "💰 *Summa:* 100,000 so‘m\n\n"
#         "🔥 To‘lovdan so‘ng chekni yuboring va qabulga yoziling!"
#     )
    
#     if update.message:
#         update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
#     else:
#         update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# def show_payment_instructions(update: Update, context: CallbackContext, method: str):
#     query = update.callback_query
#     query.answer()
    
#     instructions = {
#         'click': f"""
# 📌 *Click bilan To‘lov* 📌

# 1️⃣ Click ilovasini oching
# 2️⃣ "To‘lovlar" bo‘limiga o‘ting
# 3️⃣ "Karta orqali" ni tanlang  
# 4️⃣ Karta: `{PAYMENT_CARD}`
# 5️⃣ Summa: *100,000 so‘m*
# 6️⃣ Tasdiqlang
# 7️⃣ Chekni shu yerga yuboring
# """,
#         'payme': f"""
# 📌 *Payme bilan To‘lov* 📌

# 1️⃣ Payme ilovasini oching
# 2️⃣ "To‘lov qilish" ga o‘ting  
# 3️⃣ "Karta orqali" ni tanlang
# 4️⃣ Karta: `{PAYMENT_CARD}`
# 5️⃣ Summa: *100,000 so‘m*  
# 6️⃣ Tasdiqlang
# 7️⃣ Chekni shu yerga yuboring
# """,
#         'uzum': f"""
# 📌 *Uzum bilan To‘lov* 📌

# 1️⃣ Uzum ilovasini oching  
# 2️⃣ "To‘lovlar" ga o‘ting
# 3️⃣ "Karta orqali" ni tanlang
# 4️⃣ Karta: `{PAYMENT_CARD}`
# 5️⃣ Summa: *100,000 so‘m*
# 6️⃣ Tasdiqlang  
# 7️⃣ Chekni shu yerga yuboring
# """
#     }
    
#     buttons = [
#         [InlineKeyboardButton("◀️ Orqaga", callback_data='pay_methods')],
#         [InlineKeyboardButton("✅ To‘lov Qildim", callback_data='pay_done')]
#     ]
#     reply_markup = InlineKeyboardMarkup(buttons)
    
#     query.edit_message_text(
#         instructions[method], 
#         reply_markup=reply_markup,
#         parse_mode='Markdown'
#     )

# def handle_feedback(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     update.message.reply_text(
#         "🌟 *Fikringiz Biz Uchun Muhim!* 🌟\n\n"
#         "💬 Xizmatlarimiz haqida nima deysiz? Yozing:"
#     )
#     context.user_data['awaiting_feedback'] = True

# def save_feedback(update: Update, context: CallbackContext):
#     user = update.message.from_user
#     feedbacks[str(user.id)] = {
#         'text': update.message.text,
#         'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     save_json('feedback.json', feedbacks)
#     update.message.reply_text(f"🙏 *Rahmat, {user.first_name}!* Fikringiz qimmatli!")
#     context.user_data.pop('awaiting_feedback', None)

# def admin_panel(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         update.message.reply_text(
#             "🛠 *Admin Paneli* 🛠\n\n"
#             "🔹 /r - Ro‘yxatdan o‘tganlar\n"
#             "🔹 /f - Fikrlar\n"
#             "🔹 /c <user_id> - To‘lov tasdiqlash\n"
#             "🔹 /sp - To‘lov qilganlar\n"
#             "🔹 /dp <user_id> yoki /dp all - O‘chirish\n"
#             "🔹 /br - Barchaga xabar\n"
#             "🔹 /rp - O‘tgan qabullarni o‘chirish"
#         )
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def show_registrations(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         if not registrations:
#             update.message.reply_text("📅 Hozircha qabulga yozilganlar yo‘q.")
#             return
        
#         message = "📅 *Ro‘yxatdan O‘tganlar:*\n\n"
#         for user_id, data in registrations.items():
#             message += f"👤 *ID:* {user_id}\n"
#             message += f"🩺 {data['specialty']}\n"
#             message += f"📅 {data['date_display']}\n"
#             message += f"⏰ {data['time_slot']}\n"
#             message += f"🔹 Holat: {data.get('status', 'pending')}\n\n"
        
#         update.message.reply_text(message, parse_mode='Markdown')
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def show_feedbacks(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         if not feedbacks:
#             update.message.reply_text("📝 Hozircha fikrlar yo‘q.")
#             return
        
#         message = "📝 *Fikrlar:*\n\n"
#         for user_id, feedback in feedbacks.items():
#             message += f"👤 *ID:* {user_id}\n"
#             message += f"💬 {feedback['text']}\n"
#             message += f"📅 {feedback['date']}\n\n"
        
#         update.message.reply_text(message, parse_mode='Markdown')
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def confirm_payment(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         if len(context.args) < 1:
#             update.message.reply_text("🔑 User ID kiriting: /c <user_id>")
#             return
        
#         user_id = str(context.args[0])
#         paid_users[user_id] = True
#         save_json('paid_users.json', paid_users)
        
#         try:
#             context.bot.send_message(
#                 chat_id=user_id,
#                 text="✅ *To‘lovingiz tasdiqlandi!* Hozir qabulga yozilishingiz mumkin!"
#             )
#             context.bot.send_message(
#                 chat_id=ADMIN_ID,
#                 text=f"✅ User {user_id} uchun to‘lov tasdiqlandi."
#             )
#         except Exception as e:
#             update.message.reply_text(f"✅ Tasdiqlandi, lekin xabar yuborishda xato: {e}")
        
#         update.message.reply_text(f"✅ User {user_id} uchun to‘lov tasdiqlandi.")
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def show_paid_users(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         if not paid_users:
#             update.message.reply_text("💰 To‘lov qilganlar yo‘q.")
#             return
        
#         message = "💰 *To‘lov Qilganlar:*\n\n"
#         for user_id in paid_users:
#             message += f"🆔 {user_id}\n"
#         update.message.reply_text(message, parse_mode='Markdown')
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def delete_paid_users(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         if len(context.args) < 1:
#             update.message.reply_text("🔑 User ID yoki 'all' kiriting: /dp <user_id> yoki /dp all")
#             return
        
#         param = context.args[0]
        
#         if param.lower() == 'all':
#             if not paid_users:
#                 update.message.reply_text("💰 Ro‘yxat bo‘sh.")
#                 return
#             paid_users.clear()
#             save_json('paid_users.json', paid_users)
#             update.message.reply_text("✅ Barcha to‘lovlar o‘chirildi.")
#         else:
#             user_id = str(param)
#             if user_id in paid_users:
#                 del paid_users[user_id]
#                 save_json('paid_users.json', paid_users)
#                 update.message.reply_text(f"✅ User {user_id} o‘chirildi.")
#             else:
#                 update.message.reply_text(f"❌ User {user_id} topilmadi.")
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def broadcast_message(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         update.message.reply_text("📢 Barchaga xabar yuborish uchun matn kiriting:")
#         context.user_data['awaiting_broadcast'] = True
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def remove_past_registrations(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     if is_admin(update.message.from_user.id):
#         if not registrations:
#             update.message.reply_text("📅 Ro‘yxat bo‘sh.")
#             return
        
#         current_date = datetime.now().date()
#         removed_count = 0
#         users_to_remove = []
        
#         for user_id, data in registrations.items():
#             reg_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
#             if reg_date < current_date:
#                 users_to_remove.append(user_id)
#                 removed_count += 1
        
#         for user_id in users_to_remove:
#             del registrations[user_id]
        
#         if removed_count > 0:
#             save_json('registrations.json', registrations)
#             update.message.reply_text(f"✅ {removed_count} ta o‘tgan qabul o‘chirildi.")
#         else:
#             update.message.reply_text("❌ O‘tgan qabul topilmadi.")
#     else:
#         update.message.reply_text("❌ Faqat adminlar uchun!")

# def handle_receipt(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     user = update.message.from_user
#     user_id = str(user.id)
    
#     if update.message.photo:
#         context.bot.send_photo(
#             chat_id=ADMIN_ID,
#             photo=update.message.photo[-1].file_id,
#             caption=f"💰 *Yangi Chek*\n\n"
#                     f"👤 {user.first_name}\n"
#                     f"🆔 {user.id}\n\n"
#                     f"🔑 Tasdiqlash: /c {user.id}"
#         )
        
#         update.message.reply_text(
#             "✅ *Chek qabul qilindi!* ✅\n"
#             "⏳ Admin tasdiqlashini kuting...",
#             parse_mode='Markdown',
#             reply_markup=get_main_menu(user_id)
#         )
#     else:
#         update.message.reply_text(
#             "⚠️ Chekni *rasm* sifatida yuboring!"
#         )

# def handle_message(update: Update, context: CallbackContext):
#     if update.message is None:
#         return
#     user = update.message.from_user
#     text = update.message.text
    
#     if user.id not in context.user_data:
#         context.user_data[user.id] = {}
#     context.user_data[user.id]['first_name'] = user.first_name
#     context.user_data[user.id]['username'] = user.username
    
#     if is_admin(user.id) and context.user_data.get('awaiting_broadcast'):
#         context.user_data.pop('awaiting_broadcast', None)
#         sent_count = 0
#         for user_id in registrations.keys():
#             try:
#                 context.bot.send_message(
#                     chat_id=user_id,
#                     text=f"📢 *Xabar:* {text}"
#                 )
#                 sent_count += 1
#             except Exception as e:
#                 print(f"Xabar yuborishda xato {user_id}: {e}")
        
#         update.message.reply_text(f"✅ Xabar {sent_count} foydalanuvchiga yuborildi.")
#         return
    
#     if context.user_data.get('awaiting_feedback'):
#         save_feedback(update, context)
#         return
    
#     menu_actions = {
#         "👨‍⚕️ Doktorlarimiz": show_doctors,
#         "🏥 Klinika Haqida": about_clinic,
#         "📞 Aloqa": contact_us,
#         "📝 Fikr Bildirish": handle_feedback,
#         "💸 To'lov": show_payment_options,
#         "📅 Qabulga Yozilish": show_available_specialties,
#         "🛠 Admin Paneli": admin_panel
#     }
    
#     if text in menu_actions:
#         menu_actions[text](update, context)
#     else:
#         update.message.reply_text(
#             "⚠️ Buyruqni tushunmadim! Quyidagi menyudan tanlang 👇",
#             reply_markup=get_main_menu(user.id)
#         )

# def main():
#     TOKEN = "7685449635:AAHlZQj53Epz3g1DTuBpYkweIM5UW2HVPNk"
    
#     try:
#         updater = Updater(TOKEN, use_context=True)
#         dp = updater.dispatcher
        
#         dp.add_handler(CommandHandler("start", start))
#         dp.add_handler(CommandHandler("r", show_registrations))
#         dp.add_handler(CommandHandler("f", show_feedbacks))
#         dp.add_handler(CommandHandler("c", confirm_payment))
#         dp.add_handler(CommandHandler("sp", show_paid_users))
#         dp.add_handler(CommandHandler("dp", delete_paid_users))
#         dp.add_handler(CommandHandler("br", broadcast_message))
#         dp.add_handler(CommandHandler("rp", remove_past_registrations))
        
#         dp.add_handler(CallbackQueryHandler(handle_callback))
        
#         dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
#         dp.add_handler(MessageHandler(Filters.photo, handle_receipt))
        
#         print("Bot ishga tushdi...")
#         updater.start_polling()
#         updater.idle()
#     except Exception as e:
#         print(f"Botni ishga tushirishda xatolik: {str(e)}")

# if __name__ == "__main__":
#     main()
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, Filters
import json
import os
from datetime import datetime, timedelta

# Database initialization
paid_users = {}
registrations = {}
feedbacks = {}
doctor_appointments = {}

def load_json(filename):
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return {}

def save_json(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# Load data
paid_users = load_json('paid_users.json')
registrations = load_json('registrations.json')
feedbacks = load_json('feedback.json')
doctor_appointments = load_json('doctor_appointments.json')

ADMIN_ID = 7201258445
CLINIC_LOCATION = (41.311081, 69.240562)
CLINIC_PHONE = "+998908161706"
PAYMENT_CARD = "4073420080671617"

def generate_doctor_slots(days=7):
    slots = {}
    today = datetime.now().date()
    
    for day in range(days):
        current_date = today + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        month = {
            1: 'Yanvar', 2: 'Fevral', 3: 'Mart', 4: 'Aprel',
            5: 'May', 6: 'Iyun', 7: 'Iyul', 8: 'Avgust',
            9: 'Sentabr', 10: 'Oktabr', 11: 'Noyabr', 12: 'Dekabr'
        }[current_date.month]
        slots[date_str] = {
            'date_display': f"{current_date.day} {month}",
            'slots': [f"{hour:02d}:00-{(hour+2):02d}:00" for hour in range(9, 17, 2)]
        }
    return slots

DOCTORS = {
    "Terapevt": {"name": "Doktor Aliev", "info": "20 yillik tajriba", "price": "100,000 so'm", "available_slots": generate_doctor_slots(7)},
    "Kardiolog": {"name": "Doktor Rashidov", "info": "Yurak kasalliklari bo'yicha mutaxassis", "price": "150,000 so'm", "available_slots": generate_doctor_slots(7)},
    "Nevropatolog": {"name": "Doktor Karimova", "info": "Nevrologiya bo'yicha 15 yillik tajriba", "price": "120,000 so'm", "available_slots": generate_doctor_slots(7)},
    "Pediatr": {"name": "Doktor Usmonova", "info": "Bolalar salomatligi bo'yicha 10 yillik tajriba", "price": "90,000 so'm", "available_slots": generate_doctor_slots(7)}
}

def is_admin(user_id):
    return str(user_id) == str(ADMIN_ID)

def get_main_menu(user_id):
    menu = [
        ["👨‍⚕️ Doktorlarimiz"],
        ["🏥 Klinika Haqida", "📞 Aloqa"],
        ["📝 Fikr Bildirish", "💸 To'lov"],
        ["📅 Qabulga Yozilish"]
    ]
    if is_admin(user_id):
        menu.append(["🛠 Admin Paneli"])
    return ReplyKeyboardMarkup(menu, resize_keyboard=True, one_time_keyboard=False)

def start(update: Update, context: CallbackContext):
    if not update.message:
        return
    user = update.message.from_user
    welcome_msg = (
        f"🎉 *Assalomu alaykum, {user.first_name}!* 🎉\n"
        "ShifoNur klinikasi botiga xush kelibsiz! 🌟\n\n"
        "🔥 Sog‘ligingizni bizga ishonib topshiring:\n"
        "👇 Quyidagi tugmalar bilan tanishib, hoziroq boshlang!"
    )
    update.message.reply_text(welcome_msg, parse_mode='Markdown', reply_markup=get_main_menu(user.id))

def show_doctors(update: Update, context: CallbackContext):
    if not update.message:
        return
    message = (
        "👩‍⚕️ *Bizning Professional Doktorlarimiz* 👨‍⚕️\n\n"
        "Siz uchun eng yaxshi mutaxassislar tayyor:\n"
    )
    for specialty, doctor in DOCTORS.items():
        message += (
            f"👤 *{doctor['name']}* - {specialty}\n"
            f"ℹ️ {doctor['info']}\n"
            f"💰 Narx: {doctor['price']}\n"
            f"🕒 Dushanba-Juma, 9:00-17:00\n"
            f"🎯 *Qabulga yozilish uchun avval to‘lov qiling!* 👇\n\n"
        )
    keyboard = [
        [InlineKeyboardButton("💸 Hozir To‘lov Qilish", callback_data="pay_methods")],
        [InlineKeyboardButton("◀️ Bosh Menyuga", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

def show_available_specialties(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id) if update.message else str(update.callback_query.from_user.id)
    
    if user_id not in paid_users and not is_admin(user_id):
        text = (
            "⚠️ *Qabulga yozilish uchun avval to‘lov qiling!* ⚠️\n\n"
            "👉 '💸 To‘lov' bo‘limida to‘lov qiling va chekni yuboring.\n"
            "✅ Admin tasdiqlagach, qabulga yozilish ochiladi!"
        )
        if update.message:
            update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_main_menu(user_id))
        else:
            update.callback_query.edit_message_text(text, parse_mode='Markdown')
        return
    
    keyboard = [
        [InlineKeyboardButton(f"👩‍⚕️ {specialty}", callback_data=f"specialty_{specialty}")]
        for specialty in DOCTORS
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "📅 *Qabulga Yozilish* 📅\n\n"
        "🎯 O‘zingizga kerakli mutaxassisni tanlang:"
    )
    
    if update.message:
        update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

def show_specialty_info(update: Update, context: CallbackContext, specialty: str):
    query = update.callback_query
    query.answer()
    
    doctor = DOCTORS[specialty]
    keyboard = [
        [InlineKeyboardButton("📅 Vaqt Tanlash", callback_data=f"dates_{specialty}")],
        [InlineKeyboardButton("◀️ Bosh Menyuga", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=(
            f"👤 *{doctor['name']}* - {specialty}\n"
            f"ℹ️ {doctor['info']}\n"
            f"💰 Narx: {doctor['price']}\n\n"
            "🔥 Hozir qabul vaqtini tanlang:"
        ),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def update_doctor_slots():
    today = datetime.now().date()
    
    for doctor_name, doctor in DOCTORS.items():
        for date_str in list(doctor['available_slots'].keys()):
            slot_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if slot_date < today:
                del doctor['available_slots'][date_str]
        
        existing_dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in doctor['available_slots'].keys()]
        latest_date = max(existing_dates) if existing_dates else today - timedelta(days=1)
        
        for day in range(1, 8):
            new_date = latest_date + timedelta(days=day)
            date_str = new_date.strftime("%Y-%m-%d")
            
            if date_str not in doctor['available_slots'] and new_date.weekday() < 5:
                new_slots = generate_doctor_slots(1)
                if date_str in new_slots:
                    doctor['available_slots'][date_str] = new_slots[date_str]

def show_available_dates(update: Update, context: CallbackContext, specialty: str):
    query = update.callback_query
    query.answer()
    
    update_doctor_slots()
    
    doctor = DOCTORS[specialty]
    available_dates = sorted(doctor['available_slots'].keys())[:7]
    
    keyboard = [
        [InlineKeyboardButton(
            f"📅 {doctor['available_slots'][date]['date_display']}", 
            callback_data=f"times_{specialty}_{date}")]
        for date in available_dates
    ]
    keyboard.append([InlineKeyboardButton("◀️ Orqaga", callback_data=f"specialty_{specialty}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        f"👩‍⚕️ *{doctor['name']}*\n\n"
        "📅 Qabul kunini tanlang:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def show_time_slots(update: Update, context: CallbackContext, specialty: str, date: str):
    query = update.callback_query
    query.answer()
    
    doctor = DOCTORS[specialty]
    if date not in doctor['available_slots']:
        query.message.reply_text("❌ Bu kunda qabul yo‘q!")
        return
    
    time_slots = doctor['available_slots'][date]['slots']
    
    keyboard = [
        [InlineKeyboardButton(
            f"⏰ {slot}", 
            callback_data=f"confirm_{specialty}_{date}_{slot}")]
        for slot in time_slots
    ]
    keyboard.append([InlineKeyboardButton("◀️ Orqaga", callback_data=f"dates_{specialty}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    date_display = doctor['available_slots'][date]['date_display']
    slots_text = "\n".join(time_slots) if time_slots else "Bo‘sh vaqt yo‘q."
    
    query.message.reply_text(
        f"📅 *{date_display} uchun vaqtlar:*\n\n{slots_text}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def confirm_appointment(update: Update, context: CallbackContext, specialty: str, date: str, time_slot: str):
    query = update.callback_query
    query.answer()
    
    user_id = str(query.from_user.id)
    
    doctor = DOCTORS[specialty]
    if time_slot in doctor['available_slots'][date]['slots']:
        doctor['available_slots'][date]['slots'].remove(time_slot)
    else:
        query.message.reply_text("❌ Bu vaqt band! Boshqasini tanlang.")
        return
    
    context.user_data[user_id] = context.user_data.get(user_id, {})
    context.user_data[user_id]['pending_appointment'] = {
        'specialty': specialty,
        'date': date,
        'date_display': doctor['available_slots'][date]['date_display'],
        'time_slot': time_slot,
        'doctor_name': doctor['name']
    }
    context.user_data[user_id]['first_name'] = query.from_user.first_name
    context.user_data[user_id]['username'] = query.from_user.username or "Noma'lum"
    
    context.bot.send_message(
        chat_id=user_id,
        text=(
            f"🎉 *Tabriklaymiz, {query.from_user.first_name}!* 🎉\n"
            f"✅ Qabulingiz tasdiqlandi:\n\n"
            f"👩‍⚕️ *Doktor:* {doctor['name']}\n"
            f"📅 *Sana:* {doctor['available_slots'][date]['date_display']}\n"
            f"⏰ *Vaqt:* {time_slot}\n\n"
            f"🏥 *Manzil:* Toshkent sh., Mirzo Ulug‘bek ko‘chasi, 45\n"
            f"📞 *Aloqa:* {CLINIC_PHONE}\n\n"
            f"🔥 *Eslatma:* Qabulga 10 daqiqa oldin keling!"
        ),
        parse_mode='Markdown',
        reply_markup=get_main_menu(user_id)
    )
    
    registrations[user_id] = {
        'specialty': specialty,
        'date': date,
        'date_display': doctor['available_slots'][date]['date_display'],
        'time_slot': time_slot,
        'status': 'confirmed',
        'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'user_info': {
            'id': int(user_id),
            'name': context.user_data[user_id].get('first_name', 'Noma‘lum'),
            'username': context.user_data[user_id].get('username', 'Noma‘lum')
        }
    }
    save_json('registrations.json', registrations)
    
    if user_id in paid_users:
        del paid_users[user_id]
        save_json('paid_users.json', paid_users)
    
    if user_id in context.user_data:
        context.user_data[user_id].pop('pending_appointment', None)

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if not query:
        return
    try:
        query.answer()
        
        if query.data == 'back_to_main':
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text="🌟 Bosh menyuga xush kelibsiz!",
                reply_markup=get_main_menu(query.from_user.id)
            )
            return
            
        elif query.data == 'pay_back':
            query.message.delete()
            context.bot.send_message(
                chat_id=query.message.chat_id,
                text="🌟 Bosh menyuga qaytdingiz!",
                reply_markup=get_main_menu(query.from_user.id)
            )
            return
            
        elif query.data == 'pay_methods':
            show_payment_options(update, context)
            return
            
        elif query.data.startswith('pay_'):
            method = query.data.split('_')[1]
            if method in ['click', 'payme', 'uzum']:
                show_payment_instructions(update, context, method)
            elif method == 'done':
                query.edit_message_text(
                    "✅ *To‘lov uchun rahmat!* ✅\n"
                    "📸 Chek skrinshotini shu yerga yuboring.\n"
                    "⏳ Admin tasdiqlashini kuting...",
                    parse_mode='Markdown'
                )
            return
            
        elif query.data.startswith('specialty_'):
            specialty = query.data.split('_')[1]
            show_specialty_info(update, context, specialty)
            return
            
        elif query.data.startswith('dates_'):
            specialty = query.data.split('_')[1]
            show_available_dates(update, context, specialty)
            return
            
        elif query.data.startswith('times_'):
            parts = query.data.split('_')
            if len(parts) >= 3:
                show_time_slots(update, context, parts[1], parts[2])
            return
            
        elif query.data.startswith('confirm_'):
            parts = query.data.split('_')
            if len(parts) >= 4:
                confirm_appointment(update, context, parts[1], parts[2], '_'.join(parts[3:]))
            return
            
        query.edit_message_text("⚠️ Noma‘lum buyruq! Menyudan tanlang 👇")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        query.edit_message_text("⚠️ Xatolik yuz berdi! Qaytadan urinib ko‘ring.")

def about_clinic(update: Update, context: CallbackContext):
    if not update.message:
        return
    text = (
        "🏥 *ShifoNur - Sizning Sog‘ligingiz G‘amxo‘ri!* 🏥\n\n"
        "💙 Biz oilangiz salomatligi uchun eng yaxshi xizmatni taqdim etamiz!\n\n"
        "📍 *Manzil:* Toshkent sh., Mirzo Ulug‘bek ko‘chasi, 45\n"
        "🕒 *Ish vaqti:* Dushanba-Juma, 8:00-18:00\n"
        f"📞 *Telefon:* {CLINIC_PHONE}\n\n"
        "🎯 *Foydalanish:* Lokatsiyani oching yoki qo‘ng‘iroq qiling!"
    )
    update.message.reply_text(text, parse_mode="Markdown")
    update.message.reply_location(latitude=CLINIC_LOCATION[0], longitude=CLINIC_LOCATION[1])

def contact_us(update: Update, context: CallbackContext):
    if not update.message:
        return
    text = (
        "📞 *Biz Bilan Bog‘laning!* 📞\n\n"
        f"📱 *Telefon:* {CLINIC_PHONE}\n"
        "✈️ *Telegram:* @ShifoNurClinic\n"
        "📧 *Email:* info@shifonur.uz\n\n"
        "🔥 *Aloqa usuli:* Qo‘ng‘iroq qiling yoki Telegramda yozing!"
    )
    update.message.reply_text(text, parse_mode="Markdown")

def show_payment_options(update: Update, context: CallbackContext):
    if not update.message and not update.callback_query:
        return
    payment_urls = {
        'click': f'https://my.click.uz/services/pay?service_id=123&card_number={PAYMENT_CARD}&amount=100000',
        'payme': f'https://payme.uz/pay?card={PAYMENT_CARD}&amount=100000',
        'uzum': f'https://uzumbank.uz/pay?card={PAYMENT_CARD}&amount=100000'
    }
    
    buttons = [
        [InlineKeyboardButton(f"💳 Click - {PAYMENT_CARD}", url=payment_urls['click'])],
        [InlineKeyboardButton(f"💳 Payme - {PAYMENT_CARD}", url=payment_urls['payme'])],
        [InlineKeyboardButton(f"💳 Uzum - {PAYMENT_CARD}", url=payment_urls['uzum'])],
        [InlineKeyboardButton("◀️ Bosh Menyuga", callback_data='pay_back')],
        [InlineKeyboardButton("✅ To‘lov Qildim", callback_data='pay_done')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    text = (
        "💸 *Tez To‘lov - Qabulga Bir Qadam!* 💸\n\n"
        "🎯 Quyidagi usuldan tanlang:\n"
        f"💳 *Karta:* `{PAYMENT_CARD}`\n"
        "💰 *Summa:* 100,000 so‘m\n\n"
        "🔥 To‘lovdan so‘ng chekni yuboring va qabulga yoziling!"
    )
    
    if update.message:
        update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

def show_payment_instructions(update: Update, context: CallbackContext, method: str):
    query = update.callback_query
    query.answer()
    
    instructions = {
        'click': f"""
📌 *Click bilan To‘lov* 📌

1️⃣ Click ilovasini oching
2️⃣ "To‘lovlar" bo‘limiga o‘ting
3️⃣ "Karta orqali" ni tanlang  
4️⃣ Karta: `{PAYMENT_CARD}`
5️⃣ Summa: *100,000 so‘m*
6️⃣ Tasdiqlang
7️⃣ Chekni shu yerga yuboring
""",
        'payme': f"""
📌 *Payme bilan To‘lov* 📌

1️⃣ Payme ilovasini oching
2️⃣ "To‘lov qilish" ga o‘ting  
3️⃣ "Karta orqali" ni tanlang
4️⃣ Karta: `{PAYMENT_CARD}`
5️⃣ Summa: *100,000 so‘m*  
6️⃣ Tasdiqlang
7️⃣ Chekni shu yerga yuboring
""",
        'uzum': f"""
📌 *Uzum bilan To‘lov* 📌

1️⃣ Uzum ilovasini oching  
2️⃣ "To‘lovlar" ga o‘ting
3️⃣ "Karta orqali" ni tanlang
4️⃣ Karta: `{PAYMENT_CARD}`
5️⃣ Summa: *100,000 so‘m*
6️⃣ Tasdiqlang  
7️⃣ Chekni shu yerga yuboring
"""
    }
    
    buttons = [
        [InlineKeyboardButton("◀️ Orqaga", callback_data='pay_methods')],
        [InlineKeyboardButton("✅ To‘lov Qildim", callback_data='pay_done')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    query.edit_message_text(
        instructions[method], 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def handle_feedback(update: Update, context: CallbackContext):
    if not update.message:
        return
    update.message.reply_text(
        "🌟 *Fikringiz Biz Uchun Muhim!* 🌟\n\n"
        "💬 Xizmatlarimiz haqida nima deysiz? Yozing:"
    )
    context.user_data['awaiting_feedback'] = True

def save_feedback(update: Update, context: CallbackContext):
    user = update.message.from_user
    feedbacks[str(user.id)] = {
        'text': update.message.text,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_json('feedback.json', feedbacks)
    update.message.reply_text(f"🙏 *Rahmat, {user.first_name}!* Fikringiz qimmatli!")
    context.user_data.pop('awaiting_feedback', None)

def admin_panel(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        update.message.reply_text(
            "🛠 *Admin Paneli* 🛠\n\n"
            "🔹 /r - Ro‘yxatdan o‘tganlar\n"
            "🔹 /f - Fikrlar\n"
            "🔹 /c <user_id> - To‘lov tasdiqlash\n"
            "🔹 /sp - To‘lov qilganlar\n"
            "🔹 /dp <user_id> yoki /dp all - O‘chirish\n"
            "🔹 /br - Barchaga xabar\n"
            "🔹 /rp - O‘tgan qabullarni o‘chirish"
        )
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def show_registrations(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        if not registrations:
            update.message.reply_text("📅 Hozircha qabulga yozilganlar yo‘q.")
            return
        
        message = "📅 *Ro‘yxatdan O‘tganlar:*\n\n"
        for user_id, data in registrations.items():
            message += f"👤 *ID:* {user_id}\n"
            message += f"🩺 {data['specialty']}\n"
            message += f"📅 {data['date_display']}\n"
            message += f"⏰ {data['time_slot']}\n"
            message += f"🔹 Holat: {data.get('status', 'pending')}\n\n"
        
        update.message.reply_text(message, parse_mode='Markdown')
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def show_feedbacks(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        if not feedbacks:
            update.message.reply_text("📝 Hozircha fikrlar yo‘q.")
            return
        
        message = "📝 *Fikrlar:*\n\n"
        for user_id, feedback in feedbacks.items():
            message += f"👤 *ID:* {user_id}\n"
            message += f"💬 {feedback['text']}\n"
            message += f"📅 {feedback['date']}\n\n"
        
        update.message.reply_text(message, parse_mode='Markdown')
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def confirm_payment(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        if len(context.args) < 1:
            update.message.reply_text("🔑 User ID kiriting: /c <user_id>")
            return
        
        user_id = str(context.args[0])
        paid_users[user_id] = True
        save_json('paid_users.json', paid_users)
        
        try:
            context.bot.send_message(
                chat_id=user_id,
                text="✅ *To‘lovingiz tasdiqlandi!* Hozir qabulga yozilishingiz mumkin!"
            )
            context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"✅ User {user_id} uchun to‘lov tasdiqlandi."
            )
        except Exception as e:
            update.message.reply_text(f"✅ Tasdiqlandi, lekin xabar yuborishda xato: {e}")
        
        update.message.reply_text(f"✅ User {user_id} uchun to‘lov tasdiqlandi.")
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def show_paid_users(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        if not paid_users:
            update.message.reply_text("💰 To‘lov qilganlar yo‘q.")
            return
        
        message = "💰 *To‘lov Qilganlar:*\n\n"
        for user_id in paid_users:
            message += f"🆔 {user_id}\n"
        update.message.reply_text(message, parse_mode='Markdown')
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def delete_paid_users(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        if len(context.args) < 1:
            update.message.reply_text("🔑 User ID yoki 'all' kiriting: /dp <user_id> yoki /dp all")
            return
        
        param = context.args[0]
        
        if param.lower() == 'all':
            if not paid_users:
                update.message.reply_text("💰 Ro‘yxat bo‘sh.")
                return
            paid_users.clear()
            save_json('paid_users.json', paid_users)
            update.message.reply_text("✅ Barcha to‘lovlar o‘chirildi.")
        else:
            user_id = str(param)
            if user_id in paid_users:
                del paid_users[user_id]
                save_json('paid_users.json', paid_users)
                update.message.reply_text(f"✅ User {user_id} o‘chirildi.")
            else:
                update.message.reply_text(f"❌ User {user_id} topilmadi.")
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def broadcast_message(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        update.message.reply_text("📢 Barchaga xabar yuborish uchun matn kiriting:")
        context.user_data['awaiting_broadcast'] = True
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def remove_past_registrations(update: Update, context: CallbackContext):
    if not update.message:
        return
    if is_admin(update.message.from_user.id):
        if not registrations:
            update.message.reply_text("📅 Ro‘yxat bo‘sh.")
            return
        
        current_date = datetime.now().date()
        removed_count = 0
        users_to_remove = []
        
        for user_id, data in registrations.items():
            reg_date = datetime.strptime(data['date'], "%Y-%m-%d").date()
            if reg_date < current_date:
                users_to_remove.append(user_id)
                removed_count += 1
        
        for user_id in users_to_remove:
            del registrations[user_id]
        
        if removed_count > 0:
            save_json('registrations.json', registrations)
            update.message.reply_text(f"✅ {removed_count} ta o‘tgan qabul o‘chirildi.")
        else:
            update.message.reply_text("❌ O‘tgan qabul topilmadi.")
    else:
        update.message.reply_text("❌ Faqat adminlar uchun!")

def handle_receipt(update: Update, context: CallbackContext):
    if not update.message:
        return
    user = update.message.from_user
    user_id = str(user.id)
    
    if update.message.photo:
        context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=f"💰 *Yangi Chek*\n\n"
                    f"👤 {user.first_name}\n"
                    f"🆔 {user.id}\n\n"
                    f"🔑 Tasdiqlash: /c {user.id}"
        )
        
        update.message.reply_text(
            "✅ *Chek qabul qilindi!* ✅\n"
            "⏳ Admin tasdiqlashini kuting...",
            parse_mode='Markdown',
            reply_markup=get_main_menu(user_id)
        )
    else:
        update.message.reply_text(
            "⚠️ Chekni *rasm* sifatida yuboring!"
        )

def handle_message(update: Update, context: CallbackContext):
    if not update.message:
        return
    user = update.message.from_user
    text = update.message.text
    
    if user.id not in context.user_data:
        context.user_data[user.id] = {}
    context.user_data[user.id]['first_name'] = user.first_name
    context.user_data[user.id]['username'] = user.username
    
    if is_admin(user.id) and context.user_data.get('awaiting_broadcast'):
        context.user_data.pop('awaiting_broadcast', None)
        sent_count = 0
        for user_id in registrations.keys():
            try:
                context.bot.send_message(
                    chat_id=user_id,
                    text=f"📢 *Xabar:* {text}"
                )
                sent_count += 1
            except Exception as e:
                print(f"Xabar yuborishda xato {user_id}: {e}")
        
        update.message.reply_text(f"✅ Xabar {sent_count} foydalanuvchiga yuborildi.")
        return
    
    if context.user_data.get('awaiting_feedback'):
        save_feedback(update, context)
        return
    
    menu_actions = {
        "👨‍⚕️ Doktorlarimiz": show_doctors,
        "🏥 Klinika Haqida": about_clinic,
        "📞 Aloqa": contact_us,
        "📝 Fikr Bildirish": handle_feedback,
        "💸 To'lov": show_payment_options,
        "📅 Qabulga Yozilish": show_available_specialties,
        "🛠 Admin Paneli": admin_panel
    }
    
    if text in menu_actions:
        menu_actions[text](update, context)
    else:
        update.message.reply_text(
            "⚠️ Buyruqni tushunmadim! Quyidagi menyudan tanlang 👇",
            reply_markup=get_main_menu(user.id)
        )

def main():
    TOKEN = "7685449635:AAHlZQj53Epz3g1DTuBpYkweIM5UW2HVPNk"
    
    try:
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("r", show_registrations))
        dp.add_handler(CommandHandler("f", show_feedbacks))
        dp.add_handler(CommandHandler("c", confirm_payment))
        dp.add_handler(CommandHandler("sp", show_paid_users))
        dp.add_handler(CommandHandler("dp", delete_paid_users))
        dp.add_handler(CommandHandler("br", broadcast_message))
        dp.add_handler(CommandHandler("rp", remove_past_registrations))
        
        dp.add_handler(CallbackQueryHandler(handle_callback))
        
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        dp.add_handler(MessageHandler(Filters.photo, handle_receipt))
        
        print("Bot ishga tushdi...")
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(f"Botni ishga tushirishda xatolik: {str(e)}")

if __name__ == "__main__":
    main()