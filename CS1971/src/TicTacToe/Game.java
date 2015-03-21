package TicTacToe;

import gameObjects.Player;

import java.awt.Canvas;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferStrategy;



import java.awt.image.BufferedImage;

import Engine.BufferedImageLoader;
import Engine.Camera;
import Engine.Handler;
import Engine.KeyInput;
import Engine.ObjectId;

public class Game extends Canvas implements Runnable
{
	
	private boolean running = false;
	private Thread thread;
	
	public static int WIDTH, HEIGHT;
	
	private BufferedImage level = null;
	
	Handler handler;
	Camera cam;
	
	private void init()
	{
		WIDTH = getWidth();
		HEIGHT = getHeight();
		
		BufferedImageLoader loader = new BufferedImageLoader();
		level = loader.loadImage("levl.png");
		
		handler = new Handler();	
		
		cam = new Camera(0, 0);
		
		handler.addObject(new Player(100, 100, ObjectId.Player,handler));
		handler.createLevel();
		
		this.addKeyListener(new KeyInput(handler));
	}
	
	public synchronized void start()
	{
		if(running)
			return;
		
		running = true;
		thread = new Thread(this);
		thread.start();
		
	}
	
	private static final long serialVersionUID = -5473398027762195374L;

	public void run()
	{
		
		
		System.out.println("Thread has Begun");
		init();
		this.requestFocus();
		
		long lastTime = System.nanoTime();
		double amountOfTicks = 60.0;
		double ns = 1000000000 / amountOfTicks;
		double delta = 0;
		long timer = System.currentTimeMillis();
		int updates = 0;
		int frames = 0;
		
		while(running)
		{
			
			long now = System.nanoTime();
			delta += (now - lastTime) / ns;
			lastTime = now;
			while(delta >= 1)
			{
				tick();
				updates++;
				delta--;
			}
			render();
			frames++;
					
			if(System.currentTimeMillis() - timer > 1000)
			{
				timer += 1000;
				System.out.println("FPS: " + frames + " TICKS: " + updates);
				frames = 0;
				updates = 0;
			}
		}

		
	}
	
	
	public void tick()
	{
		handler.tick();
		for(int i = 0; i < handler.object.size(); i++)
		{
			if(handler.object.get(i).getId() == ObjectId.Player)
			{
				cam.tick(handler.object.get(i));
			}
		}
	}
	
	public void render()
	{
		BufferStrategy bs = this.getBufferStrategy();
		
		if(bs == null)
		{
			this.createBufferStrategy(3);
			return;
		}
		
		Graphics g = bs.getDrawGraphics();
		Graphics2D g2d = (Graphics2D) g;
		
		g.setColor(Color.black);
		g.fillRect(0, 0, getWidth(), getHeight());
		
		g2d.translate(cam.getX(), cam.getY());
		
		handler.render(g);
		
		g2d.translate(-cam.getX(), -cam.getY());
		
		g.dispose();
		bs.show();
	}
}
