[//]:#(Ленивые вычисления в быту) 

И хотя людей, которые для написания списка покупок или компиляции данных по квартплате используют скрипты на python, пересчитать по головам, но если так получилось, что вы, используете скрипты для решения рутинных задач и иногда скрипты работают недопустимо долго, то возможно, идея применение ленивых вычислений ко всему что движется, придётся вам по вкусу.

В предыдущих главах своего письма я дал вольное описание работы библиотеки evalcache.  
Ссылка: [Дисковое кэширование деревьев ленивых вычислений](https://habr.com/post/422937/) 

Чтобы не утомлять вас необходимостью изучать тот материал перед прочтением этого, краткое изложение прошлой части:

evalcache оборачивает данные, функции и методы в "ленивые объекты". Каждый ленивый объект имеет специальный хэш-ключ характеризуемый способом его построения. Над ленивыми объектами могут производиться операции, приводящие к генерации новых ленивых объектов. Эти операции выглядят точь-в-точь, как операции над обычными данными, но в реальности никаких вычислений не производится, вместо этого выстраивается дерево ссылающихся друг на друга ленивых объектов, помнящих свои операции и их аргументы. При необходимости получения данных, производится операция раскрытия ленивого объекта, которая или приводит в действие цепочку вычислений, или подтягивает результат из кэша, если объект с таким ключем вычислялся ранее.

## О некоторых изменениях
С момента написания прошлой статьи evalcache получил несколько дополнительных механик. 

### Механика некэшируемого исполнения
Оказывается, хэш ленивого объекта - штука настолько полезная, что хочется применять его в ситуации, когда кеширование самого объекта невозможно и ненужно.

Для этой цели введен специальный синтаксис:
```python
evalcache.LazyHash()
#Эквивалентно:
#evalcache.Lazy(self, cache=None, fastdo=True)
```

В этом варианте объект вычисляется сразу же в момент создания, но возвращается все равно ленивый файл. Это позволяет строить деревья вычислений без необходимости кеширования некоторых объектов.

### Механика неявного раскрытия
Неявное раскрытие - это ожидаемое поведение мемоизатора. Хотя evalcache изначально проектировался не для мемоизации, а для работы с деревьями вычислений, неявное раскрытие на основе алгоритмов evalcache может быть достигнуто. Для этого введены две новые опции ```onplace``` и ```onuse```. onplace приводит к раскрытию ленивого объекта сразу же после создания, а onuse при попытки его использования в какой-то из допустимых для ленивого объекта операций. 

```python
import evalcache

lazy = evalcache.Lazy(cache={}, onuse=True)
#lazy = evalcache.Lazy(cache={}, onplace=True) ### Альтернативный вариант декоратора.
#lazy = evalcache.Memoize() ### Альтернативный вариант декоратора.
#lazy = evalcache.Memoize(onplace=True) ### Альтернативный вариант декоратора.

@lazy
def fib(n):
	if n < 2:
		return n
	return fib(n - 1) + fib(n - 2)

for i in range(0,100):
	print(fib(i))
```

Но речь не об этой ненужном дополнении, призванном сделать библиотеку чуть более похожей на остальные ленификаторы. А о ленивых файлах:

### Ленивые файлы
Evalcache содержит надстройку для ленифицирования функций, генерирующих файлы. Изначально этот функционал предполагалось использовать для ленификации генерации скриншотов. Как выяснилось позже, с помощью механики ленивых файлов можно делать и другие любопытные вещи.

```python
import evalcache
import evalcache.lazyfile

lazyfile = evalcache.lazyfile.LazyFile(cache = evalcache.DirCache(".evalfile"))

@lazyfile(field="path")
def foo(data, path):
	f = open(path, "w")
	f.write(data)
	f.close()

foo("HelloWorld","data.dat")
```

Как это работает... 
В целом логика работы такая же, как и у всех ленивых объектов. ```foo("HelloWorld","data.dat")``` Начинает конструирование ленивого объекта хэш-ключ которого завязан на передаваемые ему аргументы. После чего применяется механика неявного раскрытия, приводящая к мгновенному запуску вычисления.

Но дальше порядок действий меняется.
```@lazyfile(field="path")``` Декоратор lazyfile анализирует параметр, с название указанным в field. Декоратор ожидает, что по факту выполнения функции, по этому пути будет создан файл. evalcache берет этот этот файл и создаёт на него жесткую ссылку в директории хэша ```".evalfile"```. Имя файла жесткой ссылки соответствует хэшключу ленивого объекта. В дальнейшем при нахождении в кэше файла с таким именем, evalcache при раскрытии объекта вместо вызова функции, просто создат в требуемом месте жесткую ссылку на существующий в кэше файл.

Полезно то, что ленивый файл является обычным ленивым объектом, и при его генерации могут использоваться другие ленивые объекты.

```python
import evalcache
import evalcache.lazyfile

lazy = evalcache.lazy.Lazy(cache = evalcache.DirCache(".evalcache"))
lazyfile = evalcache.lazyfile.LazyFile(cache = evalcache.DirCache(".evalfile"))

@lazyfile(field="path")
def foo(data, path):
	f = open(path, "w")
	f.write(data)
	f.close()

@lazy
def datagenerator():
	return "HelloWorld"

foo(datagenerator(),"data.dat")
```

## Применение ленификации к монтажу видео через инструмент moviepy. 

Как известно, скриптом на питоне может быть решена любая задача. Набор питоновских библиотек столь обширен, что найти задачу не покрытую питоновскими модулями очень сложно.

В частности библиотека moviepy и два часа изучения документации к ней дают нам в руки простой и функциональный видеоредактор. Монтаж - пожалуйста. Звук наложить - пожалуйста. Спецэфекты - пожалуйста.

Однако, как и всегда, у работы со скриптами есть недостаток. Каждый раз по запуску скрипта все артефакты пересобираются заново. При монтаже часового видео работа такого скрипта может длиться очень долго.

Применение библиотеки evalcache помогло внести коррективы в эту ситуацию.

```python
#!/usr/bin/env python3
#coding:utf-8

import sys
import types

from moviepy.editor import *
import evalcache.lazyfile

lazyhash = evalcache.LazyHash()
lazyfile = evalcache.lazyfile.LazyFile()

LazyVideoClip = lazyhash(VideoClip)
VideoFileClip = lazyhash(VideoFileClip)
AudioFileClip = lazyhash(AudioFileClip)
CompositeVideoClip = lazyhash(CompositeVideoClip)
concatenate_videoclips = lazyhash(concatenate_videoclips)

@lazyfile("path")
def lazy_write_videofile(path, clip):
	clip.write_videofile(path)

source = VideoFileClip("source.mp4")
music0 = AudioFileClip("music0.mp3")
music1 = AudioFileClip("music1.mp3")

music = music0
dur = 3
s0 = 1
s1 = 8
s2 = 16

part0 = source.subclip(s0, s0 + dur)
part1 = source.subclip(s1, s1 + dur * 2).fl_time(lambda t: t * 2).set_duration(2)
part2 = source.subclip(s2, s2 + dur * 4).fl_time(lambda t: t * 5).set_duration(2)

clip = concatenate_videoclips([part0, part1, part2])
clip = clip.set_audio(music.set_duration(clip.duration))

lazy_write_videofile("part0.mp4", part0)
lazy_write_videofile("part1.mp4", part1)
lazy_write_videofile("part2.mp4", part2)
lazy_write_videofile("part0_mus.mp4", part0.set_audio(music.set_duration(part0.duration)))
lazy_write_videofile("part1_mus.mp4", part1.set_audio(music.set_duration(part1.duration)))
lazy_write_videofile("part2_mus.mp4", part2.set_audio(music.set_duration(part2.duration)))

if len(sys.argv) > 1 and sys.argv[1] == "compile":
	clip.lazy_write_videofile("clip.mp4", clip)
```
Что здесь есть.

Мы применяем механику некэшируемого исполнения, так как разбираться с кэшированием объектов moviepy никакого желания и необходимости нет. При этом мы получаем все преимущества ленивых объектов для отслеживания изменений в дереве исполнения.

Оборачиваем вызовы библиотеки в ленификаторы:
```python
LazyVideoClip = lazyhash(VideoClip)
VideoFileClip = lazyhash(VideoFileClip)
AudioFileClip = lazyhash(AudioFileClip)
CompositeVideoClip = lazyhash(CompositeVideoClip)
concatenate_videoclips = lazyhash(concatenate_videoclips)
```

С помощью этой конструкции будем генерировать файлы:
```python
@lazyfile("path")
def lazy_write_videofile(path, clip):
	clip.write_videofile(path)
```

Совершив необходимые операции над видеорядом, записываем части нашего клипа в отдельные файлы. С музыкой и без:
```
lazy_write_videofile("part0.mp4", part0)
lazy_write_videofile("part1.mp4", part1)
lazy_write_videofile("part2.mp4", part2)
lazy_write_videofile("part0_mus.mp4", part0.set_audio(music.set_duration(part0.duration)))
lazy_write_videofile("part1_mus.mp4", part1.set_audio(music.set_duration(part1.duration)))
lazy_write_videofile("part2_mus.mp4", part2.set_audio(music.set_duration(part2.duration)))
```

Эти файлы будут перекомпилироваться только при изменении соответствующим им веток исполнения.

Когда результат сложился, собираем части в большой файл, используя опцию 'compile':
```python
if len(sys.argv) > 1 and sys.argv[1] == "compile":
	clip.lazy_write_videofile("clip.mp4", clip)
```

Вместо заключения:
В настоящем тексте показано, как с помощью библиотеки evalcache, можно ленифицировать алгоритм, предполагающей генерацию файлов.
Такой подход позволяет снизить зависимость от специализированного софта или избежать написания сложной логики избирательной сборки.