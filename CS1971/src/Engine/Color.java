package Engine;

public class Color 
{
	
	private float r;
	private float g;
	private float b;
	
	public Color (float r, float g, float b)
	{
		this.r = r;
		this.g = g;
		this.b = b;
	}
	
	public Color (Vector3f a)
	{
		this.r = a.getX();
		this.g = a.getY();
		this.b = a.getZ();
	}

	public float getR() {
		return r;
	}

	public void setR(float r) {
		this.r = r;
	}

	public float getG() {
		return g;
	}

	public void setG(float g) {
		this.g = g;
	}

	public float getB() {
		return b;
	}

	public void setB(float b) {
		this.b = b;
	}
	
	public static Color blue()
	{
		return new Color(0, 0, 255);
	}
	
	public static Color red()
	{
		return new Color(255, 0, 0);
	}
	
	public static Color green()
	{
		return new Color(0, 255, 0);
	}
	
	
	
	

}
