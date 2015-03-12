package TicTacToe;

import Engine.Vector2f;

public class Main {
	
	public static void main(String[] args) 
	{
		init();
	}
	
	
	public static void init()
	{
		Window window = new Window(new Vector2f(1024, 768),"Tic Tac Toe", new Game());
		window.init();
	}
	
	

}
