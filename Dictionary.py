UserState = {
    0: "Регистрация пользователя",
    1: "Действий не требуется",
    2: "Ожидание установки имени",
    3: "Утверджение имени",
    4: "Создание поста - Текст",
    5: "Создание поста - Картинка",
    6: "Создание поста - Ожидание команды на рассылку",
    7: "Создание поста - Ожидание закрытия опроса",
    8: "Регистрация на игры - Игрок Будет на играх",
    9: "Регистрация на игры - Игрок под вопросом",
    10: "Регистрация на игры - Ожидание выбора времени",
    11: "Регистрация на игры - Придёт к HH:MM"
}

UserState_invitation_state = {
    "+": 1,
    "-": 0,
    "?": 2,
    "waiting_time": 3,
    "time": 4
}

post_type = {
    "registration": 0,
    "information": 1
}

response_template_in_state = {
    0: ['Привет! Пожалуйста, введитите свой игровой ник:',
          'Какой у вас игровой ник?',
          'Как к вам можно обращаться? Назовите ваш игровой ник'],
    1: ['а я пока ничего не умею) только запоминать всех вас) вы %s',
        'а я пока ничего не умею) только запоминать всех вас) вы %s'],
    2: ['а я пока ничего не умею) только запоминать всех вас) вы %s',
        'а я пока ничего не умею) только запоминать всех вас) вы %s'],
    3: ['Привет, %s! Если что, то ты всегда можешь отредактировать своё имя попросив меня поменять твой игровой ник',
          'Привет, %s! Если тебе нужно будет отредактировать игровой ник, попроси об этом меня',
          'Приятно познакомиться, %s! Если тебе нужно будет отредактировать игровой ник, попроси об этом меня или администраторов, только у нас есть полномочия для этого',
          'Приятно познакомиться, %s! Если что, то ты всегда можешь отредактировать своё имя, просто попросив меня поменять твой игровой ник, или обратись к нашим администраторам'],
    4: ['Права на создание поста подтверждены. \n'
        'Введите текст поста',
        'Права на создание поста подтверждены. \n'
        'Каким будет текст в посте?'],
    5: ['Какое изображение использовать в посте?',
        'Пришлите фото для поста'],
    6: ['Готово. Вы можете создать новый или отправить всем этот. пожалуйста, подтвердите написав подтверждение или номер поста для публикации: ',
        'Готово. Вы можете создать новый или отправить всем этот. пожалуйста, подтвердите написав подтверждение или номер поста для публикации: '],
    7: ['Регистрация остановлена',
          'Регистрация завершена'],
    10: ['Напришите когда вы примерно придёте на игры в формате: HH:MM',
        'Когда вас ждать? Напишите время в формате: HH:MM'],
    11: ['Ты придёшь к %s, мы тебя записали)',
        'Отметили тебя на %s, хороших игр)',
        'Значит будем ждать тебя к %s, хороших игр)'],
}

template_no_name_post = ['Привет! мы завтра играем в мафию!',
          'Привет! мы сегодня играем в мафию!',
          'Привет! мы играем в мафию, придёшь?)!']


template_post_with_name = ['Привет %s! мы завтра играем в мафию!',
          'Привет %s! мы сегодня играем в мафию!',
          'Привет %s! мы играем в мафию, придёшь?)']

response_for_super_user_sending = ['Привет %s! хороших игр, пост опубликован!',
          'Пост выложен, хороших игр, %s!',
          '%s, рассылка завершена']

response_for_default_user_sending = ['Привет %s! вы не имеете доступ к этой команде',
          '%s, не берите на себя много, этим займутся администраторы',
          '%s нет в списке администраторов ']

response_to_invitation_true = ['До встречи на играх)',
          'Хороших вам игр, вы записаны)',
          'Спасибо за то что отметились, мы вас записали, хороших игр)']

response_to_invitation_false = ['Приходи в другой раз, будем вам рады)',
          'Очень жаль что вас не будет, приходите в другой раз)']

response_to_invitation_question = ['Надеемся ты сможешь сегодня поиграть с нами)',
          'Не забудьте отметиться когда узнаете о своих планах на игровой вечер)']

VA_CMD_LIST = {
    "help": ('список команд', 'команды', 'умеешь' 'твои навыки', 'навыки'),
    "not": ('нет', 'отмена', 'не', 'не выкладывай',
            'отмена поста', 'отмена игр', 'не выкладывай пост', 'стой'),
    "yes": ('да', 'верно'),
    "sending_command": ('выкладывай', 'подтверждаю', 'выложи', 'публикуй', 'рассылай', 'выкладывай пост'),
    "deactivation_post": ('отключи регистрацию', 'отмени регистрацию',
                          'закрой регистрацию', 'закрой пост'),
    "who_marked": ('кто придёт на игры', 'кто отметился', 'кто будет играть',
                          'кто будет на играх', 'кто будет'),
    "info_post_create": ('создай информационный пост',
                         'создание информационного поста',
                         'пост с информацией',
                         'пост для информирования'),


    "heeelp": ('ты живой', 'ты жив', 'где ты'),
    "ctime": ('время', 'текущее время', 'сейчас времени', 'который час'),
    "joke": ('расскажи анекдот', 'рассмеши', 'шутка', 'расскажи шутку', 'пошути', 'развесели'),
    "open_browser": ('открой браузер', 'запусти браузер', 'открой гугл хром', 'гугл хром'),
    "what_we_say_to_god": ('богу трезвости', 'бог трезвости', 'что мы говорим богу трезвости'),
    "dota_start": ('запусти доту', 'погнали в доту', 'го в доту'),
    "steam_start": ('запусти стим', 'включи стим', 'открой стим'),
    "EpicGamesStore": ('открой эпик', 'эпик', 'эпик геймс', 'запусти эпик', 'включи эпик'),
    "Fortnite": ('открой фортнайт', 'фотрнайт', 'запусти фортнайт', 'включи фортнайт'),
    "notepad": ('открой блокнот', 'блокнот', 'запусти блокнот', 'мне нужен блокнот', 'включи блокнот', 'нужно сделать зпись в блокнот'),
}

not_recognized = ['не уверен что понял вас. повторите корректно',
          'в моей базе нет подобных сочитаний слов. пожалуйста, повторите корректно']

deactivation_post = ['Созданный вами пост отменён. Можно создать новый заново вызвав соответствующую команду',
          'Пост отменён, но я готов создать новый когда скажите']

response_have_active_post = ['Активный пост уже есть, его создал %s. нужно снять с него активность ',
          '%s уже создал пост. Создать новый нельзя пока он активный']

response_who_marked = ['Сегодня отметились: \n',
          'Сегодня будут на играх: \n']

all_post_deactife = ['Сегодня нет активных постов, пожалуйста, подождите пока не появится объявление о новых играх',
          'Регистрация на пост в который вы отметились уже закончилась, пожалуйста.\nЖдите новый игровой день']

error_time_invitation = {
    ':': "Нет разделителя ':'",
    'H': "я не понимаю часы которые вы указали",
    'M': "я не понимаю минуты которые вы указали",
}

waiting_time_invitation = [
    'Напришите когда вы примерно придёте на игры в формате: HH:MM',
     'Когда вас ждать? Напишите время в формате: HH:MM'
]

set_time_invitation = [
    'Ты придёшь к %s, мы тебя записали)',
    'Отметили тебя на %s, хороших игр)',
    'Значит будем ждать тебя к %s, хороших игр)'
]