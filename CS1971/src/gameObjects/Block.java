package gameObjects;

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
	Rectangle test;

	public Block(float x, float y, int type, ObjectId id,Rectangle test) 
	{
		super(x, y, id);
		this.type = type - 1;
		this.test = test;
		
	}

	public Block(int i, int yy, int j, ObjectId block) 
	{	super(j, yy, block);
		this.type = type - 1;
	}

	public void tick(LinkedList<GameObject> object) 
	{
		
	}

	public void render(Graphics g) 
	{
		if(test.contains(getBounds()))
		g.drawImage(tex.block[type], (int)x, (int)y, null); //dirt
		
	}

	public Rectangle getBounds() 
	{
		return new Rectangle((int)x, (int)y,32,32);
	}
	
	
}
