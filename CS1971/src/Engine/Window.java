package Engine;

import java.awt.Dimension;

import javax.swing.JFrame;

import TicTacToe.Game;

public class Window 
{
	Vector2f size;
	String title;
	Game game;
	
	public Window(Vector2f size, String title, Game game)
	{
		this.size = size;
		this.title = title;
		this.game = game;
	}
	
	public void init()
	{
		 game.setPreferredSize(new Dimension((int)size.getX(), (int)size.getY()));
		 JFrame frame = new JFrame(title);
		 frame.setUndecorated(true);
		 frame.add(game);
		 frame.pack();
		 frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		 frame.setResizable(false);
		 frame.setLocationRelativeTo(null);
		 frame.setExtendedState(JFrame.MAXIMIZED_BOTH); //sets fullscreen
		 frame.setVisible(true);
		 
		 game.start();
	}
	
	
}
