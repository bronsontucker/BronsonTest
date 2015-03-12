package Engine;

import gameObjects.Block;

import java.awt.Graphics;
import java.util.LinkedList;

import TicTacToe.Game;

public class Handler 
{
	public LinkedList<GameObject> object = new LinkedList<GameObject>();
	
	private GameObject tempObject;
	
	public void tick()
	{
		for(int i = 0; i < object.size(); i++)
		{
			tempObject = object.get(i);
			tempObject.tick(object);
		}
	}
	
	public void render(Graphics g)
	{
		for(int i = 0; i < object.size(); i++)
		{
			tempObject = object.get(i);
			tempObject.render(g);
		}
	}
	
	
	public void addObject(GameObject object)
	{
		this.object.add(object);
	}
	
	public void removeObject(GameObject object)
	{
		this.object.remove(object);
	}
	
	public void createLevel()
	{
		for(int i = 0; i < Game.WIDTH+32; i+= 32)
			addObject(new Block(i, 736, ObjectId.Block));
	}
	
}
