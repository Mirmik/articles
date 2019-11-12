
#ifndef Mirm_PS_h2
#define Mirm_PS_h2

// Вывод отладочной информация:
//#define INFO_WELCOME    // Вывод приветствия.   //352 байта
//#define INFO_ERROR   // Расшифровка ошибок
//#define INFO_ERROR2   // Расшифровка ошибок
//#define CS_INFO			// Информация о запуске и остановке CS              // TODO ? 290 байт?
 
// размер буффера системного вывода (должен быть больше самой большой системной строки)
 #define BUFFERSIZE 40

// Сигналы:
#define STOPSIG 3
#define IDLESIG 2
#define WORKSIG 0

// Параметры SH:
#define TaskArrayLength 10		//длина очереди задач
#define TimerArrayLength 10		//длина очереди таймеров

// Параметры FS:
//#define FS 				//Включение многозадачности(Отключение экономит флэш)
#define STACKDEPTH 200	//Глубина стека (недостаток приводит к сбоям.Не рекомендуется <110)
#define SPSIZE 2		//Максимальное количество стеков

//Обработка ошибок
#define COLLAPSE_ON_SYS_ERROR // Убить программу при ошибке.


#endif