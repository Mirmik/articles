Наиболее развитым и применяемым сегодня методом управления манипуляторами и позиционерами различных типов являются ЧПУ системы. ЧПУ системы позволили автоматическую обрабатывать детали с точностью до микрометров. Работа ЧПУ посторена как работа слепого часовщика без обратной связи от реального процесса. ЧПУ изменяет конфигурацию управляемой системы по заранее просчитанной программе, и не имеет никаких общих средств проверки корректности выполняемого процесса. Поскольку ЧПУ слеп, для получения хорошего результата, ЧПУ система должна быть тщательно откалибрована и настроена. Такая калибровка может выполняться с помощью вспомогательных датчиков или человеком-оператором, но так или иначе выполняется она до начала цикла работы системы. Для обеспечения точности в ЧПУ системе требуется использовать высокоточные датчики перемещения отдельных звеньев - энкодеры, иметь очень тщательно проработанную геометрическую модель объекта управления, а также необходимо обеспечить достаточную жесткость, позволяющую избежать деформаций частей системы сопоставимых с заложенной точностью. 

ЧПУ системы требует предварительного учёта всевозможных факторов и потому применимы только в рамках контролируемой среды и требуют постоянного наблюдения специалиста.  

Недостаток ЧПУ - отсутствие обратной связи от результата целевого процесса. Если ЧПУ система фрезерует изделие, она не видит самого изделия, но только выполняет траекторию обхода этого изделия фрезером. Если в следствии каких-то причин изделие немного сместится или немного изменится конфигурация механизма, система продолжит работу по изначально прощитанной траектории, выдавая явно ошибочный результат.

Очевидно, что работа механизмов вне контролируемой среды или с задачами, предполагающими определенную гибкость поведения, требует учёта текущей ситуации и наличия обратной связи от целевого процесса. Для конструировании подобных систем есть прекрасный образец в виде биологических организмов, их манипуляторов-конечностей и зрительных систем.

Хотя системы управления с обратной связью известны человечеству с глубокой древности, а робото подобные строительно-добывающие машины с первой половины 19-ого века, только с развитием вычислительной техники и систем видеонаблюдения мы получили возможность  приблизить методы позиционирования манипуляторов машин к той их форме, которой 
пользуется человек и прочие биологические организмы.

Для построения обратной связи от перемещающегося в пространстве объекта необходимо каким-либо образом измерять его текущее положение относительно внешней среды, причем делать это дистанционно. Существует ряд методов дистанционного измерения расстояний:

- ультразвук.
- радар.
- визуальная триангуляция.
- оптические датчики. интерференция.
- оптические датчики. отражение.
- сенсор глубины.

Для построения обратной связи по положению наиболее широко исследовались возможности позиционирования методами машинного зрения, то есть по данным видеокамер. 

Термин visual servoing (визуальное сероуправление) был введён в работе Hill, J. & Park, W.,”Real time control of a robot with a mobile  camera”,    1979,    Proceedingsof    the    9th International  symposium  on  Industrial  robots,pp.233-246.

Согласно обзору A Brief Comparative Study of Visual Servoing System от 2018-ого года автора Sikander Hans существует несколько типов сервосистем с визуальной обратной связью.

Один из важных факторов классификации визуальных сервосистем - по месту закрепления камер. Камеры могут быть стационарными или связанными с корпусом объекта управления.

Другим важным параметром является способ замыкания обратной связи. В одном методе информация с камер непосредственно используется в алгоритме решения задачи захвата или позиционирования. Второй метод предполагает оценку положения на основе данных визуального наблюдения и последующую генерацию управления на основе проанализированных данных.

Image  based visual  servoing control is considered to be  very robust  with respect    to    camera    and    robot    calibration    errors    (see (Hutchinson  et  al.  1996)  and  (Weiss  et  al.  1987)).  Coarse calibration only affects the rate of convergence of the control law  in  the  sense  that  a  longer  time  is  needed  to  reach  the desired position[24].   

Поскольку разные варианты системы имеют свои плюсы и минусы, интерес представляет гибридный подход, в котором одновременно используются глобальные и локальные системы позиционирования.

По сути, известные на сегодняшний день системы визуального сервоуправления могут быть разделены на два метода. В одном методе информация с камер непосредственно используется в алгоритме решения задачи захвата или позиционирования. Второй метод предполагает оценку положения на основе данных визуального наблюдения и последующую генерацию управления на основе проанализированных данных.

Авторы выделяют ряд проблем связанных с построением систем визуального сервоуправления.
В первую очередь это точность и временная задержка, обусловленная тем, что анализ видеоряда требеует достаточно продолжительного времени.










Задачи управления роботами манипуляторами имеют связь с вопросами позиционирования других перемещающихся в пространстве аппаратов: летательных аппаратов, подводных дронов ипрочих изделий такого типа.

В работах, посвященных исследуемой проблематике используется много разных вариантов матаппарата, позволяющего описывать положения объектов.
Однако, повидимому, наиболее перспективвным является метод однородных координат. Метод однородных координат имеет то очевидное преимущество над прочими системами описания движений, что в этот метод также применим для построения матмодели камер и проекций изображений, что позволяет исмпользовать один и тот же матаппарат как для управления, так и для построения визуальной обратной связи.





В ситуации, когда робот используется для осуществления работ, предполагающих физический контакт с некоторым изделием, важно учитывать вибрационную составляющую 

Управление нежесткими манипуляторами ставит вопрос об учёте и фильтрации вибраций и исследовании частотных свойств объекта управления.

Задача частотного анализа манипулятора нетривиальна, поскольку собственные частоты механической системы зависят от текущего взаимного расположения звеньев манипулятора. 
(Vibration Analysis of Multilink Manipulators Based on Timoshenko Beam Theory)
Enhanced_vibration_control_of_a_multilink_flexible



1. Hill, J. & Park, W.,”Real time control of a robot with a mobile  camera”,    1979,    Proceedingsof    the    9th International  symposium  on  Industrial  robots,pp.233-246
2. A Brief Comparative Study of Visual Servoing System
3. Vibration Analysis of Multilink Manipulators Based on Timoshenko Beam Theory
