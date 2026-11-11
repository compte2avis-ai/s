from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ⚙️ CONFIGURATION
TOKEN = "8736667685:AAGI5yXvHD5ZDB18on43wIjJQYI3cBzPQ9w"  # 👈 N'OUBLIE PAS DE METTRE TON TOKEN ICI !
ADMIN_ID = 8564548755    # ✅ Ton ID est configuré

# 💰 TES ADRESSES CRYPTO
WALLET_LTC = "ltc1qwy40a9gr0r3mz65vky2nx3zuq6txz7ffuxhxpn"
WALLET_ETH = "0x5900e982f8189F93b88A1290dB8Bc62F779D2b48"

# 🟣 NOM DU BOT ET EMOJIS
NOM_BOUTIQUE = "NoCheap"
EMOJI_ETOILE = "💜"  
EMOJI_PAIEMENT = "🔮" 

# --- 1. COMMANDE /START (Visible par les clients ET les admins) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texte = (
        f"🌟 <b>Bienvenue sur {NOM_BOUTIQUE} !</b> 🌟\n\n"
        "La boutique n°1 pour acheter tes étoiles Telegram au meilleur prix. 🚀\n"
        f"Profite de nos offres exclusives avec {EMOJI_ETOILE} et paie en toute sécurité.\n\n"
        f"📩 <b>Support :</b> @X4RCS\n\n"
        "👇 <i>Que souhaites-tu faire ?</i>"
    )
    keyboard = [
        [InlineKeyboardButton(f"{EMOJI_ETOILE} Acheter des étoiles", callback_data="acheter")]
    ]
    await update.message.reply_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 2. CHOIX DU PACK (Nouveaux packs et prix) ---
async def bouton_acheter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    texte = (
        f"🛒 <b>Choisis ton pack d'étoiles</b> {EMOJI_ETOILE}\n\n"
        "Voici nos offres exclusives (paiement instantané) :"
    )
    keyboard = [
        [InlineKeyboardButton(f"{EMOJI_ETOILE} 500 étoiles - 8,90€", callback_data="pack_500_890")],
        [InlineKeyboardButton(f"{EMOJI_ETOILE} 1000 étoiles - 16,90€", callback_data="pack_1000_1690")],
        [InlineKeyboardButton(f"{EMOJI_ETOILE} 1500 étoiles - 24,90€", callback_data="pack_1500_2490")],
        [InlineKeyboardButton(f"{EMOJI_ETOILE} 2500 étoiles - 39,90€", callback_data="pack_2500_3990")],
        [InlineKeyboardButton(f"{EMOJI_ETOILE} 5000 étoiles - 75,00€", callback_data="pack_5000_7500")],
        [InlineKeyboardButton(f"{EMOJI_ETOILE} 10000 étoiles - 140,00€", callback_data="pack_10000_14000")],
        [InlineKeyboardButton("🔙 Retour", callback_data="start")]
    ]
    await query.edit_message_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 3. CHOIX DE LA CRYPTO (Uniquement ETH ou LTC) ---
async def choix_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split('_')
    context.user_data['pack_etoiles'] = parts[1] 
    context.user_data['pack_prix'] = parts[2]    
    
    texte = (
        f"🪙 <b>Quelle crypto souhaites-tu utiliser ?</b> {EMOJI_PAIEMENT}\n\n"
        f"Tu as choisi le pack de <b>{parts[1]} étoiles</b>.\n\n"
        "Choisis ta devise pour recevoir l'adresse de paiement :"
    )
    keyboard = [
        [InlineKeyboardButton("🔷 Ethereum (ETH)", callback_data="crypto_ETH")],
        [InlineKeyboardButton("🔵 Litecoin (LTC)", callback_data="crypto_LTC")],
        [InlineKeyboardButton("🔙 Retour", callback_data="acheter")]
    ]
    await query.edit_message_text(texte, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 4. ENVOI DIRECT DE L'ADRESSE + NOTIFICATION ADMIN ---
async def envoyer_adresse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    crypto = query.data.split('_')[1] 
    pack = context.user_data.get('pack_etoiles', 'Inconnu')
    prix_centimes = context.user_data.get('pack_prix', '0')
    prix_euros = f"{int(prix_centimes) / 100:.2f}€"
    
    if crypto == "ETH":
        adresse = WALLET_ETH
        devise = "Ethereum (ETH)"
    else:
        adresse = WALLET_LTC
        devise = "Litecoin (LTC)"
        
    client_id = query.message.chat.id
    client_nom = query.from_user.username or query.from_user.first_name
    
    # 1. Message direct au client (Adresse + Prix)
    texte_client = (
        f"💸 <b>Voici ton adresse de paiement</b> 💸\n\n"
        f"⭐️ Pack : <b>{pack} étoiles</b>\n"
        f"💰 Prix : <b>{prix_euros}</b>\n"
        f"🔮 Mode : <b>{devise}</b>\n\n"
        f"Envoie le montant exact à cette adresse :\n"
        f"<code>{adresse}</code>\n\n"
        "⚠️ <b>IMPORTANT :</b> Une fois le paiement effectué, envoie la preuve (capture ou hash) à @X4RCS pour recevoir tes étoiles."
    )
    await query.edit_message_text(texte_client, parse_mode="HTML")
    
    # 2. Notification à l'admin (Toi) avec le bouton "J'ai reçu"
    texte_admin = (
        f"🔔 <b>NOUVELLE COMMANDE EN COURS</b> 🔔\n\n"
        f"👤 Client : @{client_nom} (ID: {client_id})\n"
        f"⭐️ Pack : {pack} étoiles\n"
        f"💰 Prix : {prix_euros}\n"
        f"🔮 Crypto : {devise}\n\n"
        f"👇 Clique sur J'ai reçu quand le paiement est validé."
    )
    keyboard = [[InlineKeyboardButton("💰 J'ai reçu", callback_data=f"admin_recu_{client_id}")]]
    await context.bot.send_message(chat_id=ADMIN_ID, text=texte_admin, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

# --- 5. ACTION DE L'ADMIN : J'AI REÇU ---
async def admin_recu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    client_id = int(query.data.split('_')[2])
    
    # Message final au client
    texte_client = (
        f"🎉 <b>Merci pour ton achat !</b> 🎉\n\n"
        "Ton paiement a bien été reçu. ✅\n"
        f"Tes étoiles {EMOJI_ETOILE} seront créditées sur ton compte Telegram d'ici <b>1 à 2 jours maximum</b>.\n\n"
        f"Merci de ta confiance et à très vite sur {NOM_BOUTIQUE} ! 🚀"
    )
    await context.bot.send_message(chat_id=client_id, text=texte_client, parse_mode="HTML")
    
    await query.edit_message_text("✅ Commande terminée avec succès. Le client a été notifié.")

# --- DÉMARRAGE DU BOT ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(bouton_acheter, pattern="^acheter$"))
    app.add_handler(CallbackQueryHandler(choix_crypto, pattern="^pack_"))
    app.add_handler(CallbackQueryHandler(envoyer_adresse, pattern="^crypto_"))
    app.add_handler(CallbackQueryHandler(admin_recu, pattern="^admin_recu_"))
    
    print("Le bot NoCheap est en ligne !")
    app.run_polling()