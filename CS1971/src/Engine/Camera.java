package Engine;

import TicTacToe.Game;

public class Camera 
{
	private float x,y;
	public boolean camDebug = false;
	
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
		
		x = -player.x + Game.WIDTH/2;
		
		y = -player.y + Game.HEIGHT/ 1.2f;
		if(x >=0)
		{
			x = 0;
		}
		if(y >= 0)
		{
			y = 0;
		}
		
		
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
	
	
}
