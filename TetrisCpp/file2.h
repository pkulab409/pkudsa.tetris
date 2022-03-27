#pragma once
#include "Game.h"

struct file2 :Player
{
	virtual Act output(Data const* data)override
	{
		std::vector<Act>position = data->getValidAct();
		std::mt19937 mt(time(0));
		std::uniform_int_distribution<unsigned int> rd(0, position.size()-1);
		return position[rd(mt)];
	}
};
