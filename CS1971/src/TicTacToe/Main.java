package TicTacToe;

import Engine.Vector2f;
import Engine.Window;

public class Main {
	
	public static void main(String[] args) 
	{
		init();
	}
	
	
	public static void init()
	{
		Window window = new Window(new Vector2f(1024, 768),"Platform Engine Test", new Game());
		window.init();
	}
	
	

}
