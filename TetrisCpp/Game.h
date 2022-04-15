#pragma once
#include "_Time.h"// Header for timing
#include <vector>
#include <random>
#include <string>
#include <intrin.h>
unsigned int constexpr PeaceAreaWidth = 10;
unsigned int constexpr BattleAreaWidth = 5;
unsigned int constexpr PlayerWidth = PeaceAreaWidth + BattleAreaWidth;
unsigned int constexpr BoardWidth = PeaceAreaWidth * 2 + BattleAreaWidth;

// Act that player returns
struct Act
{
	int y;
	int x;
	int pos;
	bool operator==(Act const& a)const
	{
		return y == a.y && x == a.x && pos == a.pos;
	}
	void print()const
	{
		printf("(%d, %d, %d)", y, x, pos);
	}
};

// Playboard
struct Board
{
	unsigned int board[BoardWidth];

	// center pos: (2, 2)
	static unsigned int constexpr blockTable0[4][5] =
	{
		{0,0,30,0,0},
		{0,4,4,4,4},
		{0,0,15,0,0},
		{4,4,4,4,0}
	};
	// center pos: (1, 1)
	static unsigned int constexpr blockTable1to6[6][4][3] =
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

	Board() :board{ 0 } {}
	Board(Board const& a)
	{
		memcpy(board, a.board, sizeof(board));
	}

	// Print board and scores
	void print(unsigned int score1, unsigned int score2)const
	{
		char temp[1200]{ 0 };
		unsigned int offset(0);
		int deltaOffset(0);
		system("cls");
		for (int c1(20); c1 > 10; --c1)
		{
			for (int c0(0); c0 < BoardWidth; ++c0)
			{
				if ((board[c0] & (1u << c1)) != 0)
					sprintf(temp + offset, "口%n", &deltaOffset);
				else
					sprintf(temp + offset, "——%n", &deltaOffset);
				offset += deltaOffset;
			}
			if (c1 == 20)
			{
				sprintf(temp + offset, "%u %u%n", score1, score2, &deltaOffset);
				offset += deltaOffset;
			}
			sprintf(temp + offset, "\n%n", &deltaOffset);
			offset += deltaOffset;
		}
		printf("%s", temp);
	}

	// Clear board
	void clear()
	{
		for (unsigned int& a : board)a = 0;
	}

	// Check whether block(y, x) has block
	bool hasBlock(int y, int x)const
	{
		return board[y] & (1u << (x + 11));
	}

	// Operator version of hasBlock
	bool operator()(int y, int x)const
	{
		return board[y] & (1u << (x + 11));
	}

	// Check whether block(y) is full
	bool isFull(int y)const
	{
		return board[y] == 0x1FF800u;
	}

	// Return number of blocks in row y
	unsigned int blockNum(int y)const
	{
		return __popcnt(board[y]);
	}

	// Return first block position, if there is none, return -1
	int firstBlock(int y)const
	{
		unsigned long a;
		if (_BitScanForward(&a, board[y] >> 11))
			return a;
		else return -1;
	}

	// Return first blank position, if there is none, return -1
	int firstBlank(int y)const
	{
		unsigned long a;
		unsigned int data((~board[y]) & 0x1FF800u);
		if (_BitScanForward(&a, data >> 11))
			return a;
		else return -1;
	}

	// Return row transition times
	unsigned int getRowTransitions(int y)const
	{
		unsigned int a(board[y]);
		a |= 0x200400;
		return __popcnt(a ^ (a << 1)) - 2;
	}

	// Write a block into board, behaviour is undefined if act is invalid
	void writein(unsigned int type_, Act act_)
	{
		int y_ = act_.y;
		int x_ = act_.x;
		int pos_ = act_.pos;
		type_ -= 1;
		if (type_ == 0)
		{
			for (int c0(0); c0 < 5; ++c0)
			{
				int y = y_ - 2 + c0;
				unsigned int shape(blockTable0[pos_][c0]);
				if (y > PlayerWidth - 1 && shape)return;
				unsigned int shapeOffset(shape << (x_ + 9));
				if (shapeOffset & 0xFFE007FFu)return;
				if (y >= 0)
					if (board[y] & shapeOffset)
						return;
					else
						board[y] |= shapeOffset;

			}
		}
		else
		{
			for (int c0(0); c0 < 3; ++c0)
			{
				int y = y_ - 1 + c0;
				unsigned int shape(blockTable1to6[type_ - 1][pos_][c0]);
				if (y > PlayerWidth - 1 && shape)return;
				unsigned int shapeOffset(shape << (x_ + 10));
				if (shapeOffset & 0xFFE007FFu)return;
				if (y >= 0)
					if (board[y] & shapeOffset)
						return;
					else
						board[y] |= shapeOffset;
			}
		}
	}

	// Erase full lines and return erased lines number in peace area and battle area
	void erase(unsigned int* peace_, unsigned int* battle_)
	{
		unsigned int peace(0), battle(0);
		for (int c0(PlayerWidth - 1); c0 >= PeaceAreaWidth; --c0)
			if (board[c0] == 0x1FF800u)
				battle += 1;
		for (int c0(PeaceAreaWidth - 1); c0 >= 0; --c0)
			if (board[c0] == 0x1FF800u)
				peace += 1;
		int upper(PlayerWidth - 1), lower(PlayerWidth - 1);
		while (lower >= 0)
		{
			while (lower >= 0 && board[lower] == 0x1FF800u)
				board[lower--] = 0;
			while (lower >= 0 && board[lower] != 0x1FF800u)
			{
				board[upper] = board[lower];
				if (lower != upper)
					board[lower] = 0;
				lower--; upper--;
			}
		}
		*peace_ = peace;
		*battle_ = battle;
	}

	// Reverse the board
	void reverse()
	{
		for (int c0(0); c0 < BoardWidth; ++c0)
		{
			unsigned int a(board[c0]);
			a = (a & 0x55555555u) << 1 | (a & 0xaaaaaaaau) >> 1;
			a = (a & 0x33333333u) << 2 | (a & 0xccccccccu) >> 2;
			a = (a & 0x0f0f0f0fu) << 4 | (a & 0xf0f0f0f0u) >> 4;
			a = (a & 0x00ff00ffu) << 8 | (a & 0xff00ff00u) >> 8;
			a = (a & 0x0000ffffu) << 16 | (a & 0xffff0000u) >> 16;
			board[c0] = a;
		}
		for (int c0(0); c0 < BoardWidth / 2; ++c0)
		{
			unsigned int a(board[BoardWidth - c0 - 1]);
			board[BoardWidth - c0 - 1] = board[c0];
			board[c0] = a;
		}
	}

	// Return the offset of the lowest square in a block
	int blockLowestY(unsigned int type_, unsigned int pos_)
	{
		type_ -= 1;
		if (type_ == 0)
		{
			if (blockTable0[pos_][4])
				return 2;
			else if (blockTable0[pos_][3])
				return 1;
			else
				return 0;
		}
		else
		{
			if (blockTable1to6[type_ - 1][pos_][2])
				return 1;
			else
				return 0;
		}
	}
};

// Block pack
struct Pack
{
	std::mt19937 mt;
	std::uniform_int_distribution<unsigned int>rds[6];
	unsigned int blocks[560];
	int pos;

	Pack()
		:
		mt(time(0)),
		pos(-1)
	{
		init();
	}

	// Print pack
	void print()const
	{
		printf("[");
		for (int c0(pos); c0 > 0; --c0)
			printf("%u, ", blocks[c0]);
		if (pos >= 0)
			printf("%u", blocks[0]);
		printf("]\n");
	}

	// Initialize the pack into random 
	void init()
	{
		pos = 559;
		unsigned int ordered[7] = { 1,2,3,4,5,6,7 };
		for (int c0(0); c0 < 80; ++c0)
		{
			memcpy(blocks + c0 * 7, ordered, sizeof(ordered));
			std::shuffle(blocks + c0 * 7, blocks + (c0 + 1) * 7, mt);
		}
	}

	// Pop
	unsigned int pop()
	{
		return blocks[pos--];
	}

	// Return current block type
	unsigned int top()const
	{
		return blocks[pos];
	}

	// Return the next n-th block type, if n == 0, return current block type, if n > pos, return 0
	unsigned int nextNth(unsigned int n)
	{
		if (pos >= n)
			return blocks[pos - n];
		else
			return 0;
	}
};

// Player interface
struct Data
{
	bool isFirst;
	unsigned int* type;
	Pack* pack;
	Board* board;

	// Magic table
	static unsigned long long constexpr exceptionTable[7] =
	{
		0x5555555555ull,
		0x4444444444ull,
		0x4444444444ull,
		0x6666666666ull,
		0x4444444444ull,
		0x4444444444ull,
		0x4444444444ull,
	};

	Data(unsigned int* type_, Pack* pack_, Board* board_)
		:
		isFirst(false),
		type(type_),
		pack(pack_),
		board(board_)
	{

	}

	// Get current block type
	unsigned int getType()const
	{
		return *type;
	}

	// Get next n-th block type, if n == 0, return current block type, if there is no more blocks, return 0
	unsigned int getNthBlock(unsigned int n)const
	{
		return pack->nextNth(n);
	}

	// Get the whole pack, note the order
	Pack const* getBlockList()const
	{
		return pack;
	}

	// Judge whether a block in type can be placed with act into board, defalut board is game main board
	bool judge(unsigned int type_, Act act_, Board const* board_ = nullptr)const
	{
		int y_ = act_.y;
		int x_ = act_.x;
		int pos_ = act_.pos;
		if (board_ == nullptr)
			board_ = board;
		type_ -= 1;
		if (type_ == 0)
		{
			for (int c0(0); c0 < 5; ++c0)
			{
				int y = y_ - 2 + c0;
				unsigned int shape(Board::blockTable0[pos_][c0]);
				if (y > PlayerWidth - 1 && shape)
					return false;
				unsigned int shapeOffset(shape << (x_ + 9));
				if (shapeOffset & 0xFFE007FFu)
					return false;
				if (y >= 0)
					if (board_->board[y] & shapeOffset)
						return false;
			}
		}
		else
		{
			for (int c0(0); c0 < 3; ++c0)
			{
				int y = y_ - 1 + c0;
				unsigned int shape(Board::blockTable1to6[type_ - 1][pos_][c0]);
				if (y > PlayerWidth - 1 && shape)
					return false;
				unsigned int shapeOffset(shape << (x_ + 10));
				if (shapeOffset & 0xFFE007FFu)
					return false;
				if (y >= 0)
					if (board_->board[y] & shapeOffset)
						return false;
			}
		}
		return true;
	}

	// Get all repeating valid action of a block in type, default board is game main board
	std::vector<Act> getValidActRepeating(unsigned int type_ = 0, Board const* board_ = nullptr)const
	{
		unsigned long long validTable[PlayerWidth]{ 0 };
		unsigned long long resultTable[PlayerWidth];
		if (type_ == 0)
			type_ = *type;
		if (board_ == nullptr)
			board_ = board;
		for (int c0(0); c0 < PlayerWidth; ++c0)
			for (int c1(0); c1 < 10; ++c1)
				for (int c2(0); c2 < 4; ++c2)
					if (judge(type_, { c0, c1, c2 }, board_))
						validTable[c0] |= (1ull << (4 * c1 + c2));
		resultTable[0] = validTable[0];
		for (int c0(1); c0 < PlayerWidth; ++c0)
		{
			unsigned long long valid(validTable[c0]);
			unsigned long long temp = resultTable[c0 - 1] & valid;
			for (int c1(0); c1 < 10; ++c1)
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
			resultTable[c0] = temp;
		}
		for (int c0(0); c0 < PlayerWidth - 1; ++c0)
			resultTable[c0] = (resultTable[c0] ^ validTable[c0 + 1]) & resultTable[c0];
		type_ -= 1;
		resultTable[0] &= exceptionTable[type_];
		if (type_ == 0)
			resultTable[1] &= 0x7777777777ull;
		std::vector<Act>result;
		for (int c0(PlayerWidth - 1); c0 >= 0; --c0)
			for (int c1(0); c1 < 10; ++c1)
				for (int c2(0); c2 < 4; ++c2)
					if (resultTable[c0] & (1ull << (c1 * 4 + c2)))
						result.push_back({ c0, c1, c2 });
		return result;
	}

	// Get all non-repeating valid action of a block in type, default board is game main board
	std::vector<Act> getValidAct(unsigned int type_ = 0, Board const* board_ = nullptr)const
	{
		unsigned long long validTable[PlayerWidth]{ 0 };
		unsigned long long resultTable[PlayerWidth];
		if (type_ == 0)
			type_ = *type;
		if (board_ == nullptr)
			board_ = board;
		for (int c0(0); c0 < PlayerWidth; ++c0)
			for (int c1(0); c1 < 10; ++c1)
				for (int c2(0); c2 < 4; ++c2)
					if (judge(type_, { c0, c1, c2 }, board_))
						validTable[c0] |= (1ull << (4 * c1 + c2));
		resultTable[0] = validTable[0];
		for (int c0(1); c0 < PlayerWidth; ++c0)
		{
			unsigned long long valid(validTable[c0]);
			unsigned long long temp = resultTable[c0 - 1] & valid;
			for (int c1(0); c1 < 10; ++c1)
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
			resultTable[c0] = temp;
		}
		for (int c0(0); c0 < PlayerWidth - 1; ++c0)
			resultTable[c0] = (resultTable[c0] ^ validTable[c0 + 1]) & resultTable[c0];
		type_ -= 1;
		resultTable[0] &= exceptionTable[type_];
		if (type_ == 0)
			resultTable[1] &= 0x7777777777ull;
		std::vector<Act>result;
		type_ += 1;
		for (int c0(PlayerWidth - 1); c0 >= 0; --c0)
			for (int c1(0); c1 < 10; ++c1)
				for (int c2(0); c2 < 4; ++c2)
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
						result.push_back({ c0, c1, c2 });
					}
		return result;
	}
};

// Player AI base, user player must inherit from this
struct Player
{
	// MUST be implemented
	virtual Act output(Data const* data) = 0;
};

// Game class
struct Game
{
	// Game state
	enum State
	{
		Gaming,
		JudgeToEnd,
		RoundLimit,
		P1Overflow,
		P2Overflow,
		P1Error,
		P2Error,
	};
	// Game winner
	enum Winner
	{
		None = -1,
		Draw = 0,
		Player1 = 0,
		Player2 = 1,
	};

	static unsigned int constexpr peacepoint[] = { 0, 0, 1, 2, 4 };
	static unsigned int constexpr battlepoint[] = { 0, 1, 2, 4, 8 };

	Player* players[2];			// two players
	unsigned int type;			// current block type
	State state;				// current state
	Winner winner;				// game winner
	Board board;				// game main board
	Pack pack;					// block pack
	Data data;					// player interface
	std::string team1;			// player1 name
	std::string team2;			// player2 name
	unsigned int score1;		// player1 score
	unsigned int score2;		// player2 score
	unsigned int combo;			// batter counter
	unsigned int time;			// n-th block
	bool removeLine;			// whether erasing has happend in battle area in round
	Timer timer;				// timer
	std::vector<Act> validAct;	// all valid actions
	bool enablePrint;			// whether enable printing board and score
	unsigned int frameRate;		// game frame rate

	Game(Player* player1, Player* player2, bool enablePrint_ = true, unsigned int frameRate_ = 20) :
		players{ player1,player2 },
		type(0),
		state(Gaming),
		winner(None),
		board(),
		pack(),
		data(&type, &pack, &board),
		team1("player1"),
		team2("player2"),
		score1(0),
		score2(0),
		combo(0),
		time(0),
		removeLine(false),
		timer(),
		validAct(),
		enablePrint(enablePrint_),
		frameRate(frameRate_)
	{}

	// Reset the game to initial state
	void reset()
	{
		type = 0;
		state = Gaming;
		winner = None;
		board.clear();
		pack.init();
		score1 = 0;
		score2 = 0;
		combo = 0;
		time = 0;
		removeLine = false;
		validAct.clear();
	}

	// Run one turn
	void turn()
	{
		time += 1;
		if (time > 560)
		{
			state = RoundLimit;
			return;
		}
		type = pack.top();
		if (time & 1)
		{
			data.isFirst = true;
			validAct = data.getValidAct();
			if (validAct.size() == 0)
			{
				state = P1Overflow;
				winner = Player2;
				return;
			}
			Act act;
			try
			{
				//timer.begin();
				act = players[0]->output(&data);
				//timer.end();
				//timer.print();
			}
			catch (...)
			{
				state = P1Error;
				winner = Player2;
				return;
			}
			bool flag(false);
			for (Act& d : validAct)
				if (d == act)
				{
					flag = true;
					break;
				}
			if (!flag)
			{
				state = JudgeToEnd;
				winner = Player2;
				return;
			}
			if (enablePrint)
			{
				board.print(score1, score2);
				timer.wait(1000000000 / frameRate);
			}
			board.writein(type, act);
			if (enablePrint)
			{
				board.print(score1, score2);
				timer.wait(1000000000 / frameRate);
			}
			unsigned int peaceline, battleline;
			board.erase(&peaceline, &battleline);
			if (enablePrint)
			{
				board.print(score1, score2);
				timer.wait(1000000000 / frameRate);
			}
			//printf("%u %u\n", peaceline, battleline);
			if (battleline)
			{
				removeLine = true;
				score1 += battlepoint[battleline] + combo;
			}
			score1 += peacepoint[peaceline];
		}
		else
		{
			data.isFirst = false;
			board.reverse();
			validAct = data.getValidAct();
			if (validAct.size() == 0)
			{
				state = P2Overflow;
				winner = Player1;
				return;
			}
			Act act;
			try
			{
				//timer.begin();
				act = players[1]->output(&data);
				//timer.end();
				//timer.print();
			}
			catch (...)
			{
				state = P2Error;
				winner = Player1;
				return;
			}
			bool flag(false);
			for (Act& d : validAct)
				if (d == act)
				{
					flag = true;
					break;
				}
			if (!flag)
			{
				state = JudgeToEnd;
				winner = Player1;
				return;
			}
			board.writein(type, act);
			if (enablePrint)
			{
				board.reverse();
				board.print(score1, score2);
				timer.wait(1000000000 / frameRate);
				board.reverse();
			}
			unsigned int peaceline, battleline;
			board.erase(&peaceline, &battleline);
			//printf("%u %u\n", peaceline, battleline);
			if (battleline)
			{
				removeLine = true;
				score2 += battlepoint[battleline] + combo;
			}
			score2 += peacepoint[peaceline];
			board.reverse();
			if (removeLine)combo += 1;
			else combo = 0;
			removeLine = false;
		}
		pack.pop();
	}

	// Settlement of a game
	void end()
	{
		if (state == RoundLimit)
		{
			if (score1 > score2)
				winner = Player1;
			else if (score1 < score2)
				winner = Player2;
			else
				winner = Draw;
		}
		if (enablePrint)
		{
			printf("胜者是 %d\n", winner);
			printf("游戏结束原因是");
			switch (state)
			{
			case Game::Gaming:
				break;
			case Game::JudgeToEnd:
				printf("Judge to end\n");
				break;
			case Game::RoundLimit:
				printf("Round limit\n");
				break;
			case Game::P1Overflow:
				printf("Player 1 overflow\n");
				break;
			case Game::P2Overflow:
				printf("Player 2 overflow\n");
				break;
			case Game::P1Error:
				printf("Player 1 error\n");
				break;
			case Game::P2Error:
				printf("Player 2 error\n");
				break;
			default:
				break;
			}
			printf("time:\t%u\n", time);
			printf("%u\t%u\n", score1, score2);
			timer.wait(2000000000);
		}
	}
};
