#pragma once
#include <ctime>
#include <cstdio>
#include <cstring>
#include <cmath>

struct Timer
{
	timespec beginning;
	timespec ending;
	Timer() = default;
	void begin()
	{
		timespec_get(&beginning, TIME_UTC);
	}
	void end()
	{
		timespec_get(&ending, TIME_UTC);
	}
	void wait(long long _dt)
	{
		begin();
		long long dt(0);
		do
		{
			end();
			dt = 1000000000LL * (ending.tv_sec - beginning.tv_sec) + (ending.tv_nsec - beginning.tv_nsec);
		} while (dt < _dt);
	}
	void wait(long long _dt, void (*p)())
	{
		begin();
		long long dt(0);
		do
		{
			p();
			end();
			dt = 1000000000LL * (ending.tv_sec - beginning.tv_sec) + (ending.tv_nsec - beginning.tv_nsec);
		} while (dt < _dt);
	}
	void print() const
	{
		constexpr unsigned long long e3{1000U};
		constexpr unsigned long long e6{1000000U};
		constexpr unsigned long long e9{1000000000U};
		constexpr unsigned long long e12{100000000000ULL};
		long long dt = e9 * (ending.tv_sec - beginning.tv_sec) + (ending.tv_nsec - beginning.tv_nsec);
		if (dt < 0)
			printf("-");
		unsigned long long dt1 = llabs(dt);
		if (dt1 >= 500)
			dt1 -= 500;
		else
			dt1 = 0;
		double length = log10(dt1);
		if (length < 3)
			printf("%15llu ns", dt1);
		else if (length < 6)
			printf("%16llu,%03llu ns", dt1 / e3, dt1 % e3);
		else if (length < 9)
			printf("%12llu,%03llu,%03llu ns", dt1 / e6, (dt1 % e6) / e3, dt1 % e3);
		else if (length < 12)
			printf("%8llu,%03llu,%03llu,%03llu ns", dt1 / e9, (dt1 % e9) / e6, (dt1 % e6) / e3, dt1 % e3);
		else if (length < 15)
			printf("%4llu,%03llu,%03llu,%03llu,%03llu ns", dt1 / e12, (dt1 % e12) / e9, (dt1 % e6) / e6, (dt1 % e6) / e6, dt1 % e3);
		printf("\n");
	}
	void print(const char *a) const
	{
		printf("%s", a);
		print();
	}
	void print(long long minus) const
	{
		constexpr unsigned long long e3{1000U};
		constexpr unsigned long long e6{1000000U};
		constexpr unsigned long long e9{1000000000U};
		constexpr unsigned long long e12{100000000000U};
		long long dt = e9 * (ending.tv_sec - beginning.tv_sec) + (ending.tv_nsec - beginning.tv_nsec) - minus;
		if (dt < 0)
			printf("-");
		unsigned long long dt1 = llabs(dt);
		if (dt1 >= 500)
			dt1 -= 500;
		else
			dt1 = 0;
		double length = log10(dt1);
		if (length < 3)
			printf("%15llu ns", dt1);
		else if (length < 6)
			printf("%16llu,%03llu ns", dt1 / e3, dt1 % e3);
		else if (length < 9)
			printf("%12llu,%03llu,%03llu ns", dt1 / e6, (dt1 % e6) / e3, dt1 % e3);
		else if (length < 12)
			printf("%8llu,%03llu,%03llu,%03llu ns", dt1 / e9, (dt1 % e9) / e6, (dt1 % e6) / e3, dt1 % e3);
		else if (length < 15)
			printf("%4llu,%03llu,%03llu,%03llu,%03llu ns", dt1 / e12, (dt1 % e12) / e9, (dt1 % e6) / e6, (dt1 % e6) / e6, dt1 % e3);
		printf("\n");
	}
};
struct FPS
{
	timespec t0;
	timespec t1;
	int timeStamp;
	double accTime;
	unsigned long long dt;
	double fps;
	char str[128];
	bool valid;
	FPS()
		: valid(false),
		timeStamp(0),
		accTime(0)
	{
	}
	void refresh()
	{
		constexpr unsigned long long e9{1000000000U};
		if (valid)
		{
			timespec_get(&t1, TIME_UTC);
			dt = e9 * (t1.tv_sec - t0.tv_sec) + t1.tv_nsec - t0.tv_nsec;
			t0 = t1;
			fps = (double)e9 / dt;
		}
		else
		{
			timespec_get(&t0, TIME_UTC);
			valid = true;
		}
	}
	void printFPS(unsigned int a)
	{
		if (valid)
			printf("\rfps: %.*lf    ", a, fps);
	}
	void printFPSToString(unsigned int a)
	{
		if (valid)
			sprintf(str, "fps: %.*lf", a, fps);
	}
	void printFrameTime(unsigned int a)
	{
		if (valid)
			printf("\rframe time: %.*f ms  ", a, dt / 100000.0);
	}
	void printFrameTimeToString(unsigned int a)
	{
		if (valid)
			sprintf(str, "frame time: %.*f ms", a, dt / 100000.0);
	}
	void printFPSAndFrameTime(unsigned int a, unsigned int b)
	{
		if (valid)
			printf("\rfps:%.*lf\tframe time: %.*lf ms      ", a, fps, b, dt / 1000000.0);
	}
	void printFPSAndFrameTimeToString(unsigned int a, unsigned int b)
	{
		if (valid)
			sprintf(str, "fps:%.*lf    frame time: %.*lf ms", a, fps, b, dt / 1000000.0);
	}
	void printAverageFrameTime()
	{
		timeStamp++;
		if (timeStamp > 100)
			accTime += dt / 1000000.0;
		if (timeStamp == 200)
		{
			printf("accTime:%lf ms", accTime / 100);
			exit(0);
		}
	}
};
 