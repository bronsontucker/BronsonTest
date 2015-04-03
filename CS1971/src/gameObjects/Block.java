package gameObjects;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Rectangle;
import java.util.LinkedList;

import TicTacToe.Game;
import Engine.GameObject;
import Engine.ObjectId;
import Engine.Texture;

public class Block extends GameObject
{
	
	Texture tex = Game.getInstance();
	private int type;
	private boolean useFullGraphics = true;

	public Block(float x, float y, int type, ObjectId id) 
	{
		super(x, y, id);
		this.type = type;
		
	}

	public void tick(LinkedList<GameObject> object) 
	{
		
	}

	public void render(Graphics g) 
	{
		
		blockHandler(g);		
	}

	public Rectangle getBounds() 
	{
		return new Rectangle((int)x, (int)y,32,32);
	}
	
	public void blockHandler(Graphics g)
	{
		if(type == 1)
		{
			if(useFullGraphics)
			{
				g.drawImage(tex.block[0], (int)x, (int)y, null); //dirt
			}
			
			else 
			{
				g.setColor(Color.red);
				g.drawRect((int)x, (int)y, 32, 32);
			}
		}
		
		if(type == 2)
		{
			if(useFullGraphics)
			{
				g.drawImage(tex.block[1], (int)x, (int)y, null); //grass
			}
			
			else 
			{
				g.setColor(Color.green);
				g.drawRect((int)x, (int)y, 32, 32);
			}			
		}
	}
	
}
