package gameObjects;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.LinkedList;

import Engine.GameObject;
import Engine.ObjectId;

public class Block extends GameObject
{

	public Block(float x, float y, ObjectId id) 
	{
		super(x, y, id);
		
	}
	
	public Block(float x, float y) 
	{
		super(x, y);
		
	}

	public void tick(LinkedList<GameObject> object) 
	{
		
	}

	public void render(Graphics g) 
	{
		g.setColor(Color.red);
		g.drawRect((int)x, (int)y, 32, 32);
	}

	public Rectangle getBounds() 
	{
		return new Rectangle((int)x, (int)y,32,32);
	}
	
}
