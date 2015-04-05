package Engine;

import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.LinkedList;

public abstract class GameObject 
{
	protected float x,y;
	protected ObjectId id;
	protected float velX = 0, velY = 0;
	protected boolean falling = true;
	protected boolean jumping = false;
	protected int facing = 0;
	
	public GameObject(float x, float y, ObjectId id)
	{
		this.x = x;
		this.y = y;
		this.id = id;
		this.facing = facing;
	}
	public GameObject(float x, float y)
	{
		this.x = x;
		this.y = y;
	}
	
	public abstract void tick(LinkedList<GameObject> object);
	public abstract void render(Graphics g);	
	public abstract Rectangle getBounds();

	public void setFacing(int f)
	{
		facing = f;
	}
	
	public float getX()
	{
		return x;
	}
	public float getY()
	{
		return y;
	}
	public void setX(float x)
	{
		this.x = x;
	}
	public void setY(float y)
	{
		this.y = y;
	}	
	public float getVelX()
	{
		return velX;
	}
	public float getVelY()
	{
		return velY;
	}
	public void setVelX(float x)
	{
		this.velX = x;
	}
	public void setVelY(float y)
	{
		this.velY = y;
	}
	public ObjectId getId()
	{
		return id;
	}
	public boolean isFalling() 
	{
		return falling;
	}
	public boolean isJumping() 
	{
		return jumping;
	}
	public void setFalling(boolean falling) 
	{
		this.falling = falling;
	}
	public void setJumping(boolean jumping) 
	{
		this.jumping = jumping;
	}
}
