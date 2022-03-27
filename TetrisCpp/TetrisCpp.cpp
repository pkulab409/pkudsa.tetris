#include "Game.h"
#include "file1.h"
#include "file2.h"

int main()
{
	_set_printf_count_output(1);
	Player* player1 = new file1();
	Player* player2 = new file2();
	// true: Print board
	// false: Don't print board
	Game game(player1, player2, true, 40);
	Timer timer;

	unsigned int rounds(5);
	float s1(0);
	for (int c0(0); c0 < rounds; ++c0)
	{
		timer.begin();
		while (game.state == Game::Gaming)
		{
			game.turn();
		}
		timer.end();
		timer.print();
		game.end();
		if (game.winner == Game::Player1)
			s1 += game.score1;
		else
			s1 += game.score2;
		game.reset();
	}
	printf("%f", s1 / rounds);
	delete player1;
	delete player2;
}
