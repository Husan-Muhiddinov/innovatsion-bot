from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from .models import *
from django.db import IntegrityError
import json
import os
import re
from django.core.paginator import Paginator

from telegram_bot_pagination import InlineKeyboardPaginator
# from data import character_pages

WELCOME = ["ID yaratish", "ID berish", "Bo'limlar","Ro'yxat"]
BUTTON1=["Buyruq ID","Xat ID"]
BUTTON2=["Buyruq ID lar","Xat ID lar"]
BUTTON3=["Xato","Imzolanmagan","Foydalanilmagan"]





START_MESSAGE="Hey, I am a simple Test bot"
START_MESSAGE_BUTTON = [("Test", -1001869833758, 'https://t.me/+g7A6MQr9sj5lYTgy'),]




def start(update: Update, context: CallbackContext):
    user = update.effective_user
    try:
        userr=UserInformation(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )
        users = [i.user_id for i in UserInformation.objects.all()]
        if user.id not in users:
            userr.save()
    except Exception as e:
        pass
    log = Log()
    log.user_id = user.id
    # , state={'status_idp': False, 'status_buyxat': False, 'status_boolii': False, 'status_bol': False}
    # log = Log.objects.get_or_create(user_id=user.id)
    # log.state = {'status_idp': False, 'status_buyxat': False, 'status_boolii': False, 'status_bol': False}
    userrs=[i.user_id for i in Log.objects.all()]
    if user.id not in userrs:
        log.save()
    userstat=UserInformation.objects.get(username=user.username)
    try:
        if userstat.user_status==True:
            update.message.reply_text(f"Assalomu alaykum {user.first_name}, botimizga xush kelibsiz", reply_markup=keyboard_buttons(type='welcome'))
    except:
        update.message.reply_text(f"Assalomu alaykum {user.first_name}, botimizga xush kelibsiz")



def send_items(update, context, page):
    global ff
    # query=update.callback_query
    a=Ids.objects.filter(status_ID='Buyruq_ID')
    # print(a)
# Calculate the start and end index of the items for the current page
    start_index = (page - 1) * 10
    end_index = start_index + 10
    ITEMS=a[start_index:end_index]
    # if len(ITEMS) == 0:

    print(ITEMS)
    buttons = []
    for i in range(len(ITEMS)):
        button = InlineKeyboardButton(str(ITEMS[i]), callback_data=str(ITEMS[i]))
        buttons.append([button])

    # Add navigation buttons to the bottom of the keyboard
    prev_button = InlineKeyboardButton('Prev', callback_data=f'prev_{page}')
    next_button = InlineKeyboardButton('Next', callback_data=f'next_{page}')
    buttons.append([prev_button, next_button])

    # Create the InlineKeyboardMarkup with the buttons
    reply_markup = InlineKeyboardMarkup(buttons)


    # Send the message with the current page of items and the navigation buttons
    ff=context.bot.send_message(text=f'Page {page}:', chat_id=update.effective_chat.id, reply_markup=reply_markup)
    # query.edit_message_reply_markup(text=f'Page {page}:', chat_id=update.effective_chat.id, reply_markup=reply_markup)


def send_itemss(update, context, pages):
    global ff
    b=Ids.objects.filter(status_ID='Xat_ID')
    # print(b)
# Calculate the start and end index of the items for the current page
    start_indexx = (pages - 1) * 10
    end_indexx = start_indexx + 10
    ITEMSS=b[start_indexx:end_indexx]
    buttons = []

    for j in range(len(ITEMSS)):
        button = InlineKeyboardButton(str(ITEMSS[j]), callback_data=str(ITEMSS[j]))
        buttons.append([button])

    # Add navigation buttons to the bottom of the keyboard
    prevv_button = InlineKeyboardButton('Orqaga', callback_data=f'orqa_{pages}')
    nextt_button = InlineKeyboardButton('Oldinga', callback_data=f'oldin_{pages}')
    buttons.append([prevv_button, nextt_button])

    # Create the InlineKeyboardMarkup with the buttons
    reply_markup = InlineKeyboardMarkup(buttons)


    # Send the message with the current page of items and the navigation buttons
    ff=context.bot.send_message(text=f'Page {pages}:', chat_id=update.effective_chat.id, reply_markup=reply_markup)


global yangi, tahrir
yangi = False
tahrir = False
bolim = 0

def received_message(update: Update, context: CallbackContext):
    global yangi, tahrir, bolim
    user = update.effective_user
    msg = update.message.text
    log=Log.objects.filter(user_id=user.id).first()
    
    logi=Ids.objects.all()
    depart=Department.objects.all()
    userstat=UserInformation.objects.get(username=user.username)
    if msg=="ID yaratish" and userstat.user_status==True:
        log.state = {'state': 0}
        update.message.reply_text("ID lar yaratish", reply_markup=keyboard_buttons(type='BUTTON1'))
    elif msg=="Buyruq ID" and log.state['state'] == 0:
        update.message.reply_text(f"Buyruq ID yaratish", reply_markup=keyboard_buttons(type='orqaga'))
        log.state = {'state': 1, 'status_ID': 'Buyruq_ID'}
        update.message.reply_text("Yangi ID yoki quyidagi ko'rinishda ID lar ketma-ketligini kiriting: 1111-1120")
    elif msg=="Xat ID" and log.state['state'] == 0:
        update.message.reply_text(f"Xat ID yaratish", reply_markup=keyboard_buttons(type='orqaga'))
        log.state = {'state': 1, 'status_ID': 'Xat_ID'}
        update.message.reply_text("Yangi ID yoki quyidagi ko'rinishda ID lar ketma-ketligini kiriting: 1111-1120")


    elif msg=="⬅️Orqaga":
        log.state['state'] -= 1
        update.message.reply_text("Bosh sahifa:", reply_markup=keyboard_buttons(type='welcome'))
# and logi.status_ID=="Buyruq_ID"


    #  and logi['status_ID']=='Buyruq_ID'
    elif msg=="ID berish":
        update.message.reply_text("Yaratilgan ID larni ko'rish", reply_markup=keyboard_buttons(type='BUTTON2'))
    elif msg=="Buyruq ID lar":
        send_items(update, context, page=1)
        # paginator = Paginator(a, 10)
        # page_number = 1
        # page = paginator.page(page_number)
        # buttons = []
        # for item in page:
        #    buttons.append([InlineKeyboardButton(item.code_id, callback_data=item.code_id)])
        # if page.has_previous():
        #    buttons.append([InlineKeyboardButton("Orqaga", callback_data=f"prev_{page_number}")])
        # if page.has_next():
        #    buttons.append([InlineKeyboardButton("Oldinga", callback_data=f"next_{page_number}")])
        # keyboard = InlineKeyboardMarkup(buttons) 
        # update.message.reply_text(text="Buyruq ID lar:", reply_markup=keyboard)

 
    elif msg=="Xat ID lar":
        send_itemss(update, context, pages=1)
        # a=Ids.objects.filter(status_ID='Xat_ID')
        # button1=[]
        # for i in range(len(a)):
        #     button1.append([InlineKeyboardButton(str(a[i]), callback_data=str(a[i]))])
        # update.message.reply_text(
        #         'Xat ID lar:',
        #         reply_markup=InlineKeyboardMarkup(inline_keyboard=button1)
        #     )
        
        
    

    elif msg=="Bo'limlar":
        update.message.reply_text(f"Bo'limlar", reply_markup=keyboard_buttons(type='orqaga'))
        keyboard=[]
        for i in range(len(depart)):
            keyboard.append([InlineKeyboardButton(str(depart[i]),callback_data=f"boool_{depart[i]}")])
        keyboard.append([InlineKeyboardButton("➕ Qo'shish", callback_data="+")])
        update.message.reply_text(
                "Quyidagi bo'limlar mavjud:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        # update.callback_query.edit_message_reply_markup(None)
        # log.state['status_bol']=True
    elif msg=="Ro'yxat":
        update.message.reply_text("Yaratilgan Ro'yxatlarni ko'rish", reply_markup=keyboard_buttons(type='BUTTON3'))
    elif msg=="Xato":
        p=Department.objects.all()
        list123=[]
        for i in p:
            c=Ids.objects.filter(status="Xato").filter(userr__name=i)
            k=len(c)
            a=f"{i} bo'limida : {k} ta"
            list123.append(a)
            result = '\n'.join(list123)
        update.message.reply_text(f"Xatolar: \n\n{result}")


        # for i in c:
        # button1=[]
        # for i in range(len(c)):
        #     button1.append([InlineKeyboardButton(str(c[i]), callback_data=str(c[i]))])
        # update.message.reply_text(
        #         'ID lar',
        #         reply_markup=InlineKeyboardMarkup(inline_keyboard=button1)
        #     )
    elif msg=="Imzolanmagan":
        p=Department.objects.all()
        list123=[]
        for i in p:
            c=Ids.objects.filter(status="Imzolanmagan").filter(userr__name=i)
            k=len(c)
            a=f"{i} bo'limida : {k} ta"
            list123.append(a)
            result = '\n'.join(list123)
        update.message.reply_text(f"Imzolanmagan: \n\n{result}")

        
    elif msg=="Foydalanilmagan":
        p=Department.objects.all()
        list123=[]
        for i in p:
            c=Ids.objects.filter(status="Foydalanilmagan").filter(userr__name=i)
            k=len(c)
            a=f"{i} bo'limida : {k} ta"
            list123.append(a)
            result = '\n'.join(list123)
        update.message.reply_text(f"Foydalanilmagan: \n\n{result}")
        
     


    elif yangi == True:
        yangi = False
        list3=Department.objects.create(
                name=msg
            )
        context.bot.send_message(text=f"Quyidagi bo'lim muvaffaqiyatli hosil qilindi:✅\n\n{list3}",
            chat_id=update.effective_chat.id)
        keyboard=[]
        for i in range(len(depart)):
            keyboard.append([InlineKeyboardButton(str(depart[i]),callback_data=str(depart[i]))])
        keyboard.append([InlineKeyboardButton("➕ Qo'shish", callback_data="+")])
        update.message.reply_text(
                "Quyidagi bo'limlar mavjud:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
            )
        
    elif msg.isdigit() and log.state["state"]==255:
            tahrir = False
            t=Ids.objects.get(code_id=log.state["name"])
            t.code_id=msg
            tah=[i.user_id for i in Ids.objects.all()]
            try:
              if t not in tah:
                t.save()
                update.message.reply_text(f"ID quyidagi ko'rinishida tahrirlandi:\n\n{msg}")
            except:
              update.message.reply_text(f"Bu ID bazada mavjud:\n\n{msg}")


              


        
    elif (msg not in ["⬅️Orqaga", "Buyruq ID", "Xat ID", "ID berish"] and log.state['state'] == 1):
            try:
                if '-' in msg and msg:
                    ulist = []
                    msgi=msg.split('-')
                    for i in range(int(msgi[0]), int(msgi[1])+1):
                        list1 = Ids.objects.create(
                                code_id=i,
                                status_ID=log.state['status_ID'],
                        )
                        ulist.append(str(list1.code_id))
                    update.message.reply_text(f"Quyidagi ID lar muvaffaqiyatli hosil qilindi:👇\n\n{ulist}")
                    
                elif msg.isnumeric():
                    list2=Ids.objects.create(
                            code_id=msg,
                            status_ID=log.state['status_ID'],
                        )
                    update.message.reply_text(f"Quyidagi ID muvaffaqiyatli hosil qilindi:👇\n\n{list2}")
                else:
                    update.message.reply_text("Siz no'to'gri ma'lumot jo'natdingiz")

            except IntegrityError as e:
                if 'UNIQUE constraint' in str(e.args):
                    update.message.reply_text("Bu ID bazada mavjud")

            except Exception as e:
                # print (e)
                update.message.reply_text("ID xato formatda kiritildi, quyidagi shakllardan birida kiriting:\n\n11111\n\n11110")

        
    

    
        



    
        

    # if msg=="➕ Qo'shish":
    #     
    #     if msg and msg!="➕ Qo'shish":
            

        # if len(logi) % 2 == 0:
        #     for i in range(len(logi)-1):
        #         print(logi[i])
        #         button.append([InlineKeyboardButton(str(logi[i]), callback_data=str(logi[i]))])
        # else:
        #     for i in range(len(logi)-2):
        #         print(str(logi[i]))
        #         button.append([InlineKeyboardButton(str(logi[i]), callback_data=str(logi[i]))])
        #     # button.append([InlineKeyboardButton(str(logi[-1]), callback_data=str(logi[-1]))])
        # update.message.reply_text(
        #     'ID lar',
        #     reply_markup=InlineKeyboardMarkup(inline_keyboard=button)
        # )





    log.save()

# def send_character_page(message, page=1):
#     paginator = InlineKeyboardPaginator(
#         len(character_pages),
#         current_page=page,
#         data_pattern='character#{page}'
#     )

#     paginator.add_before(
#         InlineKeyboardButton('Like', callback_data='like#{}'.format(page)),
#         InlineKeyboardButton('Dislike', callback_data='dislike#{}'.format(page))
#     )
#     paginator.add_after(InlineKeyboardButton('Go back', callback_data='back'))

#     bot.send_message(
#         message.chat.id,
#         character_pages[page-1],
#         reply_markup=paginator.markup,
#         parse_mode='Markdown'
#     )

# def echo(bot, update):
#     # Any send_* methods return the sent message object
#     msg = update.message.reply_text("Sorry, you're on your own, kiddo.")
#     time.sleep(5)
#     # you can explicitly enter the details
#     bot.edit_message_text(chat_id=update.message.chat_id, 
#                           message_id=msg.message_id,
#                           text="Seriously, you're on your own, kiddo.")
#     # or use the shortcut (which pre-enters the chat_id and message_id behind)
#     msg.edit_text("Seriously, you're on your own, kiddo.")

def callback(update, context):
    global ff
    user = update.effective_user
    log=Log.objects.filter(user_id=user.id).first()
    global yangi, bolim, o, aa
    msg = update.callback_query.data
    if msg == '+':
        yangi = True
        context.bot.send_message(text="Yangi bo'lim nomini kiriting", chat_id=update.effective_chat.id)


    elif msg.isdigit():
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=ff.message_id)
        print(msg)
        a=[str(i) for i in Ids.objects.filter()]
        # print(a)
        bolim = a.index(msg)
        log.state["name"]=msg
        keyboard = [[InlineKeyboardButton('Tahrirlash', callback_data='tahrir'), InlineKeyboardButton('O\'chirish', callback_data='ochir'), InlineKeyboardButton('Bo\'lim', callback_data='bol')]]
        o=context.bot.send_message(text=f"{msg}", chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    

    elif msg=="tahrir":
        log.state["state"]=255
        # tahrir = True
        context.bot.send_message(text="Tahrirlang", chat_id=update.effective_chat.id)
    
    elif msg=='ochir':
        b = Ids.objects.filter()
        b[bolim].delete()
        context.bot.send_message(text="ID muvaffaqiyatli o'chirildi!", chat_id=update.effective_chat.id)
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=o.message_id)

    elif msg=="bol":
        j=Department.objects.all()
        keyboaard=[]
        for i in range(len(j)):
            keyboaard.append([InlineKeyboardButton(str(j[i]),callback_data=f"boltan_{j[i]}")])
        context.bot.send_message(
                text="Bo'limlardan birini tanlang:", chat_id=update.effective_chat.id,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboaard)
            )
        
    elif msg and msg.startswith('boltan_'):
        msgg=str(msg.split('_')[1])
        id = Ids.objects.get(code_id=log.state['name'])
        bol = Department.objects.get(name=msgg)
        # print(id)
        # print(bol)
        id.userr = bol
        id.save()
        context.bot.send_message(text=f"{id} {bol} bo'limiga muvaffaqiyatli saqlandi.✅", chat_id=update.effective_chat.id)



    elif msg and msg.startswith('boool_'):
        try:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=aa.message_id)
        except:
            pass
        msgg=str(msg.split('_')[1])
        print(msgg)
        q=Ids.objects.filter(userr__name=msgg)
        button1=[]
        for i in range(len(q)):
            button1.append([InlineKeyboardButton(str(q[i]),callback_data=f"butt_{q[i]}")])
        aa=context.bot.send_message(
                text=f"{msgg} bo'limiga tegishli ID lar:", chat_id=update.effective_chat.id,
                reply_markup=InlineKeyboardMarkup(inline_keyboard=button1)
            )
        
        


    elif msg and msg.startswith('butt_'):
        # print(msg)
        mssg=str(msg.split('_')[1])
        log.state["raqam"]=mssg
        b=[str(i) for i in Ids.objects.filter()]
        bolim = b.index(mssg)
        keyboard = [[InlineKeyboardButton('Status', callback_data='stat')]]
        context.bot.send_message(text=f"{mssg}", chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=aa.message_id)

    

    elif msg=="stat":
        
        keyboard = [[InlineKeyboardButton('Xato', callback_data='xat'), InlineKeyboardButton('Imzolanmagan', callback_data='imzo'), InlineKeyboardButton('Foydalanilmagan', callback_data='foyda')]]
        context.bot.send_message(text=f"{log.state['raqam']} ni qaysi ro'yhatga qo'shmoqchisiz?", chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
        # log.state['roy']=msg
        # print(log.state['roy'])

        # idddd=Ids.objects.get(code_id=log.state['raqam'])
        # idddd.status=msg
        # idddd.save()
        # context.bot.send_message(text="ID ro'yhatga muvaffaqiyatli saqlandi", chat_id=update.effective_chat.id)


    elif msg=='xat':
        idddd=Ids.objects.get(code_id=log.state['raqam'])
        idddd.status='Xato'
        idddd.save()
        context.bot.send_message(text="ID Xatolar ro'yxatiga muvaffaqiyatli saqlandi.✅", chat_id=update.effective_chat.id)



    elif msg=='imzo':
        idddd=Ids.objects.get(code_id=log.state['raqam'])
        idddd.status='Imzolanmagan'
        idddd.save()
        context.bot.send_message(text="ID Imzolanmaganlar ro'yxatiga muvaffaqiyatli saqlandi.✅", chat_id=update.effective_chat.id)

    

    elif msg=='foyda':
        idddd=Ids.objects.get(code_id=log.state['raqam'])
        idddd.status='Foydalanilmagan'
        idddd.save()
        context.bot.send_message(text="ID Foydalanilmaganlar ro'yxatiga muvaffaqiyatli saqlandi.✅", chat_id=update.effective_chat.id)



        # print(log.state['roy'])
        # idddd=Ids.objects.get(code_id=log.state['raqam'])
        # idddd.status=log.state['roy']
        # idddd.save()
        # context.bot.send_message(text="ID ro'yhatga muvaffaqiyatli saqlandi", chat_id=update.effective_chat.id)
        
            
    # elif msg and msg.startswith('boltan_'):
    #     msgg=str(msg.split('_')[1])
    #     id = Ids.objects.get(code_id=log.state['raqam'])
    #     bol = Department.objects.get(name=msgg)
    #     print(id)
    #     print(bol)
    #     id.userr = bol
    #     id.save()
    #     context.bot.send_message(text="ID bo'limga muvaffaqiyatli saqlandi", chat_id=update.effective_chat.id)

        # use = [i.name for i in Department.objects.all()]
        # if msg in use:
        # # if msg!='tan':
        #     print(msg)
        #     Ids.objects.create(
        #         userr=msg
        #     )
        #     print(msg)
        #     context.bot.send_message(text="ID bo'limga muvaffaqiyatli saqlandi", chat_id=update.effective_chat.id)

        # u = [i.name for i in Department.objects.all()]
        # print(u)
        # context.bot.send_message(text=f"Quyidagi bo'limlardan birini kiriting:\n\n{u}", chat_id=update.effective_chat.id)
        # if msg and msg!="bol":
        #     save=Department.objects.create(
        #         name=msg
        #     )
        #     use = [i.name for i in Department.objects.all()
        #     if msg in use:
        #        save.save()
        #     context.bot.send_message(text="ID bo'limga muvaffaqiyatli saqlandi", chat_id=update.effective_chat.id)





    
    elif msg.startswith('prev'):
        # Send the previous page of items
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=ff.message_id)
        send_items(update, context, page=int(msg[msg.find('_')+1:])-1)
    elif msg.startswith('next'):
        # Send the next page of items
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=ff.message_id)
        send_items(update, context, page=int(msg[msg.find('_')+1:])+1)

    elif msg.startswith('orqa'):
        # Send the previous page of items
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=ff.message_id)
        send_itemss(update, context, pages=int(msg[msg.find('_')+1:])-1)
    elif msg.startswith('oldin'):
        # Send the next page of items
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=ff.message_id)
        send_itemss(update, context, pages=int(msg[msg.find('_')+1:])+1)




    log.save()








        # a=[str(i) for i in Ids.objects.filter()]
        # print(a)
        # bolim = a.index(msg)
        # keyboard = [[InlineKeyboardButton('Status', callback_data='stat')]]
        # context.bot.send_message(text=f"{msg}", chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))



        




def keyboard_buttons(type=None):
    btn = []
    if type == 'welcome':
        for i in range(0, len(WELCOME) - 1, 2):
            btn.append([KeyboardButton(WELCOME[i]), KeyboardButton(WELCOME[i + 1])])
        if len(WELCOME) % 2 != 0:
            btn.append([KeyboardButton(WELCOME[-1])])
    elif type == 'BUTTON1':
        for i in range(0, len(BUTTON1) - 1, 2):
            btn.append([KeyboardButton(BUTTON1[i]), KeyboardButton(BUTTON1[i + 1])])
        if len(BUTTON1) % 2 != 0:
            btn.append([KeyboardButton(BUTTON1[-1])])
        btn.append([KeyboardButton("⬅️Orqaga")])
    elif type == 'BUTTON2':
        for i in range(0, len(BUTTON2) - 1, 2):
            btn.append([KeyboardButton(BUTTON2[i]), KeyboardButton(BUTTON2[i + 1])])
        if len(BUTTON2) % 2 != 0:
            btn.append([KeyboardButton(BUTTON2[-1])])
        btn.append([KeyboardButton("⬅️Orqaga")])
    elif type == 'BUTTON3':
        for i in range(0, len(BUTTON3) - 1, 2):
            btn.append([KeyboardButton(BUTTON3[i]), KeyboardButton(BUTTON3[i + 1])])
        if len(BUTTON3) % 2 != 0:
            btn.append([KeyboardButton(BUTTON3[-1])])
        btn.append([KeyboardButton("⬅️Orqaga")])

    elif type == "orqaga":
        btn = [[KeyboardButton("⬅️Orqaga")]]
    elif type == "Bosh sahifa":
        btn = [[KeyboardButton("Bosh sahifa")]]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)









































# from django.shortcuts import render
# from aiogram import Bot,types
# from aiogram.utils import executor
# from aiogram.dispatcher import Dispatcher
# from .models import Ids,UserInformation
# from aiogram.types import ReplyKeyboardRemove, \
#     ReplyKeyboardMarkup, KeyboardButton, \
#     InlineKeyboardMarkup, InlineKeyboardButton
# import config as cfg
# import logging
# import requests
# button1=KeyboardButton("ID berish")
# button2=KeyboardButton("Xatolar")
# button3=KeyboardButton("Imzolangan")
# button4=KeyboardButton("Natija")
# button5=KeyboardButton("⬅️Orqaga")
# buttons=ReplyKeyboardMarkup().row(button1,button2).row(button3,button4)
# buttons1=ReplyKeyboardMarkup().add(button5)

# # Create your views here.
# TOKEN="6244919959:AAH98ylnVENOm6mF7WFwIF2Ah8-ayMzY_y4"

# bot=Bot(token=TOKEN)
# dp=Dispatcher(bot)


# @dp.message_handler(commands=['start'])
# async def start(message:types.Message):
#     await bot.send_message(message.from_user.id,'Assalomu aleykum  bot xush kelibsiz',reply_markup=buttons)
#     # await message.answer(message.text)





# @dp.message_handler()
# async def start(message:types.Message):
#     if message.text=='ID berish':
#           await message.reply("Yangi ID yoki quyidagi ko'rinishda ID lar ketma-ketligini kiriting: 1111-1120",reply_markup=buttons1)
#           Ids.objects.create(
#           code_id=message.text
#           )






# @dp.message_handler()
# async def echo(message:types.Message):
#     await message.answer(message.text)













# executor.start_polling(dp,skip_updates=True)
