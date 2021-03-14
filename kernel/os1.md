# К вопросу о создании карманной ОС. Часть первая. История, таблица прерываний и таймеры.

Как известно, количество статей на тему "Как написать ОС" на Хабре превышает некоторое разумное количество. Многие из этих статей начинаются и завершаются написанием загрузчика. Другие идут дальше и доходят до создания диспетчера задач. Другая группа более респектабельных статей посвящена исследованию некоторых существующих проектов ОС. При том, что такие статьи хорошо раскрывают работу отдельных механизмов, их довольно сложно использовать как мануал по осеписательству. В тоже время, количество осеписателей, как известно, не убывает ни в каком поколении, и мне хочется сделать некоторый вклад в блуждания искателей системной мудрости. 

Чтобы не пополнить когорту плохих руководств по написанию собственной гениальной ОС сверхреального времени, прерывающейся сразу после многообещающего начала, я предпринял ряд мер. 

Во-первых эта серия статей не выйдет до того момента, пока не будет в полной мере дописана, и если вы это читаете, значит вся серия и готова к выходу и будет с небольшими интервалами появляться на ресурсе (Если конечно, первые статьи цикла будут одобрены сообществом). Во-вторых, учитывая, что операционная система - это не строгая научная концепция, но продукт инженерного творчества, допускающий огромное количество возможных вариантов реализации, я постараюсь построить свой рассказ не на принципе "вот вам код, делайте так как я", но вместо этого дать некоторое рассуждение, из которого логически вытекает необходимость тех или иных инструментов и имеющиеся варианты реализации. Впрочем, это не отменяет того факта, расказ будет unix центричен. В след за авторами книги "Искусство программирования Unix", я убеждён в том, что реалии вычислительной техники вынуждают создателей операционных систем раз за разом переизобретать unix. Этот идеальный, по Аристотелю, абстрактный, во множестве форм существующий unix выписывает сам себя, являясь логичным следствием решения инженерных проблем, встающих на пути осеписателя.

Конечно, современные операционные системы являются сложнейшими инженерными продуктами, с количеством строк кода настолько невообразимым, что называть его неприлично. Однако, это совсем не означает, что ядро операционной системы невозможно написать в одиночку. Как мы увидим далее, хотя и несколько примитивное, но всё же вполне функциональное и подходящее для практического применения ядро, и некоторое его окружение, потребует от нас не так уж много работы. Такой системе не удасться тягаться с монстрами вроде Linux, Windows, QNX, но помимо чисто образовательной цели, собственная ОС может быть полезным инструментом в управлении специализированными устройствами в области встраиваемых систем. Впрочем и здесь гораздо проще и быстрее воспользоваться существующими проектами, такими как FreeRTOS, embox, nuttx и прочими, кои существуют во множестве. Однако, перечисленные проекты не возникают не сами по себе. Многообразие иженерных задач и многоликость вариантов реализации ОС таковы, что всегда найдётся такая задача, для которой инженеру захочется использовать велосипед, и, может быть, бы хорошо уметь таковой сконструировать.

# Зачем человечеству ОС?

Для того чтобы понять, чтот крутится внутри ОС и как её написать, было бы неплохо разобраться для каких задач операционные системы были придуманы. 

Первые вычислительные машины, появившиеся приблизительно во время второй мировой войны не только не имели каких-либо намёков на операционные систему, но и пониманием языков программирования похвастаться не могли. Инструмментом программиста тех времён были даже не перфокарты, но коммутационная панель. За отсутствием каких-либо интерфейсов ввода-вывода назвать такую машину компьютером по современным меркам можно с большой натяжкой, поскольку он скорее напоминает голый процессор, работа с которым осуществлялась через непосредственное физическое подключения к аналогу современного арифметически-логического устройства. 

По мере развития вычислительной техники и её распространения, концепция всё больше принимала очертания цельного технического изделия, появились первые средства ввода-вывода - устройство для чтения перфокарт и принтер, оформилась идея системы комманд, появилась концепция ассемблера. Лишившись необходимости возиться с громоздскими коммутационными панелями и получив в свои руки формальную вычислительную систему, программисты выстраивались в очереди, с тем, чтобы покормить машину любовно пробитой колодой перфокарт и получить ответ в виде длинной распечатки вычисленного результата.

Практически сразу,уже 1950-х годах, на свет появляется концепция языков программирования явленная миру в виде таких известных продуктов, как Fortran (FORmula TRANslator, 1954-1957), Cobol (COmmon Business Oriented Language, 1959), Algol(Algorithmic Language, 1958). Теперь программисты могли писать код не ассемблерными инструкциями, а на более человеческом математическом языке, что, впрочем, требовало предварительной загрузки транслятора в память машины. Теперь, прежде чем скормить вычислителю целевую программу, оператор должен был должен дать ему служебную колоду перфокарт с реализацией необходимого транслятора. Чтобы не обременять добрых людей необходимостью постоянной загрузки этих инструментов в память машины, трансляторы очень быстро перекочевали в специальные устройства хранения, обычно реализованные на магнитофонных лентах. Теперь загрузка транслятора осуществлялось вызовом одной единственной инструкции, что сильно упрощало процесс и экономило время. Отметим, что тут появляется концепция стандартных программ и инструментов, к которым по необходимости может обращаться програмный код.

Очереди в компьютерные залы, длительные интервалы времени между передачей программы операторам ЭВМ и получением результата, а также постепенное распространение ЭВМ из институтов в бизнес-организации, заставило инженеров оптимизировать процесс работы с машиной. Так на свет появились системы разделения памяти (середина-конец 1960-х). Теперь память машины делилась на секции. Несколько программистов могли отдельно готовить свои программы к выполнению, а компьютер исполнял их одну за другой по мере готовности. Так система значительно снизила простой дорогущего оборудования. Несложно догадаться, что разделение памяти требовало наличия некоторого управляющего кода, способного определить факт готовности задачи, поставить её на исполнение и получить управление обратно по её завершению. 

В скорости после этого к идее разделения памяти добавилась идея разделения времени, концепция многозадачности и диалоговые терминалы (конец 1960-х, начало 1970-х), это окончательно превратило жизнь программиста в мёд и сахар и открыло к компьютеру доступ студентам и широкому кругу специалистов не являющихся программистами, чему также способствовало появление интерпретатора BASIC (Beginner’s All-purpose Symbolic Instruction Code, 1964), впоследствие перекочевавшего на уже зарождающиеся персональные машины и долгое время господствовавшего в этом сегменте.

UNIX?

Из всего этого многословного вступления нам следует сделать следующий вывод. Операционные системы зародились как средство, позволяющие группе пользователей совместно использовать процессор для решения собственных, слабо связанных между собой задач. В современных реалиях задача совместного использования одного компьютера группой специалистов встречается крайне редко, но концепция не изменилась. Вместо пользователей за ресурсы вычислителя конкурируют процессы, сосуществующие в едином пространстве системы. 

Надо так же учесть, что по мере компактизации вычислителей, несколько изменилась их роль. Если большие мейнфреймы специализировались на инженерных расчётах и довольствовались довольно примитивными устройствами ввода-вывода, то современные машины зачастую управляют сложным оборудованием не где-то в виртуальном вычислительном пространстве, но в физическом мире. Сложность написания и отладки ОС, а также многообразие аппаратных задач, с которыми сталкиваются современные вычислительные системы потребовало от ОС умения работать с зоопарком всевозможных устройств. Метод обеспечивающий взаимодействие "виртуального" вычислительного мира с физическим выкристализавался в виде концепции драйверов оборудования, имеющих стандартизированные интерфейсы. С другой стороны усложнение задач, над которыми теперь может работать не один, но несколько вычислительных процессов одновременно, потребовало синхронизации их работы и средств межпроцессного взаимодействия.

Если мазать широкими мазками, то синхронизация разделённых во времени и памяти процессов при общении с оборудованием и между собой, это и есть та самая задача, которую решает операционная система. Но как она это делает?


# Операционная система, как библиотека синхронизации процессов.

Если вы изучали код таких проектов, как linux, embox, nuttx, haiku, minix и других проектов с открытым кодом, названия которых сейчас на слуху, вы, возможно, ловили себя на мысли, что читать их код сложно. За внешним фасадом угадывается стройная, красивая, но с трудом поддающаяся осмыслению структура, которая к тому же растёт со всех сторон одновременно. 

Проблема с изучением кода операционных систем в том, что они не имеют точки входа. После того, как код инициализации ОС отбарабанил положенную ему симфонию, ОС внезапно замолкает, отдаёт управление пользовательским процессам и практически перестаёт проявлять какую либо активность. И действительно, что делает ОС? Переключает контексты процессам? Исполняет обработчики прерываний? Может быть, в лице службы сетевого стека управляет сетевым трафиком? Изменять информацию в вычислительной системе и осуществлять обращения к аппаратным устройствам, являться актором, совершающим действия может толька та сущность, которая располагает вычислительным временем.

Пользователь видит ОС как некий чёрный ящик к которому обращаются пользовательские процессы. Через непроглядную перелену, посредством системых вызовов процесс пользователя отправляет запросы и ОС, аки всемогущий Джин провозглашает "Слушаю и Повинуюсь" и исполняет желаемое. Однако, если мы изучим, что же происходит в момент пересечения пелены системных вызовов, то обнаружим, что в мифической картине мироздания с могущественным Джином-актором есть принципиальная неточность. В операционной системе нет Актора, нет Джина, который мог бы выполнить все те действия, которые, как нам кажется должна выполнять ОС и никто не перехватывает у процесса управление в момент его входа в пространство ядра. Вместо этого пользовательские процессы, перейдя в режим ядра действуют в ядре и являются акторами в нём. Ещё один тип акторов на этом поле - обработчики прерываний, перехватывающие управление по аппаратным событиям, и исполняющие системный код в своей зоне ответственности. На этом акторы системы исчерпываются. Можно, конечно, вспомнить системные службы или тасклеты, но они мало чем от обычных процессов и действуют по тем же законам, что и обычные процессы, и действуют в чётко очерченной зоне ответственности. Пожалуй, самым ярким проявлением "воли" ОС является работа диспетчера задач и момент выбора того процесса, которому следующим будет передано управление. Однако, работа диспетчера задач инициируется или обработчиком прерываний в вытесняющей модели, или одним из процессов в кооперативной модели, то есть и здесь мы не видим действия, которое можно было бы с чистой совестью приписать такому актору, как операционная система. 

Можно сказать, что классическая операционная система не является программой в общепринятом смысле и не имеет собственного времени исполнения. Однако, ей каким-то образом удаётся дерижировать многоголосым хоромом процессов и не допускать некоректного использования переферийного оборудования. Как она это делает? Если мы захотим внимательно исследовать вопрос, то обнаружим, что в первую очередь операционная система устанавливает правила для акторов, то есть, для сущностей, которые в отличии от неё самой имеют вычислительное время. Правила могут просто декларироваться как некоторый разрещённый набор АПИ, или же жёстко контролироваться с применением аппаратных ограничений на разрещённые в том или ином режиме операции. Установленные правила выделяют акторам некоторое пространство в котором актор может делать всё что угодно, но для того, чтобы взаимодействовать с не относящимися к нему переферийными устройствами или другими акторами, процесс, или обработчик, обязаны! использовать предписанный набор инструментов. Поскольку этот набор инструментов имеет строго ограниченный функционал и обвешан бесконечным набором проверок и страховочных механизмов, актору становится очень сложно каким-либо образом навредить системе.

С этой точки зрения ОС похожа не на Джина, исполняющего волю процесса, но на програмную библиотеку инструментов межпроцессной синхронизации. Именно в таком ключе удобно думать об ОС при её разработке.

..........................................

Пусть мы, начинающие разработчики ядра операционной системы, выбравшие себе боевую платформу, помигавший светодиодом и выведший "HelloWorld" через USART, если речь идёт о STM32 или любом другом семействе микроконтроллеров и отладочных плат, или, написавшие системный загрузчик и выведшие на монитор через INT10 сообщение "HelloWorld", если речь идёт о персональном компьютере на x86-64. Перед нами девственно чистая функция main процесса инициализации ненаписанной еще ОС. Вот код инициализации подвластной нам аппаратуры. Что следует написать теперь в первую очередь? Прежде чем думать о концептуальном, нужно обрести почву под ногами и создать для себя первоначальные удобства. Поскольку мы уже умеем выводить текст на одно из устройств, было бы неплохо превратить эту возможность в полноценное оружие и поэтому одной из первых подсистем в новой ОС должна стать библиотека диагностического вывода.

# Библиотека отладочной печати и диагностического вывода (dprint, diag).
"""Лучшее, чему сейчас может обучиться ваша система - громко падать."""

Может показаться, что библиотека печати не имеет никакого отношения к функциям ОС. Однако, как мы сказали раньше и будем неоднократно повторять в дальнейшем, целью является написание библиотеки, а достаточно большая библиотека, помимо основного функционала, имеет набор важных  вспомогательных инструментов, облегчающих собственную разработку.

Требования к библиотеке определяются её диагностической направленностью. Система отладочного вывода должна работать при любом состоянии окружения, без какой либо привязки к аппаратным прерываниям, без привязки к системе еще не написанных нами процессов и прочим сложным штукам. В идеале она даже не должна работать с памятью, потому что оперативная память, как показывает практика, имеет при разработке новых устройств нехорошее свойство иногда неверно инициализироваться. (Кто попадал, тот знает).

Система диагностической печати может не уметь многого. Для начала достаточно будет выводить строки, числа, рисовать дамп памяти. При необходимости сюда же можно подтянуть реализацию диагностической вариации printf, но разработка функции printf никак не является целью статью. Так что, пусть это будет просто:

Все функции приведённые выше работают через две неопределённые функции debug_putchar и debug_write. В этом месте следует учесть что по мере построения системы мы можем хотеть менять способ
вывода диагностической информации и даже захотеть изменить его прямо в рантайме. Поэтому дадим возможность подменять backend нашей библиотеки:


Интерфейс diag. Позволяет подключать различные драйверы для реализации отладочного вывода. Если речь идёт о аппаратном выводе, следует помнить, что совершаться он должен примитивнейшим из всех возможных способов. Инициализация интерфейса diag должна появиться в коде инициализации системы. В дальнейшем такой спрособ работы с аппаратнозависимой частью системы будет встречаться чуть менее, чем везде. 


## Глобальный блокировка прерываний (irqs).
"""Атомарность требует жертв."""

Для совершения атомарных операций над структурами данных в ядре, нам потребуется на короткое время отключать внешние прерывания. Код для STM32 тривиален:


, однако, в силу аксиомы аппаратной независимости, нужно подумать как реализовать эту систему аппаратно независимо. Мы могли, так же как в случае с интерфейсом diag реализовать интерфейс и подключать к нему необходимые методы. Однако, в отличии от прошлого случая глобальный лок - это одна ассемблерная инструкция и негоже прятать его за таблицу виртуальных функций, тем более, что не требуется менять поведение этих методов в рантайме. Обычно такая задача решается за счёт соглашения на имена подключаемых файлов. Действительно. Пусть мы имеем две архитектуры с различным набором ассемблерных инструкций. Если каждая из архитектур определит заголовочный файл asm/irqs.h с одинаковым набором макросов, аппаратно независимому коду понадобиться только подключить этот заголовок и пользоваться стандартным набором. Удобно обернуть функции глобального управления прерываниями во второй слой макросов, уже присутствующих в коде в единственном экземпляре, что позволит при необходимости внедрить аппаратно независимую диагностику:



## Таблица прерываний ядра (irqtable). 
Простейший, самый быстрый и правильный способ подключения обработчиков прерываний - указать адрес обработчика непосредственно в векторе прерывания. Очень логично. 

Но, операционная система любит всё контролировать и потому мы не можем допустить, чтобы прерывания случались без всякой отчётности. Поэтому развернём над прерываниями тонкий слой абстракции, работать этот слой будет следующим образом: все прерывания будут иметь однотипные первичные обработчики, отличающиеся только значением, устанавливаемым в регистр. После того, как значение установленно все обработчики выполняют функцию `do_irq(irqno)`, где `irqno` - это и есть то самое значение. Значение выбирается так, чтобы соответствиовать номеру в массиве irqtable, где храниться уже боевой обработчик прерывания, а так же сопутствующая информация:




Такая система позволяет на ходу подменять обработчики прерываний, отслеживать количество событий определённого типа и за счёт возможности передавать аргумент `privdata`, параметризировать обработчики, что в дальнейшим не раз пригодится.


 



## Служба времени (systime).
"""Если вчера уже прошло два дня после завтра, послезавтра будет сегодня или вчера?"""

Сложно переоценить значимость службы времени для ядра операционной системы. Служба времени задают ритм машинерии механизмов операционной системы и позволяет процессору разговаривать с человеком на общем, бесконечно медленном языке.

Не вдаваясь в вопрос получения точных наносекундных интервалов и воспользовавшись принципом простоты, ограничимся миллисекундными точностями, чего для системных целей пока достаточно. Для приведения в действие системы времени необходимо настроить один из таймеров с тем, чтобы время его переполнения задавало системный тик. Идею интерфейса этой системы автор спёр непосредственно из Ардуино, как вы можете догадаться по названиям функций `delay` и `millis`.

Подключение обработчика системных часов осуществим через irqtable.


Период системного тика лучше всего выбирать как 1000Гц или 10000Гц, что позволит тривиально построить функцию millis:


Переменная jifies является счётчиком системных тиков.


# Архитектура программ. От суперцикла и далее.

В классической статье камрада DiHalt изложены варианты управляющих структур предшествующих операционным системам типов. Кратко вспомним первые три пункта.

1. Суперцикл. Структура лишённая структуры. Полное отсутствие управляющего кода все действия выполняются в едином бесконечно повторяющемся цикле. Всё время выполнения принадлежит суперциклу. 

2. Суперцикл + прерывания. Часть функций передана обработчикам прерываний. Управление кодом по сути передано аппаратной части и осуществляется в силу её возможностей. Время выполнения принадлежит суперциклу, изредко прерываемому прерываниями.

3. Флаговый автомат. В системе появляется концепция задач, вызываемых в суперцикле в случае, если активирующий их флаг установлен, задачи общаются между собой через переменные. Время выполнения пока еще зыбко и эфемерно. Чётких правил диспетчеризации нет. 

## Таймер
Примерно в этом месте эволюции управляющего кода появляется такая штука как таймер. Вот полная реализация таймера:


Эта структура данных в рамках флагового автомата или суперцикла позволяет работать с интервалами времени, что очень полезно учитывая отсутствие "нормальных" sleep_for функций.

Пример использования таймера:

## Связные списоки.
Внутри операционной системы существует множество объектов, отвечающих за те или иные стороны её работы, которые нужно переодически итерировать. Идёт ли речь об обходе inode, принадлежащих определённой директории, инспекции таблицы зарегистрированных файловых систем, или обслуживанию множества процессов, ожидающих исполнения, структуры объектов должны каким-то образом упорядочиваться, чтобы можно было проитерировать объекты одного типа или объекты, находящиеся в одинаковом состоянии.

Простейшее и оптимальное по затратам памяти решение в том, чтобы хранить такие объекты в массивах. Решение это, впрочем, имеет существенные недостатки. Массивы имеют жестко фиксированную длину, а переупорядочивание массива требует операции копирований, что осложняет работу с большими объектами. Таким образом массивы хорошо подходят только для коллекций, состав и порядок которых не меняется со временем. Например, в массиве можно хранить заголовки зарегистрированных в системе файловых систем (в терминологии linux `struct file_system_type`), а вот коллекцию запланированных на исполнение процессов, пожалуй не стоит. Массивы также встречают внезапное препятствие со стороны языка программирования С/С++. Язык си требует, чтобы массив полностью был определён в едином файле. Это не всегда удобно. Например, упомянутые заголовки файловых систем было бы хорошо инстанцировать в файлах драйверов этих файловых систем, но сделав так, мы сможем построить массив разве что из указателей на эти объекты. Создатели embox, впрочем, разрешили эту проблему изящно хакнув язык си на уровне линкёра с помощью механизма `array_spread` (https://github.com/embox/embox/blob/master/src/util/array_spread/array_impl.h), что позволило системе embox таки создавать распределённые масивы.

Тем не менее, пожелав получить в свои руки более универсальный инструмент, мы придём к концепции интруссивных связных списков. Ценой небольшого увеличения затрат памяти, добавив в объект коллекции поле-указатель на следующий элемент, мы можем собирать из разрознесённых в памяти объектов упорядоченные списки. Слово "интруссивный" означает, что служебное поле списка встроено в сам связываемый объект, а не находится где-то вне объекта, как это принято, например, для std::list из STL. Тривиальная реализация списка тривиальна:

```c
struct A {
	A * next;

	... data ...
};

A * head;      //<-- Голова списка
A   a, b, c;   //<-- Элементы списка

void main() {
	// Собираем список
	head   = &a; 
	a.next = &b;
	b.next = &c;
	c.next = NULL;

	// Объодим список.
	A* it; 
	for (it = head; it != NULL; ++it) 
	{
		// do something
	}
}
``` 

К сожалению, такой список не очень удобен. Большую часть времени наш код будет иметь доступ только к голове списка, а для того, чтобы получить указатель на хвостовой элемент и совершить с ним операцию, понадобиться сперва проитерировать весь список. Работая только с головой, на таком списке можно эффективно реализовать структуру типа стэк, но отнюдь не структуру типа очередь, которая является необходимой для многих алгоритмов. Для исправления этого недостатка объекту добавляют второй указатель на предыдущий объект списка. Теперь каждый элемент ссылается и на следующий элемент и на предыдущий, а головной элемент списка указывает и на голову и на хвост. После добавления второго поля указателя обслуживание списка становится существенно менее тривиальными, поэтому для работы с "двойным связным списком" (double linked list) в ядре linux существовал целый заголовочный файл. В последних версиях ядра с целью оптимизации код list_head расплылся по подсистемам и в ядре в резных местах появилось некоторое количество различных реализаций, а потому посмотрим на классическую реализацию двойного связного списка `struct list_head` из ядра linux версии 2.5.0 (https://elixir.bootlin.com/linux/v2.5.0/source/include/linux/list.h), в которой список еще не оброс кучей ненужных дополнительных подробностей и оптимизаций. Не забудьте обратить внимание на макрос `list_entry`, восстанавливающий адрес объекта по адресу поля списка.


## Диспетчер таймеров.
Флаговый автомат с таймерами - это, конечно хорошо. Но было бы неплохо что-то поконцептуальнее и ситемнее, с более чёткими и выверенными правилами. Создадим централизованную службу контроля таймеров. Теперь в отличии от примера, проверками таймеров на срабатывание будет заниматься специальная система, шаг которой будет вызываться в суперцикле. Если таймер добавлен в систему и его интервал истёк, таймер отлинковывается от списка, а его обработчик исполняется,


# Заключение

Итак, мы получили несколько инструментов, а именно систему отладочного вывода, глобальный лок, таблицу прерываний, службу времени и, наконец, диспетчер таймеров. С  этими инструментами мы уже достаточно вольготно чуствуем себя в системе, научились вполне себе неплохо отслеживать время с миллисекундной точностью и совершать всяческие действия с помощью таймеров.

Подготовительная работа по сути завершена. Следующим пунктом списка идут процессы, диспетчер процессов.