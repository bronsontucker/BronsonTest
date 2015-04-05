package Engine;

import java.awt.Rectangle;

import TicTacToe.Game;

public class Camera 
{
	private float x,y;
	public boolean camDebug = false;
	private Rectangle test = new Rectangle((int)x, (int) y, (int) (Game.WIDTH), (int)(Game.WIDTH));
	
	public Camera(float x, float y)
	{
		this.x = x;
		this.y = y;
	}
	
	
	
	

	public float getX() {
		return x;
	}

	public float getY() {
		return y;
	}

	public void setX(float x) {
		this.x = x;
	}

	public void setY(float y) {
		this.y = y;
	}





	public void tick(GameObject player) 
	{
		
		test.x = (int) -x;
		test.y = (int) -y;
		
		x = -player.x + Game.WIDTH/2;
		
		y = -player.y + Game.WIDTH/2 - 200;
		
		
		if(x >=0)
		{
			x = 0;
		}
//		if(y >= 0)
//		{
//			y = 0;
//		}
		
		
		if(camDebug)
		{
			System.out.println("Camera X: " + x);
			System.out.println("Camera Y: " + y);
		}
		
		
	}
	
	public void setDebug(boolean x)
	{
		if(x)camDebug = true;
		else camDebug = false;
	}
	
	public Rectangle getRectangle()
	{
		return test;
	}
	
	
}
