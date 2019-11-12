
#ifndef Mirm_CH_h
#define Mirm_CH_h

extern void (*zeroFunc)(void);

class coopShedulerType
{private:
	void (*TaskArray [TaskArrayLength]) (void);
	struct 
	{unsigned long int timerStop[TimerArrayLength];
	void (*task[TimerArrayLength])(void);} TimerArray;
	unsigned char TCL;
	unsigned char TCH;	
	char name[8];
long lastIdleTime;

public:
	void start(void (*idle) (void),void (*init)(void)=zeroFunc);
	void newTask(void (*task) (void));
	void newTask(void (*task) (void),unsigned int timer);
	void stop(void);	
	long noIdleTime();
	coopShedulerType();
	char signal;
};

#endif