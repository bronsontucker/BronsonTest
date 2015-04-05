package Engine;

public class BUtil 
{
	public static int Sum(int x)
	{
				int counter = 0;
		
		while(x > 0)
		{
			counter = counter + x;
			x--;
		}
	
		return counter;		
	}
	
	public static float Sqrt (float x)
	{
		return (float)Math.sqrt(x);
	}
	public static int Sqrt (int x)
	{
		return (int)Math.sqrt(x);
	}	
	
	public static void print(String string)
	{
		System.out.println(string);
	}
	public static void print(int i) 
	{
		System.out.println(i);		
	}
}
