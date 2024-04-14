# импорт библиотек
import discord 
from discord.ext import commands
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
# создание бота
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# подключение модели
def get_class(image, model, classes):
  np.set_printoptions(suppress=True)
  
  model = load_model(model, compile=False)
 
  class_names = open(classes, "r").readlines()
  
  data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

  image = Image.open(image).convert("RGB")
  
  size = (224, 224)
  image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
  
  image_array = np.asarray(image)
  
  normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
 
  data[0] = normalized_image_array
  
  prediction = model.predict(data)
  index = np.argmax(prediction)
  class_name = class_names[index]
  confidence_score = prediction[0][index]

  print("Class:", class_name[2:], end="")
  print("Confidence Score:", confidence_score)
  
  return index


# сообщение о готовности
@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов к использованию')


# приветствие
@bot.command()
async def hello(ctx):
    await ctx.send(f'Привет! Я бот - {bot.user} проекта GreenGrow. И я помогу тебе с выбором саженцов для твоего участка!')
    await ctx.send("Перед началом работы советую прочитать раздел $info")
    await ctx.send("Как начать работу программы? Введите сообщение $soil, затем выберете картинку и отправьте сообщение.")


@bot.command()
async def info(ctx):
    await ctx.send("В 1771 году английский священник и естествоиспытатель Джозеф Пристли решил проверить правда ли, что выдыхаемый воздух становится «грязным» и может негативно воздействовать на живые организмы. Для этого он посадил под герметичный колпак маленького мышонка и начал свой простой, но очень информативный опыт. Через некоторое время мышь ослабла, а потом и вовсе умерла в страшных мучениях. Затем Пристли решил добавить в эксперимент растение и поместил под колпак не только мышь, но и росточек мяты. Мышь совершенно свободно перемещалась под колпаком и довольно долгое время чувствовала себя отлично. Так Джозеф Пристли первым изучил влияние растений на состав окружающего воздуха.")


# загрузка фото
@bot.command()
async def test(ctx):
    files = ctx.message.attachments 
    await ctx.send(files)
    await ctx.send(files[0].filename )
    await ctx.send(files[0].url)
    syf = files[0].filename.split(".")[-1]
    await files[0].save(f"file.{syf}" )

# защита + ответ от модели 
@bot.command()
async def soil(ctx):
    files = ctx.message.attachments 
    syf = files[0].filename.split(".")[-1]
    
    if syf !='jpg' and syf !='jpeg' and syf !='png':
        await ctx.send("Неверное расширение")
        return
    
    await files[0].save(f"file.{syf}" )
    indx = get_class( f"file.{syf}",
                     "keras_model.h5",
                      "labels.txt" )
    
    if indx == 0:
        await ctx.send("Глинистые почвы")
        await ctx.send("На глинистых почвах хорошо растут и даже дают урожай: яблоня, вишня, рябина.")
        await ctx.send(" Данные культуры не являются рекордсменами по выработки кислорода, но принесут приятную пользу для вас и вашего сада.")
        with open('images/яблоня.jpg', 'rb') as f:
             picture = discord.File(f)
        await ctx.send(file=picture)
        with open('images/вишня.jpg', 'rb') as f:
             picture = discord.File(f)
        await ctx.send(file=picture)
        with open('images/рябина.jpg', 'rb') as f:
             picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send("Рекомендации по уходу: саженцы сильно подвержены вредителям, поэтому они требуют большого внимания и качественного ухода. Кроме полива и подкормки эти растения нужно обрезать весной и тщательно следить за сорниками вокруг стволов дерева.")

      
    if indx == 1:
         await ctx.send("Супеси")
         await ctx.send("Для супесных почв подходят хвойные растения: ели, можжевельник, лиственница.")
         await ctx.send("Хвойные растения черезвычайно полезны из-за выработки фитонцидов, которые оказывают антибактериальные свойства и очищают воздух от болезнетворных бактерий, а также эти растения удерживают в своих кронах от 30-50 тонн пыли.")
         with open('images/ель.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         with open('images/можжевельник.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         with open('images/лиственница.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         await ctx.send("Рекомендации по уходу: Молодые растения желательно поливать 1 раз в неделю, особенно в жаркий период. Взрослые растения поливаются 2-3 раза за сезон, но достаточно большим количеством воды. Без исключения все хвойные любят частое дождевание (опрыскивание из шланга кроны дерева), которое следует производить в утренние или вечерние часы.")
      
    if indx == 2:
         await ctx.send("Песчанная")
         await ctx.send("Дуб, Каштан и Тополь не любят заболоченные почвы, поэтому им хорошо подхлдят песчанные почвы.")
         await ctx.send("Эти деревья являются абсолютными рекордсменами по выработки кислорода и устойчивочти к выхлопным газам, ежегодно одно дерево поглощает около 180 кг углекислого газа, а выделяет 30 кг кислорода.")
         with open('images/дуб.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         with open('images/каштан.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         with open('images/тополь.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         await ctx.send("Рекомендации по уходу: Эти деревья не прихотливы, поэтому уход за ними сводится к поливу и рыхлению почвы, подкормке удобрениями")

    if indx == 3:
         await ctx.send("Чернозём")
         await ctx.send("Шиповник, Сирень и Берёза предпочитают плодородную почву, поэтому чернозём для них лучший выбор.")
         await ctx.send("Маленькие кустарники оказываются очень полезны для борьбы с пылевым загрязнением воздуха, они удерживают в 6 разбольше пыли, чем тополь")
         with open('images/шиповник.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         with open('images/сирень.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         with open('images/береза.jpg', 'rb') as f:
             picture = discord.File(f)
         await ctx.send(file=picture)
         await ctx.send("Рекомендации по уходу: данные растения любят хорошо удобренную и в меру влажную почву, но часто поддвержены вредителям, поэтому за ними требуются тщательный уход.")

         


bot.run("")
