package TicTacToe;

import java.awt.Toolkit;



import Engine.BUtil;
import Engine.Vector2f;
import Engine.Window;


public class Main 
{
	
	private static int Width = Toolkit.getDefaultToolkit().getScreenSize().width;
	private static int Height = Toolkit.getDefaultToolkit().getScreenSize().height;
	
	public static void main(String[] args) 
	{
		System.setProperty("sun.java2d.opengl", "true");
		init();
	}
		
	public static void init()
	{			
		Window window = new Window(new Vector2f(Width, Height),"Platform Engine Test", new Game());
		window.init();		
	}
	
	public static int count(int x)
	{
				int counter = 0;
		
		while(x > 0)
		{
			counter = counter + x;
			x--;
		}
	
		return counter;		
	}

}
