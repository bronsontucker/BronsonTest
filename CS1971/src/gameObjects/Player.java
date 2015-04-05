package gameObjects;

import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.LinkedList;





import TicTacToe.Game;
import Engine.GameObject;
import Engine.Handler;
import Engine.ObjectId;
import Engine.Texture;

public class Player extends GameObject
{
	private int width = 48, height = 96;
	private float gravity = 0.2f;
	private final float MAX_SPEED = 10;
	Texture tex = Game.getInstance();
	
	private Handler handler;

	public Player(float x, float y, ObjectId id,Handler handler) 
	{
		super(x, y, id);
		this.handler = handler;
	}

	public void tick(LinkedList<GameObject> object) 
	{
		
		x = x + velX;
		y = y + velY;
		
		if(falling || jumping)
		{
			velY += gravity;
			if(velY > MAX_SPEED)
			{
				velY = MAX_SPEED;
			}
		}
		
		falling = true;
		Collision(object);
		
		if(velY <= -10)
		{
			velY = -10;
		}
		
		
	}
	
	public void RenderHandler(Graphics g)
	{
		if(facing == 0)
		g.drawImage(tex.player[0], (int)x, (int)y, null);
		
		if(facing == 1)
			g.drawImage(tex.player[1], (int)x, (int)y, null);
	}
	
	private void Collision(LinkedList<GameObject> object)
	{
		for(int i = 0; i < handler.object.size(); i++)
		{
			
			
			GameObject tempObject = handler.object.get(i);
			
			if(tempObject.getId() == ObjectId.Block)
			{
				
				if(getBounds().intersects(tempObject.getBounds()))
				{
					y = tempObject.getY() - height;
					velY = 0;
					falling = false;
					jumping = false;
				}
				
				if(getBoundsTop().intersects(tempObject.getBounds()))
				{
					y = tempObject.getY() +  height / 3;
					velY = 0;
				}
				if(getBoundsRight().intersects(tempObject.getBounds()))
				{
					x = tempObject.getX() - width + 2;
					
				}
				if(getBoundsLeft().intersects(tempObject.getBounds()))
				{
					x = tempObject.getX() + 32;
				}
				
			}
		}
	}

	public void render(Graphics g) 
	{
//		g.setColor(Color.blue);
//		g.fill3DRect((int)x, (int)y, width, height, true);	
//		Graphics2D g2d = (Graphics2D) g;
		
	//	g.drawImage(tex.player[0], (int)x, (int)y, null);
		
		RenderHandler(g);
		
//		g.setColor(Color.GRAY);
//		g2d.draw(getBounds());
//		g2d.draw(getBoundsRight());
//		g2d.draw(getBoundsLeft());
//		g2d.draw(getBoundsTop());
	}

	public Rectangle getBounds() 
	{
		return new Rectangle((int)x + (width/2) - width/4 , (int)y + (height/2) , width/2, height/2);
	}
	public Rectangle getBoundsTop() 
	{
		return new Rectangle((int)x + (width/2) - width/4, (int)y, width/2, height/2);
	}
	public Rectangle getBoundsRight() 
	{
		return new Rectangle((int)x + width - 5, (int)y + 5, 5, height-10);
	}
	public Rectangle getBoundsLeft() 
	{
		return new Rectangle((int)x, (int)y +5 , 5, height-10);
	}
	
	
}
