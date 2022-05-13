#include <array>
#include <bitset>
#include <iomanip>
#include <memory>
#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>


// center pos: (2, 2)
unsigned int constexpr blockTable0[4][5] =
{
	{0,0,30,0,0},
	{0,4,4,4,4},
	{0,0,15,0,0},
	{4,4,4,4,0}
};
// center pos: (2, 1)
unsigned int constexpr blockTable1to6[6][4][3] =
{
	{
		{1,7,0},
		{6,2,2},
		{0,7,4},
		{2,2,3}
	},
	{
		{4,7,0},
		{2,2,6},
		{0,7,1},
		{3,2,2}
	},
	{
		{6,6,0},
		{0,6,6},
		{0,3,3},
		{3,3,0}
	},
	{
		{6,3,0},
		{2,6,4},
		{0,6,3},
		{1,3,2}
	},
	{
		{2,7,0},
		{2,6,2},
		{0,7,2},
		{2,3,2}
	},
	{
		{3,6,0},
		{4,6,2},
		{0,3,6},
		{2,3,1}
	}
};
unsigned long long constexpr exceptionTable[7] =
{
	0x5555555555ull,
	0x4444444444ull,
	0x4444444444ull,
	0x6666666666ull,
	0x4444444444ull,
	0x4444444444ull,
	0x4444444444ull,
};
unsigned int field[25] = { 0 };
// use low 40 bits
unsigned long long validTable[15] = { 0 };
unsigned long long resultTable[15] = { 0 };
// x: [0,9], y: [0, 14]
unsigned int judge(unsigned int type_, unsigned int x_, unsigned int y_, unsigned int pos_, unsigned int const* field)
{
	if (type_ == 0)
	{
		for (int c0(0); c0 < 5; ++c0)
		{
			int y = y_ - 2 + c0;
			unsigned int shape(blockTable0[pos_][c0]);
			if (y > 14 && shape)
				return 0;
			unsigned int shapeOffset(shape << (x_ + 9));
			if (shapeOffset & 0xFFE007FFu)
				return 0;
			if (y >= 0)
				if (field[y] & shapeOffset)
					return 0;
		}
	}
	else
	{
		for (int c0(0); c0 < 3; ++c0)
		{
			int y = y_ - 1 + c0;
			unsigned int shape(blockTable1to6[type_ - 1][pos_][c0]);
			if (y > 14 && shape)
				return 0;
			unsigned int shapeOffset(shape << (x_ + 10));
			if (shapeOffset & 0xFFE007FFu)
				return 0;
			if (y >= 0)
				if (field[y] & shapeOffset)
					return 0;
		}
	}
	return 1;
}
void getValidPos(unsigned int type_, unsigned int const* field_,
	unsigned long long* validTable_, unsigned long long* resultTable_, unsigned int layers = 10)
{
	for (int c0(0); c0 < 15; ++c0)
	{
		validTable_[c0] = 0;
		for (int c1(0); c1 < 10; ++c1)
			for (int c2(0); c2 < 4; ++c2)
				if (judge(type_, c1, c0, c2, field_))
					validTable_[c0] |= (1ull << (4 * c1 + c2));
	}
	resultTable_[0] = validTable_[0];
	for (int c0(1); c0 < 15; ++c0)
	{
		unsigned long long valid(validTable_[c0]);
		unsigned long long temp = resultTable_[c0 - 1] & valid;
		for (int c1(0); c1 < layers; ++c1)
		{
			temp |= (temp << 4) & valid;
			temp &= 0xFFFFFFFFFFull;
			temp |= (temp >> 4) & valid;
			temp &= 0xFFFFFFFFFFull;
			unsigned long long mask0(0x0F0F0F0F0Full);
			unsigned long long mask1(0xF0F0F0F0F0ull);
			unsigned long long temp0(temp & mask0);
			unsigned long long temp1(temp & mask1);
			temp0 |= (temp0 << 3) | (temp0 << 2) | (temp0 << 1) | (temp0 >> 1) | (temp0 >> 2) | (temp0 >> 3);
			temp1 |= (temp1 << 3) | (temp1 << 2) | (temp1 << 1) | (temp1 >> 1) | (temp1 >> 2) | (temp1 >> 3);
			temp0 &= mask0;
			temp1 &= mask1;
			temp0 |= temp1;
			temp = temp0 & valid;
		}
		resultTable_[c0] = temp;
	}
	for (int c0(0); c0 < 14; ++c0)
		resultTable_[c0] = (resultTable_[c0] ^ validTable_[c0 + 1]) & resultTable_[c0];
	resultTable_[0] &= exceptionTable[type_];
	if (type_ == 0)
		resultTable_[1] &= 0x7777777777ull;
}
pybind11::list GetAllValidActionRepeating(unsigned int type_, pybind11::list field_)
{
	for (int c0(0); c0 < 15; ++c0)
	{
		field[c0] = 0;
		for (int c1(0); c1 < 10; ++c1)
		{
			if (pybind11::cast<int>((pybind11::cast<pybind11::list>(field_[c0]))[c1]) != 0)
				field[c0] |= 1u << (c1 + 11);
		}
	}
	getValidPos(type_ - 1, field, validTable, resultTable);
	pybind11::list result;
	for (int c0(14); c0 >= 0; --c0)
		for (int c1(0); c1 < 10; ++c1)
			for (int c2(0); c2 < 4; ++c2)
			{
				if (resultTable[c0] & (1ull << (c1 * 4 + c2)))
					result.append(pybind11::make_tuple(c0, c1, c2));
			}
	return result;
}
pybind11::list GetAllValidAction(unsigned int type_, pybind11::list field_)
{
	for (int c0(0); c0 < 15; ++c0)
	{
		field[c0] = 0;
		for (int c1(0); c1 < 10; ++c1)
		{
			if (pybind11::cast<int>((pybind11::cast<pybind11::list>(field_[c0]))[c1]) != 0)
				field[c0] |= 1u << (c1 + 11);
		}
	}
	getValidPos(type_ - 1, field, validTable, resultTable);
	pybind11::list result;
	for (int c0(14); c0 >= 0; --c0)
		for (int c1(0); c1 < 10; ++c1)
			for (int c2(0); c2 < 4; ++c2)
			{
				if (resultTable[c0] & (1ull << (c1 * 4 + c2)))
				{
					if (type_ == 1)
					{
						if (c2 == 2)
						{
							if (resultTable[c0] & (1ull << ((c1 - 1) * 4 + 0)))
								continue;
						}
						else if (c2 == 3)
						{
							if (resultTable[c0 - 1] & (1ull << (c1 * 4 + 1)))
								continue;
						}
					}
					else if (type_ == 4)
					{
						bool flag(false);
						switch (c2)
						{
						case 0:break;
						case 1:
						{
							if (resultTable[c0 + 1] & (1ull << (c1 * 4 + 0)))
								flag = true;
						}
						break;
						case 2:
						{
							if (resultTable[c0 + 1] & (1ull << ((c1 - 1) * 4 + 0)))
								flag = true;
							else if (resultTable[c0] & (1ull << ((c1 - 1) * 4 + 1)))
								flag = true;
						}
						break;
						case 3:
						{
							if (resultTable[c0] & (1ull << ((c1 - 1) * 4 + 0)))
								flag = true;
							else if (resultTable[c0 - 1] & (1ull << ((c1 - 1) * 4 + 1)))
								flag = true;
							else if (resultTable[c0 - 1] & (1ull << (c1 * 4 + 2)))
								flag = true;
						}
						break;
						}
						if (flag)continue;
					}
					else if (type_ == 5 || type_ == 7)
					{
						if (c2 == 2)
						{
							if (resultTable[c0 + 1] & (1ull << (c1 * 4 + 0)))
								continue;
						}
						else if (c2 == 3)
						{
							if (resultTable[c0] & (1ull << ((c1 - 1) * 4 + 1)))
								continue;
						}
					}
					result.append(pybind11::make_tuple(c0, c1, c2));
				}
			}
	return result;
}

PYBIND11_MODULE(CppAcceleration38, m)
{
	m.doc() = "Get all valid block positions"; // optional module docstring
	m.def("GetAllValidActionRepeating", &GetAllValidActionRepeating, "Returns all valid actions in a tuple list");
	m.def("GetAllValidAction", &GetAllValidAction, "Returns all non-repeating valid actions in a tuple list");
}
