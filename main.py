import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

TOKEN = "8302215113:AAGQGQo1uvQZ1XTNSN95UIA6ZHbwtDgUweQ"

dp = Dispatcher(storage=MemoryStorage())


class BotSteps(StatesGroup):
  video_step = State()
  joke_step = State()


VIDEOS = [
    "https://www.youtube.com/shorts/yztuTuipM5E",
    "https://www.youtube.com/shorts/uUOpURcjROY",
    "https://www.youtube.com/shorts/jz51XRzcry8?feature=share",
    "https://www.youtube.com/shorts/J1BWlaCLowA?feature=share",
    "https://www.youtube.com/shorts/mjLbvt7wIq8",
    "https://www.youtube.com/shorts/GX97uhAb_4A?feature=share",
    "https://www.youtube.com/shorts/J9Gi8i6gJ3I?feature=share",
    "https://www.youtube.com/shorts/_5MMrMSpJS0?feature=share",
    "https://www.youtube.com/shorts/DTxdKkwRvoM?feature=share",
    "https://www.youtube.com/shorts/oTFUVW8_A4c?feature=share",
    "https://www.youtube.com/shorts/7IoCb_eoxlQ?feature=share",
    "https://www.youtube.com/shorts/CTcRPhIqX8I?feature=share",
    "https://www.youtube.com/shorts/qj2QbrL_kw8?feature=share",
    "https://youtu.be/jY98EwB1IJQ",
    "https://youtu.be/qZ9ZpSn3eOs",
    "https://youtu.be/9zvFQDqxiZM",
    "https://youtu.be/FNjWoKRKe6s",
]

JOKES = [
    (
        "1. UYLANIŞ VA VADA\n\nBir yigit uylanishidan oldin bo'lajak"
        " qaynonasining oldiga kelib, o'zining qanchalik saxiy va odobli"
        " ekanligini ko'rsatmoqchi bo'libdi:\n— Onajon, qizingizni menga"
        " bersangiz, uni kaftimda ko'tarib yuraman! Har kuni tillolarga"
        " ko'maman, dunyoni aylantiraman, har aytganini muhokamasiz"
        " bajaraman!\n\nTo'y o'tibdi. Aradan olti oy o'tgach, qaynona"
        " kuyovnikiga mehmon bo'lib kelibdi. Qarasa, qizi oshxonada idish"
        " yuvyapti, pollarni arziyapti, kuyov esa divanda yotib olib televizor"
        " ko'ryapti.\n\nQaynona jahli chiqib kuyovga debdi:\n— Ie, uylanishdan"
        " oldin bergan va'dalaringiz qani? Qizimni kaftimda ko'taraman"
        " degandingiz-ku!\n\nKuyov xotirjamlik bilan boshini ko'tarib:\n— E,"
        " onajon, u paytda qizingiz 50 kilo edi! Hozir 85 kilo bo'lib ketdi,"
        " uning o'zi bir tomonga, kaftim bir tomonga ketib qoladi-ku!"
    ),
    (
        "2. BOZORDA TARVUZ SOTISH\n\nBozorda bir sotuvchi tarvuz sotib"
        " o'tirgan ekan. Oldiga bir chortroq xaridor kelib, tarvuzni urib-urib"
        " ko'ribdi-da, so'rabdi:\n— Aka, bu tarvuzingiz shirinmi? Ichida g'o'ri"
        " yo'qmi o'zi?\n— Sotuvchi: E, aka! Bu tarvuz shunday shirin, shunday"
        " mazali-ki, bittasini yesangiz, dardingiz qolmaydi! Shakar"
        " qilganday!\n\nXaridor tarvuzni sotib olib, uyiga borib so'ysa, ichi"
        " bemaza, oq va umuman shakari yo'q ekan. Jahli chiqib, tarvuzni ko'tarib"
        " yana bozorga kelibdi:\n— Ey sotuvchi! Meni aldaysanmi? Qani bu yerdagi"
        " shakar? Ichi oq, bemaza-ku!\n\nSotuvchi xotirjam tarvuzga qarap debdi:\n—"
        " Aka, u tarvuz emas, u shunchaki tarvuzning po'stlog'i edi-da! Ichidagi"
        " hamma shakarni boya sizga aytayotganimda og'zimdan chirib chiqib"
        " ketgan edi-da!"
    ),
    (
        "3. SHIFOKOR VA BEMOR\n\nShifokor qabuliga juda g'alati bemor"
        " kirib kelibdi. Yuzlari g'amgin, ko'zlari shishgan.\n— Do'xtirjon,"
        " menga yordam bering! Har kuni kechasi uxlasam, tushimda ayiqlar kelib"
        " men bilan shaxmat o'ynayapti! Yutqazsam, meni o'rmon bo'ylab"
        " quvlaydi. Charchab o'lib bo'ldim, uxlashga ham qo'rqaman!\n\nShifokor"
        " unga qarab:\n— Mana bu dorini iching, bugun kechasi tinchgina"
        " uxlaysiz, tushingizga hech qanday ayiq ham, shaxmat ham kirmaydi!\n\nBemor"
        " dorini qo'liga olib, biroz o'ylanib turibdi-da, debdi:\n— Do'xtir,"
        " shu dorini ertagadan ichishni boshlasam bo'ladimi?\n— Nega?"
        " Bugunoq ichishingiz kerak-ku!\n— Axir bugun final o'yini bor-da,"
        " guruhdan chiqib bo'ldim, endi tashlab qochsam uyat bo'ladi!"
    ),
    (
        "4. SUD VA ER-XOTIN\n\nSudda 40 yil birge yashagan er-xotinning"
        " ajrashish davosi ko'rilayotgan ekan. Sudya hayron bo'lib"
        " so'rabdi:\n— Ota, ona! 40 yil birga yashabsizlar, bir-biringizga"
        " suyanib umr o'tkazibsizlar. Nima sabab bo'ldi-ki, shuncha yildan"
        " keyin ajrashishga qaror qildingizlar?\n\nOta og'ir xo'rsinib"
        " debdi:\n— Hukmron sudya shifokor! Mana bu xotinim bilan 40 yildan"
        " beri yashaydigan bo'lsam, har kuni choy ichayotganimda 'qoshiqni"
        " pialadan olib qo'y' deb baqiradi!\n\nSudya onaga qarab debdi:\n— Ona,"
        " nahotki shunday kichkina narsa uchun eringizning dilini og'ritib"
        " kelsangiz?\n\nOna yig'lamoqdan beri bo'lib debdi:\n— Sudya aka, 40"
        " yildan beri aytaman! Qoshiqni piyoladan olmasa, ko'ziga kirib"
        " ketadi-ku, men u kishining ko me'yoriy ko'rishini o'ylayman-da!"
    ),
    (
        "5. POLISYA VA HAYDOVCHI\n\nTungi soat 3 da YHXX xodimi yo'lda zigzag"
        " chizib ketayotgan mashinani to'xtatibdi. Ichidan kayfi joyida bo'lgan"
        " haydovchi tushibdi.\n— Avtomobilni nega bunday xavfli boshqarayapsiz?"
        " Hujjatlaringizni ko'rsating!\n— Aka, ishonasizmi, ro'paramdan birdan"
        " daraxt chiqib qoldi! Chapga burdim — yana daraxt! O'ngga burdim —"
        " yana daraxt! Qochay deb arang boshqardim!\n\nXodim mashina ichiga"
        " mo'ralab qaradi-da, debdi:\n— Aka, darhol ro'parangizdagi mashina"
        " oynasidagi xushbo'ylatgich (osilib turgan archacha)ni olib ko'rsangiz"
        " bo'larkan, yo'lingizda hech qanday daraxt yo'q!"
    ),
    (
        "6. MAKTABDA TEKSHIRUV\n\nMaktabga viloyatdan katta inspektor"
        " kelibdi. 4-sinfga kirib, o'quvchilarning bilimini tekshirish uchun"
        " so'rabdi:\n— Xo'sh, bolalar, aytinglar-chi, 'O'tkan kunlar' asarini"
        " kim yozgan?\n\nSinfda jim-jitlik. Barchaning boshi quyi."
        " Ketma-ket o'tirgan Eshmat o'rnidan turib, titrab debdi:\n— Ustoz,"
        " xudoga qasam, men yozganim yo'q! Kecha kechasi bilan uyda dars"
        " tayyorladim!\n\nInspektorning jahli chiqib, o'qituvchiga qarasa,"
        " o'qituvchi yelka qisib debdi:\n— Inspektor aka, bu bolani tanıymiz,"
        " juda to'g'ri so'z bola. Agar 'men yozmadim' dedimi, demak rostdan u"
        " yozmagan!"
    ),
    (
        "7. QO'SHNILAR SUHBATI\n\nIkki qo'shni hovlida gurunglashib"
        " o'tirishgan ekan. Biri ikkinchisiga xavas bilan qarab"
        " debdi:\n— Qo'shni, sizning xotiningiz juda ajoyib-da! Har kuni"
        " ertalab sizga shirin so'zlar aytadi, kiyimlaringizni dazmollab"
        " beradi, ishga kuzatayotganda bag'riga bosadi. Bunga qanday"
        " erishgansiz?\n\nIkkinchi qo'shni sekin pichirlab debdi:\n— Juda"
        " oddiy! O'tgan yili uyimizga o'g'ri tushganida, xotinim o'g'riga"
        " qarab 'meni olib ket, erimni teginma' deb baqirgan edi. Men esa"
        " o'g'riga sekin 'dostim, ikkalamizga ham joy yetadi' deb javob bergan"
        " edim. Shundan beri xotinim menga juda mehribon!"
    ),
    (
        "8. RESTORANDA MEHMON\n\nQimmat restoranga bir kishi kirib,"
        " eng qimmat taomni buyurtma qilibdi. Ofitsiant taomni olib kelib"
        " stolda qoldiribdi. Mehmon ovqatni yeyishni boshlaganda, uning"
        " ichidan bitta pashsha chiqib qolibdi!\n\nJahli chiqqan mehmon"
        " ofitsiantni chaqiribdi:\n— Bu nima degani?! Mavlono, mening"
        " sho'rbamda pashsha suzib yuribdi-ku!\n\nOfitsiant taomga diqqat"
        " bilan qarab, tabassum bilan debdi:\n— Bosh egam, shunaqa ham"
        " sho'x-a! Shuncha qimmat taom turganda, u atigi suzish bilan"
        " band-a!"
    ),
    (
        "9. ELEKTRİK VA SHOGIRD\n\nUsta elektrik yangi binoda yuqori"
        " kuchlanishli simlarni ulayotgan ekan. Yoni kelgan yangi shogirdiga"
        " ikkita simni ko'rsatib debdi:\n— Shogird, ushbu ikkala simdan bittasini"
        " qo'ling bilan ushlab tur-chi!\n\nShogird simni ushlabdi."
        " Usta so'rabdi:\n— Xo'sh, biror narsa sezdingmi? Tok urdimi?\n—"
        " Yo'q, usta, hech narsa sezmadim.\n— Juda soz! Demak, anavi ikkinchi"
        " simga umuman tegib bo'lmas ekan, u 10.000 voltli sim!"
    ),
    (
        "10. O'G'RI VA UY EGGASI\n\nTunda uyga o'g'ri kiribdi. Sandiqlarni"
        " titib, javonlarni ochib, pul va qimmatbaho buyumlarni qidirayotgan"
        " ekan. Shunda to'satdan qorong'uda uy egasining ovozi eshitilibdi:\n—"
        " Birodar, behuda vaqtingni ketkazma!\n\nO'g'ri cho'chib tushib,"
        " pichoqni to'g'rilabdi:\n— Kim bor? Jim tur, bo'lmasa so'yaman!\n\nUy"
        " egasi divanda yotganicha xotirjam debdi:\n— Men shu uyning egasiman."
        " Kunduzi yorug'da o'zim topolmagan pulni, sen qorong'uda qanday"
        " topmoqchisan? Yana topsang, menga ham yarmini bergin!"
    ),
    (
        "11. PARASHYUTCHILAR\n\nSamolyotdan birinchi marta parashyutdan"
        " sakrayotgan uchta do'st havoda uchib borishayotgan ekan. Biri"
        " ipni tortsa, parashyut ochilmabdi!\n\nU ikkinchi do'stiga baqiribdi:\n—"
        " Mening parashyutim ochilmayapti! Nima qilay?\n\nIkkinchi do'st"
        " ham ipni tortib ko'rib, debdi:\n— Voy, mening ham parashyutim"
        " ochilmayapti! Uchinchisidan so'ra!\n\nUchinchi do'stlariga yetib"
        " kelib, kulib debdi:\n— Ey ahmoqlar, axir bu parashyutdan sakrash"
        " mashg'uloti emas, bu samolyot halokatga uchramoqda, tezroq yerga"
        " yetib olishimiz kerak!"
    ),
    (
        "12. DOKTOR VA AQLSIZLAR\n\nRuhshunos shifokor ruhiy kasalxonadagi"
        " bemorlarni tekshirayotgan ekan. Bemorlar hovlida suv qo'yilmagan"
        " bo'sh basseynga ketma-ket sakrab, mazza qilib 'suzishyapti'."
        "\n\nFaqat bir bemor chetda, daraxt tagida g'amgin o'tirgan ekan."
        " Shifokor xursand bo'lib, 'buning miyasi joyiga kelibdi' deb yoniga"
        " boribdi:\n— Sen nega u joyga borib suzmayapsan?\n\nBemor unga qarab"
        " pichirlabdi:\n— Do'xtirjon, men ularga o'xshab ahmoq emasman! Hozir"
        " suzmayman, chunki men hali suvning haroratini o o'lchaganim yo'q!"
    ),
    (
        "13. ZIYOFA T VA DO'STLAR\n\nUchta oshna choyxonada o'tirib"
        " o'z xotinlaridan shikoyat qilishayotgan ekan. Birinchisi debdi:\n—"
        " Mening xotinim shunday injiq, kun bo'yi uyni yig'ishtiradi, baribir"
        " biror narsadan ayb topadi!\n\nIkkinchisi debdi:\n— Mening xotinim"
        " undan ham o'tib tushadi, har kuni yangi kiyim olib bermasangiz"
        " janjal qiladi!\n\nUchinchisi og'ir xo'rsinib debdi:\n— E do'stlar,"
        " sizlar baxtli ekansizlar! Mening xotinim umuman gapirmaydi..."
        "\n— Ie, bu zo'r-ku! Tinchlik bo'ladi-da!\n— Qaydanam zo'r bo'lsin,"
        " u faqat qosh-ko'zi bilan buyruq beradi, tushunmay qolsam — kaltak"
        " yeyman!"
    ),
    (
        "14. IMTIHON VA TALABA\n\nTalaba imtihonga umuman tayyorlanmasdan"
        " kiribdi. Professor unga qarab so'rabdi:\n— Xo'sh, yigit! Bitta ham"
        " savolga javob bera olmadingiz. Sizga bitta imkoniyat beraman:"
        " mening stolimda nechta chiroq yonib turibdi?\n\nTalaba sanoqni"
        " boshlabdi:\n— Bitta, ikkita, uchta... Jami 4 ta chiroq, ustoz!\n\nProfessor"
        " kulib debdi:\n— Noto'g'ri! Stolimda atigi 3 ta chiroq bor. Siz"
        " yiqildingiz!\n\nTalaba cho'ntagidan o'zining fonarchasini olib"
        " yoqibdi-da debdi:\n— Mana endi rosa 4 ta bo'ldi, ustoz! '5' bahoni"
        " qo'yaversangiz bo'ladi!"
    ),
    (
        "15. TAKSIST VA O'ZBEK\n\nTaksida ketayotgan yo'lovchi haydovchining"
        " yelkasiga sekin teginib so'rabdi:\n— Aka, vokzalga yetishga hali"
        " ko'p bormi?\n\nTaksist birdan baland ovozda baqirib, rulni qo'yib"
        " yuboribdi, mashina yo'l chetidagi ariqga tushib ketishiga sal"
        " qolibdi. Xayriyatki, to'xtabdi.\n\nTaksist pishillab debdi:\n—"
        " Aka, qarindosh, ikkinchi marta bunday qilmang! Yuragim yorilib"
        " o'lay dedim!\n\nYo'lovchi hayron bo'lib debdi:\n— Atigi yelkangizga"
        " tegindim-ku, shunga shunchalikmi?\n\nTaksist debdi:\n— Kechirasiz,"
        " men bugun birinchi marta taksi haydayapman! Oxirgi 20 yil davomida"
        " katafalk (murdalarni tashish mashinasi) haydovchisi bo'lib"
        " ishlaganman!"
    ),
    (
        "16. DORS VA O'QUVCHI\n\nO'qituvchi darsda o'quvchiga savol beribdi:\n—"
        " Bolam, ayting-chi, agar sen bir cho'ntagingdan 50 ming so'm, ikkinchi"
        " cho'ntagingdan 100 ming so'm topsang, nima bo'ladi?\n\nO'quvchi"
        " o'ylanmasdan debdi:\n— Ustoz, men boshqa birovning shimini kiyib"
        " olgan bo'laman!"
    ),
    (
        "17. YORT VA BO'YDOG'ILIK\n\nIkki bo'ydoq do'st suhbatlashyapti:\n—"
        " Jo'ra, uylangandan keyin hayot rostdan ham o'zgaradimi?\n— Albatta!"
        " Masalan, ilgarilari uyga kelsam, muzlatgichni ochib ko'rardim —"
        " hech narsa yo'q, keyin xafachilikdan o'ringa yotardim.\n— Hozir-chi?\n—"
        " Hozir uyga kelsam, xotinim o'rinda yotgan bo'ladi, keyin xafachilikdan"
        " muzlatgichni ochaman — baribir hech narsa yo'q!"
    ),
    (
        "18. OILAAVIY SAYOHAT\n\nEr-xotin dengiz bo'yiga dam og'ani"
        " borishibdi. Xotini suvga tushib suza boshlabdi, er esa qirg'oqda"
        " yotibdi. To'satdan xotini cho'kishni boshlab, baqiribdi:\n— Dadasiga,"
        " yordam bering! Cho'kyapman, akulalar kelayapti!\n\nEri o'rnidan"
        " ham turmasdan debdi:\n— Xotinjon, xavotir olma! Akulalar ham"
        " insofli hayvonlar, ular ham xom go'sht yeyishmaydi!"
    ),
    (
        "19. BOZOR VA SOTUVCHI\n\nBozorda kiyim sotayotgan ayol xaridorga"
        " shart qo'yyapti:\n— Opa, bu ko'ylak sizga shunday yarashdi-ki,"
        " xuddi siz uchun tikilgandek! Olmasangiz uvol bo'ladi!\n\nXaridor"
        " kiyib ko'rib debdi:\n— Lekin bu ko'ylak menga biroz torlik"
        " qilyapti-ku?\n\nSotuvchi tirjayib debdi:\n— E opa, tor bo'lsa"
        " ozasiz-da! Sizga ham foyda, menga ham savdo!"
    ),
    (
        "20. TAFFAKKUR VA AQL\n\nIkki o'rtoq koinot haqida bahslashmoqda:\n—"
        " Oyda odamlar yashaydi deb o'ylaysanmi?\n— Yo'q, albatta! Yashagandada,"
        " u yoqda chiroq o'chganda bizga ham ko'rinardi-ku!"
    ),
]


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
  await state.clear()
  await message.answer(
      f"Salom, {html.bold(message.from_user.full_name)}! Kulishni xohlasangiz"
      " 'ketdik' deb yozing 😊"
  )


@dp.message(F.text.lower().in_({"ketdik", "ketik", "кетдик", "кетик"}))
async def ketdik_handler(message: Message, state: FSMContext) -> None:
  await state.set_state(BotSteps.video_step)
  await state.update_data(current_video=0)

  await message.answer(
      text=(
          "Mana birinchi video! Yana ko'rish uchun 'yana' deb"
          f" yozing:\n{VIDEOS[0]}"
      )
  )


@dp.message(BotSteps.video_step, F.text.lower().in_({"yana", "яна"}))
async def yana_handler(message: Message, state: FSMContext) -> None:
  data = await state.get_data()
  current_video = data.get("current_video", 0) + 1

  if current_video < len(VIDEOS):
    await state.update_data(current_video=current_video)
    await message.answer(
        text=(
            "Mana shu ham bor! Yana xohlasangiz 'yana' deb"
            f" yozing:\n{VIDEOS[current_video]}"
        )
    )
  else:
    await state.clear()
    await message.answer(
        text=(
            "Barcha 17 ta videolar tugadi! Maza qilib kulib oldingiz deb"
            " o'ylayman. Ana endi uzun va juda kulgili yozma latifalarga"
            " o'tamiz, bo'ladimi? 'ha' yoki 'yo'q' deb javob bering."
        )
    )


@dp.message(F.text.lower().in_({"ha", "ха"}))
async def ha_handler(message: Message, state: FSMContext) -> None:
  await state.set_state(BotSteps.joke_step)
  await state.update_data(current_joke=0)

  await message.answer(
      text=(
          f"{JOKES[0]}\n\nKeyingi latifa uchun 'keyingi' deb yozing (yoki 'g')"
      )
  )


@dp.message(
    BotSteps.joke_step, F.text.lower().in_({"keyingi", "кейинги", "g", "г"})
)
async def keyingi_anekdot_handler(message: Message, state: FSMContext) -> None:
  data = await state.get_data()
  current_joke = data.get("current_joke", 0) + 1

  if current_joke < len(JOKES):
    await state.update_data(current_joke=current_joke)
    await message.answer(
        text=(
            f"{JOKES[current_joke]}\n\nKeyingi latifa uchun 'keyingi' deb"
            " yozing 😊"
        )
    )
  else:
    await state.clear()
    await message.answer(
        text=(
            "Barcha 20 ta uzun va kulgili latifalar tugadi! Umid qilaman sizga"
            " juda yoqdi 😃\nBoshidan boshlash uchun /start bosing."
        )
    )


@dp.message(F.text.lower().in_({"yo'q", "yoq", "йок", "йоқ"}))
async def yoq_handler(message: Message, state: FSMContext) -> None:
  await state.clear()
  await message.answer(text="Mayli, ko'rishamiz 👋")


@dp.message()
async def echo_handler(message: Message) -> None:
  await message.answer(text="Boshlash uchun 'ketdik' deb yozing 🥺")


async def main() -> None:
  bot = Bot(
      token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
  )

  # Webhook'ni o'chirib, polling'ga yo'l ochamiz
  await bot.delete_webhook(drop_pending_updates=True)

  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())



# import asyncio
# import logging
# import sys
# from os import getenv

# from aiogram import Bot, Dispatcher, html , F , types
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message

# TOKEN = "8302215113:AAGQGQo1uvQZ1XTNSN95UIA6ZHbwtDgUweQ"

# dp = Dispatcher()

# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:

#     await message.answer(f"salom, {html.bold(message.from_user.full_name)} kulishni xoxlasangiz 'ketik' deb yozing ")


# @dp.message(F.text.lower().in_({"Salom", "salom","салом","Салом"}))
# async def salom_handler(message: Message) -> None:
#     await message.answer(text=f"salom, {html.bold(message.from_user.last_name)}")

# @dp.message(F.text.lower().in_({"ketdik", "ketik", "кетдик", "кетик"}))
# async def ketdik_handler(message: Message) -> None:
#     await message.answer_photo(
#         caption="Mana sizga vidio, yana xohlasangiz 'yana' deb yozing: https://www.youtube.com/shorts/yztuTuipM5E"
#     )

# @dp.message(F.text.lower().in_({"yana", "янан"}))
# async def yana_handler(message: Message) -> None:
#     await message.answer_photo(
#         caption="Mana, kechirasiz men bitta so'zga qilolmayman 😔 https://www.youtube.com/shorts/uUOpURcjROY?feature=share"
#     )

# @dp.message()
# async def echo_handler(message: Message) -> None:
#     await message.answer(text="oka boshlash uchin 'ketik' deb yozing iltimos sizdan🥺")
# async def main() -> None:
  
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())


# import asyncio
# import logging
# import sys
# from os import getenv

# from aiogram import Bot, Dispatcher, html, F, types
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.types import Message

# TOKEN = "8302215113:AAGQGQo1uvQZ1XTNSN95UIA6ZHbwtDgUweQ"

# dp = Dispatcher()

# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(f"salom, {html.bold(message.from_user.full_name)} kulishni xoxlasangiz 'ketdik' deb yozing ")

# @dp.message(F.text.lower().in_({"salom", "салом"}))
# async def salom_handler(message: Message) -> None:
#     last_name = message.from_user.last_name or ""
#     await message.answer(text=f"salom, {html.bold(last_name)}")

# @dp.message(F.text.lower().in_({"ketdik", "ketik", "кетдик", "кетик"}))
# async def ketdik_handler(message: Message) -> None:
#     await message.answer(text="Mana sizga video! Yana xohlasangiz 'yana' deb yozing:\nhttps://www.youtube.com/shorts/yztuTuipM5E")

# @dp.message(F.text.lower().in_({"yana", "яна"}))
# async def yana_handler(message: Message) -> None:
#     await message.answer(text="Mana shu yana hohlasangiz b deb yozing yana bor juda ko'p: https://www.youtube.com/shorts/uUOpURcjROY")

# @dp.message(F.text.lower().in_({"B","b","Б","б"}))
# async def b_handler(message: Message) -> None:
#     await message.answer(text="Mana shu yana hohlasangiz c deb yozing yana bor juda ko'p: https://www.youtube.com/shorts/jz51XRzcry8?feature=share")

# @dp.message(F.text.lower().in_({"C","c", "С","с" }))
# async def c_handler(message: Message) -> None:
#     await message.answer(text="Mana shu yana hohlasangiz d deb yozing yana bor : https://www.youtube.com/shorts/J1BWlaCLowA?feature=share")

# @dp.message(F.text.lower().in_({"D", "d" "Д","д"}))
# async def d_handler(message: Message) -> None:
#     await message.answer(text="Mana shu yana f deb yozing vidio ham bor endi tema boshqacha endi Million:https://youtu.be/mjLbvt7wIq8 ")

# @dp.message(F.text.lower().in_({"F", "f", "Ф" , "ф"}))
# async def c_handler(message: Message) -> None:
#     await message.answer(text="Mana shu yana hohlasangiz 'u' deb yozing yana bor : https://www.youtube.com/shorts/GX97uhAb_4A?feature=share")

# @dp.message(F.text.lower().in_({"U","u","У","у" }))
# async def u_handler(message: Message) -> None:
#     await message.answer(text="Mana shu yana hohlasangiz 'a' deb yozing yana bor : https://www.youtube.com/shorts/J9Gi8i6gJ3I?feature=share")

# @dp.message(F.text.lower().in_({"A","a","а","а" }))
# async def u_handler(message: Message) -> None:
#     await message.answer(text="Mana maza qilib kulib oldiz deb oilayman ana endi yozma anigdotlarga otamiz boladimi ha yoki yoq deb jovob bering")

# @dp.message(F.text.lower().in_({"Yo'q","yo'q","йок","Йок" }))
# async def u_handler(message: Message) -> None:
#     await message.answer(text="mayli ko'rishamiz")

# @dp.message(F.text.lower().in_({"ha","ha","Ха","ха" }))
# async def u_handler(message: Message) -> None:
#     await message.answer(text="bo'lmasa davom etamis")

# @dp.message(F.text.lower().in_({"E","e","Е","е" }))
# async def u_handler(message: Message) -> None:
#     await message.answer(text="bo'lmasa davom etamis")
    

# @dp.message()
# async def echo_handler(message: Message) -> None:
#     await message.answer(text="Oka boshlash uchun 'ketdik' deb yozing iltimos sizdan 🥺")

# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     await dp.start_polling(bot)

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
# import asyncio
# import logging
# import sys

# from aiogram import Bot, Dispatcher, F, html
# from aiogram.client.default import DefaultBotProperties
# from aiogram.enums import ParseMode
# from aiogram.filters import CommandStart
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import Message

# TOKEN = "8302215113:AAGQGQo1uvQZ1XTNSN95UIA6ZHbwtDgUweQ"

# dp = Dispatcher(storage=MemoryStorage())


# # Bot holatlari
# class BotSteps(StatesGroup):
#   video_step = State()
#   joke_step = State()


# # Videolar ro'yxati
# VIDEOS = [
#     "https://www.youtube.com/shorts/yztuTuipM5E",
#     "https://www.youtube.com/shorts/uUOpURcjROY",
#     "https://www.youtube.com/shorts/jz51XRzcry8?feature=share",
#     "https://www.youtube.com/shorts/J1BWlaCLowA?feature=share",
#     "https://www.youtube.com/shorts/mjLbvt7wIq8",
#     "https://www.youtube.com/shorts/GX97uhAb_4A?feature=share",
#     "https://www.youtube.com/shorts/J9Gi8i6gJ3I?feature=share",
#     "https://www.youtube.com/shorts/_5MMrMSpJS0?feature=share",
#     "https://www.youtube.com/shorts/DTxdKkwRvoM?feature=share",
#     "https://www.youtube.com/shorts/oTFUVW8_A4c?feature=share",
#     "https://www.youtube.com/shorts/7IoCb_eoxlQ?feature=share",
#     "https://www.youtube.com/shorts/CTcRPhIqX8I?feature=share",
#     "https://www.youtube.com/shorts/qj2QbrL_kw8?feature=share",
#     "https://youtu.be/jY98EwB1IJQ",
#     "https://youtu.be/qZ9ZpSn3eOs",
#     "https://youtu.be/9zvFQDqxiZM",
#     "https://youtu.be/FNjWoKRKe6s", 
# ]

# # 12 ta qiziqarli yozma latifalar ro'yxati
# JOKES = [
#     (
#         "1. Бир куни Нормат амаки яна бозорга бориб, энг охирги русумдаги,"
#         " «мукаммал» деган ақлли соатни сотиб олибди.\n\nУйга келиб, хотини"
#         " кўрмасин деб, секин сандиқнинг тагига яшириб қўйибди. Кечқурун ҳамма"
#         " ухлаганидан кейин соатни олиб, секин пичирлаб сўрабди:\n— Соатжон,"
#         " хотиним ухлаяптими?\n\nСоат астагина жавоб берибди:\n— Ҳа, Нормат ака,"
#         " хотинингиз чуқур уйқуда.\n\nНормат амаки хурсанд бўлиб:\n— Ие, гап"
#         " йўқ-ку! Энди айт-чи, эртага менга нима совға қилади?\n\nСоат аста"
#         " шивирлабди:\n— Эртага 200 долларлик янги соат яшириб қўйганингизни билиб"
#         " қаттиқ уришади!\n\nНормат амаки ҳайрон бўлиб:\n— Ие, қаердан билди? У"
#         " ухлаяптику!\n\nСоат:\n— У ухлаяпти, лекин мен маълумотларни"
#         " хотинингизнинг смарт-билезигига юбориб бўлдим, оилавий синхронизация"
#         " ёқилган эди!"
#     ),
#     (
#         "2. Ikki ulfatchilik qilib oʻtirgan doʻst suhbatlashyapti:\n— Joʻra,"
#         " xotinim bilan har kuni urishamiz, oxiri kelisha olmay ajrashishga"
#         " qaror qildik.\n— Ie, mol-mulkni qanday boʻlishasizlar endi?\n— Juda"
#         " adolatli boʻlishdik: uy, mashina va jamgʻarilgan pullar xotinimga"
#         " tegadigan boʻldi.\n— Senga-chi, senga nima tegdi?\n— Menga..."
#         " erkinlik tegdi, joʻra!"
#     ),
#     (
#         "3. Shifokor qabulida:\n— Do'xtir, har kuni tushimda kalamushlar futbol"
#         " o'ynayapti! Charchab ketdim...\n— Mana bu dorini iching, bugun tunda"
#         " tinch uyqlaysiz.\n— Do'xtirjon, dorini ertaga ichsam bo'ladimi?\n—"
#         " Ie, nega?\n— Bugun final o'yini bor-da!"
#     ),
#     (
#         "4. Xotini eriga e'tiroz bildiryapti:\n— Dadasiga, qo'shnimiz xotiniga har"
#         " kuni gul sovg'a qiladi, aylantirgani olib chiqadi. Siz nega unday"
#         " qilmaysiz?\nEri tirjayib:\n— Xotinjon, axir men u qo'shnimning"
#         " xotinini umuman tanimayman-ku!"
#     ),
#     (
#         "5. Bir kishi svetoforning qizil chirog'ida o'tib ketibdi. YHXX xodimi"
#         " to'xtatibdi:\n— Nega qizilga o'tdingiz?\n— Haydovchi: Aka, kechiring,"
#         " qizil yonib turganini ko'rmay qolibman.\n— Militsioner: Shuncha yorug'"
#         " chiroqni ko'rmadingizmi?\n— Haydovchi: Chiroqni-ku ko'rdim, lekin"
#         " sizni ko'rmay qolibman-da!"
#     ),
#     (
#         "6. Eri xotiniga demoqda:\n— Xotin, bugun ovqat juda mazali chiqibdi,"
#         " nima bo'ldi?\n— Dadasiga, shunchaki bugun gaz o'chib qoldi, taomni"
#         " mehrim bilan pishirdim!\n— Ha, tushunarli... Ertaga ham gazetani"
#         " o'qib o'tir, gaz yonmasin!"
#     ),
#     (
#         "7. Bozorda xaridor sotuvchiga:\n— Bu tarvuzingiz shirinmi o'zi?\n—"
#         " Sotuvchi: Aka, shunday shirin-ki, tilni yorasiz!\n— Xaridor: Bo'lmasa"
#         " bitta kesib bering, totib ko'ray.\n— Sotuvchi: Yo'q aka, tilingiz"
#         " yorilsa javob berolmayman!"
#     ),
#     (
#         "8. Matematika darsida o'qituvchi:\n— Eshmat, yonimda 5 ta olma bor."
#         " Undan 3 tasini senga bersam, nechta olma qoladi?\n— Eshmat: Ustoz,"
#         " baribir beramaysiz-ku, nima qilasiz xayolimni buzib!"
#     ),
#     (
#         "9. Bir kishi taksiga o'tiribdi:\n— Haydovchi aka, vokzalga tezroq olib"
#         " boring, poezdim ketib qoladi!\n— Haydovchi: Havotir olmang aka, tezlik"
#         " cheklangan bo'lsa ham ulagizamiz.\n— Yo'lovchi: Poezd soat 5 da"
#         " ketadi, hozir 4:55!\n— Haydovchi: Ie, u holda poezd kettimi deb"
#         " hisoblayvering!"
#     ),
#     (
#         "10. Kompyuter ta'mirlovchiga telefon qilishdi:\n— Usta, kompyuterim"
#         " ishlamay qoldi!\n— Nima bo'ldi?\n— Choy to'kilib ketdi.\n— Qanaqa"
#         " choy?\n— Shakarsiz choy... Lekin nimagadir baribir shirin uyquga"
#         " ketdi!"
#     ),
#     (
#         "11. Avtobusda tirbandlik. Bir kishi ikkinchisiga:\n— Aka, sal nariroq"
#         " turing, nafas ololmayapman!\n— Ikkinchisi: Aka, bu joyda nafas olish"
#         " pullik emas, lekin siqilib turganingiz bepul!"
#     ),
#     (
#         "12. Imtihonda talaba va o'qituvchi:\n— O'qituvchi: Savolga javob"
#         " bersang 5 qo'yaman.\n— Talaba: Ustoz, qiyinroq savol bering,"
#         " bilmasam ham mayli, muhimi bilimim sinalsin!\n— O'qituvchi: Bo'ptisiz,"
#         " Yer bilan Quyosh orasidagi masofa necha millimetr?\n— Talaba:"
#         " Domla, uzr, men '5' ga rozi bo'la qolay!"
#     ),
# ]


# @dp.message(CommandStart())
# async def command_start_handler(message: Message, state: FSMContext) -> None:
#   await state.clear()
#   await message.answer(
#       f"Salom, {html.bold(message.from_user.full_name)}! Kulishni xohlasangiz"
#       " 'ketdik' deb yozing 😊"
#   )


# @dp.message(F.text.lower().in_({"ketdik", "ketik", "кетдик", "кетик"}))
# async def ketdik_handler(message: Message, state: FSMContext) -> None:
#   await state.set_state(BotSteps.video_step)
#   await state.update_data(current_video=0)

#   await message.answer(
#       text=(
#           "Mana birinchi video! Yana ko'rish uchun 'yana' deb"
#           f" yozing:\n{VIDEOS[0]}"
#       )
#   )


# @dp.message(BotSteps.video_step, F.text.lower().in_({"yana", "яна"}))
# async def yana_handler(message: Message, state: FSMContext) -> None:
#   data = await state.get_data()
#   current_video = data.get("current_video", 0) + 1

#   if current_video < len(VIDEOS):
#     await state.update_data(current_video=current_video)
#     await message.answer(
#         text=(
#             "Mana shu ham bor! Yana xohlasangiz 'yana' deb"
#             f" yozing:\n{VIDEOS[current_video]}"
#         )
#     )
#   else:
#     await state.clear()
#     await message.answer(
#         text=(
#             "Videolar tugadi! Maza qilib kulib oldingiz deb o'ylayman. Ana endi"
#             " yozma anekdotlarga o'tamiz, bo'ladimi? 'ha' yoki 'yo'q' deb"
#             " javob bering."
#         )
#     )


# @dp.message(F.text.lower().in_({"ha", "ха"}))
# async def ha_handler(message: Message, state: FSMContext) -> None:
#   await state.set_state(BotSteps.joke_step)
#   await state.update_data(current_joke=0)

#   await message.answer(
#       text=(
#           f"{JOKES[0]}\n\nKeyingi latifa uchun 'keyingi' deb yozing (yoki 'g')"
#       )
#   )


# @dp.message(
#     BotSteps.joke_step, F.text.lower().in_({"keyingi", "кейинги", "g", "г"})
# )
# async def keyingi_anekdot_handler(message: Message, state: FSMContext) -> None:
#   data = await state.get_data()
#   current_joke = data.get("current_joke", 0) + 1

#   if current_joke < len(JOKES):
#     await state.update_data(current_joke=current_joke)
#     await message.answer(
#         text=(
#             f"{JOKES[current_joke]}\n\nKeyingi latifa uchun 'keyingi' deb"
#             " yozing 😊"
#         )
#     )
#   else:
#     await state.clear()
#     await message.answer(
#         text=(
#             "Barcha 12 ta latifalar tugadi! Umid qilaman sizga yoqdi 😃\nBoshidan"
#             " "
#         )
#     )


# @dp.message(F.text.lower().in_({"yo'q", "yoq", "йок", "йоқ"}))
# async def yoq_handler(message: Message, state: FSMContext) -> None:
#   await state.clear()
#   await message.answer(text="Mayli, ko'rishamiz 👋")


# @dp.message()
# async def echo_handler(message: Message) -> None:
#   await message.answer(text="Boshlash uchun 'ketdik' deb yozing 🥺")


# async def main() -> None:
#     bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
#     # Webhook'ni o'chirib, polling'ga yo'l ochamiz
#     await bot.delete_webhook(drop_pending_updates=True)
    
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#   asyncio.run(main())